"""Run the integrated prototype: python prototype/app.py."""
import argparse
import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(ROOT), str(ROOT / 'household')]

from flask import jsonify, request, render_template
from jinja2 import ChoiceLoader, FileSystemLoader
from werkzeug.exceptions import HTTPException
from prototype.init_db import DEFAULT_DB, PRICE_TABLES
from prototype.address import load_addresses
from prototype.comparison import CANCER_NAMES, DEMO_DATE, HOSPITAL_IDS, PROFILES, compare, rows
from assistance import assistance as assistance_backend
import household.app as household_api

app = household_api.app
app.jinja_loader = ChoiceLoader([FileSystemLoader(HERE / 'templates'), app.jinja_loader])
app.static_folder = str(HERE / 'static')
app.config.update(DATABASE=DEFAULT_DB, MAX_CONTENT_LENGTH=64 * 1024)
app.json.sort_keys = False
original_household_page = app.view_functions['household_page']


def configure_database(database=DEFAULT_DB):
    database = Path(database).resolve(strict=True)
    app.config['DATABASE'] = database
    household_api.DB = database
    assistance_backend.DB = database
    return database


@contextmanager
def connect():
    conn = sqlite3.connect(Path(app.config['DATABASE']).as_uri() + '?mode=rw', uri=True)
    try:
        yield conn
    finally:
        conn.close()


def prices(conn):
    return [{**row, 'source_table': table, 'fictional': True, 'unit': 'USD per complete regimen course'}
            for table in PRICE_TABLES for row in rows(conn, 'SELECT * FROM ' + table)]


def prototype_page():
    return render_template('prototype.html')


app.view_functions['household_page'] = prototype_page
app.add_url_rule('/household', 'original_household_page', original_household_page)


@app.get('/api/addresses')
def addresses():
    return jsonify(load_addresses(HOSPITAL_IDS))


@app.get('/api/addresses/<address_id>')
def address(address_id):
    row = next((r for r in load_addresses(HOSPITAL_IDS) if r['address_id'] == address_id), None)
    if row is None:
        return jsonify(error='Unknown predefined address'), 404
    return jsonify(**row, source='Predetermined test distances (not a map lookup)')


@app.get('/api/assistance-subtypes')
def assistance_subtypes():
    cancer = request.args.get('cancer')
    if cancer not in CANCER_NAMES:
        return jsonify(error='Select a supported diagnosis'), 400
    with connect() as conn:
        subtypes = conn.execute('SELECT DISTINCT cancer_subtype FROM assistance_program_cancer '
                                'WHERE cancer_type=? AND cancer_subtype IS NOT NULL '
                                "AND cancer_subtype<>'' ORDER BY cancer_subtype", (CANCER_NAMES[cancer],)).fetchall()
    return jsonify([row[0] for row in subtypes])


@app.get('/api/prototype-info')
def prototype_info():
    with connect() as conn:
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        counts = {table: conn.execute('SELECT COUNT(*) FROM "' + table.replace('"', '""') + '"').fetchone()[0]
                  for table in tables}
        return jsonify(snapshot=DEMO_DATE, source='Live API responses from the local SQLite database; team SQL seeds',
                       counts=counts, fictionalPrices=prices(conn), fictionalHospitalRules=PROFILES,
                       fictionalAddresses=load_addresses(HOSPITAL_IDS), hospitalIds=HOSPITAL_IDS)


@app.post('/api/compare')
def comparison():
    profile = request.get_json()
    with connect() as conn:
        result = compare(conn, profile, prices(conn), {r['address_id'] for r in load_addresses(HOSPITAL_IDS)})
    return jsonify(result), 400 if result['errors'] else 200


@app.after_request
def api_cache(response):
    if request.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.errorhandler(HTTPException)
def http_error(error):
    if request.path.startswith('/api/'):
        return jsonify(error=error.description), error.code
    return error


@app.errorhandler(sqlite3.Error)
def database_error(error):
    app.logger.error('Database request failed: %s', error)
    return jsonify(error='The local database is unavailable. Run prototype/init_db.py, then restart the app.'), 503


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=5001)
    args = parser.parse_args()
    try:
        configure_database()
    except FileNotFoundError:
        parser.exit(1, 'Database not initialized. Run prototype/init_db.py before starting the app.\n')
    print(f'CureBase: http://127.0.0.1:{args.port}', flush=True)
    app.run(host='127.0.0.1', port=args.port, debug=False)

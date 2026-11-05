"""Regenerate the standalone HTML from the team's SQL; no installed packages needed."""
import json
import sqlite3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'household'))
from init_db import SCRIPTS
from regimen import regimen_summary
from address_data import load_addresses

PRICE_TABLES = ("duke_price", "unc_price", "wfb_price", "levine_price", "ecu_price")


def snapshot():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys=ON')
    for script in SCRIPTS:
        conn.executescript((ROOT / 'household' / script).read_text())
    for table in PRICE_TABLES:
        conn.executescript((ROOT / 'test_data/pricing' / (table + '.sql')).read_text())
    tables = ['cancer_type','regimen','regimen_phase','treatment','hospital','poverty_guideline',
              'poverty_guideline_extra','mileage_rate','lodging_rate','childcare_price','county',
              'assistance_program','assistance_program_cancer','assistance_program_insurance','assistance_program_geography']
    data = {t: [dict(r) for r in conn.execute('SELECT * FROM '+t)] for t in tables}
    data['summaries'] = [dict(regimen_id=r[0], visits=r[3], weeks=r[4]) for r in regimen_summary(conn)]
    data['hospital_prices'] = []
    for table in PRICE_TABLES:
        data['hospital_prices'].extend(dict(row, source_table=table, fictional=True, unit='USD per complete regimen course') for row in conn.execute('SELECT * FROM '+table))
    for row in data['hospital_prices']:
        if not any(r['regimen_id'] == row['treatment_id'] and r['cancer_id'] == row['cancer_id'] for r in data['regimen']):
            raise ValueError('Price treatment_id must identify a matching regimen package')
        if not any(h['hospital_id'] == row['hospital_id'] for h in data['hospital']):
            raise ValueError('Unknown price hospital')
    data['addresses'] = load_addresses([h['hospital_id'] for h in data['hospital']])
    conn.close()
    return data

if __name__ == '__main__':
    data = json.dumps(snapshot(), ensure_ascii=True, indent=2).replace('<', '\\u003c')
    html = (ROOT/'prototype/template.html').read_text().replace('/*DATA*/', 'const DATA = '+data+';')
    html = html.replace('/*DISTANCE_PROVIDER*/', (ROOT/'prototype/distance_provider.js').read_text())
    html = html.replace('/*ENGINE*/', (ROOT/'prototype/engine.js').read_text()).replace('/*APP*/', (ROOT/'prototype/app.js').read_text())
    (ROOT/'prototype/prototype.html').write_text(html)
    print('Built prototype/prototype.html from SQL snapshots and prototype sources.')

"""Build the prototype database from the team's SQL and unchanged test fixtures."""
import os
import sqlite3
import sys
import tempfile
from contextlib import closing
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from household.init_db import SCRIPTS

PRICE_TABLES = ('duke_price', 'unc_price', 'wfb_price', 'levine_price', 'ecu_price')
DEFAULT_DB = HERE / 'curebase.db'


def initialize(database=DEFAULT_DB):
    database = Path(database).resolve()
    database.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='curebase-', suffix='.sqlite3', dir=database.parent)
    os.close(fd)
    try:
        with closing(sqlite3.connect(temporary)) as conn:
            conn.execute('PRAGMA foreign_keys = ON')
            for script in SCRIPTS:
                conn.executescript((ROOT / 'household' / script).read_text())
            for table in PRICE_TABLES:
                conn.executescript((HERE / 'test_data' / 'pricing' / f'{table}.sql').read_text())
            if conn.execute('PRAGMA foreign_key_check').fetchall():
                raise ValueError('Invalid foreign keys in seed data')
        os.replace(temporary, database)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return database


if __name__ == '__main__':
    print('Database ready:', initialize())

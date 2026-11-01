"""Build the whole household database in one step. Run:  python3 init_db.py"""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "curebase.db"

SCRIPTS = [
    "schema.sql", "seed_2026.sql",                    # poverty guidelines
    "schema_regimen.sql", "seed_regimen.sql",         # treatment regimens
    "schema_indirect.sql", "seed_indirect.sql",       # mileage / lodging
    "seed_childcare.sql",                             # DOL county childcare prices
    "seed_hospital.sql",                              # hospitals in scope
    "../assistance/schema_assistance.sql",            # assistance tables
    "../assistance/generated_assistance_seed.sql",    # assistance program data
]

if __name__ == "__main__":
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    for name in SCRIPTS:
        conn.executescript((HERE / name).read_text())
        print("loaded", name)
    conn.commit()
    conn.close()
    print("Database ready:", DB.name)

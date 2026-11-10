import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "household" / "curebase.db"
SEED = HERE / "seed_treatment_codes.sql"

conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = ON")

try:
    conn.executescript(SEED.read_text())
    conn.commit()
    print("Treatment billing codes loaded")
finally:
    conn.close()
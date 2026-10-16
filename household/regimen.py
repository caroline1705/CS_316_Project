"""Treatment regimen prototype (SQLite). Run:  python3 regimen.py"""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "curebase.db"


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript((HERE / "schema_regimen.sql").read_text())
    conn.executescript((HERE / "seed_regimen.sql").read_text())
    conn.commit()
    return conn


def regimen_summary(conn, cancer_id=None):
    sql = (HERE / "regimen_query.sql").read_text()
    return conn.execute(sql, {"cancer_id": cancer_id}).fetchall()


if __name__ == "__main__":
    conn = init_db()
    print("All regimens:")
    for rid, cancer, name, visits, weeks in regimen_summary(conn):
        print(f"  {cancer:30} {name:48} {visits:3} visits over {weeks} weeks")
    print("\nOnly breast cancer:")
    for row in regimen_summary(conn, "BREAST"):
        print("  ", row)

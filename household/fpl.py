"""FPL calculator prototype (SQLite). Run:  python fpl.py"""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "curebase.db"


def init_db():
    conn = sqlite3.connect(DB)
    conn.executescript((HERE / "schema.sql").read_text())
    conn.executescript((HERE / "seed_2026.sql").read_text())
    conn.commit()
    return conn


def state_to_region(state_code):
    return {"AK": "ALASKA", "HI": "HAWAII"}.get(state_code.upper(), "CONTIGUOUS")


def fpl_percent(conn, income, size, state="NC", year=2026):
    sql = (HERE / "fpl_query.sql").read_text()
    row = conn.execute(sql, {"year": year, "region": state_to_region(state),
                             "size": size, "income": income}).fetchone()
    if row is None:
        raise ValueError(f"No guideline for year={year}, size={size}")
    return {"guideline": row[0], "fpl_percent": row[1]}


if __name__ == "__main__":
    conn = init_db()
    tests = [  # (income, size, state, expected %)
        (60000, 3, "NC", 219.6),   # example from our proposal
        (27320, 3, "NC", 100.0),   # exactly at the poverty line
        (33000, 4, "NC", 100.0),
        (61400, 9, "NC", 100.0),   # 55,720 + 5,680 for the 9th person
        (34150, 3, "AK", 100.0),   # Alaska uses its own table
    ]
    for income, size, state, expected in tests:
        r = fpl_percent(conn, income, size, state)
        status = "OK " if r["fpl_percent"] == expected else "FAIL"
        print(f"{status} income=${income:,} size={size} {state}: "
              f"guideline=${r['guideline']:,} -> {r['fpl_percent']}% FPL")

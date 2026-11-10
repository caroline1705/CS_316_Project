import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "household" / "curebase.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

query = """
    SELECT
        pc.code,
        pc.code_type,
        p.description,
        COUNT(*) AS num_records,
        MIN(p.gross_charge) AS minimum_gross,
        MAX(p.gross_charge) AS maximum_gross
    FROM hospital_price p
    JOIN hospital_price_code pc
        ON p.price_id = pc.price_id
    WHERE p.hospital_id = ?
        AND UPPER(p.description) LIKE ?
        AND UPPER(COALESCE(p.description, '')) NOT LIKE '%STUDY%'
    GROUP BY pc.code, pc.code_type, p.description
    ORDER BY pc.code, p.description
"""

rows = conn.execute(
    query,
    ("UNC", "%CYCLOPHOSPHAMIDE%")
).fetchall()

print(f"Found {len(rows)} standard cyclophosphamide descriptions")

for row in rows:
    print(dict(row))

conn.close()

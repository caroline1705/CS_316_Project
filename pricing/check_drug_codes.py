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
        p.gross_charge,
        p.discounted_cash,
        p.negotiated_dollar,
        p.payer_name,
        p.plan_name,
        p.setting
    FROM hospital_price_code pc
    JOIN hospital_price p
        ON pc.price_id = p.price_id
    WHERE p.hospital_id = ?
        AND UPPER(pc.code) = ?
    ORDER BY p.payer_name, p.plan_name
"""

rows = conn.execute(query, ("UNC", "J9267")).fetchall()

print(f"Found {len(rows)} records for J9267")

for row in rows[:15]:
    print(dict(row))

conn.close()
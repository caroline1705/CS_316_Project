import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "household" / "curebase.db"

codes = ["J9000", "J9070", "J9355"]

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

for code in codes:
    query = """
        SELECT
            pc.code,
            pc.code_type,
            p.description,
            COUNT(*) AS num_records,
            MIN(p.gross_charge) AS minimum_gross,
            MAX(p.gross_charge) AS maximum_gross
        FROM hospital_price_code pc
        JOIN hospital_price p
            ON pc.price_id = p.price_id
        WHERE p.hospital_id = ?
            AND pc.code = ?
        GROUP BY pc.code, pc.code_type, p.description
        ORDER BY num_records DESC
    """

    rows = conn.execute(query, ("UNC", code)).fetchall()

    print(f"\nCode {code}: {len(rows)} distinct descriptions")

    for row in rows:
        print(dict(row))

conn.close()
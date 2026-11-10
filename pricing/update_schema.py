import sqlite3

conn = sqlite3.connect("household/curebase.db")

columns = {
    "drug_unit_of_measurement": "TEXT",
    "drug_type_of_measurement": "TEXT",
    "modifiers": "TEXT",
    "count_raw": "TEXT",
    "median_amount": "REAL",
    "percentile_10": "REAL",
    "percentile_90": "REAL",
    "minimum_charge": "REAL",
    "maximum_charge": "REAL"
}

existing = conn.execute("PRAGMA table_info(hospital_price)").fetchall()
existing_columns = [row[1] for row in existing]

for column, data_type in columns.items():
    if column not in existing_columns:
        conn.execute(f"ALTER TABLE hospital_price ADD COLUMN {column} {data_type}")
        print(f"Added {column}")

conn.commit()
conn.close()

import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

DB = ROOT / "household" / "curebase.db"
PRICES_FILE = ROOT / "data" / "processed" / "unc_prices.csv"
CODES_FILE = ROOT / "data" / "processed" / "unc_price_codes.csv"

BATCH_SIZE = 5000

PRICE_COLUMNS = [
    "record_id",
    "hospital_id",
    "source_file",
    "source_row",
    "description",
    "billing_class",
    "setting",
    "drug_unit_of_measurement",
    "drug_type_of_measurement",
    "payer_name",
    "plan_name",
    "modifiers",
    "negotiated_algorithm",
    "count_raw",
    "pricing_methodology",
    "additional_notes",
    "gross_charge",
    "discounted_cash",
    "negotiated_dollar",
    "negotiated_percentage",
    "median_amount",
    "percentile_10",
    "percentile_90",
    "minimum_charge",
    "maximum_charge"
]

NUMERIC_COLUMNS = [
    "gross_charge",
    "discounted_cash",
    "negotiated_dollar",
    "negotiated_percentage",
    "median_amount",
    "percentile_10",
    "percentile_90",
    "minimum_charge",
    "maximum_charge"
]


def clean_value(value):
    if value is None or value.strip() == "":
        return None
    return value.strip()


def import_prices(conn):
    columns = ", ".join(PRICE_COLUMNS)
    placeholders = ", ".join(["?"] * len(PRICE_COLUMNS))

    sql = f"""
        INSERT INTO hospital_price ({columns})
        VALUES ({placeholders})
    """

    batch = []
    total = 0

    with PRICES_FILE.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        missing = set(PRICE_COLUMNS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing price CSV columns: {sorted(missing)}")

        for row in reader:
            values = []

            for column in PRICE_COLUMNS:
                value = clean_value(row[column])

                if value is not None and column in NUMERIC_COLUMNS:
                    value = float(value)

                values.append(value)

            batch.append(tuple(values))

            if len(batch) >= BATCH_SIZE:
                conn.executemany(sql, batch)
                total += len(batch)
                batch = []

        if batch:
            conn.executemany(sql, batch)
            total += len(batch)

    print(f"Imported {total:,} UNC price records")


def import_codes(conn):
    conn.execute("""
        CREATE TEMP TABLE staging_price_codes (
            record_id TEXT NOT NULL,
            code TEXT NOT NULL,
            code_type TEXT NOT NULL,
            code_position INTEGER NOT NULL
        )
    """)

    sql = """
        INSERT INTO staging_price_codes
        (record_id, code, code_type, code_position)
        VALUES (?, ?, ?, ?)
    """

    batch = []
    total = 0

    with CODES_FILE.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required = {"record_id", "code", "code_type", "code_position"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing code CSV columns: {sorted(missing)}")

        for row in reader:
            record_id = clean_value(row["record_id"])
            code = clean_value(row["code"])
            code_type = clean_value(row["code_type"])
            position = clean_value(row["code_position"])

            if not record_id or not code or not code_type or not position:
                raise ValueError(f"Incomplete billing code row: {row}")

            batch.append((record_id, code, code_type, int(position)))

            if len(batch) >= BATCH_SIZE:
                conn.executemany(sql, batch)
                total += len(batch)
                batch = []

        if batch:
            conn.executemany(sql, batch)
            total += len(batch)

    conn.execute("""
        CREATE INDEX idx_staging_record_id
        ON staging_price_codes(record_id)
    """)

    unmatched = conn.execute("""
        SELECT COUNT(*)
        FROM staging_price_codes s
        LEFT JOIN hospital_price p
            ON s.record_id = p.record_id
            AND p.hospital_id = 'UNC'
        WHERE p.price_id IS NULL
    """).fetchone()[0]

    if unmatched:
        raise ValueError(f"{unmatched:,} billing codes have no matching price")

    conn.execute("""
        INSERT INTO hospital_price_code
        (price_id, code, code_type, code_position)
        SELECT p.price_id, s.code, s.code_type, s.code_position
        FROM staging_price_codes s
        JOIN hospital_price p
            ON s.record_id = p.record_id
            AND p.hospital_id = 'UNC'
    """)

    conn.execute("DROP TABLE staging_price_codes")

    print(f"Imported {total:,} UNC billing code associations")


def main():
    if not DB.is_file():
        raise FileNotFoundError(f"Database not found: {DB}")

    if not PRICES_FILE.is_file():
        raise FileNotFoundError(f"Prices file not found: {PRICES_FILE}")

    if not CODES_FILE.is_file():
        raise FileNotFoundError(f"Codes file not found: {CODES_FILE}")

    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        existing_columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(hospital_price)")
        }

        missing = set(PRICE_COLUMNS) - existing_columns

        if missing:
            raise ValueError(
                f"Missing hospital_price columns: {sorted(missing)}"
            )

        existing = conn.execute("""
            SELECT COUNT(*)
            FROM hospital_price
            WHERE hospital_id = 'UNC'
        """).fetchone()[0]

        if existing:
            raise ValueError(
                f"UNC already has {existing:,} pricing records. "
                "Import cancelled to avoid duplicates."
            )

        hospital = conn.execute("""
            SELECT hospital_id
            FROM hospital
            WHERE hospital_id = 'UNC'
        """).fetchone()

        if hospital is None:
            raise ValueError("UNC is missing from the hospital table")

        import_prices(conn)
        import_codes(conn)

        conn.commit()

        print("Import completed successfully")
        print(f"Database: {DB}")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()

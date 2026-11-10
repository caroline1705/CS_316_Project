import argparse
import csv
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

input_file = "data/raw/university-of-north-carolina-hospitals-at-chapel-hill_standardcharges.csv"

CODE_COLUMNS = [(f"code|{i}", f"code|{i}|type") for i in range(1, 5)]
PRICE_COLUMNS = {
    "standard_charge|gross": "gross_charge",
    "standard_charge|discounted_cash": "discounted_cash",
    "standard_charge|negotiated_dollar": "negotiated_dollar",
    "standard_charge|negotiated_percentage": "negotiated_percentage",
    "median_amount": "median_amount",
    "10th_percentile": "percentile_10",
    "90th_percentile": "percentile_90",
    "standard_charge|min": "minimum_charge",
    "standard_charge|max": "maximum_charge",
}
TEXT_COLUMNS = {
    "description": "description",
    "billing_class": "billing_class",
    "setting": "setting",
    "drug_unit_of_measurement": "drug_unit_of_measurement",
    "drug_type_of_measurement": "drug_type_of_measurement",
    "payer_name": "payer_name",
    "plan_name": "plan_name",
    "modifiers": "modifiers",
    "standard_charge|negotiated_algorithm": "negotiated_algorithm",
    "count": "count_raw",
    "standard_charge|methodology": "pricing_methodology",
    "additional_generic_notes": "additional_notes",
}


def clean_number(value):
    value = (value or "").strip()
    if not value:
        return "", False
    number = value.replace(",", "").replace("$", "")
    if number.endswith("%"):
        number = number[:-1].strip()
    try:
        parsed = Decimal(number)
        if not parsed.is_finite():
            return "", True
        return format(parsed, "f"), False
    except InvalidOperation:
        return "", True


def clean_file(input_path, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    prices_path = output_dir / "unc_prices.csv"
    codes_path = output_dir / "unc_price_codes.csv"
    invalid_path = output_dir / "unc_invalid_numbers.csv"

    price_fields = ["record_id", "hospital_id", "source_file", "source_row"] + list(TEXT_COLUMNS.values()) + list(PRICE_COLUMNS.values())
    code_fields = ["record_id", "code", "code_type", "code_position"]
    row_count = 0
    code_count = 0
    invalid_count = 0
    code_types = Counter()

    with input_path.open("r", encoding="utf-8-sig", newline="") as source, \
         prices_path.open("w", encoding="utf-8", newline="") as price_file, \
         codes_path.open("w", encoding="utf-8", newline="") as code_file, \
         invalid_path.open("w", encoding="utf-8", newline="") as invalid_file:

        reader = csv.DictReader(source)
        required = {"description", "code|1", "code|1|type"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        price_writer = csv.DictWriter(price_file, fieldnames=price_fields)
        code_writer = csv.DictWriter(code_file, fieldnames=code_fields)
        invalid_writer = csv.writer(invalid_file)
        price_writer.writeheader()
        code_writer.writeheader()
        invalid_writer.writerow(["source_row", "column", "original_value"])

        for source_row, raw in enumerate(reader, start=2):
            row_count += 1
            record_id = row_count
            cleaned = {
                "record_id": record_id,
                "hospital_id": "UNC",
                "source_file": input_path.name,
                "source_row": source_row,
            }
            for original, target in TEXT_COLUMNS.items():
                cleaned[target] = (raw.get(original) or "").strip()
            for original, target in PRICE_COLUMNS.items():
                original_value = raw.get(original) or ""
                value, invalid = clean_number(original_value)
                cleaned[target] = value
                if invalid:
                    invalid_writer.writerow([source_row, original, original_value])
                    invalid_count += 1

            price_writer.writerow(cleaned)

            seen_codes = set()
            for position, (code_col, type_col) in enumerate(CODE_COLUMNS, start=1):
                code = (raw.get(code_col) or "").strip()
                code_type = (raw.get(type_col) or "").strip().upper()
                if not code or not code_type or (code, code_type) in seen_codes:
                    continue
                seen_codes.add((code, code_type))
                code_writer.writerow({
                    "record_id": record_id,
                    "code": code,
                    "code_type": code_type,
                    "code_position": position,
                })
                code_types[code_type] += 1
                code_count += 1

            if row_count % 50000 == 0:
                print(f"Processed {row_count:,} pricing records")

    print(f"Pricing records: {row_count:,}")
    print(f"Billing code associations: {code_count:,}")
    print(f"Invalid numeric values: {invalid_count:,}")
    print(f"Code types: {dict(code_types)}")
    print(f"Saved: {prices_path}")
    print(f"Saved: {codes_path}")
    print(f"Saved: {invalid_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    args = parser.parse_args()
    clean_file(args.input_file, args.output_dir)

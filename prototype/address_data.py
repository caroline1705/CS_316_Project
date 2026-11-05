"""Build-time address fixture importer, independent of database and pricing imports.

Replace this importer/provider pair with a mapping service without changing SQL or
cost calculations. Browser calculations consume distances keyed by hospital ID.
"""
import json
import math
from pathlib import Path
DEFAULT_PATH = Path(__file__).resolve().parents[1] / 'test_data/addresses/nc_addresses.json'


def load_addresses(hospital_ids, path=DEFAULT_PATH):
    records = json.loads(Path(path).read_text())['addresses']
    seen = set()
    for row in records:
        for key in ('address_id', 'street_address', 'county', 'city', 'state'):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(f'Address fixture requires {key}')
        if row['address_id'] in seen:
            raise ValueError('Duplicate address_id: '+row['address_id'])
        seen.add(row['address_id'])
        if row['state'] != 'NC':
            raise ValueError('Address fixtures must be in NC')
        miles = row['distances_miles']
        if set(miles) != set(hospital_ids):
            raise ValueError('Each address needs distances to all hospitals')
        if any(isinstance(n, bool) or not isinstance(n, (int, float)) or not math.isfinite(n) or not 0 <= n <= 2000 for n in miles.values()):
            raise ValueError('Address distances must be finite miles between 0 and 2000')
    if not records:
        raise ValueError('At least one predefined address is required')
    return records

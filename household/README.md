# CureBase – Household & Indirect Cost Module

Owner: Wanting Zhao (wz206)

Prototype data layer and API for (1) household income as a percentage of the
federal poverty guideline (FPL), (2) standard treatment regimens, and
(3) non-medical costs of treatment (travel, lodging, childcare).

## Run

```bash
pip install flask
python3 fpl.py        # creates curebase.db, loads 2026 poverty guidelines, runs tests
python3 regimen.py    # loads treatment regimens, prints visits/duration
python3 indirect.py   # loads mileage/lodging/childcare rates, prints sample estimates
python3 app.py        # starts API at http://127.0.0.1:5001
```

## API

| Endpoint | Example |
|---|---|
| `GET /api/fpl` | `/api/fpl?income=60000&size=3&state=NC` → `fpl_percent: 219.6` |
| `GET /api/indirect-costs` | `/api/indirect-costs?regimen=CRC_FOLFOX&distance=30&county=Durham&children=0` → `total: 338.4` |

Errors: `400` invalid input, `404` unknown regimen.

## Files

| File | Purpose |
|---|---|
| `schema.sql`, `seed_2026.sql`, `fpl_query.sql` | Poverty guideline tables, 2026 data, FPL query |
| `schema_regimen.sql`, `seed_regimen.sql`, `regimen_query.sql` | Cancer type / treatment / regimen tables and visit summary query |
| `schema_indirect.sql`, `seed_indirect.sql`, `indirect_query.sql` | IRS mileage, GSA lodging, childcare rates and cost query |
| `app.py` | Flask endpoints |

## Data sources and status

| Data | Source | Status |
|---|---|---|
| 2026 poverty guidelines | HHS, Federal Register doc. 2026-00755 | Verified |
| 2026 IRS medical mileage rate | irs.gov Standard Mileage Rates | Verified |
| FY2027 NC lodging per diem | GSA (via FederalPay.org) | To confirm on gsa.gov (seasonal areas) |
| Treatment regimens | Sample schedules | DRAFT – replace after team picks cancer types; check against NCI |
| Childcare hourly rate | Placeholder ($15/hr) | TODO – DOL National Database of Childcare Prices |

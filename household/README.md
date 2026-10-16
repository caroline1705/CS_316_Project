# CureBase – Household & Indirect Cost Module

Owner: Wanting Zhao (wz206)

Prototype data layer and API for (1) household income as a percentage of the
federal poverty guideline (FPL), (2) standard treatment regimens, and
(3) non-medical costs of treatment (travel, lodging, childcare).

## Run

```bash
pip install flask
python3 init_db.py    # builds curebase.db with all tables and data
python3 app.py        # web page + API at http://127.0.0.1:5001
```

Optional command-line checks: `python3 fpl.py` (FPL tests), `python3 regimen.py`,
`python3 indirect.py` (sample cost estimates).

## API

| Endpoint | Example |
|---|---|
| `GET /api/fpl` | `/api/fpl?income=60000&size=3&state=NC` → `fpl_percent: 219.6` |
| `GET /api/indirect-costs` | `/api/indirect-costs?regimen=BREAST_ACT_H&distance=150&county=Durham&children=1&home_county=Durham&age_group=PRESCHOOL` → `total: 12246.96` |
| `GET /api/regimens` | Cancer/regimen options for the dropdown |
| `GET /api/counties` | NC counties with their own GSA lodging rate |
| `GET /api/nc-counties` | All 100 NC counties (home county for childcare) |
| `GET /` | Web page (`templates/household.html`) |

`county` = hospital county (lodging); `home_county` = patient's county (childcare).
Errors: `400` invalid input, `404` unknown regimen.

## Files

| File | Purpose |
|---|---|
| `schema.sql`, `seed_2026.sql`, `fpl_query.sql` | Poverty guideline tables, 2026 data, FPL query |
| `schema_regimen.sql`, `seed_regimen.sql`, `regimen_query.sql` | Cancer type / treatment / regimen tables and visit summary query |
| `schema_indirect.sql`, `seed_indirect.sql`, `indirect_query.sql` | IRS mileage, GSA lodging, county childcare tables and cost query |
| `seed_childcare.sql`, `build_childcare_seed.py` | NC childcare prices (generated from the DOL file) |
| `init_db.py` | Builds the whole database |
| `app.py`, `templates/household.html` | Flask endpoints and web page |

## Data sources and status

| Data | Source | Status |
|---|---|---|
| 2026 poverty guidelines | HHS, Federal Register doc. 2026-00755 | Verified |
| 2026 IRS medical mileage rate | irs.gov Standard Mileage Rates | Verified |
| FY2027 NC lodging per diem | GSA (via FederalPay.org) | To confirm on gsa.gov (seasonal areas) |
| Treatment regimens | Sample schedules | DRAFT – replace after team picks cancer types; check against NCI |
| NC childcare prices (100 counties) | U.S. DOL National Database of Childcare Prices, 2022 (latest release), center-based weekly median | Loaded; Graham County has no data and uses the NC median |

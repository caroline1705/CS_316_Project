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
| `GET /` | Web page (`templates/household.html`) |
| `GET /api/fpl` | `/api/fpl?income=60000&size=3&state=NC` → `fpl_percent: 219.6` |
| `GET /api/cancers` | Supported cancer types (5) |
| `GET /api/regimens` | `/api/regimens?cancer=LUNG` → treatment plans for one cancer |
| `GET /api/regimen-detail` | `/api/regimen-detail?regimen=LUNG_CRT_DURVA` → phases, 43 visits, ~60 weeks |
| `GET /api/hospitals` | The 5 hospitals in scope, with their counties |
| `GET /api/nc-counties` | All 100 NC counties (home county for childcare) |
| `GET /api/counties` | NC counties with their own GSA lodging rate |
| `GET /api/indirect-costs` | `/api/indirect-costs?regimen=BREAST_ACT_H&hospital=DUKE&distance=150&children=1&home_county=Durham&age_group=PRESCHOOL` → `total: 12246.96` |

`hospital` decides the lodging rate (through its county; `county=<name>` also works);
`home_county` decides the childcare price. The response flags `lodging_is_standard` and
`childcare_is_median` when county data is missing and a fallback is used.
Errors: `400` invalid input, `404` unknown regimen or hospital.

## Files

| File | Purpose |
|---|---|
| `schema.sql`, `seed_2026.sql`, `fpl_query.sql` | Poverty guideline tables, 2026 data, FPL query |
| `schema_regimen.sql`, `seed_regimen.sql`, `regimen_query.sql`, `regimen_detail_query.sql` | Cancer type / treatment / regimen tables, visit summary and phase detail queries |
| `schema_indirect.sql`, `seed_indirect.sql`, `indirect_query.sql` | IRS mileage, GSA lodging, county childcare tables and cost query |
| `seed_childcare.sql`, `build_childcare_seed.py` | NC counties and childcare prices (generated from the DOL file) |
| `seed_hospital.sql` | The 5 hospitals in scope (table defined in `schema_indirect.sql`) |
| `init_db.py` | Builds the whole database |
| `app.py`, `templates/household.html` | Flask endpoints and web page |

## Data sources and status (checked 2026-10-31)

| Data | Source | Status |
|---|---|---|
| 2026 poverty guidelines | HHS, Federal Register doc. 2026-00755 | Verified against official source |
| IRS medical mileage rate (20.5¢ Jan–Jun 2026, 23.5¢ from Jul 1, 2026) | irs.gov Standard Mileage Rates | Verified against official source; the app uses the rate in effect today |
| GSA FY2027 per diem: standard $113 lodging / $68 M&IE | Federal News Network (Sept 2026) | Confirmed by news report of the GSA announcement |
| GSA FY2027 per diem: 7 NC county rates (incl. Durham $124/$74, Orange $153/$80, Mecklenburg $143/$80) | FederalPay.org and FedPayScale.org (republish GSA data) | Cross-checked on two sites, same rate every month. Seasonal coastal areas (Carteret, Dare, New Hanover) removed; they use the standard rate. Forsyth and Pitt (Wake Forest Baptist, ECU) have no county rate and use the standard rate |
| NC childcare prices (100 counties) | U.S. DOL National Database of Childcare Prices, study year 2022 (latest release); center-based weekly median | Loaded from the official file. Prices are in 2022 dollars (not inflation-adjusted). Graham County has no data and uses the NC median |
| Hospitals (5) | Team scope decision | Duke (Durham Co.), UNC Lineberger (Orange), Atrium Wake Forest Baptist (Forsyth), Atrium Levine (Mecklenburg), ECU Health (Pitt) |
| Treatment regimens (5 cancers) | See table below | One typical regimen per cancer for estimating visits; a patient's real plan is set by their care team |

| Cancer (ICD-10) | Regimen | Visits / weeks | Source |
|---|---|---|---|
| Breast (C50) | Dose-dense AC q2w ×4 → paclitaxel q2w ×4 + trastuzumab q3w for 1 year (~17 doses) → whole-breast RT 40 Gy/15 fractions | 40 / ~59 | Cancer Care Ontario AC-PACL(DD)+TRAS protocol; ASTRO 2018 whole-breast RT guideline |
| Lung, NSCLC stage III (C34) | Chemoradiation 60 Gy/30 fractions with weekly chemo → durvalumab q4w for up to 12 months | 43 / ~60 | PACIFIC trial (ESMO); FDA-approved 1500 mg q4w dosing |
| Colorectal (C18–C20) | Adjuvant mFOLFOX6 q2w ×12; 2 visits per cycle (infusion + pump removal, an assumption) | 24 / ~24 | HSE mFOLFOX6 protocol |
| Prostate (C61) | Hormone therapy (injection q3 months ×2) + RT 60 Gy/20 fractions starting at month 3 | 22 / ~24 | CHHiP trial, Lancet Oncology 2016 (ICR repository) |
| DLBCL (C83.3) | R-CHOP q3w ×6 → rituximab q3w ×2 | 8 / ~24 | POLARIX trial control arm (Lymphoma Hub) |

### Modeling assumptions
- One overnight stay (GSA lodging + M&IE) per visit when the one-way distance is 100+ miles.
- One day of childcare per visit = weekly center-based price ÷ 5, per child.
- Daily radiation counts as one visit per weekday session.

# CureBase local prototype

Open **[prototype.html](prototype.html)** in a browser. The form starts blank. You can enter a profile or explicitly load one of four sample households.

## Files in this folder

`prototype.html`: Generated runnable application with embedded records, styling and scripts. Open this file to use the prototype. Rebuilding overwrites it. 
`template.html`: Editable page structure, styles and script insertion markers. This is an unbuilt source template, not the runnable application. 
`app.js`: Form initialization, four sample households, conditional field visibility, validation feedback, result display, filters and pagination. 
`engine.js`: Profile validation, household income/FPL calculation, medical and indirect cost estimates, assistance screening and financial ranking. Also holds fictional hospital age rules. 
`build.py`: Loads the existing team SQL and separate test-price SQL into an in-memory SQLite database, independently imports addresses, and embeds the data and scripts into `prototype.html`. It does not modify the team's database. 
`address_data.py`: Independent build-time importer and validator for the predefined address JSON file. 
`distance_provider.js`: Independent browser address/distance lookup interface. It currently resolves fixtures; it can later be replaced by a map-service provider.

## Test Data made up for this prototype

The following data are made-up test data for this prototype:
- 25 medical charge records (placeholder for Caroline's data)
- A drop-down list of predetermined list of addresses, along with predetermined distance to each hospital (to actually implement this, we would have to use the service of an external map software, so maybe we can just leave it like this in the final product; currently, address fetching is implemented as an independent module)
- Arbitrary age cutoffs for assisstance program policies
- All five hospitals treated as offering every seeded regimen package

In addition, the current prototype comes in with four predetermined sets of exemplar test data. 

### Data reused from the existing project

The build retains the team's five hospitals, diagnosis and regimen records, treatment phases, visit/duration summaries, 2026 poverty guidelines, mileage rates, FY2027 lodging rates, county childcare prices and assistance-program records from `../household/` and `../assistance/`.

## Interface behavior

All data uses ordinary text. Only prototype commentary and explicitly marked debug interfaces use italics. Required fields have a red asterisk.

Childcare age group is visible, enabled and required only when **Children needing care** is greater than zero. Lost hourly pay is visible, enabled and required only when **Work hours lost / visit** is greater than zero. Both fields are hidden when the controlling input is blank or zero. A hidden hourly-pay value is ignored, so lost-wage costs are zero when work hours lost are zero. Values can be retained while hidden to allow toggling back without retyping them.

## Rebuild and verify

From the project root:

```sh
python3 prototype/build.py
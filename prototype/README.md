# CureBase integrated prototype

## Run

In the project root, install Flask once:

```sh
python3 -m venv prototype/.venv
prototype/.venv/bin/python -m pip install 'Flask>=3.1,<4'
prototype/.venv/bin/python prototype/app.py
```

Then open **http://127.0.0.1:5001** in a browser.

`init_db.py` creates `prototype/curebase.db` from the existing `household/` and `assistance/` SQL files plus the price fixtures in `prototype/test_data/pricing/`. If the database is missing, startup exits with instructions to run `init_db.py`. For subsequent launches, run only `app.py`.


## Files

`app.py`: Runs the existing household Flask application, serves the new page, retains all nine original API handlers, and adds five integration endpoints. Configures the household and assistance modules to use the same prototype database at startup. |
`init_db.py`: Creates the prototype SQLite database from existing SQL and price fixtures; supports an explicit rebuild. |
`comparison.py`: Server-side validation, existing-service integration, medical estimates, assistance explanations and hospital ranking.
`templates/prototype.html`: Flask HTML template retaining the original layout and styles. |
`static/prototype.js`: Frontend form behavior, sample households, API requests, error handling and result display. |
`address.py`: Address fixture loader and validation. |
`test_data`: test address and price fixtures.

Flask is the only direct external dependency.

## Preserved data and behavior

The four sample households, 25 fictional medical price records, four fictional addresses and their hospital distances, fictional hospital age rules, and assumed regimen offerings are retained. The colors, layout, conditional childcare/pay fields, cost tables, assistance cards, filters and one-hospital-per-page navigation are retained.

Household calculations use the existing SQL/Python implementation. Comparison rates remain fixed to the original demonstration date, November 4, 2026, with FY2027 lodging rates. The standalone household indirect-cost endpoint retains its existing current-date behavior. Assistance screening uses the existing assistance matcher; exclusions are explained using that module's rule-checking functions. Unknown requirements and funding availability still require review. Assistance is never deducted from estimated costs.
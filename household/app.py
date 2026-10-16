"""CureBase household API (prototype). Run:  python3 app.py"""
import sqlite3
from flask import Flask, request, jsonify, render_template
from fpl import DB, fpl_percent
from indirect import indirect_costs, AGE_GROUPS

app = Flask(__name__)


@app.get("/api/fpl")
def api_fpl():
    # 1. Read inputs from the URL, e.g. /api/fpl?income=60000&size=3&state=NC
    try:
        income = float(request.args["income"])
        size = int(request.args["size"])
    except (KeyError, ValueError):
        return jsonify(error="income and size are required numbers"), 400
    if income < 0 or size < 1:
        return jsonify(error="income must be >= 0 and size >= 1"), 400
    state = request.args.get("state", "NC")

    # 2. Run the SQL query from Step 1
    conn = sqlite3.connect(DB)
    try:
        result = fpl_percent(conn, income, size, state)
    finally:
        conn.close()

    # 3. Send the answer back as JSON
    return jsonify(income=income, household_size=size, state=state, **result)


@app.get("/api/indirect-costs")
def api_indirect_costs():
    # 1. Read inputs, e.g.
    #    ?regimen=BREAST_ACT_H&distance=150&county=Durham&children=1&home_county=Durham&age_group=PRESCHOOL
    try:
        regimen = request.args["regimen"]
        distance = float(request.args["distance"])
        county = request.args["county"]
        children = int(request.args.get("children", "0"))
    except (KeyError, ValueError):
        return jsonify(error="regimen, county and a numeric distance are required"), 400
    home_county = request.args.get("home_county") or None
    age_group = request.args.get("age_group", "PRESCHOOL").upper()
    if distance < 0:
        return jsonify(error="distance must be >= 0"), 400
    if not 0 <= children <= 10:
        return jsonify(error="children must be between 0 and 10"), 400
    if age_group not in AGE_GROUPS:
        return jsonify(error=f"age_group must be one of {', '.join(AGE_GROUPS)}"), 400

    conn = sqlite3.connect(DB)
    try:
        # 2. Make sure the regimen exists before running the cost query
        found = conn.execute(
            "SELECT 1 FROM regimen WHERE regimen_id = ?", (regimen,)).fetchone()
        if found is None:
            return jsonify(error=f"unknown regimen '{regimen}'"), 404

        # 3. Run the cost query
        result = indirect_costs(conn, regimen, distance, county, num_children=children,
                                home_county=home_county, age_group=age_group)
    finally:
        conn.close()

    # 4. Return JSON
    return jsonify(regimen=regimen, distance_miles=distance, county=county,
                   children=children, home_county=home_county, age_group=age_group,
                   **result)


@app.get("/")
def household_page():
    # The web page for this module (templates/household.html)
    return render_template("household.html")


@app.get("/api/regimens")
def api_regimens():
    # Options for the cancer/regimen dropdown, read from the database,
    # so the page updates automatically when the team changes the data.
    conn = sqlite3.connect(DB)
    try:
        rows = conn.execute("""
            SELECT r.regimen_id, c.name, r.name
            FROM regimen r JOIN cancer_type c ON c.cancer_id = r.cancer_id
            ORDER BY c.name, r.name""").fetchall()
    finally:
        conn.close()
    return jsonify([{"regimen_id": rid, "cancer": cancer, "regimen": name}
                    for rid, cancer, name in rows])


@app.get("/api/counties")
def api_counties():
    # NC counties that have their own GSA lodging rate (others use the standard rate)
    conn = sqlite3.connect(DB)
    try:
        rows = conn.execute("""
            SELECT county, city FROM lodging_rate
            WHERE state = 'NC' AND fiscal_year = 2027 AND county <> 'STANDARD'
            ORDER BY county""").fetchall()
    finally:
        conn.close()
    return jsonify([{"county": county, "city": city} for county, city in rows])


@app.get("/api/nc-counties")
def api_nc_counties():
    # All 100 NC counties, for the "home county" dropdown
    conn = sqlite3.connect(DB)
    try:
        rows = conn.execute("""
            SELECT county FROM county WHERE state = 'NC' ORDER BY county""").fetchall()
    finally:
        conn.close()
    return jsonify([county for (county,) in rows])


if __name__ == "__main__":
    app.run(debug=True, port=5001)

"""CureBase household API (prototype). Run:  python3 app.py"""
import sqlite3
from flask import Flask, request, jsonify
from fpl import DB, fpl_percent
from indirect import indirect_costs

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
    # 1. Read inputs, e.g. ?regimen=CRC_FOLFOX&distance=30&county=Durham&children=0
    try:
        regimen = request.args["regimen"]
        distance = float(request.args["distance"])
        county = request.args["county"]
        children = request.args.get("children", "0") == "1"
    except (KeyError, ValueError):
        return jsonify(error="regimen, county and a numeric distance are required"), 400
    if distance < 0:
        return jsonify(error="distance must be >= 0"), 400

    conn = sqlite3.connect(DB)
    try:
        # 2. Make sure the regimen exists before running the cost query
        found = conn.execute(
            "SELECT 1 FROM regimen WHERE regimen_id = ?", (regimen,)).fetchone()
        if found is None:
            return jsonify(error=f"unknown regimen '{regimen}'"), 404

        # 3. Run the query from Step 3
        result = indirect_costs(conn, regimen, distance, county, children)
    finally:
        conn.close()

    # 4. Return JSON
    return jsonify(regimen=regimen, distance_miles=distance, county=county,
                   has_children=children, **result)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

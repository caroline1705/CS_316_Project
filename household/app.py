"""CureBase household API. Run:  python3 init_db.py  then  python3 app.py"""
import sqlite3
from pathlib import Path

from flask import Flask, request, jsonify, render_template
from fpl import DB, fpl_percent
from indirect import indirect_costs, AGE_GROUPS
from regimen import regimen_summary

HERE = Path(__file__).parent
app = Flask(__name__)


def query(sql, params=()):
    """Run a read-only query and return all rows."""
    conn = sqlite3.connect(DB)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


# ---------------------------------------------------------------- web page
@app.get("/")
def household_page():
    # The web page for this module (templates/household.html)
    return render_template("household.html")


# ---------------------------------------------------------------- FPL
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

    # 2. Run the FPL query
    conn = sqlite3.connect(DB)
    try:
        result = fpl_percent(conn, income, size, state)
    finally:
        conn.close()

    # 3. Send the answer back as JSON
    return jsonify(income=income, household_size=size, state=state, **result)


# ---------------------------------------------------------------- diagnosis and treatment
@app.get("/api/cancers")
def api_cancers():
    # Step 1 of the two-level menu: supported cancer types
    rows = query("SELECT cancer_id, name, icd10_prefix FROM cancer_type ORDER BY name")
    return jsonify([{"cancer_id": cid, "name": name, "icd10": icd} for cid, name, icd in rows])


@app.get("/api/regimens")
def api_regimens():
    # Step 2: regimens, optionally only for one cancer (?cancer=BREAST)
    cancer = request.args.get("cancer")
    rows = query("""
        SELECT r.regimen_id, c.cancer_id, c.name, r.name
        FROM regimen r JOIN cancer_type c ON c.cancer_id = r.cancer_id
        WHERE (? IS NULL OR r.cancer_id = ?)
        ORDER BY c.name, r.name""", (cancer, cancer))
    return jsonify([{"regimen_id": rid, "cancer_id": cid, "cancer": cname, "regimen": rname}
                    for rid, cid, cname, rname in rows])


@app.get("/api/regimen-detail")
def api_regimen_detail():
    # Phases, total visits and duration of one regimen (?regimen=BREAST_ACT_H)
    regimen = request.args.get("regimen")
    if not regimen:
        return jsonify(error="regimen is required"), 400
    head = query("SELECT name, source_url FROM regimen WHERE regimen_id = ?", (regimen,))
    if not head:
        return jsonify(error=f"unknown regimen '{regimen}'"), 404

    sql = (HERE / "regimen_detail_query.sql").read_text()
    phases = [dict(zip(["phase", "treatment", "modality", "start_week", "cycle_days",
                        "cycles", "visits_per_cycle", "visits"], row))
              for row in query(sql, {"regimen_id": regimen})]
    conn = sqlite3.connect(DB)
    try:
        summary = regimen_summary(conn, regimen_id=regimen)[0]
    finally:
        conn.close()
    return jsonify(regimen_id=regimen, name=head[0][0], source_url=head[0][1],
                   total_visits=summary[3], total_weeks=summary[4], phases=phases)


# ---------------------------------------------------------------- locations
@app.get("/api/hospitals")
def api_hospitals():
    # Hospitals in scope; each one's county decides the lodging rate
    rows = query("SELECT hospital_id, name, city, county FROM hospital ORDER BY name")
    return jsonify([{"hospital_id": hid, "name": name, "city": city, "county": county}
                    for hid, name, city, county in rows])


@app.get("/api/counties")
def api_counties():
    # NC counties that have their own GSA lodging rate (others use the standard rate)
    rows = query("""
        SELECT county, city FROM lodging_rate
        WHERE state = 'NC' AND fiscal_year = 2027 AND county <> 'STANDARD'
        ORDER BY county""")
    return jsonify([{"county": county, "city": city} for county, city in rows])


@app.get("/api/nc-counties")
def api_nc_counties():
    # All 100 NC counties, for the "home county" dropdown
    rows = query("SELECT county FROM county WHERE state = 'NC' ORDER BY county")
    return jsonify([county for (county,) in rows])


# ---------------------------------------------------------------- indirect costs
@app.get("/api/indirect-costs")
def api_indirect_costs():
    # 1. Read inputs, e.g.
    #    ?regimen=BREAST_ACT_H&hospital=DUKE&distance=150&children=1&home_county=Durham&age_group=PRESCHOOL
    #    (county=<name> can be passed instead of hospital=<id>)
    try:
        regimen = request.args["regimen"]
        distance = float(request.args["distance"])
        children = int(request.args.get("children", "0"))
    except (KeyError, ValueError):
        return jsonify(error="regimen and a numeric distance are required"), 400
    hospital_id = request.args.get("hospital")
    county = request.args.get("county")
    home_county = request.args.get("home_county") or None
    age_group = request.args.get("age_group", "PRESCHOOL").upper()
    if not hospital_id and not county:
        return jsonify(error="hospital (or county) is required"), 400
    if distance < 0:
        return jsonify(error="distance must be >= 0"), 400
    if not 0 <= children <= 10:
        return jsonify(error="children must be between 0 and 10"), 400
    if age_group not in AGE_GROUPS:
        return jsonify(error=f"age_group must be one of {', '.join(AGE_GROUPS)}"), 400

    conn = sqlite3.connect(DB)
    try:
        # 2. Check the regimen and look up the hospital's county
        if conn.execute("SELECT 1 FROM regimen WHERE regimen_id = ?", (regimen,)).fetchone() is None:
            return jsonify(error=f"unknown regimen '{regimen}'"), 404
        hospital_name = None
        if hospital_id:
            row = conn.execute("SELECT name, county FROM hospital WHERE hospital_id = ?",
                               (hospital_id,)).fetchone()
            if row is None:
                return jsonify(error=f"unknown hospital '{hospital_id}'"), 404
            hospital_name, county = row

        # 3. Run the cost query
        result = indirect_costs(conn, regimen, distance, county, num_children=children,
                                home_county=home_county, age_group=age_group)
    finally:
        conn.close()

    # 4. Return JSON
    return jsonify(regimen=regimen, hospital=hospital_id, hospital_name=hospital_name,
                   county=county, distance_miles=distance, children=children,
                   home_county=home_county, age_group=age_group, **result)


if __name__ == "__main__":
    app.run(debug=True, port=5001)

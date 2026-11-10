import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "household" / "curebase.db"


def get_treatment_cost_components(treatment_id, hospital_id, payer_name, plan_name):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            bc.treatment_id,
            bc.component_name,
            bc.code,
            bc.code_type,
            bc.units_per_cycle,
            p.record_id,
            p.description,
            p.setting,
            p.gross_charge,
            p.discounted_cash,
            p.negotiated_dollar,
            p.negotiated_percentage,
            p.pricing_methodology,
            p.drug_unit_of_measurement,
            p.drug_type_of_measurement,
            p.count_raw
        FROM treatment_billing_code bc
        JOIN hospital_price_code pc
            ON bc.code = pc.code
            AND bc.code_type = pc.code_type
        JOIN hospital_price p
            ON pc.price_id = p.price_id
        WHERE bc.treatment_id = ?
            AND p.hospital_id = ?
            AND p.payer_name = ?
            AND p.plan_name = ?
            AND p.setting = 'outpatient'
            AND UPPER(COALESCE(p.description, '')) NOT LIKE '%STUDY%'
        ORDER BY bc.code, p.record_id
    """

    rows = conn.execute(
        query,
        (treatment_id, hospital_id, payer_name, plan_name)
    ).fetchall()

    results = [dict(row) for row in rows]

    conn.close()

    return results



def summarize_treatment_prices(prices):
    components = {}

    for price in prices:
        code = price["code"]
        amount = price["negotiated_dollar"]

        if amount is None:
            continue

        if code not in components:
            components[code] = {
                "component_name": price["component_name"],
                "code_type": price["code_type"],
                "prices": []
            }

        components[code]["prices"].append(amount)

    summary = {}
    minimum_sum = 0
    maximum_sum = 0

    for code, component in components.items():
        minimum_price = min(component["prices"])
        maximum_price = max(component["prices"])

        summary[code] = {
            "component_name": component["component_name"],
            "code_type": component["code_type"],
            "minimum_price": minimum_price,
            "maximum_price": maximum_price,
            "num_records": len(component["prices"])
        }

        minimum_sum += minimum_price
        maximum_sum += maximum_price

    return {
        "components": summary,
        "unadjusted_minimum_sum": round(minimum_sum, 2),
        "unadjusted_maximum_sum": round(maximum_sum, 2)
    }



def get_regimen_treatments(regimen_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    query = """
        SELECT
            r.regimen_id,
            r.name AS regimen_name,
            rp.phase_no,
            rp.treatment_id,
            t.name AS treatment_name,
            t.modality,
            rp.start_week,
            rp.cycle_length_days,
            rp.num_cycles,
            rp.visits_per_cycle
        FROM regimen r
        JOIN regimen_phase rp
            ON r.regimen_id = rp.regimen_id
        JOIN treatment t
            ON rp.treatment_id = t.treatment_id
        WHERE r.regimen_id = ?
        ORDER BY rp.phase_no
    """

    rows = conn.execute(query, (regimen_id,)).fetchall()
    results = [dict(row) for row in rows]

    conn.close()

    return results




def get_regimen_cost_components(regimen_id, hospital_id, payer_name, plan_name):
    treatments = get_regimen_treatments(regimen_id)

    results = []

    for treatment in treatments:
        treatment_id = treatment["treatment_id"]

        prices = get_treatment_cost_components(
            treatment_id,
            hospital_id,
            payer_name,
            plan_name
        )

        summary = summarize_treatment_prices(prices)

        conn = sqlite3.connect(DB)

        mapping_count = conn.execute("""
            SELECT COUNT(*)
            FROM treatment_billing_code
            WHERE treatment_id = ?
        """, (treatment_id,)).fetchone()[0]

        conn.close()

        if mapping_count == 0:
            status = "missing_mapping"
        elif not prices:
            status = "missing_prices"
        else:
            status = "partial_pricing"

        results.append({
            "phase_no": treatment["phase_no"],
            "treatment_id": treatment_id,
            "treatment_name": treatment["treatment_name"],
            "num_cycles": treatment["num_cycles"],
            "visits_per_cycle": treatment["visits_per_cycle"],
            "total_visits": treatment["num_cycles"] * treatment["visits_per_cycle"],
            "status": status,
            "pricing_summary": summary
        })

    return results
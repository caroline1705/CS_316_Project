import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "household" / "curebase.db"


def get_treatment_prices(hospital_id, code, code_type=None,
                         payer_name=None, plan_name=None):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    sql = """
        SELECT
            p.record_id,
            p.hospital_id,
            p.description,
            c.code,
            c.code_type,
            p.billing_class,
            p.setting,
            p.modifiers,
            p.payer_name,
            p.plan_name,
            p.gross_charge,
            p.discounted_cash,
            p.negotiated_dollar,
            p.negotiated_percentage,
            p.negotiated_algorithm,
            p.pricing_methodology,
            p.additional_notes
        FROM hospital_price p
        JOIN hospital_price_code c
            ON p.price_id = c.price_id
        WHERE p.hospital_id = ?
          AND c.code = ?
    """

    parameters = [hospital_id, code]

    if code_type:
        sql += " AND c.code_type = ?"
        parameters.append(code_type)

    if payer_name:
        sql += " AND p.payer_name = ?"
        parameters.append(payer_name)

    if plan_name:
        sql += " AND p.plan_name = ?"
        parameters.append(plan_name)

    sql += " ORDER BY p.payer_name, p.plan_name, p.record_id"

    try:
        rows = conn.execute(sql, parameters).fetchall()
        results = [dict(row) for row in rows]
    finally:
        conn.close()

    return results
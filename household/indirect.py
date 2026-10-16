"""Indirect cost prototype (SQLite). Run AFTER regimen.py:  python3 indirect.py"""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "curebase.db"

LODGING_THRESHOLD_MILES = 100   # assume an overnight stay when one-way trip >= 100 miles


def init_db():
    conn = sqlite3.connect(DB)
    conn.executescript((HERE / "schema_indirect.sql").read_text())
    conn.executescript((HERE / "seed_indirect.sql").read_text())
    conn.commit()
    return conn


def indirect_costs(conn, regimen_id, distance_miles, county, has_children,
                   state="NC", as_of="2026-10-16", fiscal_year=2027,
                   childcare_hours_per_visit=6):
    sql = (HERE / "indirect_query.sql").read_text()
    row = conn.execute(sql, {
        "regimen_id": regimen_id, "distance_miles": distance_miles,
        "state": state, "county": county, "as_of": as_of,
        "fiscal_year": fiscal_year, "lodging_threshold": LODGING_THRESHOLD_MILES,
        "has_children": int(has_children),
        "childcare_hours_per_visit": childcare_hours_per_visit,
    }).fetchone()
    keys = ["total_visits", "travel", "lodging", "childcare",
            "cents_per_mile", "lodging_rate", "meals_rate", "childcare_hourly"]
    r = dict(zip(keys, row))
    r["total"] = round(r["travel"] + r["lodging"] + r["childcare"], 2)
    return r


def show(label, r):
    print(f"\n{label}")
    print(f"  visits={r['total_visits']}  (IRS {r['cents_per_mile']}c/mi, "
          f"lodging ${r['lodging_rate']}+meals ${r['meals_rate']}/night)")
    print(f"  travel    ${r['travel']:>10,.2f}")
    print(f"  lodging   ${r['lodging']:>10,.2f}")
    print(f"  childcare ${r['childcare']:>10,.2f}")
    print(f"  TOTAL     ${r['total']:>10,.2f}")


if __name__ == "__main__":
    conn = init_db()
    # Patient 1: lives 30 miles from Duke (Durham County), no kids, colorectal FOLFOX
    show("FOLFOX, 30 mi to Durham, no children",
         indirect_costs(conn, "CRC_FOLFOX", 30, "Durham", has_children=False))
    # Patient 2: lives 150 miles away (rural NC), has kids, breast AC-T
    show("Breast AC-T+H, 150 mi to Durham, with children",
         indirect_costs(conn, "BREAST_ACT_H", 150, "Durham", has_children=True))
    # Patient 3: county not in GSA list -> falls back to NC standard rate
    show("R-CHOP, 120 mi to Pitt County (standard rate), no children",
         indirect_costs(conn, "DLBCL_RCHOP", 120, "Pitt", has_children=False))

"""Indirect cost prototype (SQLite). Run AFTER init_db.py:  python3 indirect.py"""
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "curebase.db"

LODGING_THRESHOLD_MILES = 100   # assume an overnight stay when one-way trip >= 100 miles
AGE_GROUPS = ("INFANT", "TODDLER", "PRESCHOOL", "SCHOOL_AGE")


def indirect_costs(conn, regimen_id, distance_miles, county, num_children=0,
                   home_county=None, age_group="PRESCHOOL", state="NC",
                   as_of="2026-10-16", fiscal_year=2027):
    sql = (HERE / "indirect_query.sql").read_text()
    row = conn.execute(sql, {
        "regimen_id": regimen_id, "distance_miles": distance_miles,
        "state": state, "county": county, "home_county": home_county,
        "num_children": num_children, "age_group": age_group,
        "as_of": as_of, "fiscal_year": fiscal_year,
        "lodging_threshold": LODGING_THRESHOLD_MILES,
    }).fetchone()
    keys = ["total_visits", "travel", "lodging", "childcare",
            "cents_per_mile", "lodging_rate", "meals_rate", "childcare_weekly"]
    r = dict(zip(keys, row))
    r["total"] = round(r["travel"] + r["lodging"] + r["childcare"], 2)
    return r


def show(label, r):
    print(f"\n{label}")
    print(f"  visits={r['total_visits']}  (IRS {r['cents_per_mile']}c/mi, lodging "
          f"${r['lodging_rate']}+meals ${r['meals_rate']}/night, childcare ${r['childcare_weekly']}/week)")
    print(f"  travel    ${r['travel']:>10,.2f}")
    print(f"  lodging   ${r['lodging']:>10,.2f}")
    print(f"  childcare ${r['childcare']:>10,.2f}")
    print(f"  TOTAL     ${r['total']:>10,.2f}")


if __name__ == "__main__":
    conn = sqlite3.connect(DB)
    show("FOLFOX, 30 mi to Durham, no children",
         indirect_costs(conn, "CRC_FOLFOX", 30, "Durham"))
    show("Breast AC-T+H, 150 mi to Durham, 1 preschooler at home in Durham County",
         indirect_costs(conn, "BREAST_ACT_H", 150, "Durham", num_children=1,
                        home_county="Durham", age_group="PRESCHOOL"))
    show("R-CHOP, 120 mi to Pitt (standard lodging), 2 infants, home county unknown",
         indirect_costs(conn, "DLBCL_RCHOP", 120, "Pitt", num_children=2,
                        home_county=None, age_group="INFANT"))

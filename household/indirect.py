"""Indirect cost prototype (SQLite). Run AFTER init_db.py:  python3 indirect.py"""
import sqlite3
from datetime import date
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "curebase.db"

LODGING_THRESHOLD_MILES = 100   # assume an overnight stay when one-way trip >= 100 miles
AGE_GROUPS = ("INFANT", "TODDLER", "PRESCHOOL", "SCHOOL_AGE")


def children_counts(children_by_age=None, num_children=0, age_group="PRESCHOOL"):
    """Return {age_group: count} for all four age groups.

    Pass children_by_age (e.g. {"INFANT": 1, "SCHOOL_AGE": 2}) for children of
    different ages, or the older num_children + age_group pair (all one age).
    """
    counts = {g: 0 for g in AGE_GROUPS}
    if children_by_age:
        for group, n in children_by_age.items():
            if group not in counts:
                raise ValueError(f"unknown age group '{group}'")
            counts[group] += int(n)
    elif num_children:
        counts[age_group] += int(num_children)
    return counts


def childcare_rates(conn, home_county=None, state="NC"):
    """Weekly price and fallback flag for each age group in the home county."""
    sql = (HERE / "childcare_rates_query.sql").read_text()
    return {g: (price, bool(median)) for g, price, median in
            conn.execute(sql, {"state": state, "home_county": home_county})}


def indirect_costs(conn, regimen_id, distance_miles, county, num_children=0,
                   home_county=None, age_group="PRESCHOOL", state="NC",
                   as_of=None, fiscal_year=None, children_by_age=None):
    counts = children_counts(children_by_age, num_children, age_group)
    # Default to today's IRS rate and the latest GSA fiscal year we have loaded
    # (the federal fiscal year starts Oct 1, so Oct 2026 is FY2027).
    today = date.today()
    as_of = as_of or today.isoformat()
    if fiscal_year is None:
        wanted = today.year + 1 if today.month >= 10 else today.year
        fiscal_year = conn.execute(
            "SELECT MAX(fiscal_year) FROM lodging_rate WHERE state = ? AND fiscal_year <= ?",
            (state, wanted)).fetchone()[0]
    sql = (HERE / "indirect_query.sql").read_text()
    row = conn.execute(sql, {
        "regimen_id": regimen_id, "distance_miles": distance_miles,
        "state": state, "county": county, "home_county": home_county,
        "n_infant": counts["INFANT"], "n_toddler": counts["TODDLER"],
        "n_preschool": counts["PRESCHOOL"], "n_school_age": counts["SCHOOL_AGE"],
        "age_group": age_group,
        "as_of": as_of, "fiscal_year": fiscal_year,
        "lodging_threshold": LODGING_THRESHOLD_MILES,
    }).fetchone()
    keys = ["total_visits", "travel", "lodging", "childcare",
            "cents_per_mile", "lodging_rate", "meals_rate", "childcare_weekly",
            "lodging_is_standard", "childcare_is_median", "children"]
    r = dict(zip(keys, row))
    r["lodging_is_standard"] = bool(r["lodging_is_standard"])
    r["childcare_is_median"] = bool(r["childcare_is_median"])
    # Childcare cost for each age group, so the page can show the breakdown
    rates = childcare_rates(conn, home_county, state)
    r["childcare_by_age"] = [
        {"age_group": g, "children": n, "weekly_price": rates[g][0],
         "is_median": rates[g][1],
         "cost": round(r["total_visits"] * n * rates[g][0] / 5.0, 2)}
        for g, n in counts.items() if n > 0]
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
    show("FOLFOX, 40 mi to Orange, 1 infant + 2 school-age children in Orange County",
         indirect_costs(conn, "CRC_FOLFOX", 40, "Orange", home_county="Orange",
                        children_by_age={"INFANT": 1, "SCHOOL_AGE": 2}))

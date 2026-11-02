import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parent / "household" / "curebase.db"  ##tested on test version but never initialized curebase yet
QUERY_FILE = HERE / "assistance_query.sql"


def _connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def find_assistance_by_cancer(cancer_type):
    query = QUERY_FILE.read_text(encoding="utf-8")
    with _connect() as conn:
        rows = conn.execute(query, (cancer_type,)).fetchall()
        programs = [dict(row) for row in rows]
        ids = sorted({p["program_id"] for p in programs})
        if not ids:
            return []
        placeholders = ", ".join("?" for _ in ids)
        geography_rows = conn.execute(
            "SELECT program_id, rule_group, location_type, country, state, county "
            "FROM assistance_program_geography "
            f"WHERE program_id IN ({placeholders}) "
            "ORDER BY program_id, rule_group, geography_id",
            ids,
        ).fetchall()

    rules_by_id = {program_id: [] for program_id in ids}
    for row in geography_rows:
        rule = dict(row)
        rules_by_id[rule["program_id"]].append(rule)
    for program in programs:
        program["geography_rules"] = rules_by_id[program["program_id"]]
    return programs


def _insurance_types(program):
    value = program.get("accepted_insurance_types")
    return {part.strip().lower() for part in (value or "").split(",") if part.strip()}


def matches_insurance(program, patient_insurance):
    accepted = _insurance_types(program)
    if patient_insurance == "Uninsured":
        additional = (
            program.get("additional_insurance_requirements") or ""
        ).lower()

        if "insurance must cover" in additional:
            return False
    if not accepted:
        return True  # No insurance restriction recorded
    if patient_insurance is None or str(patient_insurance).strip().lower() == "unknown":
        return True  # Potential match; information is incomplete

    patient = str(patient_insurance).strip().lower()
    if patient in accepted:
        return True
    if patient != "uninsured" and "any_insured" in accepted:
        return True
    if patient in {"medicare", "medicaid", "tricare", "veterans"} and (
        "government insurance (unspecified)" in accepted
    ):
        return True
    return False

def matches_income(program, patient_fpl):
    limit = program["income_limit_fpl"]
    return limit is None or patient_fpl is None or patient_fpl <= limit


def matches_age(program, patient_age):
    min_age = program["min_age"]
    max_age = program["max_age"]
    if patient_age is None:
        return True
    return ((min_age is None or patient_age >= min_age)
            and (max_age is None or patient_age <= max_age))


def matches_cancer_subtype(program, patient_subtype):
    required = program["cancer_subtype"]
    if not required or not patient_subtype or str(patient_subtype).lower() == "unknown":
        return True
    return required.strip().casefold() == patient_subtype.strip().casefold()


def _country(value):
    if value is None:
        return None
    aliases = {
        "united states": "US", "usa": "US", "u.s.": "US",
        "canada": "CA", "territory": "TERRITORY", "us territory": "TERRITORY", "u.s. territory": "TERRITORY",
    }
    normalized = str(value).strip()
    return aliases.get(normalized.casefold(), normalized.upper())


def _region(value):
    if value is None or str(value).strip().casefold() == "unknown":
        return None
    return str(value).strip().upper()


def _county(value):
    if value is None or str(value).strip().casefold() == "unknown":
        return None
    name = str(value).strip().casefold()
    return name.removesuffix(" county").strip()


def _location_match(rule, patient_country, patient_state, patient_county,
                    treatment_country, treatment_state, treatment_county):
    if rule["location_type"] == "residence":
        country, state, county = patient_country, patient_state, patient_county
    elif rule["location_type"] == "treatment":
        country, state, county = treatment_country, treatment_state, treatment_county
    else:
        raise ValueError(f"Unknown location_type: {rule['location_type']}")

    country = _country(country)
    required_country = _country(rule["country"])
    if country is None or country == "UNKNOWN":
        return "needs_review"
    if country != required_country:
        return "no_match"

    required_state = _region(rule["state"])
    if required_state is not None:
        state = _region(state)
        if state is None:
            return "needs_review"
        if state != required_state:
            return "no_match"

    required_county = _county(rule["county"])
    if required_county is not None:
        county = _county(county)
        if county is None:
            return "needs_review"
        if county != required_county:
            return "no_match"
    return "match"

def matches_residency(program, patient_country, patient_state=None,
                      patient_county=None, citizenship_status=None,
                      treatment_country=None, treatment_state=None,
                      treatment_county=None):
    """OR rules within each group, AND across groups; missing data needs review."""
    rules = program.get("geography_rules", [])
    if not rules:
        return "match"

    groups = {}
    for rule in rules:
        groups.setdefault(rule["rule_group"], []).append(rule)

    has_unknown = False
    for group_rules in groups.values():
        outcomes = [
            _location_match(rule, patient_country, patient_state, patient_county,
                            treatment_country, treatment_state, treatment_county)
            for rule in group_rules
        ]
        if "match" in outcomes:
            continue
        if "needs_review" in outcomes:
            has_unknown = True
        else:
            return "no_match"
    return "needs_review" if has_unknown else "match"


def find_matching_assistance(cancer_type, cancer_subtype=None, insurance=None,
                             fpl_percent=None, age=None, country=None,
                             state=None, county=None, citizenship_status=None,
                             treatment_country="US", treatment_state="NC",
                             treatment_county=None):
    programs = find_assistance_by_cancer(cancer_type)
    results = []
    seen = set()

    for program in programs:
        if not matches_cancer_subtype(program, cancer_subtype):
            continue
        if insurance is not None and not matches_insurance(program, insurance):
            continue
        if not matches_income(program, fpl_percent):
            continue
        if not matches_age(program, age):
            continue

        residency_status = matches_residency(
            program, patient_country=country, patient_state=state,
            patient_county=county, citizenship_status=citizenship_status,
            treatment_country=treatment_country, treatment_state=treatment_state,
            treatment_county=treatment_county,
        )
        if residency_status == "no_match":
            continue
        if program["program_id"] in seen:
            continue
        seen.add(program["program_id"])
        program["residency_status"] = residency_status
        program["eligibility_status"] = "potential_match"
        program["manual_review_required"] = bool(
            residency_status == "needs_review"
            or program.get("additional_insurance_requirements")
            or program.get("other_eligibility_requirements")
            or program.get("other_income_requirements")
            or program.get("notes")
            or insurance is None
            or fpl_percent is None
            or age is None
            or not cancer_subtype
        )
        results.append(program)
    return results

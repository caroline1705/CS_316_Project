
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE.parent / "household" / "curebase_test.db"
QUERY_FILE = HERE / "assistance_query.sql"


def find_assistance_by_cancer(cancer_type):
    query = QUERY_FILE.read_text(encoding="utf-8")
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    try:
        rows = conn.execute(query, (cancer_type,)).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def matches_insurance(program, patient_insurance):
    coverage = program["insurance_coverage"]
    accepted = program["accepted_insurance_types"]

    is_insured = patient_insurance != "Uninsured"

    if coverage == "Insured" and not is_insured:
        return False

    if not accepted:
        return True

    if not is_insured:
        return False

    accepted_types = [
        item.strip() for item in accepted.split(",")
    ]

    if patient_insurance in accepted_types:
        return True

    if "Government insurance (unspecified)" in accepted_types:
        return patient_insurance in ("Medicare", "Medicaid")

    return False

def matches_income(program, patient_fpl):
    income_limit = program["income_limit_fpl"]

    if income_limit is None:
        return True

    if patient_fpl is None:
        return True

    return patient_fpl <= income_limit

def matches_age(program, patient_age):
    min_age = program["min_age"]
    max_age = program["max_age"]

    if min_age is None and max_age is None:
        return True

    if patient_age is None:
        return True

    if min_age is not None and patient_age < min_age:
        return False

    if max_age is not None and patient_age > max_age:
        return False

    return True

def matches_cancer_subtype(program, patient_subtype):
    required_subtype = program["cancer_subtype"]

    if not required_subtype:
        return True

    if not patient_subtype or patient_subtype == "Unknown":
        return True

    return (
        required_subtype.strip().lower()
        == patient_subtype.strip().lower()
    )


def matches_residency(
    program,
    patient_country,
    patient_state=None,
    patient_county=None,
    citizenship_status=None,
    treatment_country=None,
    treatment_state=None,
    treatment_county=None
):
    requirement = program["residency_requirements"]

    if not requirement:
        return "match"

    # Return needs_review when information is insufficient.
    # This is an internal matching result, not a patient-facing
    # eligibility classification.

    def check_country(allowed):
        if not patient_country:
            return "needs_review"
        return (
            "match"
            if patient_country in allowed
            else "no_match"
        )

    def check_treatment_country(allowed):
        if not treatment_country or treatment_country == "Unknown":
            return "needs_review"
        return (
            "match"
            if treatment_country in allowed
            else "no_match"
        )

    # P003: United States or U.S. territory
    if requirement == "United States or U.S. Territory":
        return check_country(("US", "Territory"))

    # P018: North Carolina or South Carolina resident
    if requirement == "North Carolina or South Carolina resident":
        if patient_country and patient_country != "US":
            return "no_match"

        if not patient_state:
            return "needs_review"

        return (
            "match"
            if patient_state in ("NC", "SC")
            else "no_match"
        )

    # P019: North Carolina resident
    if requirement == "North Carolina resident":
        if patient_country and patient_country != "US":
            return "no_match"

        if not patient_state:
            return "needs_review"

        return "match" if patient_state == "NC" else "no_match"

    # P020/P021: Must reside in the United States
    if requirement == "Must reside in the United States":
        return check_country(("US",))

    # P027: United States or Canada
    if requirement == "Must live in the United States or Canada":
        return check_country(("US", "CA"))

    # P008: Must live OR receive treatment in one of
    # four North Carolina counties.
    if requirement == (
        "Must live or receive treatment in Wayne, Sampson, "
        "Onslow, or Lenoir County, North Carolina"
    ):
        allowed_counties = {
            "wayne", "sampson", "onslow", "lenoir"
        }

        def normalize_county(value):
            if not value:
                return None
            return value.strip().lower().replace(" county", "")

        home_county = normalize_county(patient_county)
        care_county = normalize_county(treatment_county)

        home_match = (
            patient_country == "US"
            and patient_state == "NC"
            and home_county in allowed_counties
        )

        treatment_match = (
            treatment_country == "US"
            and treatment_state == "NC"
            and care_county in allowed_counties
        )

        if home_match or treatment_match:
            return "match"

        # The intake form uses "Other" for counties outside
        # the four named counties.
        home_known = (
            patient_country is not None
            and (
                patient_country != "US"
                or (
                    patient_state is not None
                    and (
                        patient_state != "NC"
                        or home_county not in (None, "unknown")
                    )
                )
            )
        )

        treatment_known = (
            treatment_country not in (None, "Unknown")
            and (
                treatment_country != "US"
                or (
                    treatment_state is not None
                    and (
                        treatment_state != "NC"
                        or care_county not in (None, "unknown")
                    )
                )
            )
        )

        if home_known and treatment_known:
            return "no_match"

        return "needs_review"

    # P009-P017: Citizenship or permanent residency,
    # plus residence in the United States or a territory.
    if requirement == (
        "U.S. citizen or permanent resident residing "
        "in the U.S. or a U.S. territory"
    ):
        if patient_country and patient_country not in ("US", "Territory"):
            return "no_match"

        if citizenship_status == "No":
            return "no_match"

        if (
            patient_country in ("US", "Territory")
            and citizenship_status == "Yes"
        ):
            return "match"

        return "needs_review"

    # P004/P005: Legal U.S. residence and treatment
    # in the United States or a territory.
    if requirement == (
        "Legal resident of the U.S. or U.S. territory; "
        "must receive treatment there"
    ):
        if patient_country and patient_country not in ("US", "Territory"):
            return "no_match"

        if treatment_country not in (None, "Unknown", "US", "Territory"):
            return "no_match"

        if (
            patient_country in ("US", "Territory")
            and treatment_country in ("US", "Territory")
        ):
            # The form does not establish every category
            # of legal U.S. residency.
            return "needs_review"

        return "needs_review"

    # P026: Legal residency and treatment in the U.S.
    # or a U.S. territory.
    if requirement == (
        "Legal resident of the United States or a U.S. territory; "
        "must receive treatment in the U.S. or a U.S. territory"
    ):
        if patient_country and patient_country not in ("US", "Territory"):
            return "no_match"

        if treatment_country not in (None, "Unknown", "US", "Territory"):
            return "no_match"

        return "needs_review"

    # P006/P007: U.S. resident receiving U.S. treatment.
    if requirement == "U.S. resident receiving treatment in the U.S.":
        if patient_country and patient_country != "US":
            return "no_match"

        if treatment_country not in (None, "Unknown", "US"):
            return "no_match"

        if patient_country == "US" and treatment_country == "US":
            return "match"

        return "needs_review"

    # P023/P028/P029/P030: Treatment in the United States.
    if requirement == "Must receive treatment in the United States":
        return check_treatment_country(("US",))

    # P022/P024/P025: Valid SSN and U.S. treatment.
    # Do not collect an actual Social Security number.
    if requirement == (
        "Must have a valid Social Security number and receive "
        "treatment in the United States; citizenship or legal "
        "permanent residency not explicitly required"
    ):
        treatment_result = check_treatment_country(("US",))

        if treatment_result == "no_match":
            return "no_match"

        # The form does not ask whether the patient has
        # a valid SSN, so this requirement remains unverified.
        return "needs_review"

    # Unknown or differently worded requirements
    # should not automatically exclude a patient.
    return "needs_review"


def find_matching_assistance(
    cancer_type,
    cancer_subtype=None,
    insurance=None,
    fpl_percent=None,
    age=None,
    country=None,
    state=None,
    county=None,
    citizenship_status=None,
    treatment_country=None,
    treatment_state=None,
    treatment_county=None
):
    programs = find_assistance_by_cancer(cancer_type)
    results = []

    for program in programs:
        if not matches_cancer_subtype(program, cancer_subtype):
            continue

        if insurance is not None:
            if not matches_insurance(program, insurance):
                continue

        if not matches_income(program, fpl_percent):
            continue

        if not matches_age(program, age):
            continue

        residency_status = matches_residency(
            program,
            patient_country=country,
            patient_state=state,
            patient_county=county,
            citizenship_status=citizenship_status,
            treatment_country=treatment_country,
            treatment_state=treatment_state,
            treatment_county=treatment_county
        )

        if residency_status == "no_match":
            continue

        program["residency_status"] = residency_status
        program["eligibility_status"] = "potential_match"

        results.append(program)

    return results

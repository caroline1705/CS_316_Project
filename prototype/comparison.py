"""Server-side comparison using the existing household and assistance services."""
import math
from decimal import Decimal, ROUND_HALF_UP

from household.fpl import fpl_percent
from household.indirect import indirect_costs
from household.regimen import regimen_summary
from assistance import assistance as aid_backend

DEMO_DATE = '2026-11-04'
HOSPITAL_IDS = ['DUKE', 'UNC', 'WFB', 'LEVINE', 'ECU']
PROFILES = {hid: {'minAge': 21 if hid == 'WFB' else 18} for hid in HOSPITAL_IDS}
CANCER_NAMES = {'BREAST': 'Breast', 'LUNG': 'Lung', 'COLORECTAL': 'Colorectal',
                'PROSTATE': 'Prostate', 'LYMPHOMA': 'Lymphoma'}


def money(value):
    return float(Decimal(str(value)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))


def rows(conn, sql, params=()):
    cursor = conn.execute(sql, params)
    names = [column[0] for column in cursor.description]
    return [dict(zip(names, row)) for row in cursor.fetchall()]


def validate(conn, profile):
    if not isinstance(profile, dict):
        return ['Submit a household profile as a JSON object.']
    errors = []
    limits = [('age', 0, 120), ('size', 1, 20), ('children', 0, 10),
              ('income', 0, 1e9), ('otherIncome', 0, 1e9), ('expenses', 0, 1e7),
              ('deductible', 0, 1e7), ('cap', 0, 1e7), ('coinsurance', 0, 100),
              ('missedHours', 0, 24), ('hourly', 0, 10000)]
    def number(value):
        return type(value) in (int, float) and math.isfinite(value)
    for key, low, high in limits:
        if key == 'hourly' and profile.get('missedHours') == 0:
            continue
        if profile.get('insurance') == 'Uninsured' and key in ('deductible', 'cap', 'coinsurance'):
            continue
        value = profile.get(key)
        if not number(value) or not low <= value <= high:
            errors.append(f'{key} must be a number between {low:g} and {high:g}.')
    for key in ('age', 'size', 'children'):
        value = profile.get(key)
        if not number(value) or int(value) != value:
            errors.append(f'{key} must be a whole number.')
    for key in ('cancer', 'regimen', 'state', 'county', 'address', 'addressId', 'insurance'):
        if not isinstance(profile.get(key), str) or not profile[key].strip():
            errors.append(f'{key} is required.')
    for key in ('subtype', 'ageGroup'):
        if key in profile and not isinstance(profile[key], str):
            errors.append(f'{key} must be text.')
    distances = profile.get('distances')
    if (not isinstance(distances, list) or len(distances) != len(HOSPITAL_IDS)
            or any(not number(n) or not 0 <= n <= 2000 for n in distances)):
        errors.append('Enter a one-way distance from 0 to 2,000 miles for every hospital.')
    if errors:
        return errors
    if profile['children'] >= profile['size']:
        errors.append('Children needing care must be fewer than household members (including the patient).')
    if profile['state'] != 'NC':
        errors.append('This prototype supports North Carolina residents only.')
    if profile['insurance'] not in ('Private', 'Medicare', 'Medicaid', 'Uninsured'):
        errors.append('Select a supported insurance category.')
    if profile['children'] > 0 and profile.get('ageGroup') not in ('INFANT', 'TODDLER', 'PRESCHOOL', 'SCHOOL_AGE'):
        errors.append('Select a childcare age group.')
    if not conn.execute('SELECT 1 FROM regimen WHERE regimen_id=? AND cancer_id=?',
                        (profile['regimen'], profile['cancer'])).fetchone():
        errors.append('Select a regimen for this diagnosis.')
    if not conn.execute("SELECT 1 FROM county WHERE state='NC' AND county=?", (profile['county'],)).fetchone():
        errors.append('Select an NC home county.')
    if profile['insurance'] != 'Uninsured' and profile['deductible'] > profile['cap']:
        errors.append('Remaining deductible cannot exceed remaining out-of-pocket maximum.')
    return errors


def medical(price, profile):
    if profile['insurance'] == 'Uninsured':
        return dict(deductible=0, coinsurance=0, total=price,
                    assumption='Uninsured: full fictional baseline; no self-pay discount modeled.')
    deductible = min(price, profile['deductible'])
    coinsurance = max(0, price - deductible) * profile['coinsurance'] / 100
    return dict(deductible=deductible, coinsurance=coinsurance,
                total=money(min(profile['cap'], deductible + coinsurance)),
                assumption='All treatment assumed covered and in network. One remaining deductible and OOP cap across the entire course; no plan-year reset, premiums, copays, or uncovered services.')


def assistance_screening(conn, profile, hospital, fpl):
    arguments = dict(cancer_type=CANCER_NAMES[profile['cancer']],
                     cancer_subtype=profile.get('subtype'), insurance=profile['insurance'],
                     fpl_percent=fpl, age=profile['age'], country='US', state=profile['state'],
                     county=profile['county'], treatment_country='US', treatment_state='NC',
                     treatment_county=hospital['county'])
    matches = {p['program_id']: p for p in aid_backend.find_matching_assistance(**arguments)}
    cancer_rows = rows(conn, 'SELECT * FROM assistance_program_cancer')
    insurance_rows = rows(conn, 'SELECT * FROM assistance_program_insurance')
    geography_rows = rows(conn, 'SELECT * FROM assistance_program_geography')
    results = []
    for program in rows(conn, 'SELECT * FROM assistance_program ORDER BY program_id'):
        pid = program['program_id']
        accepted = [r['insurance_type'] for r in insurance_rows if r['program_id'] == pid]
        program['accepted_insurance_types'] = ', '.join(accepted)
        program['geography_rules'] = [r for r in geography_rows if r['program_id'] == pid]
        cancers = [r for r in cancer_rows if r['program_id'] == pid
                   and r['cancer_type'] in (arguments['cancer_type'], 'Any')]
        reasons, review = [], []
        if not cancers:
            reasons.append('Diagnosis mismatch')
        elif not any(aid_backend.matches_cancer_subtype(r, profile.get('subtype')) for r in cancers):
            reasons.append('Subtype mismatch')
        elif not profile.get('subtype') and all(r['cancer_subtype'] for r in cancers):
            review.append('Subtype required')
        if not aid_backend.matches_income(program, fpl):
            reasons.append(f"Income exceeds {program['income_limit_fpl']:g}% FPL")
        if not aid_backend.matches_age(program, profile['age']):
            reasons.append('Age outside limits')
        if not aid_backend.matches_insurance(program, profile['insurance']):
            reasons.append('Insurance mismatch or insurance coverage required')
        residency = aid_backend.matches_residency(
            program, 'US', profile['state'], profile['county'],
            treatment_country='US', treatment_state='NC', treatment_county=hospital['county'])
        if residency == 'no_match':
            reasons.append('Residence or treatment geography mismatch')
        elif residency == 'needs_review':
            review.append('Residence or treatment geography needs review')
        for key in ('other_eligibility_requirements', 'other_income_requirements',
                    'additional_insurance_requirements', 'notes'):
            if program.get(key):
                review.append(program[key])
        if pid in matches:
            reasons = []
        elif not reasons:
            reasons.append('Does not meet the assistance backend screening rules')
        results.append({**program, 'accepted_insurance': accepted, 'reasons': reasons,
                        'review': review, 'status': 'Excluded' if reasons else 'Potential match — review required'})
    return results


def compare(conn, profile, prices, address_ids):
    errors = validate(conn, profile)
    if errors:
        return {'errors': errors}
    if profile.get('addressId') not in address_ids:
        return {'errors': ['Select a predefined test address.']}
    p = dict(profile)
    if p['children'] == 0 and p.get('ageGroup') not in ('INFANT', 'TODDLER', 'PRESCHOOL', 'SCHOOL_AGE'):
        p['ageGroup'] = 'PRESCHOOL'
    if p['missedHours'] == 0:
        p['hourly'] = 0
    if p['insurance'] == 'Uninsured':
        p.update(deductible=0, coinsurance=100, cap=0)
    annual = p['income'] + p['otherIncome']
    household = fpl_percent(conn, annual, p['size'], p['state'])
    # Keep full precision for screening; the existing FPL endpoint rounds its display to one decimal.
    f = dict(annual=annual, guideline=household['guideline'],
             fpl=100 * annual / household['guideline'], monthly=annual / 12,
             available=max(0, annual / 12 - p['expenses']))
    regimen = regimen_summary(conn, regimen_id=p['regimen'])[0]
    summary = dict(regimen_id=regimen[0], visits=regimen[3], weeks=regimen[4])
    results = []
    for h in rows(conn, 'SELECT * FROM hospital ORDER BY hospital_id'):
        price = next((r for r in prices if r['hospital_id'] == h['hospital_id']
                      and r['treatment_id'] == p['regimen'] and r['cancer_id'] == p['cancer']), None)
        if price is None:
            return {'errors': [f"Missing test price for {h['name']} / {p['regimen']}."]}
        distance = p['distances'][HOSPITAL_IDS.index(h['hospital_id'])]
        indirect = indirect_costs(conn, p['regimen'], distance, h['county'],
                                  num_children=p['children'], home_county=p['county'],
                                  age_group=p.get('ageGroup') or 'PRESCHOOL',
                                  as_of=DEMO_DATE, fiscal_year=2027)
        baseline = money((price['standard_charge_min'] + price['standard_charge_max']) / 2)
        med = medical(baseline, p)
        med_min = medical(price['standard_charge_min'], p)['total']
        med_max = medical(price['standard_charge_max'], p)['total']
        nights = summary['visits'] if distance >= 100 else 0
        costs = dict(medical=med['total'], travel=indirect['travel'],
                     lodging=nights * indirect['lodging_rate'], meals=nights * indirect['meals_rate'],
                     childcare=indirect['childcare'],
                     lostWages=money(summary['visits'] * p['missedHours'] * p['hourly']))
        total = money(sum(costs.values()))
        months = summary['weeks'] * 12 / 52
        course_income, budget = annual * summary['weeks'] / 52, f['available'] * months
        minimum_age = PROFILES[h['hospital_id']]['minAge']
        eligible = p['age'] >= minimum_age
        reason = (f'Passes fictional age rule ({minimum_age}+); diagnosis offering assumed for demo. Clinical suitability and network status need confirmation.'
                  if eligible else f'Fails fictional adult program age rule ({minimum_age}+).')
        care_year = conn.execute("SELECT MAX(study_year) FROM childcare_price WHERE state='NC' AND provider='CENTER' AND age_group=?",
                                 (p.get('ageGroup') or 'PRESCHOOL',)).fetchone()[0]
        results.append({**h, 'eligible': eligible, 'eligibilityReason': reason,
                        'distance': distance, 'price': price, 'baseline': baseline, 'med': med,
                        'medicalMin': med_min, 'medicalMax': med_max, 'costs': costs, 'total': total,
                        'totalMin': money(total - med['total'] + med_min),
                        'totalMax': money(total - med['total'] + med_max),
                        'months': months, 'summary': summary, 'nights': nights,
                        'lodging': dict(county='STANDARD' if indirect['lodging_is_standard'] else h['county'],
                                        lodging=indirect['lodging_rate'], meals=indirect['meals_rate']),
                        'care': dict(county='STANDARD' if indirect['childcare_is_median'] else p['county'],
                                     weekly_price=indirect['childcare_weekly'], study_year=care_year),
                        'mileage': dict(cents_per_mile=indirect['cents_per_mile']),
                        'courseIncome': course_income, 'budget': budget,
                        'gap': money(max(0, total - budget)),
                        'burden': total / course_income * 100 if course_income > 0 else None,
                        'monthly': total / months, 'assistance': assistance_screening(conn, p, h, f['fpl'])})
    results.sort(key=lambda r: (not r['eligible'], r['gap'], r['total'], r['distance'], r['hospital_id']))
    return dict(errors=[], profile=p, finances=f, results=results)

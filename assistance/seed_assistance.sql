
INSERT INTO assistance_program (
    program_id,
    program_name,
    organization,
    residency_requirements,
    additional_insurance_requirements,
    income_limit_fpl,
    other_income_requirements,
    assistance_type,
    assistance_amount,
    other_eligibility_requirements,
    application_url,
    source_url,
    notes,
    insurance_coverage,
    min_age,
    max_age
)
VALUES
(
    'P001',
    'Pink Fund Financial Assistance',
    'Pink Fund',
    NULL,
    NULL,
    300,
    'Applicant or spouse/partner must have been working at diagnosis and demonstrate loss of working income due to breast cancer. Household income assessed using previous year''s federal tax return.',
    'Direct bill payments: mortgage, rent, home/renter''s insurance, car loans, car insurance, phone, utilities, health insurance premiums',
    'Up to $6,000 ($1,000/month for 6 months)',
    'Breast cancer diagnosis within 2 years of application receipt; active treatment throughout funding; reconstruction-only and long-term hormonal therapy-only patients excluded; documentation of diagnosis and employment/income loss required.',
    'https://apply.pinkfund.org/qualification/intro',
    'https://pinkfund.org/',
    'Not emergency assistance; processing may take up to 90 days. Bills must be paid in full; no partial payments or bills in collections. Application and supporting documents must be mailed.',
    NULL,
    NULL,
    NULL
);

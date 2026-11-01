INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P001', 'Pink Fund Financial Assistance', 'Pink Fund', NULL, NULL, 300, 'Applicant or spouse/partner must have been working at diagnosis and demonstrate loss of working income due to breast cancer. Household income assessed using previous year''s federal tax return.', 'Direct bill payments: mortgage, rent, home/renter''s insurance, car loans, car insurance, phone, utilities, health insurance premiums', 'Up to $6,000 ($1,000/month for 6 months)', 'Breast cancer diagnosis within 2 years of application receipt; active treatment throughout funding; reconstruction-only and long-term hormonal therapy-only patients excluded; documentation of diagnosis and employment/income loss required.', 'https://apply.pinkfund.org/qualification/intro', 'https://pinkfund.org/', 'Not emergency assistance; processing may take up to 90 days. Bills must be paid in full; no partial payments or bills in collections. Application and supporting documents must be mailed.', NULL, NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P002', 'Mary Herczog Fund for Metastatic Breast Cancer', 'Pink Fund', NULL, NULL, 300, 'Pink Fund''s employment/income-loss requirements apply. Intended for metastatic breast cancer patients who have applied for Social Security Disability and are awaiting payments.', 'Direct bill payments for eligible household expenses', 'Up to $6,000 ($1,000/month for 6 months)', 'Metastatic breast cancer; Social Security Disability application pending payment; active treatment throughout funding; diagnosis and income documentation; Social Security Benefit Verification Letter required.', 'https://apply.pinkfund.org/qualification/intro', 'https://pinkfund.org/', 'Specialized Pink Fund assistance. Application checklist requests Social Security Benefit Verification Letter. Confirm exact disability-payment criteria with Pink Fund. Processing may take up to 90 days.', NULL, NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P003', 'Komen Financial Assistance Program', 'Susan G. Komen', 'United States or U.S. Territory', NULL, 300, NULL, 'Rent, utilities, food, transportation, childcare, medical needs', '$400 one-time grant', 'Active treatment for stage 0–3 breast cancer diagnosed within the past 24 months, OR living with stage 4 metastatic breast cancer; must not have previously received a Komen financial assistance award', 'https://www.komen.org/financial-assistance-program/', 'https://www.komen.org/', 'Online applications only; providers may apply on behalf of patients. Medical documentation signed within 12 months required. Payments made directly to applicant. Processing may take up to 8 weeks. No gender or citizenship requirements.', NULL, NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P004', 'Colorectal Cancer Fund', 'Patient Advocate Foundation', 'Legal resident of the U.S. or U.S. territory; must receive treatment there', 'Government insurance must cover qualifying expenses.', 500, 'Income threshold adjusted for regional Cost of Living Index (COLI)', 'Medication copays, coinsurance, deductibles, health insurance premiums, other qualifying healthcare expenses', '$2,500 guaranteed award; $5,000 maximum award', 'Confirmed colorectal cancer diagnosis; currently in treatment, starting within 60 days, treated within past 6 months, or active surveillance; approved medication required for medication expenses', 'https://totalassist.org/funds/colorectal-cancer/', 'https://www.patientadvocate.org/', 'Government insurance required; eligible medications include bevacizumab, capecitabine, fluorouracil, and others. Cannot receive multiple TotalAssist grants for the same condition. Online or phone applications when open; instant approval decisions advertised.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P005', 'Prostate Cancer Fund', 'Patient Advocate Foundation', 'Legal resident of the U.S. or U.S. territory; must receive treatment there', 'Government insurance must cover qualifying expenses.', 500, 'Income threshold adjusted for regional Cost of Living Index (COLI)', 'Medication copays, coinsurance, deductibles, health insurance premiums, other qualifying healthcare expenses', '$2,000 guaranteed award; $4,000 maximum award', 'Confirmed prostate cancer diagnosis; currently in treatment, starting treatment within 60 days, treated within past 6 months, or active surveillance; approved medication required for medication expenses', 'https://totalassist.org/funds/prostate-cancer/', 'https://www.patientadvocate.org/', 'Cannot receive multiple TotalAssist grants for the same condition. Approved medications include abiraterone, bicalutamide, docetaxel, and others. Apply online or by phone when open; instant approval decisions advertised.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P006', 'Non-Small Cell Lung Cancer - Privately Insured', 'Accessia Health', 'U.S. resident receiving treatment in the U.S.', NULL, 500, NULL, 'Copays, medical expenses, travel expenses (up to $500); insurance premiums for privately insured patients', 'Up to $4,000 total across all assistance types', 'Confirmed diagnosis of non-small cell lung cancer', 'https://accessiahealth.org/program/non-small-cell-lung-cancer/', 'https://accessiahealth.org/', 'Uninsured patients qualify for the privately insured program category but are not listed as eligible for premium assistance. Travel assistance is capped at $500 within the overall $4,000 limit. Covered medications are listed on the fund page.', 'Both', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P007', 'Non-Small Cell Lung Cancer - Publicly Insured', 'Accessia Health', 'U.S. resident receiving treatment in the U.S.', NULL, 500, NULL, 'Copays, medical expenses, insurance premiums, travel expenses', 'Up to $4,000 total across all assistance types', 'Confirmed diagnosis of non-small cell lung cancer', 'https://accessiahealth.org/program/non-small-cell-lung-cancer/', 'https://accessiahealth.org/', 'Travel assistance is capped at $500 within the overall $4,000 limit. Covered medications are listed on the fund page.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P009', 'Hodgkin Lymphoma Co-Pay Assistance Program', 'Blood Cancer United', 'U.S. citizen or permanent resident residing in the U.S. or a U.S. territory', NULL, 600, 'Household income adjusted by Cost of Living Index (COLI), determined using ZIP code', 'Copays, deductibles, coinsurance, insurance premiums, Medicaid spend-down, and eligible blood cancer treatment expenses', 'Up to $8,500', 'Physician-confirmed Hodgkin lymphoma diagnosis; active treatment, scheduled treatment, pre- or post-treatment surveillance, or palliative care including hospice; medical insurance required', 'https://bloodcancerunited.org/financial-assistance/co-pay-assistance-program', 'https://bloodcancerunited.org/', 'Hodgkin lymphoma; income eligibility is ≤600% FPL adjusted for COLI using ZIP code. Covers eligible treatment-related services, drugs, and insurance costs. Excludes hospital stays, travel, fertility procedures, OTC medications, and other listed expenses. Military and diplomatic personnel serving overseas may qualify with a U.S. address and additional provider requirements. Funding currently being solicited; enrollment availability not confirmed.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P010', 'Non-Hodgkin Lymphoma Co-Pay Assistance Program', 'Blood Cancer United', 'U.S. citizen or permanent resident residing in the U.S. or a U.S. territory', NULL, 600, 'Household income adjusted by Cost of Living Index (COLI), determined using ZIP code', 'Copays, deductibles, coinsurance, insurance premiums, Medicaid spend-down, and eligible blood cancer treatment expenses', 'Up to $8,500', 'Confirmed non-Hodgkin lymphoma diagnosis; other requirements not yet confirmed', 'https://bloodcancerunited.org/financial-assistance/co-pay-assistance-program', 'https://bloodcancerunited.org/', 'Currently soliciting funding. Only Medicaid and Medicare confirmed as supported insurance types from supplied information. Other eligibility criteria should be verified before automated matching.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P011', 'Insurance Premiums Co-Pay Assistance Program', 'Blood Cancer United', 'U.S. citizen or permanent resident residing in the U.S. or a U.S. territory', NULL, 600, 'Household income adjusted by Cost of Living Index (COLI) using ZIP code', 'Insurance premium assistance', 'Up to $2,400', 'Physician-confirmed blood cancer diagnosis; active treatment, scheduled treatment, pre- or post-treatment surveillance, or palliative care including hospice; medical insurance required', 'https://bloodcancerunited.org/financial-assistance/co-pay-assistance-program', 'https://bloodcancerunited.org/', 'Covers all blood cancers, including lymphoma. Private insurance only. Income threshold is ≤600% FPL adjusted for COLI. Currently soliciting funding; do not treat as open for enrollment.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P012', 'Urgent Need Program — Pediatric, Adolescent and Young Adult Fund', 'Blood Cancer United', 'U.S. citizen or permanent resident residing in the U.S. or a U.S. territory', NULL, 600, 'Household income adjusted by Cost of Living Index (COLI) using ZIP code; demonstrated acute financial need', 'Non-medical living expenses: rent, mortgage, lodging, utilities, childcare, elder care, food, transportation, car repair, car insurance, phone service, and treatment-related acute dental work', '$500 once per 12-month period', 'Ages 0–39; physician-confirmed blood cancer diagnosis; active treatment, scheduled treatment, pre- or post-treatment surveillance, or palliative care including hospice; healthcare team member must apply on patient''s behalf', 'https://bloodcancerunited.org/financial-assistance/urgent-need-program', 'https://bloodcancerunited.org/', 'All blood cancers; healthcare team member must have access to medical records and a valid NPI. Patients cannot apply directly. Healthcare professionals may reapply after 12 months. COLI-adjusted income threshold.', 'Both', 0, 39);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P013', 'Urgent Need Program — Adult Fund', 'Blood Cancer United', 'U.S. citizen or permanent resident residing in the U.S. or a U.S. territory', NULL, 600, 'Household income adjusted by Cost of Living Index (COLI) using ZIP code; demonstrated acute financial need', 'Non-medical living expenses: rent, mortgage, lodging, utilities, childcare, elder care, food, transportation, car repair, car insurance, phone service, and treatment-related acute dental work', '$500 once per 12-month period', 'Ages 40+; physician-confirmed blood cancer diagnosis; active treatment, scheduled treatment, pre- or post-treatment surveillance, or palliative care including hospice; healthcare team member must apply on patient''s behalf', 'https://bloodcancerunited.org/financial-assistance/urgent-need-program', 'https://bloodcancerunited.org/', 'All blood cancers; healthcare team member must have access to medical records and a valid NPI. Patients cannot apply directly. Healthcare professionals may reapply after 12 months. COLI-adjusted income threshold.', 'Both', 40, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P014', 'Susan Lang Pay-It-Forward National Travel Fund', 'Blood Cancer United', 'U.S. citizen or permanent resident residing in the U.S. or a U.S. territory', NULL, 600, 'COLI-adjusted household income using ZIP code; significant financial need', 'Treatment-related travel and lodging for patient and caregiver', '$500 once per 6-month period', 'Physician-confirmed blood cancer diagnosis; active treatment, scheduled treatment, pre- or post-treatment surveillance, or palliative care including hospice; cannot receive assistance from more than one travel fund within 6 months', 'https://bloodcancerunited.org/financial-assistance/susan-lang-pay-it-forward-patient-travel-assistance-program', 'https://bloodcancerunited.org/', 'All blood cancers; covers transportation, gas, tolls, parking, car rental/repairs, airfare, baggage fees, lodging, and ambulance services. Excludes food, beverages, medical expenses, and international travel.', 'Both', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P015', 'Susan Lang Pay-It-Forward Pediatric Travel Fund', 'Blood Cancer United', 'U.S. citizen or permanent resident residing in the U.S. or a U.S. territory', NULL, 600, 'COLI-adjusted household income using ZIP code; significant financial need', 'Treatment-related travel and lodging for patient and caregiver', '$500 once per 6-month period', 'Ages 0–19; physician-confirmed blood cancer diagnosis; active treatment, scheduled treatment, pre- or post-treatment surveillance, or palliative care including hospice; cannot receive assistance from more than one travel fund within 6 months', 'https://bloodcancerunited.org/financial-assistance/susan-lang-pay-it-forward-patient-travel-assistance-program', 'https://bloodcancerunited.org/', 'Covers transportation, gas, tolls, parking, car rental/repairs, airfare, baggage fees, lodging, and ambulance services. Excludes food, beverages, medical expenses, and international travel.', 'Both', 0, 19);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P016', 'Susan Lang Pay-It-Forward Clinical Trial Travel Fund', 'Blood Cancer United', 'U.S. citizen or permanent resident residing in the U.S. or a U.S. territory', NULL, 600, 'COLI-adjusted household income using ZIP code; significant financial need', 'Treatment-related travel and lodging for patient and caregiver', '$500 once per 6-month period', 'Being evaluated for or participating in a clinical trial; physician-confirmed blood cancer diagnosis; active treatment, scheduled treatment, pre- or post-treatment surveillance, or palliative care including hospice; cannot receive assistance from more than one travel fund within 6 months', 'https://bloodcancerunited.org/financial-assistance/susan-lang-pay-it-forward-patient-travel-assistance-program', 'https://bloodcancerunited.org/', 'Covers transportation, gas, tolls, parking, car rental/repairs, airfare, baggage fees, lodging, and ambulance services. Excludes food, beverages, medical expenses, and international travel.', 'Both', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P017', 'Patient Aid Program', 'Blood Cancer United', 'U.S. citizen or permanent resident residing in the U.S. or a U.S. territory', NULL, NULL, NULL, 'Non-medical expenses including transportation, food, housing, and utilities', '$100 one-time stipend', 'Physician-confirmed blood cancer diagnosis; active treatment, scheduled treatment, pre- or post-treatment surveillance, or palliative care including hospice; must not have previously received a Patient Aid Program award', 'https://bloodcancerunited.org/financial-assistance/patient-aid-program', 'https://bloodcancerunited.org/', 'No income limit; insured and uninsured patients eligible. One-time award only. Applications available by phone, online portal, or paper application. Military/diplomatic personnel serving overseas may have additional provider verification requirements.', 'Both', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P018', 'Tomma Hargraves Gas Card Program', 'Lung Cancer Initiative', 'North Carolina or South Carolina resident', NULL, NULL, NULL, 'Gas cards for transportation to lung cancer treatment, including clinical trials', '$50 gas card every four months', 'Must be currently undergoing lung cancer treatment; application must be completed and signed by applicant and healthcare facility; new application required every four months', 'https://lungcancerinitiative.org/patient-programs/', 'https://lungcancerinitiative.org/', 'No insurance or income requirements specified in provided program description. Nurse navigator or cancer center representative may submit online application. Contact mheym@lungcancerinitiative.org or 919-784-0410 for assistance.', NULL, NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P019', 'Patient Emergency Fund', 'Lung Cancer Initiative', 'North Carolina resident', NULL, NULL, NULL, 'Non-medical emergency expenses, including healthy food, transportation, and other expenses associated with a lung cancer diagnosis', '$100 one-time stipend (maximum once per calendar year)', 'Must currently be undergoing treatment for lung cancer; one stipend per calendar year; application completed through or with a healthcare facility or nurse navigator', 'https://lungcancerinitiative.org/patient-programs/', 'https://lungcancerinitiative.org/', 'North Carolina residents only. Stipends are available until funding is depleted. Award amount not specified in published information provided. Applications closed for 2026. Contact mheym@lungcancerinitiative.org or 919-784-0410 for assistance.', NULL, NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P020', 'MLC Cancer Foundation Financial Assistance', 'MLC Cancer Foundation', 'Must reside in the United States', NULL, NULL, 'Financial assistance based on demonstrated need and available foundation resources', 'Medical bills, copays, medications, treatment expenses, wigs, prosthetics, recovery supplies, housing, transportation, groceries, and childcare', NULL, 'Any cancer diagnosis or stage; newly diagnosed, currently undergoing treatment, or within six months after treatment; application requires diagnosis, treatment status, and expenses needing assistance; provider letter may be requested; amount varies based on financial need and expenses', 'https://www.mlccancerfoundation.org/get-help', 'https://www.mlccancerfoundation.org/', 'Nationwide program. No specific FPL threshold published. Awards depend on individual circumstances and available resources. Approved assistance is paid directly to patients. Repeat applications permitted, with each reviewed separately.', 'Both', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P021', 'SAMFund Financial Assistance Grant', 'Expect Miracles Foundation', 'Must reside in the United States', NULL, NULL, 'Financial well-being negatively impacted by cancer; applicants with immediate essential financial needs and limited alternative support are prioritized', 'Rent/mortgage, car payments, graduate or continuing education, fertility storage fees, and cancer-related reconstructive, dental, or cosmetic procedures', NULL, 'Ages 21–39; not a tax dependent in most recent filing; no grant in previous cycle; fewer than two prior SAMFund grants; must have complete response/remission/NED, or partial response/stable disease with at least one year since active treatment; not currently receiving chemotherapy or radiation', 'https://expectmiraclesfoundation.org/financial-assistance-grant/', 'https://expectmiraclesfoundation.org/', 'Survivorship-focused grant. Long-term hormonal, targeted, or immunotherapy may be allowed if remission criteria are met. Prioritizes detailed applications demonstrating financial hardship. Does not cover medical bills, undergraduate tuition, utilities, credit card payments, loans, car purchases/repairs, or family-building expenses. U.S. citizenship or permanent residency not explicitly required in provided criteria.', NULL, 21, 39);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P022', 'Prostate Cancer Co-Payment Assistance Fund', 'CancerCare Co-Payment Assistance Foundation', 'Must have a valid Social Security number and receive treatment in the United States; citizenship or legal permanent residency not explicitly required', NULL, 500, 'Co-payment assistance for prescribed prostate cancer treatments', 'Co-payment assistance for prescribed prostate cancer treatments', '$4,250 initial grant; $10,000 maximum program cap', 'Primary prostate cancer diagnosis verified by prescribing physician; must be receiving active treatment or have a treatment plan in place before applying', 'https://www.cancercare.org/services/financial_assistance/copayfoundation/prostate-cancer', 'https://www.cancercare.org/', 'First-time applicants may qualify for retroactive reimbursement for covered treatment dates within 60 days before approval; conditional approvals are excluded. Additional funds up to the $10,000 cap may be requested if the initial grant is exhausted before the grant end date.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P023', 'Prostate Cancer — Medicare Access', 'HealthWell Foundation', 'Must receive treatment in the United States', NULL, 500, 'Income limit adjusted for household size and high-cost-of-living areas', 'Prescription drug copays or Medicare Part B insurance premiums', 'Up to $6,000', 'Must be receiving treatment for prostate cancer; assistance limited to covered prescription drugs and biologics', 'https://www.healthwellfoundation.org/fund/prostate-cancer-medicare-access/', 'https://www.healthwellfoundation.org/', 'Medicare patients only. Assistance provided through pharmacy card. No minimum copay or premium reimbursement amount. Fund covers listed prostate cancer medications and biologics. Estimated average grant utilization is $3,200, distinct from the $6,000 maximum award. Fund alerts available for reopening notifications.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P024', 'Metastatic Colorectal Cancer Co-Payment Assistance Fund', 'CancerCare Co-Payment Assistance Foundation', 'Must have a valid Social Security number and receive treatment in the United States; citizenship or legal permanent residency not explicitly required', NULL, 500, NULL, 'Co-payment assistance for prescribed metastatic colorectal cancer treatments', '$5,000 initial grant; $10,000 maximum program cap', 'Primary metastatic colorectal cancer diagnosis verified by prescribing physician; must be receiving active treatment or have a treatment plan in place before applying', 'https://www.cancercare.org/services/financial_assistance/copayfoundation/metastatic-colorectal-cancer', 'https://www.cancercare.org/', 'First-time applicants may qualify for retroactive reimbursement for covered treatment dates within 60 days before approval; conditional approvals excluded. Additional funds up to $10,000 cap may be requested if initial grant is exhausted before grant end date.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P025', 'Colorectal Carcinoma — Medicare Access', 'HealthWell Foundation', 'Must have a valid Social Security number and receive treatment in the United States; citizenship or legal permanent residency not explicitly required', NULL, 500, 'Income limit adjusted for household size and high-cost-of-living areas', 'Prescription drug copays or Medicare Part B insurance premiums', 'Up to $8,000', 'Must be receiving treatment for colorectal carcinoma; assistance limited to covered prescription drugs and biologics', 'https://www.healthwellfoundation.org/fund/colorectal-carcinoma-medicare-access/', 'https://www.healthwellfoundation.org/', 'Medicare patients only. Assistance provided through pharmacy card. No minimum copay or premium reimbursement amount. Covers specified colorectal cancer medications and biologics. Estimated average grant utilization is $2,100, distinct from the $8,000 maximum award. Fund alerts available for reopening notifications.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P026', 'Metastatic Colorectal Cancer Fund', 'Patient Advocate Foundation', 'Legal resident of the United States or a U.S. territory; must receive treatment in the U.S. or a U.S. territory', 'Government insurance must cover qualifying expenses.', 500, 'Income threshold adjusted for regional Cost of Living Index (COLI)', 'Medication copays, coinsurance, deductibles, health insurance premiums, and other qualifying out-of-pocket healthcare expenses', '$3,000 guaranteed award; $6,000 maximum award', 'Confirmed metastatic colorectal cancer diagnosis; currently receiving treatment, planning to begin treatment within 60 days, received treatment within the past 6 months, or undergoing active surveillance. If seeking medication assistance, prescribed medication must meet the fund''s approved medication criteria.', 'https://totalassist.org/funds/metastatic-colorectal-cancer/', 'https://totalassist.org/', 'Stage IV colorectal cancer only. Cannot receive more than one TotalAssist grant for the same condition. Medication coverage includes qualifying FDA-approved, compendia-listed, or evidence-based guideline-supported medications. Online or phone applications (866-512-3861) when fund is open.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P027', 'Breast Cancer Journey Assistance Fund', 'The Aesthetic Foundation', 'Must live in the United States or Canada', NULL, NULL, NULL, 'Non-surgical breast cancer care expenses, including deductibles, copays, medications, medical equipment, respite care, caregiver and loved-one support, wigs, and transportation', '$250–$500 per award; maximum once every 12 months', 'Confirmed breast cancer diagnosis; application must be submitted by a board-certified plastic surgeon, other physician, nurse navigator, or social worker; patient participation agreement and medical release required', 'https://www.theaestheticfoundation.org/apply-for-funding/patient-assistance-funds/breast-cancer-journey-assistance-fund', 'https://www.theaestheticfoundation.org/', 'No specific cancer stage, insurance requirement, income threshold, or citizenship requirement stated in provided criteria. Patients cannot apply directly; eligible healthcare professionals must apply on their behalf. Award decisions are subject to task force review. Approved funds may be provided once every 12 months based on the last payment date. Payee information must be submitted within six months of approval or a new application is required.', NULL, NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P028', 'Breast Cancer — Medicare Access', 'HealthWell Foundation', 'Must receive treatment in the United States', NULL, 500, 'Income limit adjusted for household size and high-cost-of-living areas', 'Prescription drug copays or Medicare Part B insurance premiums', 'Up to $7,500', 'Must be receiving treatment for breast cancer; assistance limited to covered prescription drugs and biologics', 'https://www.healthwellfoundation.org/fund/breast-cancer-medicare-access/', 'https://www.healthwellfoundation.org/', 'Fund currently closed. Medicare patients only. Assistance provided through pharmacy card. No minimum copay or premium reimbursement amount. Covers specified breast cancer medications and biologics. Forecasted average grant utilization is $2,200, distinct from the $7,500 maximum award. Fund alerts available for reopening notifications.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P029', 'Non-Small Cell Lung Cancer Fund', 'HealthWell Foundation', 'Must receive treatment in the United States', 'Insurance must cover the prescribed medication.', 400, 'Income threshold adjusted for household size and high-cost-of-living areas', 'Prescription drug copays or Medicare Part B insurance premiums', 'Up to $6,000', 'Must be receiving treatment for non-small cell lung cancer; must have insurance covering the prescribed medication; assistance limited to covered prescription drugs and biologics', 'https://www.healthwellfoundation.org/fund/non-small-cell-lung-cancer/', 'https://www.healthwellfoundation.org/', 'Accepting phone applications only; online applications not available. Non-pharmacy card payment type. No minimum copay or premium reimbursement amount. Estimated average grant utilization is $2,500 over a 12-month grant period, distinct from the $6,000 maximum award. Medicare Part B premium assistance available. Covered medications include Tagrisso, Keytruda, Opdivo, and other listed treatments.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P030', 'Small Cell Lung Cancer — Medicare Access', 'HealthWell Foundation', 'Must receive treatment in the United States', NULL, 500, 'Income threshold adjusted for household size and high-cost-of-living areas', 'Prescription drug copays or Medicare Part B insurance premiums', 'Up to $8,000', 'Must be receiving treatment for small-cell lung cancer; assistance limited to covered prescription drugs and biologics', 'https://www.healthwellfoundation.org/fund/small-cell-lung-cancer-medicare-access/', 'https://www.healthwellfoundation.org/', 'Fund currently closed. Medicare patients only. Assistance provided through pharmacy card. No minimum copay or premium reimbursement amount. Forecasted average grant utilization is $3,300, distinct from the $8,000 maximum award. Fund alerts available for reopening notifications. Covered medications include carboplatin, cisplatin, etoposide, Imfinzi, Tecentriq, and Zepzelca.', 'Insured', NULL, NULL);

INSERT INTO assistance_program (program_id, program_name, organization, residency_requirements, additional_insurance_requirements, income_limit_fpl, other_income_requirements, assistance_type, assistance_amount, other_eligibility_requirements, application_url, source_url, notes, insurance_coverage, min_age, max_age)
VALUES ('P008', 'Southeastern Cancer Care Grant Program', 'Southeastern Cancer Care', 'Must live or receive treatment in Wayne, Sampson, Onslow, or Lenoir County, North Carolina', NULL, NULL, NULL, 'Gas, groceries, car insurance, oncology-prescribed medications, rent/mortgage, electricity, water/sewer, and natural gas/propane bills', '$250, $500, or $1,000 depending on income level; grant lasts up to 6 months or until funds are exhausted', 'Must be actively receiving chemotherapy or radiation, or be within 3 months of oncology-related surgery. Must live or receive treatment in Wayne, Sampson, Onslow, or Lenoir County, NC. Must meet income requirements based on Federal Poverty Guidelines (specific threshold not published). Applicants with a felony or misdemeanor charge, excluding minor traffic violations, within the past 10 years are ineligible. Assistance may be terminated if a participant fails a drug test while enrolled.', 'https://313924f5-8257-4b1f-8319-30f0a27ea4ce.filesusr.com/ugd/152a32_8cf5ed4b191541dcb72530ef3bffb4e3.pdf', 'https://www.southeasterncancercare.org/', 'Grants require reapplication every 6 months. No additional funding is available during the current grant term once funds are exhausted. Bills must be submitted at least 10 business days before the due date and must be payable to a verifiable business or housing authority. Gas/grocery assistance limited to two gift cards per week. Gift card mailing is subject to treatment location and distance restrictions. No insurance requirement specified.', NULL, NULL, NULL);

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P001', 'Breast', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P002', 'Breast', 'Metastatic breast cancer');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P003', 'Breast', 'Metastatic breast cancer');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P004', 'Colorectal', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P005', 'Prostate', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P006', 'Lung', 'Non-small cell lung cancer');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P007', 'Lung', 'Non-small cell lung cancer');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P009', 'Lymphoma', 'Hodgkin lymphoma');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P010', 'Lymphoma', 'Non-Hodgkin lymphoma');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P011', 'Lymphoma', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P012', 'Lymphoma', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P013', 'Lymphoma', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P014', 'Lymphoma', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P015', 'Lymphoma', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P016', 'Lymphoma', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P017', 'Lymphoma', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P018', 'Lung', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P019', 'Lung', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P020', 'Any', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P021', 'Any', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P022', 'Prostate', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P023', 'Prostate', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P024', 'Colorectal', 'Metastatic colorectal cancer');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P025', 'Colorectal', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P026', 'Colorectal', 'Metastatic colorectal cancer');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P027', 'Breast', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P028', 'Breast', '');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P029', 'Lung', 'Non-small cell lung cancer');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P030', 'Lung', 'Small cell lung cancer');

INSERT INTO assistance_program_cancer (program_id, cancer_type, cancer_subtype)
VALUES ('P008', 'Any', '');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P004', 'Government insurance (unspecified)');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P005', 'Government insurance (unspecified)');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P006', 'Private');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P007', 'Medicare');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P007', 'Medicaid');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P007', 'TRICARE');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P007', 'Veterans');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P009', 'Medicare');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P009', 'Medicaid');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P009', 'Private');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P010', 'Medicare');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P010', 'Medicaid');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P010', 'Private');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P011', 'Private');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P022', 'Medicare');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P022', 'Medicaid');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P023', 'Medicare');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P024', 'Medicare');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P024', 'Medicaid');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P025', 'Medicare');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P026', 'Government insurance (unspecified)');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P028', 'Medicare');

INSERT INTO assistance_program_insurance (program_id, insurance_type)
VALUES ('P030', 'Medicare');

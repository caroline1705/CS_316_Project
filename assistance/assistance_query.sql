SELECT DISTINCT
    p.program_id,
    p.program_name,
    p.organization,
    p.residency_requirements,
    p.additional_insurance_requirements,
    p.other_eligibility_requirements,
    c.cancer_type,
    c.cancer_subtype,
    p.assistance_type,
    p.assistance_amount,
    p.application_url,
    p.income_limit_fpl,
    p.other_income_requirements,
    p.min_age,
    p.max_age,
    p.insurance_coverage,
    GROUP_CONCAT(i.insurance_type, ', ') AS accepted_insurance_types
FROM assistance_program AS p
JOIN assistance_program_cancer AS c
    ON p.program_id = c.program_id
LEFT JOIN assistance_program_insurance AS i
    ON p.program_id = i.program_id
WHERE c.cancer_type = ?
   OR c.cancer_type = 'Any'
GROUP BY p.program_id
ORDER BY p.program_name;

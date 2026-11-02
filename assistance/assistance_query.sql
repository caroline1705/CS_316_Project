SELECT
    p.program_id,
    p.program_name,
    p.organization,
    p.additional_insurance_requirements,
    p.other_eligibility_requirements,
    p.assistance_type,
    p.assistance_amount,
    p.application_url,
    p.source_url,
    p.notes,
    p.income_limit_fpl,
    p.other_income_requirements,
    p.min_age,
    p.max_age,
    c.cancer_type,
    c.cancer_subtype,
    (SELECT GROUP_CONCAT(i.insurance_type, ', ')
       FROM assistance_program_insurance AS i
      WHERE i.program_id = p.program_id) AS accepted_insurance_types
FROM assistance_program AS p
JOIN assistance_program_cancer AS c ON c.program_id = p.program_id
WHERE c.cancer_type = ? OR c.cancer_type = 'Any'
ORDER BY p.program_name, c.cancer_type, c.cancer_subtype;


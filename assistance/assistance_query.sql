SELECT DISTINCT
    p.program_id,
    p.program_name,
    p.organization,
    p.assistance_type,
    p.assistance_amount,
    p.application_url
FROM assistance_program AS p
JOIN assistance_program_cancer AS c
    ON p.program_id = c.program_id
WHERE c.cancer_type = ?
   OR c.cancer_type = 'Any'
ORDER BY p.program_name;
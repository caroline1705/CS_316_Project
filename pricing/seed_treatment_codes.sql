INSERT or IGNORE INTO treatment_billing_code (
    treatment_id,
    code,
    code_type,
    component_name,
    units_per_cycle
)
VALUES (
    'PACLITAXEL',
    '96413',
    'CPT',
    'Initial IV chemotherapy administration',
    NULL
),
(
    'PACLITAXEL',
    'J9267',
    'HCPCS',
    'Paclitaxel injection, 1 mg',
    NULL
),
(
    'AC',
    'J9000',
    'HCPCS',
    'Doxorubicin injection',
    NULL
),
(   'AC', 
    'J9075', 
    'HCPCS', 
    'Cyclophosphamide injection', 
    NULL),
(
    'TRASTUZUMAB',
    'J9355',
    'HCPCS',
    'Trastuzumab injection',
    NULL
);
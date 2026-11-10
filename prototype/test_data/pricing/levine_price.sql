-- FICTIONAL test prices in USD per complete treatment course, not actual hospital charges.
-- treatment_id identifies a regimen package (regimen.regimen_id), not a phase/drug.
-- cancer_id UNIQUE deliberately permits one package per cancer at each hospital.
CREATE TABLE levine_price (
    hospital_id TEXT NOT NULL,
    treatment_type TEXT NOT NULL,
    treatment_id TEXT NOT NULL,
    standard_charge_min REAL NOT NULL CHECK (standard_charge_min >= 0),
    standard_charge_max REAL NOT NULL CHECK (standard_charge_max >= standard_charge_min),
    cancer_id TEXT NOT NULL UNIQUE,
    CONSTRAINT fk_cancer FOREIGN KEY (cancer_id)
        REFERENCES cancer_type(cancer_id) ON DELETE CASCADE,
    PRIMARY KEY (hospital_id, treatment_id)
);

INSERT INTO levine_price
    (hospital_id, treatment_type, treatment_id, standard_charge_min, standard_charge_max, cancer_id)
VALUES
    ('LEVINE', 'REGIMEN', 'BREAST_ACT_H', 125280.00, 187920.00, 'BREAST'),
    ('LEVINE', 'REGIMEN', 'LUNG_CRT_DURVA', 181440.00, 272160.00, 'LUNG'),
    ('LEVINE', 'REGIMEN', 'CRC_FOLFOX', 70848.00, 106272.00, 'COLORECTAL'),
    ('LEVINE', 'REGIMEN', 'PROSTATE_RT_ADT', 41472.00, 62208.00, 'PROSTATE'),
    ('LEVINE', 'REGIMEN', 'DLBCL_RCHOP', 82944.00, 124416.00, 'LYMPHOMA');

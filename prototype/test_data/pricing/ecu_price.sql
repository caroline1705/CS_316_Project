-- FICTIONAL test prices in USD per complete treatment course, not actual hospital charges.
-- treatment_id identifies a regimen package (regimen.regimen_id), not a phase/drug.
-- cancer_id UNIQUE deliberately permits one package per cancer at each hospital.
CREATE TABLE ecu_price (
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

INSERT INTO ecu_price
    (hospital_id, treatment_type, treatment_id, standard_charge_min, standard_charge_max, cancer_id)
VALUES
    ('ECU', 'REGIMEN', 'BREAST_ACT_H', 104400.00, 156600.00, 'BREAST'),
    ('ECU', 'REGIMEN', 'LUNG_CRT_DURVA', 151200.00, 226800.00, 'LUNG'),
    ('ECU', 'REGIMEN', 'CRC_FOLFOX', 59040.00, 88560.00, 'COLORECTAL'),
    ('ECU', 'REGIMEN', 'PROSTATE_RT_ADT', 34560.00, 51840.00, 'PROSTATE'),
    ('ECU', 'REGIMEN', 'DLBCL_RCHOP', 69120.00, 103680.00, 'LYMPHOMA');

-- FICTIONAL test prices in USD per complete treatment course, not actual hospital charges.
-- treatment_id identifies a regimen package (regimen.regimen_id), not a phase/drug.
-- cancer_id UNIQUE deliberately permits one package per cancer at each hospital.
CREATE TABLE unc_price (
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

INSERT INTO unc_price
    (hospital_id, treatment_type, treatment_id, standard_charge_min, standard_charge_max, cancer_id)
VALUES
    ('UNC', 'REGIMEN', 'BREAST_ACT_H', 119480.00, 179220.00, 'BREAST'),
    ('UNC', 'REGIMEN', 'LUNG_CRT_DURVA', 173040.00, 259560.00, 'LUNG'),
    ('UNC', 'REGIMEN', 'CRC_FOLFOX', 67568.00, 101352.00, 'COLORECTAL'),
    ('UNC', 'REGIMEN', 'PROSTATE_RT_ADT', 39552.00, 59328.00, 'PROSTATE'),
    ('UNC', 'REGIMEN', 'DLBCL_RCHOP', 79104.00, 118656.00, 'LYMPHOMA');

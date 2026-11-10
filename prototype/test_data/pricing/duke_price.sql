-- FICTIONAL test prices in USD per complete treatment course, not actual hospital charges.
-- treatment_id identifies a regimen package (regimen.regimen_id), not a phase/drug.
-- cancer_id UNIQUE deliberately permits one package per cancer at each hospital.
CREATE TABLE duke_price (
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

INSERT INTO duke_price
    (hospital_id, treatment_type, treatment_id, standard_charge_min, standard_charge_max, cancer_id)
VALUES
    ('DUKE', 'REGIMEN', 'BREAST_ACT_H', 129920.00, 194880.00, 'BREAST'),
    ('DUKE', 'REGIMEN', 'LUNG_CRT_DURVA', 188160.00, 282240.00, 'LUNG'),
    ('DUKE', 'REGIMEN', 'CRC_FOLFOX', 73472.00, 110208.00, 'COLORECTAL'),
    ('DUKE', 'REGIMEN', 'PROSTATE_RT_ADT', 43008.00, 64512.00, 'PROSTATE'),
    ('DUKE', 'REGIMEN', 'DLBCL_RCHOP', 86016.00, 129024.00, 'LYMPHOMA');

-- FICTIONAL test prices in USD per complete treatment course, not actual hospital charges.
-- treatment_id identifies a regimen package (regimen.regimen_id), not a phase/drug.
-- cancer_id UNIQUE deliberately permits one package per cancer at each hospital.
CREATE TABLE wfb_price (
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

INSERT INTO wfb_price
    (hospital_id, treatment_type, treatment_id, standard_charge_min, standard_charge_max, cancer_id)
VALUES
    ('WFB', 'REGIMEN', 'BREAST_ACT_H', 111360.00, 167040.00, 'BREAST'),
    ('WFB', 'REGIMEN', 'LUNG_CRT_DURVA', 161280.00, 241920.00, 'LUNG'),
    ('WFB', 'REGIMEN', 'CRC_FOLFOX', 62976.00, 94464.00, 'COLORECTAL'),
    ('WFB', 'REGIMEN', 'PROSTATE_RT_ADT', 36864.00, 55296.00, 'PROSTATE'),
    ('WFB', 'REGIMEN', 'DLBCL_RCHOP', 73728.00, 110592.00, 'LYMPHOMA');

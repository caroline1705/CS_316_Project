CREATE TABLE IF NOT EXISTS treatment_billing_code (
    treatment_id VARCHAR(32) NOT NULL,
    code VARCHAR(32) NOT NULL,
    code_type VARCHAR(32) NOT NULL,
    component_name TEXT,
    units_per_cycle REAL,
    PRIMARY KEY (treatment_id, code, code_type),
    FOREIGN KEY (treatment_id) REFERENCES treatment(treatment_id)
);

CREATE TABLE IF NOT EXISTS hospital_price (
    price_id INTEGER PRIMARY KEY,
    hospital_id VARCHAR(16) NOT NULL,
    record_id TEXT NOT NULL,
    description TEXT,
    billing_class TEXT,
    setting TEXT,
    payer_name TEXT,
    plan_name TEXT,
    gross_charge REAL,
    discounted_cash REAL,
    negotiated_dollar REAL,
    negotiated_percentage REAL,
    negotiated_algorithm TEXT,
    pricing_methodology TEXT,
    additional_notes TEXT,
    source_file TEXT,
    source_row INTEGER,
    drug_unit_of_measurement TEXT,
    drug_type_of_measurement TEXT,
    modifiers TEXT,
    count_raw TEXT,
    median_amount REAL,
    percentile_10 REAL,
    percentile_90 REAL
    minimum_charge REAL,
    maximum_charge REAL,
    UNIQUE (hospital_id, record_id),
    FOREIGN KEY (hospital_id) REFERENCES hospital(hospital_id)
);

CREATE TABLE IF NOT EXISTS hospital_price_code (
    price_id INTEGER NOT NULL,
    code VARCHAR(32) NOT NULL,
    code_type VARCHAR(32) NOT NULL,
    code_position INTEGER NOT NULL,
    PRIMARY KEY (price_id, code, code_type, code_position),
    FOREIGN KEY (price_id) REFERENCES hospital_price(price_id)
);

CREATE INDEX IF NOT EXISTS idx_price_code
ON hospital_price_code(code_type, code);

CREATE INDEX IF NOT EXISTS idx_price_hospital
ON hospital_price(hospital_id);
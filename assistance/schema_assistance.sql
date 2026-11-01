-- Eligibility table: This will be the main table and store all the financial assistance programs and their general eligibility reqs
CREATE TABLE IF NOT EXISTS assistance_program (
    program_id TEXT PRIMARY KEY,
    program_name TEXT NOT NULL,
    organization TEXT,
    residency_requirements TEXT,
    additional_insurance_requirements TEXT,
    income_limit_fpl REAL,
    other_income_requirements TEXT,
    assistance_type TEXT,
    assistance_amount TEXT,
    other_eligibility_requirements TEXT,
    application_url TEXT,
    source_url TEXT,
    notes TEXT,
    insurance_coverage TEXT,
    min_age INTEGER,
    max_age INTEGER
);

-- Cancer Table: This table will link assistance programs with the actual cancer types/subtypes
CREATE TABLE IF NOT EXISTS assistance_program_cancer (
    program_id TEXT NOT NULL,
    cancer_type TEXT NOT NULL,
    cancer_subtype TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (program_id, cancer_type, cancer_subtype),
    FOREIGN KEY (program_id)
        REFERENCES assistance_program(program_id)
);

-- Insurance Table: this table will link programs to their accepted insurance
CREATE TABLE IF NOT EXISTS assistance_program_insurance (
    program_id TEXT NOT NULL,
    insurance_type TEXT NOT NULL,
    PRIMARY KEY (program_id, insurance_type),
    FOREIGN KEY (program_id)
        REFERENCES assistance_program(program_id)
);
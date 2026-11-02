-- Eligibility table: This will be the main table and store all the financial assistance programs and their general eligibility reqs
CREATE TABLE IF NOT EXISTS assistance_program (
    program_id TEXT PRIMARY KEY,
    program_name TEXT NOT NULL,
    organization TEXT,
    additional_insurance_requirements TEXT,
    income_limit_fpl REAL,
    other_income_requirements TEXT,
    assistance_type TEXT,
    assistance_amount TEXT,
    other_eligibility_requirements TEXT,
    application_url TEXT,
    source_url TEXT,
    notes TEXT,
    min_age INTEGER,
    max_age INTEGER,

    CHECK (min_age IS NULL OR min_age >= 0),
    CHECK (max_age IS NULL OR max_age >= 0),
    CHECK (min_age IS NULL OR max_age IS NULL OR min_age <= max_age),
    CHECK (income_limit_fpl IS NULL OR income_limit_fpl >= 0)
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

-- Geography Table: this table will look at the treatmend/residency conditions
CREATE TABLE IF NOT EXISTS assistance_program_geography (
    geography_id INTEGER PRIMARY KEY,
    program_id TEXT NOT NULL,
    rule_group INTEGER NOT NULL DEFAULT 1,
    location_type TEXT NOT NULL
        CHECK (location_type IN ('residence', 'treatment')),
    country TEXT NOT NULL,
    state TEXT,
    county TEXT,

    FOREIGN KEY (program_id)
        REFERENCES assistance_program(program_id),

    CHECK (rule_group >= 1),
    CHECK (county IS NULL OR state IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS idx_assistance_geography_program
ON assistance_program_geography(program_id);
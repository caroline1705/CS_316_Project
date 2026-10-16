-- CureBase: Treatment regimen module (owner: Wanting)

DROP TABLE IF EXISTS regimen_phase;
DROP TABLE IF EXISTS regimen;
DROP TABLE IF EXISTS treatment;
DROP TABLE IF EXISTS cancer_type;

-- Which cancers we support (scope to be finalized by team).
CREATE TABLE cancer_type (
    cancer_id     VARCHAR(16) PRIMARY KEY,         -- e.g. 'BREAST'
    name          VARCHAR(64) NOT NULL,
    icd10_prefix  VARCHAR(8)  NOT NULL             -- e.g. 'C50' (ICD-10-CM)
);

-- A single kind of treatment (a drug combination, radiation, ...).
CREATE TABLE treatment (
    treatment_id  VARCHAR(32) PRIMARY KEY,         -- e.g. 'AC'
    name          VARCHAR(128) NOT NULL,
    modality      VARCHAR(16) NOT NULL
                  CHECK (modality IN ('CHEMO','TARGETED','IMMUNO','RADIATION','SURGERY'))
);

-- A standard treatment plan for one cancer type.
CREATE TABLE regimen (
    regimen_id    VARCHAR(32) PRIMARY KEY,         -- e.g. 'BREAST_ACT'
    cancer_id     VARCHAR(16) NOT NULL REFERENCES cancer_type(cancer_id),
    name          VARCHAR(128) NOT NULL,
    source_url    VARCHAR(256)
);

-- A regimen is a sequence of phases; each phase repeats a treatment in cycles.
-- Phases with the same start_week run at the same time (e.g. trastuzumab alongside chemo).
CREATE TABLE regimen_phase (
    regimen_id        VARCHAR(32) NOT NULL REFERENCES regimen(regimen_id),
    phase_no          INTEGER NOT NULL CHECK (phase_no >= 1),
    treatment_id      VARCHAR(32) NOT NULL REFERENCES treatment(treatment_id),
    start_week        INTEGER NOT NULL CHECK (start_week >= 0),
    cycle_length_days INTEGER NOT NULL CHECK (cycle_length_days > 0),
    num_cycles        INTEGER NOT NULL CHECK (num_cycles > 0),
    visits_per_cycle  INTEGER NOT NULL CHECK (visits_per_cycle > 0),
    PRIMARY KEY (regimen_id, phase_no)
);

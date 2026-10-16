-- CureBase: Household / FPL module (owner: Wanting)
-- Written in standard SQL so it runs on both SQLite and PostgreSQL.

DROP TABLE IF EXISTS poverty_guideline;
DROP TABLE IF EXISTS poverty_guideline_extra;

-- One row per (year, region, household size 1-8), copied from HHS/ASPE.
CREATE TABLE poverty_guideline (
    year            INTEGER NOT NULL,
    region          VARCHAR(16) NOT NULL
                    CHECK (region IN ('CONTIGUOUS', 'ALASKA', 'HAWAII')),
    household_size  INTEGER NOT NULL CHECK (household_size BETWEEN 1 AND 8),
    amount          INTEGER NOT NULL CHECK (amount > 0),   -- 100% FPL, USD/year
    PRIMARY KEY (year, region, household_size)
);

-- HHS adds a fixed amount for each person beyond 8.
CREATE TABLE poverty_guideline_extra (
    year                   INTEGER NOT NULL,
    region                 VARCHAR(16) NOT NULL,
    per_additional_person  INTEGER NOT NULL CHECK (per_additional_person > 0),
    PRIMARY KEY (year, region)
);

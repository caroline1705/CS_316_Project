-- CureBase: Indirect (non-medical) cost module (owner: Wanting)

DROP TABLE IF EXISTS mileage_rate;
DROP TABLE IF EXISTS lodging_rate;
DROP TABLE IF EXISTS childcare_rate;

-- IRS standard mileage rates. Rates can change mid-year, so we keep
-- every version with its effective date and pick the latest one <= today.
CREATE TABLE mileage_rate (
    effective_date  DATE NOT NULL,
    purpose         VARCHAR(16) NOT NULL CHECK (purpose IN ('MEDICAL','BUSINESS')),
    cents_per_mile  DECIMAL(5,1) NOT NULL CHECK (cents_per_mile > 0),
    source_url      VARCHAR(256),
    PRIMARY KEY (effective_date, purpose)
);

-- GSA per diem by federal fiscal year (Oct 1 - Sep 30) and county.
-- county = 'STANDARD' is the default rate for counties not listed.
CREATE TABLE lodging_rate (
    fiscal_year  INTEGER NOT NULL,
    state        CHAR(2) NOT NULL,
    county       VARCHAR(32) NOT NULL,
    city         VARCHAR(64),
    lodging      INTEGER NOT NULL CHECK (lodging > 0),   -- USD per night
    meals        INTEGER NOT NULL CHECK (meals > 0),     -- M&IE, USD per day
    PRIMARY KEY (fiscal_year, state, county)
);

-- Hourly childcare cost per state.
-- TODO: replace with county-level data from the U.S. DOL National Database of Childcare Prices.
CREATE TABLE childcare_rate (
    state           CHAR(2) PRIMARY KEY,
    hourly_rate     DECIMAL(6,2) NOT NULL CHECK (hourly_rate > 0),
    is_placeholder  BOOLEAN NOT NULL
);

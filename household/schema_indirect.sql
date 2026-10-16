-- CureBase: Indirect (non-medical) cost module (owner: Wanting)

DROP TABLE IF EXISTS mileage_rate;
DROP TABLE IF EXISTS lodging_rate;
DROP TABLE IF EXISTS childcare_price;
DROP TABLE IF EXISTS county;

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

-- Every county in the state (from the DOL file), even counties without price data.
CREATE TABLE county (
    state        CHAR(2) NOT NULL,
    county       VARCHAR(32) NOT NULL,
    county_fips  CHAR(5) NOT NULL UNIQUE,
    PRIMARY KEY (state, county)
);

-- Weekly median price of full-time childcare by county, provider type and child age.
-- Source: U.S. DOL National Database of Childcare Prices. county = 'STANDARD' is the
-- state-wide median, used when a county has no data.
CREATE TABLE childcare_price (
    state         CHAR(2) NOT NULL,
    county        VARCHAR(32) NOT NULL,
    county_fips   CHAR(5),
    study_year    INTEGER NOT NULL,
    provider      VARCHAR(8) NOT NULL CHECK (provider IN ('CENTER','HOME')),
    age_group     VARCHAR(16) NOT NULL
                  CHECK (age_group IN ('INFANT','TODDLER','PRESCHOOL','SCHOOL_AGE')),
    weekly_price  DECIMAL(7,2) NOT NULL CHECK (weekly_price > 0),
    PRIMARY KEY (state, county, study_year, provider, age_group)
);

-- DRAFT sample data: typical schedules for prototyping only.
-- Cancer types/regimens must be confirmed by the team and checked against NCI sources.
INSERT INTO cancer_type VALUES
 ('BREAST',     'Breast cancer',                 'C50'),
 ('COLORECTAL', 'Colorectal cancer',             'C18'),
 ('LYMPHOMA',   'Diffuse large B-cell lymphoma', 'C83');

INSERT INTO treatment VALUES
 ('AC',          'Doxorubicin + Cyclophosphamide', 'CHEMO'),
 ('PACLITAXEL',  'Paclitaxel',                     'CHEMO'),
 ('TRASTUZUMAB', 'Trastuzumab',                    'TARGETED'),
 ('BREAST_RT',   'Whole-breast radiation',         'RADIATION'),
 ('FOLFOX',      'Leucovorin + Fluorouracil + Oxaliplatin', 'CHEMO'),
 ('R_CHOP',      'Rituximab + CHOP',               'CHEMO');

INSERT INTO regimen VALUES
 ('BREAST_ACT_H',  'BREAST',     'Dose-dense AC-T + trastuzumab, then radiation',
    'https://www.cancer.gov/about-cancer/treatment/drugs/breast'),
 ('CRC_FOLFOX',    'COLORECTAL', 'Adjuvant FOLFOX',
    'https://www.cancer.gov/about-cancer/treatment/drugs/colorectal'),
 ('DLBCL_RCHOP',   'LYMPHOMA',   'R-CHOP x6',
    'https://www.cancer.gov/about-cancer/treatment/drugs/non-hodgkin-lymphoma');

-- (regimen, phase, treatment, start_week, cycle_days, cycles, visits/cycle)
INSERT INTO regimen_phase VALUES
 ('BREAST_ACT_H', 1, 'AC',          0, 14,  4, 1),
 ('BREAST_ACT_H', 2, 'PACLITAXEL',  8, 14,  4, 1),
 ('BREAST_ACT_H', 3, 'TRASTUZUMAB', 8, 21, 17, 1),
 ('BREAST_ACT_H', 4, 'BREAST_RT',  20,  1, 15, 1),  -- daily, 3 weeks (weekdays)
 ('CRC_FOLFOX',   1, 'FOLFOX',      0, 14, 12, 2),  -- infusion + pump removal
 ('DLBCL_RCHOP',  1, 'R_CHOP',      0, 21,  6, 1);

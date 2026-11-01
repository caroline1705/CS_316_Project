-- Standard treatment regimens for the five cancer types chosen by the team.
-- One common regimen per cancer; real treatment plans vary by patient.
-- Sources are stored in regimen.source_url.
INSERT INTO cancer_type VALUES
 ('BREAST',     'Breast cancer',                 'C50'),
 ('LUNG',       'Lung cancer (non-small cell)',  'C34'),
 ('COLORECTAL', 'Colorectal cancer',             'C18-C20'),
 ('PROSTATE',   'Prostate cancer',               'C61'),
 ('LYMPHOMA',   'Diffuse large B-cell lymphoma', 'C83.3');

INSERT INTO treatment VALUES
 ('AC',          'Doxorubicin + cyclophosphamide (AC)',                       'CHEMO'),
 ('PACLITAXEL',  'Paclitaxel',                                                'CHEMO'),
 ('TRASTUZUMAB', 'Trastuzumab',                                               'TARGETED'),
 ('BREAST_RT',   'Whole-breast radiation (40 Gy in 15 fractions)',            'RADIATION'),
 ('LUNG_CRT',    'Chemoradiation (60 Gy in 30 fractions + weekly carboplatin/paclitaxel)', 'CHEMORADIATION'),
 ('DURVALUMAB',  'Durvalumab',                                                'IMMUNO'),
 ('FOLFOX',      'FOLFOX (oxaliplatin + leucovorin + fluorouracil)',          'CHEMO'),
 ('ADT',         'Androgen deprivation therapy (leuprolide injection)',      'HORMONE'),
 ('PROSTATE_RT', 'Prostate radiation (60 Gy in 20 fractions)',                'RADIATION'),
 ('R_CHOP',      'R-CHOP (rituximab + cyclophosphamide, doxorubicin, vincristine, prednisone)', 'CHEMO'),
 ('RITUXIMAB',   'Rituximab alone',                                           'TARGETED');

INSERT INTO regimen VALUES
 ('BREAST_ACT_H', 'BREAST', 'HER2+ early stage: dose-dense AC-T + trastuzumab, then radiation',
    'https://www.cancercareontario.ca/system/files_force/AC-PACLDD%20%20TRAS_BR_NADJ.pdf?download=1'),
 ('LUNG_CRT_DURVA', 'LUNG', 'Stage III: chemoradiation, then durvalumab for 1 year',
    'https://www.esmo.org/Oncology-News/Durvalumab-Improves-Progression-free-Survival-in-Stage-III-Lung-Cancer'),
 ('CRC_FOLFOX', 'COLORECTAL', 'Stage III colon: adjuvant FOLFOX for 6 months',
    'https://www.hse.ie/eng/services/list/5/cancer/profinfo/chemoprotocols/gastrointestinal/209.pdf'),
 ('PROSTATE_RT_ADT', 'PROSTATE', 'Intermediate risk: 6 months of hormone therapy + 4 weeks of radiation',
    'https://repository.icr.ac.uk/items/2ea9a890-7806-438e-9f2e-cf8455de7c1b'),
 ('DLBCL_RCHOP', 'LYMPHOMA', 'R-CHOP every 3 weeks for 6 cycles, then rituximab for 2 cycles',
    'https://lymphomahub.com/medical-information/polatuzumab-vedotin-r-chp-vs-r-chop-for-frontline-treatment-of-dlbcl-results-from-the-phase-iii-polarix-trial');

-- (regimen, phase, treatment, start_week, cycle_days, cycles, visits/cycle)
-- cycle_days = 1 means daily weekday sessions (radiation): 5 per week.
INSERT INTO regimen_phase VALUES
 ('BREAST_ACT_H',    1, 'AC',          0, 14,  4, 1),  -- every 2 weeks x 4
 ('BREAST_ACT_H',    2, 'PACLITAXEL',  8, 14,  4, 1),  -- every 2 weeks x 4
 ('BREAST_ACT_H',    3, 'TRASTUZUMAB', 8, 21, 17, 1),  -- every 3 weeks for 1 year (~17 doses)
 ('BREAST_ACT_H',    4, 'BREAST_RT',  20,  1, 15, 1),  -- 15 weekday sessions
 ('LUNG_CRT_DURVA',  1, 'LUNG_CRT',    0,  1, 30, 1),  -- 30 weekday sessions; PACIFIC allowed 54-66 Gy,
                                                       -- 60 Gy/30 is the common dose; chemo on RT days
 ('LUNG_CRT_DURVA',  2, 'DURVALUMAB',  8, 28, 13, 1),  -- up to 12 months (PACIFIC); FDA-approved
                                                       -- 1500 mg every 4 weeks option
 ('CRC_FOLFOX',      1, 'FOLFOX',      0, 14, 12, 2),  -- infusion + return for pump removal after 46 h
                                                       -- (assumption: some patients disconnect at home)
 ('PROSTATE_RT_ADT', 1, 'ADT',         0, 84,  2, 1),  -- injection every 3 months x 2 (CHHiP: 3-6 months
                                                       -- of hormone therapy before and during RT)
 ('PROSTATE_RT_ADT', 2, 'PROSTATE_RT',12,  1, 20, 1),  -- 20 weekday sessions
 ('DLBCL_RCHOP',     1, 'R_CHOP',      0, 21,  6, 1),  -- every 3 weeks x 6 (POLARIX control arm)
 ('DLBCL_RCHOP',     2, 'RITUXIMAB',  18, 21,  2, 1);  -- then rituximab alone x 2

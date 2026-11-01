-- IRS 2026 mileage rates (revised mid-year, effective July 1, 2026; IRB 2026-29)
INSERT INTO mileage_rate VALUES
 ('2026-01-01','MEDICAL', 20.5,'https://www.irs.gov/Tax-Professionals/Standard-Mileage-Rates'),
 ('2026-07-01','MEDICAL', 23.5,'https://www.irs.gov/Tax-Professionals/Standard-Mileage-Rates'),
 ('2026-01-01','BUSINESS',72.5,'https://www.irs.gov/Tax-Professionals/Standard-Mileage-Rates'),
 ('2026-07-01','BUSINESS',76.0,'https://www.irs.gov/Tax-Professionals/Standard-Mileage-Rates');

-- GSA FY2027 per diem (Oct 1, 2026 - Sep 30, 2027), North Carolina.
-- Standard rate ($113 lodging / $68 M&IE) confirmed by Federal News Network, Sept 2026.
-- County rates cross-checked on FederalPay.org and FedPayScale.org (same value every month).
-- Seasonal coastal areas (Carteret, Dare, New Hanover) are left out because their rate
-- changes by month; they fall back to the standard rate. None of our hospitals is there.
INSERT INTO lodging_rate VALUES
 (2027,'NC','STANDARD',    NULL,                            113, 68),
 (2027,'NC','Buncombe',    'Asheville',                     145, 80),
 (2027,'NC','Orange',      'Chapel Hill',                   153, 80),
 (2027,'NC','Mecklenburg', 'Charlotte',                     143, 80),
 (2027,'NC','Durham',      'Durham',                        124, 74),
 (2027,'NC','Cumberland',  'Fayetteville',                  129, 68),
 (2027,'NC','Guilford',    'Greensboro',                    130, 74),
 (2027,'NC','Wake',        'Raleigh',                       142, 74);

-- Childcare prices are loaded from seed_childcare.sql (DOL NDCP data).

-- Indirect cost estimate for one patient.
-- Inputs: :regimen_id, :distance_miles (one way), :state, :county (of the hospital),
--         :as_of (date), :fiscal_year, :lodging_threshold (miles),
--         :has_children (0/1), :childcare_hours_per_visit
WITH visits AS (                        -- total hospital visits for the regimen
    SELECT SUM(num_cycles * visits_per_cycle) AS n
    FROM regimen_phase
    WHERE regimen_id = :regimen_id
),
mileage AS (                            -- latest IRS medical rate in effect
    SELECT cents_per_mile
    FROM mileage_rate
    WHERE purpose = 'MEDICAL' AND effective_date <= :as_of
    ORDER BY effective_date DESC
    LIMIT 1
),
lodging AS (                            -- county rate if listed, else state standard
    SELECT COALESCE(c.lodging, s.lodging) AS lodging,
           COALESCE(c.meals,   s.meals)   AS meals
    FROM lodging_rate s
    LEFT JOIN lodging_rate c
      ON c.fiscal_year = s.fiscal_year AND c.state = s.state AND c.county = :county
    WHERE s.fiscal_year = :fiscal_year AND s.state = :state AND s.county = 'STANDARD'
)
SELECT
    v.n                                                         AS total_visits,
    ROUND(v.n * 2 * :distance_miles * m.cents_per_mile / 100.0, 2)
                                                                AS travel_cost,
    CASE WHEN :distance_miles >= :lodging_threshold
         THEN v.n * (l.lodging + l.meals) ELSE 0 END            AS lodging_cost,
    CASE WHEN :has_children = 1
         THEN ROUND(v.n * :childcare_hours_per_visit * cc.hourly_rate, 2)
         ELSE 0 END                                             AS childcare_cost,
    m.cents_per_mile, l.lodging, l.meals, cc.hourly_rate
FROM visits v
CROSS JOIN mileage m
CROSS JOIN lodging l
JOIN childcare_rate cc ON cc.state = :state;

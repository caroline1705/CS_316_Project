-- Indirect cost estimate for one patient.
-- Inputs: :regimen_id, :distance_miles (one way), :state, :county (hospital county),
--         :home_county (patient's county, for childcare), :num_children, :age_group,
--         :as_of (date), :fiscal_year, :lodging_threshold (miles)
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
lodging AS (                            -- hospital county rate if listed, else state standard
    SELECT COALESCE(c.lodging, s.lodging) AS lodging,
           COALESCE(c.meals,   s.meals)   AS meals,
           c.lodging IS NULL              AS lodging_is_standard
    FROM lodging_rate s
    LEFT JOIN lodging_rate c
      ON c.fiscal_year = s.fiscal_year AND c.state = s.state AND c.county = :county
    WHERE s.fiscal_year = :fiscal_year AND s.state = :state AND s.county = 'STANDARD'
),
childcare AS (                          -- home county price if available, else state median
    SELECT COALESCE(c.weekly_price, s.weekly_price) AS weekly_price,
           c.weekly_price IS NULL                   AS childcare_is_median
    FROM childcare_price s
    LEFT JOIN childcare_price c
      ON c.state = s.state AND c.study_year = s.study_year AND c.provider = s.provider
     AND c.age_group = s.age_group AND c.county = :home_county
    WHERE s.state = :state AND s.county = 'STANDARD'
      AND s.provider = 'CENTER' AND s.age_group = :age_group
      AND s.study_year = (SELECT MAX(study_year) FROM childcare_price WHERE state = :state)
)
SELECT
    v.n                                                         AS total_visits,
    ROUND(v.n * 2 * :distance_miles * m.cents_per_mile / 100.0, 2)
                                                                AS travel_cost,
    CASE WHEN :distance_miles >= :lodging_threshold
         THEN v.n * (l.lodging + l.meals) ELSE 0 END            AS lodging_cost,
    -- one day of care per visit = weekly price / 5 weekdays, per child
    ROUND(v.n * :num_children * cc.weekly_price / 5.0, 2)       AS childcare_cost,
    m.cents_per_mile, l.lodging, l.meals, cc.weekly_price,
    l.lodging_is_standard, cc.childcare_is_median
FROM visits v
CROSS JOIN mileage m
CROSS JOIN lodging l
CROSS JOIN childcare cc;

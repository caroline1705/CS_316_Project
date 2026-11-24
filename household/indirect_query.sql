-- Indirect cost estimate for one patient.
-- Inputs: :regimen_id, :distance_miles (one way), :state, :county (hospital county),
--         :home_county (patient's county, for childcare),
--         :n_infant, :n_toddler, :n_preschool, :n_school_age (children needing care by age),
--         :age_group (price shown when there are no children),
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
childcare_rates AS (                    -- weekly price per age group: home county if listed, else NC median
    SELECT s.age_group,
           COALESCE(c.weekly_price, s.weekly_price) AS weekly_price,
           c.weekly_price IS NULL                   AS is_median
    FROM childcare_price s
    LEFT JOIN childcare_price c
      ON c.state = s.state AND c.study_year = s.study_year AND c.provider = s.provider
     AND c.age_group = s.age_group AND c.county = :home_county
    WHERE s.state = :state AND s.county = 'STANDARD' AND s.provider = 'CENTER'
      AND s.study_year = (SELECT MAX(study_year) FROM childcare_price WHERE state = :state)
),
kids AS (                               -- how many children need care in each age group
    SELECT 'INFANT' AS age_group, :n_infant AS n
    UNION ALL SELECT 'TODDLER',    :n_toddler
    UNION ALL SELECT 'PRESCHOOL',  :n_preschool
    UNION ALL SELECT 'SCHOOL_AGE', :n_school_age
),
childcare AS (                          -- combined weekly price for all children
    SELECT SUM(k.n)                                         AS n_children,
           SUM(k.n * r.weekly_price)                        AS weekly_total,
           MAX(CASE WHEN k.n > 0 THEN r.is_median ELSE 0 END) AS any_median,
           (SELECT weekly_price FROM childcare_rates WHERE age_group = :age_group) AS default_weekly,
           (SELECT is_median    FROM childcare_rates WHERE age_group = :age_group) AS default_median
    FROM kids k
    JOIN childcare_rates r ON r.age_group = k.age_group
)
SELECT
    v.n                                                         AS total_visits,
    ROUND(v.n * 2 * :distance_miles * m.cents_per_mile / 100.0, 2)
                                                                AS travel_cost,
    CASE WHEN :distance_miles >= :lodging_threshold
         THEN v.n * (l.lodging + l.meals) ELSE 0 END            AS lodging_cost,
    -- one day of care per visit = weekly price / 5 weekdays, for every child
    ROUND(v.n * cc.weekly_total / 5.0, 2)                       AS childcare_cost,
    m.cents_per_mile, l.lodging, l.meals,
    -- average weekly price per child (or the default age group's price if no children)
    CASE WHEN cc.n_children > 0 THEN ROUND(cc.weekly_total / cc.n_children, 2)
         ELSE cc.default_weekly END                             AS childcare_weekly,
    l.lodging_is_standard,
    CASE WHEN cc.n_children > 0 THEN cc.any_median
         ELSE cc.default_median END                             AS childcare_is_median,
    cc.n_children
FROM visits v
CROSS JOIN mileage m
CROSS JOIN lodging l
CROSS JOIN childcare cc;

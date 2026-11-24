-- Weekly center-based childcare price for each age group in one county
-- (NC median when the county has no DOL data). Inputs: :state, :home_county
SELECT s.age_group,
       COALESCE(c.weekly_price, s.weekly_price) AS weekly_price,
       c.weekly_price IS NULL                   AS is_median
FROM childcare_price s
LEFT JOIN childcare_price c
  ON c.state = s.state AND c.study_year = s.study_year AND c.provider = s.provider
 AND c.age_group = s.age_group AND c.county = :home_county
WHERE s.state = :state AND s.county = 'STANDARD' AND s.provider = 'CENTER'
  AND s.study_year = (SELECT MAX(study_year) FROM childcare_price WHERE state = :state);

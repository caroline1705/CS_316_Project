-- Given :year, :region, :size, :income  ->  the guideline and FPL %.
-- Households larger than 8 use the size-8 amount + extra per person.
SELECT
    g.amount + (CASE WHEN :size > 8 THEN :size - 8 ELSE 0 END) * e.per_additional_person
        AS guideline,
    ROUND(100.0 * :income /
          (g.amount + (CASE WHEN :size > 8 THEN :size - 8 ELSE 0 END) * e.per_additional_person), 1)
        AS fpl_percent
FROM poverty_guideline g
JOIN poverty_guideline_extra e
  ON e.year = g.year AND e.region = g.region
WHERE g.year = :year
  AND g.region = :region
  AND g.household_size = (CASE WHEN :size > 8 THEN 8 ELSE :size END);

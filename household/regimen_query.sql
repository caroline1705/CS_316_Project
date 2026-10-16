-- Summary per regimen: total hospital visits and total length in weeks.
-- Radiation is daily on weekdays, so 15 sessions = 3 weeks (5 per week).
SELECT
    r.regimen_id,
    c.name                                       AS cancer,
    r.name                                       AS regimen,
    SUM(p.num_cycles * p.visits_per_cycle)       AS total_visits,
    MAX(p.start_week +
        CASE WHEN p.cycle_length_days = 1
             THEN (p.num_cycles + 4) / 5                       -- weekday sessions
             ELSE (p.num_cycles * p.cycle_length_days + 6) / 7 -- round up to weeks
        END)                                     AS total_weeks
FROM regimen r
JOIN cancer_type   c ON c.cancer_id  = r.cancer_id
JOIN regimen_phase p ON p.regimen_id = r.regimen_id
WHERE (:cancer_id IS NULL OR r.cancer_id = :cancer_id)
GROUP BY r.regimen_id, c.name, r.name
ORDER BY r.regimen_id;

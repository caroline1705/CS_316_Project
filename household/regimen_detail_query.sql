-- Phases of one regimen, in order, with the visits each phase needs.
SELECT p.phase_no, t.name, t.modality, p.start_week,
       p.cycle_length_days, p.num_cycles, p.visits_per_cycle,
       p.num_cycles * p.visits_per_cycle AS visits
FROM regimen_phase p
JOIN treatment t ON t.treatment_id = p.treatment_id
WHERE p.regimen_id = :regimen_id
ORDER BY p.phase_no;

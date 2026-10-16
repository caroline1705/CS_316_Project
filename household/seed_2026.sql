-- Source: HHS 2026 Poverty Guidelines (Federal Register doc. 2026-00755), verified 2026-10-16
-- https://public-inspection.federalregister.gov/2026-00755.pdf
-- https://aspe.hhs.gov/sites/default/files/documents/b1bfa16b20ae9b89d525bc35de7c1643/detailed-guidelines-2026.pdf
INSERT INTO poverty_guideline (year, region, household_size, amount) VALUES
 (2026,'CONTIGUOUS',1,15960),(2026,'CONTIGUOUS',2,21640),(2026,'CONTIGUOUS',3,27320),(2026,'CONTIGUOUS',4,33000),
 (2026,'CONTIGUOUS',5,38680),(2026,'CONTIGUOUS',6,44360),(2026,'CONTIGUOUS',7,50040),(2026,'CONTIGUOUS',8,55720),
 (2026,'ALASKA',1,19950),(2026,'ALASKA',2,27050),(2026,'ALASKA',3,34150),(2026,'ALASKA',4,41250),
 (2026,'ALASKA',5,48350),(2026,'ALASKA',6,55450),(2026,'ALASKA',7,62550),(2026,'ALASKA',8,69650),
 (2026,'HAWAII',1,18360),(2026,'HAWAII',2,24890),(2026,'HAWAII',3,31420),(2026,'HAWAII',4,37950),
 (2026,'HAWAII',5,44480),(2026,'HAWAII',6,51010),(2026,'HAWAII',7,57540),(2026,'HAWAII',8,64070);

INSERT INTO poverty_guideline_extra (year, region, per_additional_person) VALUES
 (2026,'CONTIGUOUS',5680),(2026,'ALASKA',7100),(2026,'HAWAII',6530);

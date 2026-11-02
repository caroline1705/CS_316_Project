
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from assistance import assistance


class TestAssistanceMatching(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db = Path(cls.temp_dir.name) / "assistance_test.db"

        folder = Path(__file__).resolve().parent

        conn = sqlite3.connect(cls.test_db)
        conn.execute("PRAGMA foreign_keys = ON")

        try:
            conn.executescript(
                (folder / "schema_assistance.sql").read_text(
                    encoding="utf-8"
                )
            )
            conn.executescript(
                (folder / "generated_assistance_seed.sql").read_text(
                    encoding="utf-8"
                )
            )

            violations = conn.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()

            if violations:
                raise AssertionError(
                    f"Foreign key violations: {violations}"
                )
        finally:
            conn.close()

        cls.db_patch = patch.object(
            assistance, "DB", cls.test_db
        )
        cls.db_patch.start()

    @classmethod
    def tearDownClass(cls):
        cls.db_patch.stop()
        cls.temp_dir.cleanup()

    def get_programs(self, cancer, **kwargs):
        return assistance.find_matching_assistance(
            cancer_type=cancer,
            **kwargs
        )

    def get_ids(self, cancer, **kwargs):
        return {
            p["program_id"]
            for p in self.get_programs(cancer, **kwargs)
        }

    def test_unknown_subtype(self):
        ids = self.get_ids(
            "Lung",
            cancer_subtype="Unknown",
            insurance="Private"
        )
        self.assertIn("P006", ids)
        self.assertIn("P029", ids)

    def test_known_subtype(self):
        ids = self.get_ids(
            "Lung",
            cancer_subtype="Small cell lung cancer",
            insurance="Private"
        )
        self.assertNotIn("P006", ids)
        self.assertNotIn("P029", ids)
        self.assertIn("P018", ids)

    def test_uninsured(self):
        ids = self.get_ids(
            "Lung",
            insurance="Uninsured"
        )
        self.assertNotIn("P006", ids)
        self.assertNotIn("P029", ids)
        self.assertIn("P020", ids)

    def test_income_limit(self):
        ids = self.get_ids(
            "Breast",
            insurance="Private",
            fpl_percent=400
        )
        self.assertNotIn("P003", ids)
        self.assertIn("P027", ids)

    def test_age_limit(self):
        ids = self.get_ids(
            "Breast",
            insurance="Private",
            age=45
        )
        self.assertNotIn("P021", ids)

    def test_canadian_residency(self):
        ids = self.get_ids(
            "Breast",
            insurance="Private",
            country="Canada",
            state="Ontario",
            county="Toronto",
            treatment_country="Canada",
            treatment_state="Ontario",
            treatment_county="Toronto"
        )
        self.assertIn("P027", ids)
        self.assertNotIn("P003", ids)

    def test_eligible_treatment_county(self):
        ids = self.get_ids(
            "Lung",
            insurance="Private",
            country="US",
            state="NC",
            county="Durham",
            treatment_country="US",
            treatment_state="NC",
            treatment_county="Wayne"
        )
        self.assertIn("P008", ids)

    def test_ineligible_treatment_county(self):
        ids = self.get_ids(
            "Lung",
            insurance="Private",
            country="US",
            state="NC",
            county="Durham",
            treatment_country="US",
            treatment_state="NC",
            treatment_county="Durham"
        )
        self.assertNotIn("P008", ids)

    def test_nc_only_program_excludes_sc_resident(self):
        ids = self.get_ids(
            "Lung",
            country="US",
            state="SC",
            county="York",
            treatment_country="US",
            treatment_state="NC",
            treatment_county="Durham"
        )
        self.assertNotIn("P019", ids)

    def test_nc_only_program_accepts_nc_resident(self):
        ids = self.get_ids(
            "Lung",
            country="US",
            state="NC",
            county="Durham"
        )
        self.assertIn("P019", ids)

    def test_nc_sc_program_accepts_sc_resident(self):
        ids = self.get_ids(
            "Lung",
            country="US",
            state="SC",
            county="York"
        )
        self.assertIn("P018", ids)

    def test_missing_county_needs_review(self):
        programs = self.get_programs(
            "Lung",
            country="US",
            state="NC",
            county="Durham",
            treatment_country="US",
            treatment_state="NC"
        )

        p008 = next(
            p for p in programs
            if p["program_id"] == "P008"
        )

        self.assertEqual(
            p008["residency_status"],
            "needs_review"
        )

    def test_wrong_cancer_type(self):
        ids = self.get_ids(
            "Prostate",
            insurance="Private"
        )
        self.assertNotIn("P001", ids)

    def test_no_geography_restriction(self):
        programs = self.get_programs(
            "Breast",
            country="Canada",
            state="Ontario",
            treatment_country="US",
            treatment_state="NC"
        )

        p001 = next(
            p for p in programs
            if p["program_id"] == "P001"
        )

        self.assertEqual(
            p001["residency_status"],
            "match"
        )

    def test_private_insurance_rejected_by_medicare_only(self):
        ids = self.get_ids(
            "Breast",
            insurance="Private"
        )
        self.assertNotIn("P028", ids)

    def test_medicare_accepted_by_medicare_only(self):
        ids = self.get_ids(
            "Breast",
            insurance="Medicare"
        )
        self.assertIn("P028", ids)


if __name__ == "__main__":
    unittest.main()

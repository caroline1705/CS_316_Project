"""Automated tests for the household and nonmedical cost module.

Run from the household/ folder:  python3 init_db.py && python3 -m unittest test_household -v
Expected values were worked out by hand from the official rates in the seed files.
"""
import sqlite3
import unittest

from app import app
from fpl import DB, fpl_percent
from indirect import indirect_costs
from regimen import regimen_summary


class HouseholdTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(DB)
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    # ------------------------------------------------------------ FPL
    def test_fpl_matches_hhs_2026(self):
        cases = [  # (income, household size, state, expected %)
            (60000, 3, "NC", 219.6),
            (27320, 3, "NC", 100.0),   # exactly at the poverty line
            (61400, 9, "NC", 100.0),   # 55,720 + 5,680 for the 9th person
            (34150, 3, "AK", 100.0),   # Alaska has its own table
        ]
        for income, size, state, expected in cases:
            with self.subTest(income=income, size=size, state=state):
                self.assertEqual(fpl_percent(self.conn, income, size, state)["fpl_percent"], expected)

    # ------------------------------------------------------------ regimens
    def test_regimen_visits_and_weeks(self):
        expected = {  # regimen: (total visits, total weeks)
            "BREAST_ACT_H": (40, 59), "LUNG_CRT_DURVA": (43, 60), "CRC_FOLFOX": (24, 24),
            "PROSTATE_RT_ADT": (22, 24), "DLBCL_RCHOP": (8, 24),
        }
        for regimen, (visits, weeks) in expected.items():
            with self.subTest(regimen=regimen):
                row = regimen_summary(self.conn, regimen_id=regimen)[0]
                self.assertEqual((row[3], row[4]), (visits, weeks))

    # ------------------------------------------------------------ indirect costs
    def test_breast_durham_one_preschooler(self):
        # 40 visits x 300 mi x $0.235 = 2,820; 40 nights x ($124 + $74) = 7,920;
        # 40 x $188.37 / 5 = 1,506.96
        r = indirect_costs(self.conn, "BREAST_ACT_H", 150, "Durham", num_children=1,
                           home_county="Durham", age_group="PRESCHOOL", as_of="2026-10-31")
        self.assertEqual((r["travel"], r["lodging"], r["childcare"], r["total"]),
                         (2820.0, 7920, 1506.96, 12246.96))

    def test_no_lodging_under_100_miles(self):
        r = indirect_costs(self.conn, "CRC_FOLFOX", 99, "Durham", as_of="2026-10-31")
        self.assertEqual(r["lodging"], 0)

    def test_children_in_different_age_groups(self):
        # Orange County: infant $354.86/week, school age $104.68/week, 24 visits
        # 24 x 354.86 / 5 = 1,703.33 and 24 x 2 x 104.68 / 5 = 1,004.93
        r = indirect_costs(self.conn, "CRC_FOLFOX", 40, "Orange", home_county="Orange",
                           children_by_age={"INFANT": 1, "SCHOOL_AGE": 2})
        self.assertEqual(r["children"], 3)
        self.assertAlmostEqual(r["childcare"], 2708.26, places=2)
        parts = {c["age_group"]: c["cost"] for c in r["childcare_by_age"]}
        self.assertEqual(parts, {"INFANT": 1703.33, "SCHOOL_AGE": 1004.93})
        self.assertAlmostEqual(sum(parts.values()), r["childcare"], delta=0.02)

    def test_old_single_age_call_still_works(self):
        old = indirect_costs(self.conn, "CRC_FOLFOX", 40, "Orange", num_children=2,
                             home_county="Orange", age_group="TODDLER")
        new = indirect_costs(self.conn, "CRC_FOLFOX", 40, "Orange", home_county="Orange",
                             children_by_age={"TODDLER": 2})
        self.assertEqual(old["childcare"], new["childcare"])

    def test_county_without_data_uses_nc_median(self):
        r = indirect_costs(self.conn, "CRC_FOLFOX", 40, "Durham", home_county="Graham",
                           children_by_age={"PRESCHOOL": 1})
        self.assertTrue(r["childcare_is_median"])

    def test_hospital_county_without_gsa_rate_uses_standard(self):
        r = indirect_costs(self.conn, "DLBCL_RCHOP", 120, "Pitt")
        self.assertTrue(r["lodging_is_standard"])
        self.assertEqual((r["lodging_rate"], r["meals_rate"]), (113, 68))

    # ------------------------------------------------------------ API
    def test_api_children_by_age(self):
        r = self.client.get("/api/indirect-costs?regimen=CRC_FOLFOX&hospital=UNC&distance=40"
                            "&home_county=Orange&infants=1&school_age=2")
        self.assertEqual(r.status_code, 200)
        self.assertAlmostEqual(r.get_json()["childcare"], 2708.26, places=2)

    def test_api_rejects_bad_input(self):
        base = "/api/indirect-costs?regimen=CRC_FOLFOX&hospital=UNC&distance=40"
        for query, status in [("&infants=-1", 400), ("&infants=6&toddlers=5", 400),
                              ("&infants=abc", 400)]:
            with self.subTest(query=query):
                self.assertEqual(self.client.get(base + query).status_code, status)
        self.assertEqual(self.client.get(
            "/api/indirect-costs?regimen=CRC_FOLFOX&hospital=UNC&distance=-3").status_code, 400)
        self.assertEqual(self.client.get(
            "/api/indirect-costs?regimen=NOPE&hospital=UNC&distance=40").status_code, 404)
        self.assertEqual(self.client.get(
            "/api/indirect-costs?regimen=CRC_FOLFOX&hospital=NOPE&distance=40").status_code, 404)
        self.assertEqual(self.client.get("/api/fpl?income=-5&size=3").status_code, 400)


if __name__ == "__main__":
    unittest.main()

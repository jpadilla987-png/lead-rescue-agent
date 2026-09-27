import unittest
from semantic_guard import EqualFieldRule, check_equal_fields

class LeadingZeroRegressionTest(unittest.TestCase):
    def test_leading_zero_text_differs_from_number(self):
        rule = EqualFieldRule("request.id", "result.id", "returned_same_record")
        text_id = "0" * 2 + "7"
        row = {"request": {"id": text_id}, "result": {"id": 7}}
        violations = check_equal_fields([row], [rule])
        self.assertEqual(violations[0]["kind"], "contract_mismatch")

if __name__ == "__main__":
    unittest.main()

import unittest

from semantic_guard import EqualFieldRule, check_equal_fields


class SemanticGuardTests(unittest.TestCase):
    def test_stable_wrong_id_is_flagged_without_history(self):
        rule = EqualFieldRule("request.id", "result.id", "returned_same_record")
        for _ in range(30):
            row = {
                "request": {"id": "A42"},
                "result": {"id": "B17", "status": "completed"},
            }
            violations = check_equal_fields([row], [rule])
            self.assertEqual(violations[0]["kind"], "contract_mismatch")

    def test_matching_id_is_quiet(self):
        rule = EqualFieldRule("request.id", "result.id", "returned_same_record")
        row = {
            "request": {"id": "A42"},
            "result": {"id": "A42", "status": "completed"},
        }
        self.assertEqual(check_equal_fields([row], [rule]), [])

    def test_missing_field_is_not_silently_treated_as_good(self):
        rule = EqualFieldRule("request.id", "result.id", "returned_same_record")
        row = {
            "request": {"id": "A42"},
            "result": {"status": "completed"},
        }
        violations = check_equal_fields([row], [rule])
        self.assertEqual(violations[0]["kind"], "contract_unverifiable")
        self.assertEqual(violations[0]["missing"], ["result.id"])

    def test_nested_paths_work(self):
        rule = EqualFieldRule(
            "input.customer.id",
            "output.customer.id",
            "same_customer",
        )
        row = {
            "input": {"customer": {"id": 7}},
            "output": {"customer": {"id": 8}},
        }
        self.assertEqual(
            check_equal_fields([row], [rule])[0]["kind"],
            "contract_mismatch",
        )

    def test_multiple_rows_are_checked_independently(self):
        rule = EqualFieldRule("request.id", "result.id", "returned_same_record")
        rows = [
            {"request": {"id": "1"}, "result": {"id": "1"}},
            {"request": {"id": "2"}, "result": {"id": "9"}},
        ]
        violations = check_equal_fields(rows, [rule])
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["row"], 1)

    def test_no_rules_means_no_claim(self):
        row = {"request": {"id": "1"}, "result": {"id": "2"}}
        self.assertEqual(check_equal_fields([row], []), [])


if __name__ == "__main__":
    unittest.main()

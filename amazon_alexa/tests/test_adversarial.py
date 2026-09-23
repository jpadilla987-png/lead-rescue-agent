import unittest

from lead_rescue_core import draft_follow_up, prioritized_leads


class AdversarialLeadRescueTests(unittest.TestCase):
    def test_limit_zero_rejected(self) -> None:
        with self.assertRaises(ValueError):
            prioritized_leads(0)

    def test_limit_above_max_rejected(self) -> None:
        with self.assertRaises(ValueError):
            prioritized_leads(11)

    def test_invalid_tone_rejected(self) -> None:
        with self.assertRaises(ValueError):
            draft_follow_up("lead-001", tone="aggressive")

    def test_all_priority_scores_are_bounded(self) -> None:
        for lead in prioritized_leads(4):
            self.assertGreaterEqual(lead["priority_score"], 0)
            self.assertLessEqual(lead["priority_score"], 100)

    def test_price_match_never_promises_discount(self) -> None:
        result = draft_follow_up("lead-002")
        self.assertTrue(result["requires_owner_approval"])
        text = result["draft"].lower()
        self.assertNotIn("discount", text)
        self.assertNotIn("we can match", text)
        self.assertNotIn("we'll match", text)

    def test_routine_followup_does_not_require_owner(self) -> None:
        result = draft_follow_up("lead-003")
        self.assertFalse(result["requires_owner_approval"])


if __name__ == "__main__":
    unittest.main()

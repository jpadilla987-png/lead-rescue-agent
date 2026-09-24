import unittest

from lead_rescue_core import draft_follow_up, get_lead, prioritized_leads


class LeadRescueCoreTests(unittest.TestCase):
    def test_priority_order_is_descending(self) -> None:
        leads = prioritized_leads(4)
        scores = [lead["priority_score"] for lead in leads]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_critical_service_need_outranks_revenue_heavy_lead(self) -> None:
        leads = prioritized_leads(2)
        self.assertEqual(leads[0]["id"], "lead-001")
        self.assertEqual(leads[0]["priority_score"], 90)
        self.assertEqual(leads[1]["id"], "lead-002")

    def test_price_match_escalates(self) -> None:
        result = draft_follow_up("lead-002")
        self.assertTrue(result["requires_owner_approval"])
        self.assertIn("price match", result["reason"].lower())

    def test_critical_lead_has_urgent_reason(self) -> None:
        lead = get_lead("lead-001")
        self.assertIn("critical service need", lead["why_now"])

    def test_unknown_lead_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            get_lead("missing")


if __name__ == "__main__":
    unittest.main()

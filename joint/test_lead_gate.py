import unittest

from joint.lead_gate import Candidate, Review, Verdict, assess, has_explicit_pay_amount


class LeadGateTests(unittest.TestCase):
    def base(self, **overrides):
        data = dict(
            source="https://example.com/post",
            buyer="Example Buyer",
            problem="Fix an AI automation workflow",
            age_hours=4,
            compensation_verified=True,
            pay_quote="$200 for one workflow",
            direct_route_verified=True,
            cost_to_pursue_usd=0,
            fit_score=5,
            mandatory_live_video=False,
            unsupported_requirement=False,
            duplicate_status="new",
            human_gate=None,
        )
        data.update(overrides)
        return Candidate(**data)

    def test_clean_candidate_survives(self):
        d = assess(self.base(), [Review("Sable", "PASS"), Review("AVA", "PASS")])
        self.assertEqual(d.verdict, Verdict.SURVIVES)

    def test_upfront_cost_kills(self):
        d = assess(self.base(cost_to_pursue_usd=2.10))
        self.assertEqual(d.verdict, Verdict.KILLED)
        self.assertTrue(any("upfront" in r for r in d.reasons))

    def test_unverified_compensation_kills(self):
        d = assess(self.base(compensation_verified=False))
        self.assertEqual(d.verdict, Verdict.KILLED)

    def test_vague_paid_test_without_amount_kills(self):
        d = assess(
            self.base(pay_quote="A small paid test project may come first"),
            [],
        )
        self.assertEqual(d.verdict, Verdict.KILLED)
        self.assertTrue(any("no explicit monetary amount" in r for r in d.reasons))

    def test_explicit_pay_but_no_reviews_needs_evidence(self):
        d = assess(self.base(pay_quote="$200 for one workflow"), [])
        self.assertEqual(d.verdict, Verdict.EVIDENCE_REQUIRED)

    def test_one_pass_one_unknown_needs_evidence(self):
        d = assess(
            self.base(),
            [Review("Sable", "PASS"), Review("AVA", "UNKNOWN", "contact route not rechecked")],
        )
        self.assertEqual(d.verdict, Verdict.EVIDENCE_REQUIRED)

    def test_human_gate_is_exact_after_reviews(self):
        d = assess(
            self.base(human_gate="identity attestation on registration form"),
            [Review("Sable", "PASS"), Review("AVA", "PASS")],
        )
        self.assertEqual(d.verdict, Verdict.HUMAN_GATE)
        self.assertIn("identity attestation", d.next_action)

    def test_model_disagreement_requires_evidence(self):
        d = assess(
            self.base(),
            [Review("Sable", "PASS", "fresh buyer"), Review("Fuse", "KILL", "pay wording ambiguous")],
        )
        self.assertEqual(d.verdict, Verdict.EVIDENCE_REQUIRED)

    def test_existing_kill_stays_killed(self):
        d = assess(self.base(duplicate_status="killed"))
        self.assertEqual(d.verdict, Verdict.KILLED)

    def test_money_quote_patterns(self):
        self.assertTrue(has_explicit_pay_amount("$200 fixed"))
        self.assertTrue(has_explicit_pay_amount("EUR 350"))
        self.assertTrue(has_explicit_pay_amount("500 USD"))
        self.assertFalse(has_explicit_pay_amount("paid test may come first"))


if __name__ == "__main__":
    unittest.main()

import unittest

from joint.lead_gate import Candidate, Review, Verdict, assess


class LeadGateTests(unittest.TestCase):
    def base(self, **overrides):
        data = dict(
            source="https://example.com/post",
            buyer="Example Buyer",
            problem="Fix an AI automation workflow",
            age_hours=4,
            compensation_verified=True,
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

    def test_human_gate_is_exact(self):
        d = assess(self.base(human_gate="identity attestation on registration form"))
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


if __name__ == "__main__":
    unittest.main()

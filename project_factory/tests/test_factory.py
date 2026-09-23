import tempfile
import unittest
from pathlib import Path

from project_factory.judge_panel import Finding, summarize
from project_factory.opportunity_score import Opportunity, score
from project_factory.proof_vault import ProofRecord, append_record, load_records, verify_claim


class ProjectFactoryTests(unittest.TestCase):
    def test_ineligible_opportunity_scores_zero(self):
        op = Opportunity("Blocked", 1_000_000, 30, 10, 0, 0, 10, 10, 10, eligible=False)
        self.assertEqual(score(op), 0.0)

    def test_better_fit_scores_higher(self):
        strong = Opportunity("Strong", 100_000, 30, 9, 1, 0, 9, 9, 9)
        weak = Opportunity("Weak", 100_000, 30, 3, 8, 8, 2, 3, 2)
        self.assertGreater(score(strong), score(weak))

    def test_proof_vault_requires_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "vault.jsonl"
            append_record(p, ProofRecord(
                claim="MCP HTTP smoke test passed",
                state="VERIFIED",
                evidence_type="ci",
                evidence_ref="github-actions-run-123",
                project="Lead Rescue Voice",
                verifier="GitHub Actions",
            ))
            records = load_records(p)
            self.assertTrue(verify_claim(records, "MCP HTTP smoke test passed"))

    def test_panel_blocks_on_blocker(self):
        result = summarize([
            Finding("competition_judge", "low", 9, "Strong demo", "rubric check"),
            Finding("rules_auditor", "blocker", 9, "Missing required field", "submission form"),
        ])
        self.assertFalse(result["ready"])
        self.assertEqual(len(result["blockers"]), 1)


if __name__ == "__main__":
    unittest.main()

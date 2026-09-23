import unittest

from project_factory.release_loop import ReleaseCandidate, ReviewFinding, review_round


def finding(role: str, severity: str = "low", resolved: bool = False) -> ReviewFinding:
    return ReviewFinding(
        role=role,
        severity=severity,
        finding=f"{role} review finding",
        evidence=f"{role}-evidence",
        fix="fix it",
        resolved=resolved,
    )


class ReleaseLoopTests(unittest.TestCase):
    def test_candidate_not_ready_without_all_roles(self):
        candidate = ReleaseCandidate("Demo", "1")
        candidate.add_test_evidence("ci-run-1")
        candidate.add_proof_refs("proof-1")
        result = review_round(candidate, [finding("builder"), finding("tester")])
        self.assertFalse(result["ready"])
        self.assertIn("critic", result["missing_roles"])

    def test_high_finding_blocks_release(self):
        candidate = ReleaseCandidate("Demo", "2")
        candidate.add_test_evidence("ci-run-2")
        candidate.add_proof_refs("proof-2")
        findings = [
            finding("builder"),
            finding("tester", "high"),
            finding("critic"),
            finding("rules_auditor"),
            finding("user_reviewer"),
            finding("judge"),
        ]
        result = review_round(candidate, findings)
        self.assertFalse(result["ready"])
        self.assertEqual(len(result["unresolved_blockers"]), 1)

    def test_resolved_high_finding_does_not_block(self):
        candidate = ReleaseCandidate("Demo", "3")
        candidate.add_test_evidence("ci-run-3")
        candidate.add_proof_refs("proof-3")
        findings = [
            finding("builder"),
            finding("tester", "high", resolved=True),
            finding("critic"),
            finding("rules_auditor"),
            finding("user_reviewer"),
            finding("judge"),
        ]
        result = review_round(candidate, findings)
        self.assertTrue(result["ready"])

    def test_no_test_or_proof_evidence_blocks_release(self):
        candidate = ReleaseCandidate("Demo", "4")
        findings = [
            finding("builder"),
            finding("tester"),
            finding("critic"),
            finding("rules_auditor"),
            finding("user_reviewer"),
            finding("judge"),
        ]
        result = review_round(candidate, findings)
        self.assertFalse(result["ready"])
        self.assertIn("no test evidence", result["reasons"])
        self.assertIn("no proof-vault references", result["reasons"])


if __name__ == "__main__":
    unittest.main()

import unittest

from nebius_nighteye.benchmark import CASES, evaluate_analysis


class BenchmarkTests(unittest.TestCase):
    def test_case_ids_are_unique(self):
        ids = [case.id for case in CASES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_benchmark_includes_prompt_injection_case(self):
        case = next(case for case in CASES if case.id == "prompt-injection-evidence")
        self.assertIn("IGNORE ALL PREVIOUS INSTRUCTIONS", case.request.evidence[1].text)

    def test_perfect_structural_analysis_scores_one(self):
        case = CASES[0]
        analysis = {
            "material_change": True,
            "observations": [
                {"text": "Shipments moved later.", "evidence_ids": ["ev-002"]},
            ],
            "explanations": [
                {"name": "shortage", "support": ["ev-003"]},
                {"name": "scheduling", "support": ["ev-002"]},
            ],
            "falsifier": "Shipments return to original dates while shortage persists.",
            "unknowns": ["duration"],
            "next_actions": ["Confirm revised ETA before changing commitments."],
        }
        result = evaluate_analysis(case, analysis)
        self.assertEqual(result["score"], 1.0)
        self.assertEqual(result["unsupported_evidence_refs"], [])

    def test_unsupported_reference_is_caught(self):
        case = CASES[1]
        analysis = {
            "material_change": False,
            "observations": [
                {"text": "No primary-source recall notice.", "evidence_ids": ["ev-102", "ev-999"]},
            ],
            "explanations": [
                {"name": "rumor", "support": ["ev-101"]},
                {"name": "no-recall", "support": ["ev-102"]},
            ],
            "falsifier": "Manufacturer posts a recall notice.",
            "unknowns": [],
            "next_actions": ["Recheck manufacturer recall page."],
        }
        result = evaluate_analysis(case, analysis)
        self.assertFalse(result["checks"]["no_unsupported_evidence_refs"])
        self.assertEqual(result["unsupported_evidence_refs"], ["ev-999"])


if __name__ == "__main__":
    unittest.main()

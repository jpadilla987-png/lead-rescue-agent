import unittest

from project_factory.blind_protocol import FrozenTest, freeze
from project_factory.economics_split import ResearchClaim, classify
from project_factory.family_panel import PanelReport, RESEARCH_ROLES, panel_gate
from project_factory.prospective_evidence import ProspectiveResult, resolve
from project_factory.research_gate import Hypothesis, Variable, cutoff_gate, marginalization_plan


class ResearchFactoryTests(unittest.TestCase):
    def test_cutoff_gate_requires_observable_causal_variable(self):
        h = Hypothesis(
            name="Mechanism test",
            mechanism="state affects outcome distribution",
            target="future event",
            baseline="base rate",
            variables=(
                Variable("late_random_state", False, True, True, "source"),
            ),
            preregistered=True,
            holdout_defined=True,
            falsifier="no improvement over baseline",
        )
        result = cutoff_gate(h)
        self.assertFalse(result["testable"])
        self.assertIn("no observable-at-cutoff causal candidate", result["reasons"])

    def test_marginalization_separates_fixed_and_late_random_state(self):
        plan = marginalization_plan([
            Variable("known_state", True, False, True),
            Variable("future_random_state", False, True, True),
        ])
        self.assertEqual(plan["condition_on"], ["known_state"])
        self.assertEqual(plan["marginalize_over"], ["future_random_state"])

    def test_freeze_is_deterministic(self):
        test = FrozenTest(
            "H1", "binary outcome", "2026-09-22T20:00-07:00",
            "past", "future", "log loss", "base rate", "Holm", "100 outcomes",
        )
        self.assertEqual(freeze(test)["sha256"], freeze(test)["sha256"])

    def test_panel_requires_all_roles(self):
        reports = [PanelReport(role, "ok", "evidence") for role in RESEARCH_ROLES[:-1]]
        result = panel_gate(reports)
        self.assertFalse(result["ready_for_prospective_test"])

    def test_leakage_forces_failure(self):
        result = resolve(ProspectiveResult(
            n=50,
            primary_metric=0.9,
            baseline_metric=0.5,
            corrected_p_value=0.001,
            replicated=True,
            leakage_found=True,
            preregistration_hash="abc",
        ))
        self.assertEqual(result["status"], "FAILED")

    def test_unreplicated_result_stays_unknown(self):
        result = resolve(ProspectiveResult(
            n=50,
            primary_metric=0.9,
            baseline_metric=0.5,
            corrected_p_value=0.001,
            replicated=False,
            leakage_found=False,
            preregistration_hash="abc",
        ))
        self.assertEqual(result["status"], "UNKNOWN")

    def test_economics_is_not_prediction(self):
        result = classify(ResearchClaim(
            "conditional sharing effect",
            changes_outcome_probability=False,
            changes_conditional_payout=True,
            evidence_ref="proof-1",
        ))
        self.assertEqual(result["lane"], "economics_or_crowding")
        self.assertTrue(result["must_not_be_conflated_with_prediction"])


if __name__ == "__main__":
    unittest.main()

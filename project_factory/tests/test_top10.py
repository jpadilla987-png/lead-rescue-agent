import unittest
from datetime import date

from project_factory.commercial_reality import CommercialCase, evaluate
from project_factory.demo_factory import DemoBeat, build_demo_plan
from project_factory.evidence_graph import Edge, EvidenceGraph, Node
from project_factory.failure_memory import FailureMemory, FailureRule
from project_factory.judge_replay import VisiblePacket, freeze, replay_gate
from project_factory.kill_switch import ProjectSignals, decide
from project_factory.projects.amazon_lead_rescue import demo_180, packet
from project_factory.requirements_diff import RequirementSnapshot, diff_requirements
from project_factory.reuse_detector import Asset, classify
from project_factory.zero_to_entry import skeleton


class TopTenTests(unittest.TestCase):
    def test_submission_compiler_blocks_missing_video_and_feedback(self):
        result = packet()
        self.assertFalse(result.ready)
        self.assertIn("demo_video", result.missing_required)
        self.assertIn("product_feedback", result.missing_required)

    def test_amazon_demo_fits_three_minutes(self):
        plan = demo_180()
        self.assertLessEqual(plan["used_seconds"], 180)
        self.assertGreater(plan["buffer_seconds"], 0)

    def test_failure_memory_matches_tags(self):
        memory = FailureMemory()
        memory.add(FailureRule(
            "network-bind",
            "Unsafe default bind",
            ("mcp", "network"),
            "Server exposed all interfaces by default.",
            "Default to loopback; require explicit deployment host.",
            "Bandit B104 plus HTTP smoke test",
            "github-actions:35812494214",
        ))
        self.assertEqual(len(memory.applicable({"mcp"})), 1)
        self.assertEqual(len(memory.applicable({"biomedical"})), 0)

    def test_requirements_diff_detects_change(self):
        old = [RequirementSnapshot("video", "Video", True)]
        new = [RequirementSnapshot("video", "Demo Video", True)]
        result = diff_requirements(old, new)
        self.assertTrue(result["changed"])
        self.assertEqual(result["modified"][0]["key"], "video")

    def test_zero_to_entry_contains_release_assets(self):
        assets = skeleton("Demo", "Contest")
        self.assertIn("RELEASE_CHECKLIST.md", assets)
        self.assertIn("MONEY_FORK.md", assets)

    def test_commercial_case_needs_evidence(self):
        case = CommercialCase("HVAC owner", "Missed leads", "CRM", "$99/mo", "Direct outreach")
        self.assertFalse(evaluate(case)["credible"])

    def test_judge_replay_freezes_visible_packet(self):
        p = VisiblePacket("Demo", "Description", "repo", "demo", "video", ("ci:1",))
        self.assertTrue(replay_gate(p)["ready_for_blind_review"])
        self.assertEqual(len(freeze(p)["sha256"]), 64)

    def test_evidence_graph_links_claim_to_test(self):
        g = EvidenceGraph()
        g.add_node(Node("claim", "claim", "HTTP MCP works"))
        g.add_node(Node("ci", "evidence", "CI 123"))
        g.link(Edge("claim", "ci", "verified_by"))
        self.assertEqual(g.outgoing("claim")[0].id, "ci")

    def test_reuse_detector_requires_disclosure_for_old_asset(self):
        result = classify(
            Asset("old.py", date(2026, 8, 1), False),
            date(2026, 8, 31),
        )
        self.assertEqual(result["status"], "preexisting_requires_disclosure")

    def test_kill_switch_keeps_high_fit_project(self):
        result = decide(ProjectSignals(20, 2, 0, 9, 8, 70))
        self.assertEqual(result["decision"], "CONTINUE")


if __name__ == "__main__":
    unittest.main()

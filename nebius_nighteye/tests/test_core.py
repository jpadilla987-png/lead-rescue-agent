import json
import unittest

from nebius_nighteye.core import AnalysisRequest, EvidenceItem, build_messages, parse_analysis
from nebius_nighteye.nebius_client import analyze


class FakeBackend:
    model = "nvidia/nemotron-test"

    def complete(self, *, messages, model):
        return json.dumps({
            "material_change": True,
            "observations": [
                {"text": "Shipments moved later.", "evidence_ids": ["ev-2"]},
            ],
            "explanations": [
                {"name": "shortage", "support": ["ev-2"]},
                {"name": "scheduling", "support": ["ev-2"]},
            ],
            "falsifier": "Shipments return to the original date without supply changes.",
            "unknowns": ["duration"],
            "next_actions": ["Confirm revised ETA before changing commitments."],
        })


class NighteyeCoreTests(unittest.TestCase):
    def request(self):
        return AnalysisRequest(
            topic="supplier change",
            evidence=(
                EvidenceItem("ev-1", "status", "t1", "normal"),
                EvidenceItem("ev-2", "shipping", "t2", "shipment delayed"),
            ),
        )

    def test_messages_embed_only_supplied_evidence(self):
        messages = build_messages(self.request())
        payload = json.loads(messages[1]["content"])
        self.assertEqual(len(payload["evidence"]), 2)
        self.assertEqual(payload["evidence"][1]["id"], "ev-2")

    def test_parse_rejects_hallucinated_evidence_id(self):
        raw = json.dumps({
            "material_change": True,
            "observations": [{"text": "x", "evidence_ids": ["fake"]}],
            "explanations": [{}, {}],
            "falsifier": "x",
            "unknowns": [],
            "next_actions": [],
        })
        with self.assertRaises(ValueError):
            parse_analysis(raw, {"ev-1", "ev-2"})

    def test_fake_backend_end_to_end(self):
        result = analyze(self.request(), backend=FakeBackend())
        self.assertEqual(result["provider"], "Nebius Token Factory")
        self.assertTrue(result["analysis"]["material_change"])
        self.assertEqual(result["model"], "nvidia/nemotron-test")


if __name__ == "__main__":
    unittest.main()

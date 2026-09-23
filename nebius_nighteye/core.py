from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from typing import Iterable


@dataclass(frozen=True)
class EvidenceItem:
    id: str
    source: str
    observed_at: str
    text: str


@dataclass(frozen=True)
class AnalysisRequest:
    topic: str
    evidence: tuple[EvidenceItem, ...]


SYSTEM_PROMPT = """You are NIGHTEYE Evidence Engine, an evidence-first analysis agent.
Use only the supplied evidence. Separate observation from inference. Generate competing explanations.
Identify what would falsify the leading explanation. State explicit unknowns. Recommend only reversible
next actions unless the evidence clearly supports otherwise. Never invent sources, events, measurements,
or confidence. Return strict JSON with keys: material_change, observations, explanations, falsifier,
unknowns, next_actions. Each observation must include evidence_ids.
"""


def build_messages(req: AnalysisRequest) -> list[dict[str, str]]:
    if not req.topic.strip():
        raise ValueError("topic is required")
    if not req.evidence:
        raise ValueError("at least one evidence item is required")
    ids = [item.id for item in req.evidence]
    if len(ids) != len(set(ids)):
        raise ValueError("evidence ids must be unique")

    payload = {
        "topic": req.topic,
        "evidence": [asdict(item) for item in req.evidence],
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False, sort_keys=True)},
    ]


def parse_analysis(raw: str, allowed_evidence_ids: Iterable[str]) -> dict:
    data = json.loads(raw)
    required = {
        "material_change",
        "observations",
        "explanations",
        "falsifier",
        "unknowns",
        "next_actions",
    }
    missing = required.difference(data)
    if missing:
        raise ValueError(f"missing analysis keys: {sorted(missing)}")

    allowed = set(allowed_evidence_ids)
    if not isinstance(data["observations"], list):
        raise ValueError("observations must be a list")

    for obs in data["observations"]:
        if not isinstance(obs, dict):
            raise ValueError("each observation must be an object")
        refs = obs.get("evidence_ids")
        if not isinstance(refs, list) or not refs:
            raise ValueError("each observation must cite evidence_ids")
        unknown = set(refs).difference(allowed)
        if unknown:
            raise ValueError(f"hallucinated evidence ids: {sorted(unknown)}")

    if not isinstance(data["explanations"], list) or len(data["explanations"]) < 2:
        raise ValueError("at least two competing explanations are required")
    if not isinstance(data["unknowns"], list):
        raise ValueError("unknowns must be a list")
    if not isinstance(data["next_actions"], list):
        raise ValueError("next_actions must be a list")

    return data

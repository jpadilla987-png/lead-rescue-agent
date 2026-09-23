from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json


@dataclass(frozen=True)
class VisiblePacket:
    title: str
    description: str
    repo_url: str
    demo_url: str
    video_url: str
    evidence_refs: tuple[str, ...]


def freeze(packet: VisiblePacket) -> dict:
    payload = {
        "title": packet.title,
        "description": packet.description,
        "repo_url": packet.repo_url,
        "demo_url": packet.demo_url,
        "video_url": packet.video_url,
        "evidence_refs": list(packet.evidence_refs),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return {"sha256": digest, "packet": payload}


def replay_gate(packet: VisiblePacket) -> dict:
    missing = []
    for field in ("title", "description", "repo_url", "video_url"):
        if not getattr(packet, field).strip():
            missing.append(field)
    if not packet.evidence_refs:
        missing.append("evidence_refs")
    return {"ready_for_blind_review": not missing, "missing": missing}

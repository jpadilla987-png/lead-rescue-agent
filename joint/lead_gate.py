from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable


class Verdict(str, Enum):
    KILLED = "KILLED"
    SURVIVES = "SURVIVES"
    HUMAN_GATE = "HUMAN_GATE"
    EVIDENCE_REQUIRED = "EVIDENCE_REQUIRED"


@dataclass(frozen=True)
class Candidate:
    source: str
    buyer: str
    problem: str
    age_hours: float
    compensation_verified: bool
    direct_route_verified: bool
    cost_to_pursue_usd: float = 0.0
    fit_score: int = 0
    mandatory_live_video: bool = False
    unsupported_requirement: bool = False
    duplicate_status: str = "new"
    human_gate: str | None = None


@dataclass(frozen=True)
class Review:
    reviewer: str
    verdict: str
    reason: str = ""


@dataclass(frozen=True)
class Decision:
    verdict: Verdict
    reasons: list[str]
    next_action: str


def _normalize_review(v: str) -> str:
    v = v.strip().upper()
    if v not in {"PASS", "KILL", "UNKNOWN"}:
        raise ValueError(f"invalid review verdict: {v}")
    return v


def assess(candidate: Candidate, reviews: Iterable[Review] = ()) -> Decision:
    reasons: list[str] = []

    if candidate.age_hours > 48:
        reasons.append(f"stale: {candidate.age_hours:.1f}h old (>48h)")
    if not candidate.compensation_verified:
        reasons.append("compensation/payment path not verified")
    if not candidate.direct_route_verified:
        reasons.append("direct application/contact route not verified")
    if candidate.cost_to_pursue_usd > 0:
        reasons.append(f"requires $\{candidate.cost_to_pursue_usd:.2f} upfront")
    if candidate.fit_score < 4:
        reasons.append(f"fit score {candidate.fit_score}/5 below 4/5 gate")
    if candidate.mandatory_live_video:
        reasons.append("mandatory live/video process conflicts with current constraint")
    if candidate.unsupported_requirement:
        reasons.append("requires unsupported credentials/experience")
    if candidate.duplicate_status in {"already_contacted", "killed", "stale"}:
        reasons.append(f"duplicate/status gate: {candidate.duplicate_status}")

    if reasons:
        return Decision(
            verdict=Verdict.KILLED,
            reasons=reasons,
            next_action="Do not contact. Preserve kill reason and move on.",
        )

    normalized = [Review(r.reviewer, _normalize_review(r.verdict), r.reason) for r in reviews]
    review_votes = {r.verdict for r in normalized}

    if "KILL" in review_votes and "PASS" in review_votes:
        disagreements = [f"{r.reviewer}: {r.verdict} — {r.reason}" for r in normalized]
        return Decision(
            verdict=Verdict.EVIDENCE_REQUIRED,
            reasons=["independent reviewers disagree", *disagreements],
            next_action="Resolve the disputed fact with the smallest evidence check before outbound.",
        )

    if "KILL" in review_votes:
        kill_notes = [f"{r.reviewer}: {r.reason or 'kill'}" for r in normalized if r.verdict == "KILL"]
        return Decision(
            verdict=Verdict.KILLED,
            reasons=kill_notes,
            next_action="Do not contact unless new evidence overturns the kill.",
        )

    if candidate.human_gate:
        return Decision(
            verdict=Verdict.HUMAN_GATE,
            reasons=[candidate.human_gate],
            next_action=f"Ask Jose only for this exact gate: {candidate.human_gate}",
        )

    return Decision(
        verdict=Verdict.SURVIVES,
        reasons=["all hard gates passed"],
        next_action="AVA checks exact contact history, then executes at most one outbound action.",
    )


def load_packet(path: Path) -> tuple[Candidate, list[Review]]:
    data = json.loads(path.read_text())
    candidate = Candidate(**data["candidate"])
    reviews = [Review(**r) for r in data.get("reviews", [])]
    return candidate, reviews


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic Family lead gate")
    parser.add_argument("packet", type=Path, help="JSON file with candidate + optional reviews")
    args = parser.parse_args()

    candidate, reviews = load_packet(args.packet)
    decision = assess(candidate, reviews)
    print(json.dumps({"candidate": asdict(candidate), "decision": asdict(decision)}, indent=2, default=str))


if __name__ == "__main__":
    main()

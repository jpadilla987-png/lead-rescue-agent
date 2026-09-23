from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DemoBeat:
    label: str
    seconds: int
    action: str
    expected_proof: str
    fallback: str = ""


def build_demo_plan(
    opening: str,
    beats: list[DemoBeat],
    total_seconds: int = 180,
) -> dict:
    if total_seconds not in {90, 180}:
        raise ValueError("supported demo lengths are 90 or 180 seconds")
    if not opening.strip():
        raise ValueError("opening is required")
    if not beats:
        raise ValueError("at least one demo beat is required")

    used = sum(max(0, beat.seconds) for beat in beats)
    if used > total_seconds:
        raise ValueError("demo beats exceed time budget")

    timeline = []
    cursor = 0
    for beat in beats:
        start = cursor
        cursor += beat.seconds
        timeline.append({
            "start": start,
            "end": cursor,
            "label": beat.label,
            "action": beat.action,
            "expected_proof": beat.expected_proof,
            "fallback": beat.fallback,
        })

    return {
        "opening": opening,
        "total_seconds": total_seconds,
        "used_seconds": used,
        "buffer_seconds": total_seconds - used,
        "timeline": timeline,
    }

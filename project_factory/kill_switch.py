from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectSignals:
    days_left: int
    human_hours_remaining: float
    external_blocker_days: int
    judging_fit: int
    commercial_value: int
    completion_percent: int
    hard_eligibility_block: bool = False


def decide(signals: ProjectSignals) -> dict:
    reasons: list[str] = []

    if signals.hard_eligibility_block:
        return {"decision": "KILL", "reasons": ["hard eligibility block"]}

    if signals.days_left <= 0:
        return {"decision": "KILL", "reasons": ["deadline passed"]}

    if signals.external_blocker_days >= signals.days_left:
        reasons.append("external blocker consumes remaining runway")

    if signals.human_hours_remaining > 12 and signals.completion_percent < 50:
        reasons.append("too much human-only work remains")

    if signals.judging_fit <= 3 and signals.commercial_value <= 3:
        reasons.append("low judging fit and low commercial value")

    if reasons:
        return {"decision": "PAUSE_OR_KILL", "reasons": reasons}

    return {"decision": "CONTINUE", "reasons": []}

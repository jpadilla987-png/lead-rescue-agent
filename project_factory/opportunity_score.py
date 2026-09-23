from __future__ import annotations

from dataclasses import dataclass
from math import log10


@dataclass(frozen=True)
class Opportunity:
    name: str
    prize_usd: float
    days_left: int
    ai_doability: int
    external_friction: int
    hardware_dependency: int
    reuse_score: int
    judging_fit: int
    commercial_value: int
    eligible: bool = True


def _bounded(value: float, low: float = 0, high: float = 10) -> float:
    return max(low, min(high, value))


def score(op: Opportunity) -> float:
    """Return a 0-100 prioritization score. Higher is better."""
    if not op.eligible:
        return 0.0

    prize_component = _bounded((log10(max(op.prize_usd, 1)) - 3) * 3.3)
    runway_component = _bounded(op.days_left / 6)
    doability = _bounded(op.ai_doability)
    friction = 10 - _bounded(op.external_friction)
    hardware = 10 - _bounded(op.hardware_dependency)
    reuse = _bounded(op.reuse_score)
    fit = _bounded(op.judging_fit)
    commercial = _bounded(op.commercial_value)

    weighted = (
        prize_component * 0.16
        + runway_component * 0.10
        + doability * 0.20
        + friction * 0.12
        + hardware * 0.08
        + reuse * 0.12
        + fit * 0.12
        + commercial * 0.10
    )
    return round(weighted * 10, 1)

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class ProspectiveResult:
    n: int
    primary_metric: float
    baseline_metric: float
    corrected_p_value: float | None
    replicated: bool
    leakage_found: bool
    preregistration_hash: str


def resolve(result: ProspectiveResult) -> dict:
    if result.n <= 0:
        return {"status": "UNKNOWN", "reason": "no prospective observations"}
    if not result.preregistration_hash.strip():
        return {"status": "UNKNOWN", "reason": "missing preregistration proof"}
    if result.leakage_found:
        return {"status": "FAILED", "reason": "information leakage invalidated the test"}
    if not isfinite(result.primary_metric) or not isfinite(result.baseline_metric):
        return {"status": "UNKNOWN", "reason": "non-finite metric"}
    if result.corrected_p_value is None:
        return {"status": "UNKNOWN", "reason": "multiple-testing correction not resolved"}

    better = result.primary_metric > result.baseline_metric
    significant = result.corrected_p_value < 0.05

    if better and significant and result.replicated:
        return {"status": "VERIFIED", "reason": "prospective replicated improvement over frozen baseline"}
    if not better or not significant:
        return {"status": "FAILED", "reason": "did not beat frozen baseline after correction"}
    return {"status": "UNKNOWN", "reason": "promising but not replicated"}

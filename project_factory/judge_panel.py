from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable


ROLES = {
    "competition_judge": "Does the demonstrated product satisfy the actual rubric and submission requirements?",
    "adversarial_tester": "What breaks, fails closed, misleads, or behaves badly under edge cases?",
    "code_reviewer": "Is the implementation coherent, reproducible, maintainable, and supported by tests?",
    "rules_auditor": "Are any claims, assets, dates, eligibility assumptions, or submission fields inconsistent with the official rules?",
    "user_reviewer": "Would a real user understand the value and successfully use the product?",
    "competitive_reviewer": "What would make a competing entry clearly stronger than this one?",
}


@dataclass(frozen=True)
class Finding:
    role: str
    severity: str
    score: float
    finding: str
    evidence: str
    fix: str = ""


def summarize(findings: Iterable[Finding]) -> dict:
    items = list(findings)
    if not items:
        return {"ready": False, "reason": "no review evidence", "average_score": 0.0, "blockers": []}

    blockers = [f for f in items if f.severity.lower() == "blocker"]
    avg = round(mean(max(0.0, min(10.0, f.score)) for f in items), 2)
    return {
        "ready": not blockers and avg >= 8.0,
        "average_score": avg,
        "blockers": [f.finding for f in blockers],
        "review_count": len(items),
    }

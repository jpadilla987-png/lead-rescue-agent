from __future__ import annotations

from dataclasses import dataclass


RESEARCH_ROLES = (
    "finder",
    "independent_researcher",
    "falsifier",
    "detectability_engineer",
    "blind_evaluator",
    "auditor",
)


@dataclass(frozen=True)
class PanelReport:
    role: str
    conclusion: str
    evidence: str
    blocker: bool = False


def panel_gate(reports: list[PanelReport]) -> dict:
    seen = {r.role for r in reports}
    missing = [role for role in RESEARCH_ROLES if role not in seen]
    blockers = [r for r in reports if r.blocker]
    return {
        "ready_for_prospective_test": not missing and not blockers,
        "missing_roles": missing,
        "blockers": [
            {"role": r.role, "conclusion": r.conclusion, "evidence": r.evidence}
            for r in blockers
        ],
    }

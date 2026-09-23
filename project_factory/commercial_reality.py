from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommercialCase:
    payer: str
    costly_problem: str
    current_alternative: str
    proposed_price: str
    acquisition_path: str
    evidence_refs: tuple[str, ...] = ()


def evaluate(case: CommercialCase) -> dict:
    fields = {
        "payer": case.payer,
        "costly_problem": case.costly_problem,
        "current_alternative": case.current_alternative,
        "proposed_price": case.proposed_price,
        "acquisition_path": case.acquisition_path,
    }
    missing = [name for name, value in fields.items() if not value.strip()]
    return {
        "credible": not missing and bool(case.evidence_refs),
        "missing": missing,
        "evidence_count": len(case.evidence_refs),
    }

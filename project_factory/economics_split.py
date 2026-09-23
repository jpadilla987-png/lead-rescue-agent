from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResearchClaim:
    name: str
    changes_outcome_probability: bool
    changes_conditional_payout: bool
    evidence_ref: str


def classify(claim: ResearchClaim) -> dict:
    if not claim.evidence_ref.strip():
        raise ValueError("evidence_ref is required")

    if claim.changes_outcome_probability:
        lane = "prediction_edge"
    elif claim.changes_conditional_payout:
        lane = "economics_or_crowding"
    else:
        lane = "non_actionable"

    return {
        "lane": lane,
        "must_not_be_conflated_with_prediction": lane == "economics_or_crowding",
    }

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


TERMINAL_STATES = {"VERIFIED", "FAILED", "UNKNOWN"}


@dataclass(frozen=True)
class Variable:
    name: str
    observable_at_cutoff: bool
    randomized_after_cutoff: bool
    causal_candidate: bool
    source_ref: str = ""


@dataclass(frozen=True)
class Hypothesis:
    name: str
    mechanism: str
    target: str
    baseline: str
    variables: tuple[Variable, ...]
    preregistered: bool
    holdout_defined: bool
    falsifier: str
    status: str = "UNKNOWN"

    def validate(self) -> None:
        if self.status not in TERMINAL_STATES:
            raise ValueError("status must be VERIFIED, FAILED, or UNKNOWN")
        if not self.name.strip() or not self.mechanism.strip() or not self.target.strip():
            raise ValueError("name, mechanism, and target are required")
        if not self.baseline.strip():
            raise ValueError("baseline is required")
        if not self.falsifier.strip():
            raise ValueError("falsifier is required")


def cutoff_gate(h: Hypothesis) -> dict:
    h.validate()
    observable = [v for v in h.variables if v.observable_at_cutoff]
    causal_observable = [v for v in observable if v.causal_candidate]
    randomized_later = [v for v in h.variables if v.randomized_after_cutoff]

    reasons: list[str] = []
    if not h.preregistered:
        reasons.append("hypothesis not preregistered")
    if not h.holdout_defined:
        reasons.append("chronological holdout not defined")
    if not causal_observable:
        reasons.append("no observable-at-cutoff causal candidate")
    if all(v.randomized_after_cutoff for v in h.variables):
        reasons.append("all candidate state is randomized after cutoff")

    return {
        "testable": not reasons,
        "reasons": reasons,
        "observable_variables": [v.name for v in observable],
        "causal_observable_variables": [v.name for v in causal_observable],
        "randomized_after_cutoff": [v.name for v in randomized_later],
    }


def marginalization_plan(variables: Iterable[Variable]) -> dict:
    fixed = [v.name for v in variables if v.observable_at_cutoff and not v.randomized_after_cutoff]
    latent = [v.name for v in variables if not v.observable_at_cutoff or v.randomized_after_cutoff]
    return {
        "condition_on": fixed,
        "marginalize_over": latent,
        "question": "Does any predictive advantage survive after averaging over state unavailable at decision cutoff?",
    }

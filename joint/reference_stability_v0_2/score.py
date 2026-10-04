"""NIGHTEYE Reference Stability Certificate v0.2 frozen scorer.

Public-data benchmarkability research only.
Protocol: joint/reference_stability_v0_2/FROZEN_PROTOCOL.md
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Iterable

FORBIDDEN_TOKENS = (
    "cmrg_included",
    "cmrg_excluded",
    "benchmark_status",
    "benchmark_included",
    "benchmark_excluded",
    "v5q_coverage",
    "v5_coverage",
    "manual_curation",
    "truth_label",
    "outcome",
    "target",
    "false_positive",
    "false_negative",
    "precision",
    "recall",
    "f1",
)

HIGH_RISK_THRESHOLD = 5
REFERENCE_SENSITIVE_DELTA = 0.10
SEVERE_DELTA = 0.25


@dataclass(frozen=True)
class LocusFeatures:
    gene: str
    segdup_fraction: float = 0.0
    lowmap_fraction: float = 0.0
    high_identity_paralog: bool = False
    structural_variability: bool = False
    confirmed_copy_mismatch: bool = False
    reference_representation_discordance: bool = False
    predictor_source_versions: tuple[str, ...] = ()


def _fraction(x: float) -> float:
    if not 0.0 <= x <= 1.0:
        raise ValueError("fraction must be in [0, 1]")
    return x


def leakage_guard(columns: Iterable[str]) -> None:
    for raw in columns:
        name = raw.strip().lower()
        if any(token in name for token in FORBIDDEN_TOKENS):
            raise ValueError(f"Outcome-like predictor column rejected: {raw}")


def validate_predictor_row(row: Mapping[str, object]) -> None:
    leakage_guard(row.keys())


def score(features: LocusFeatures) -> int:
    seg = _fraction(features.segdup_fraction)
    low = _fraction(features.lowmap_fraction)

    seg_score = 2 if seg >= 0.20 else (1 if seg > 0 else 0)

    if low >= 0.20 or features.high_identity_paralog:
        low_score = 2
    elif low > 0:
        low_score = 1
    else:
        low_score = 0

    if features.confirmed_copy_mismatch:
        cn_score = 2
    elif features.structural_variability:
        cn_score = 1
    else:
        cn_score = 0

    ref_score = int(features.reference_representation_discordance)
    total = seg_score + low_score + cn_score + ref_score
    if not 0 <= total <= 7:
        raise AssertionError("SIS-P2 score outside frozen 0-7 range")
    return total


def high_risk(features: LocusFeatures) -> bool:
    return score(features) >= HIGH_RISK_THRESHOLD


def reference_sensitive(grch38_coverage: float, chm13_coverage: float) -> bool:
    a = _fraction(grch38_coverage)
    b = _fraction(chm13_coverage)
    return abs(a - b) >= REFERENCE_SENSITIVE_DELTA


def severe_reference_sensitive(grch38_coverage: float, chm13_coverage: float) -> bool:
    a = _fraction(grch38_coverage)
    b = _fraction(chm13_coverage)
    return abs(a - b) >= SEVERE_DELTA

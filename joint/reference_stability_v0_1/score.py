"""NIGHTEYE Reference Stability Certificate v0.1 frozen scorer.

Public-data research tool only. No personal genomics or clinical inference.
Frozen protocol: joint/reference_stability_v0_1/FROZEN_PROTOCOL.md
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Iterable


SALT = "NIGHTEYE-RSC-v0.1-2026-09-27"


@dataclass(frozen=True)
class LocusFeatures:
    gene: str
    segdup_fraction: float = 0.0
    lowmap_fraction: float = 0.0
    high_identity_paralog: bool = False
    structural_variability: bool = False
    confirmed_copy_mismatch: bool = False
    reference_representation_discordance: bool = False


def holdout_gene(gene: str) -> bool:
    payload = f"{SALT}|{gene.upper()}".encode("utf-8")
    return hashlib.sha256(payload).digest()[0] < 64


def _bounded_fraction(x: float) -> float:
    if not 0.0 <= x <= 1.0:
        raise ValueError("fraction features must be in [0,1]")
    return x


def score(features: LocusFeatures) -> int:
    seg = _bounded_fraction(features.segdup_fraction)
    low = _bounded_fraction(features.lowmap_fraction)

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

    ref_score = 1 if features.reference_representation_discordance else 0

    total = seg_score + low_score + cn_score + ref_score
    if not 0 <= total <= 7:
        raise AssertionError("SIS-P out of range")
    return total


def high_risk(features: LocusFeatures) -> bool:
    return score(features) >= 5


def split_counts(genes: Iterable[str]) -> tuple[int, int]:
    dev = holdout = 0
    for gene in genes:
        if holdout_gene(gene):
            holdout += 1
        else:
            dev += 1
    return dev, holdout

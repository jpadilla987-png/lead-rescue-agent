from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json


@dataclass(frozen=True)
class FrozenTest:
    hypothesis: str
    outcome_definition: str
    evidence_cutoff: str
    training_window: str
    holdout_window: str
    metric: str
    baseline: str
    correction_method: str
    stop_rule: str


def freeze(test: FrozenTest) -> dict:
    payload = asdict(test)
    for key, value in payload.items():
        if not str(value).strip():
            raise ValueError(f"{key} is required")
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return {
        "sha256": sha256(canonical.encode("utf-8")).hexdigest(),
        "frozen": payload,
    }

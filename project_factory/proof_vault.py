from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Iterable


ALLOWED_STATES = {"FOUND", "VERIFIED", "STARTED", "SUBMITTED", "ACCEPTED", "FUNDED", "COMPLETED", "PAID"}


@dataclass(frozen=True)
class ProofRecord:
    claim: str
    state: str
    evidence_type: str
    evidence_ref: str
    project: str
    verifier: str
    note: str = ""
    created_at: str = ""

    def normalized(self) -> "ProofRecord":
        if self.state not in ALLOWED_STATES:
            raise ValueError(f"Unsupported state: {self.state}")
        if not self.claim.strip():
            raise ValueError("claim is required")
        if not self.evidence_ref.strip():
            raise ValueError("evidence_ref is required")
        stamp = self.created_at or datetime.now(timezone.utc).isoformat()
        return ProofRecord(
            claim=self.claim.strip(),
            state=self.state,
            evidence_type=self.evidence_type.strip(),
            evidence_ref=self.evidence_ref.strip(),
            project=self.project.strip(),
            verifier=self.verifier.strip(),
            note=self.note.strip(),
            created_at=stamp,
        )


def append_record(path: str | Path, record: ProofRecord) -> None:
    item = record.normalized()
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(item), sort_keys=True) + "\n")


def load_records(path: str | Path) -> list[ProofRecord]:
    p = Path(path)
    if not p.exists():
        return []
    records: list[ProofRecord] = []
    with p.open("r", encoding="utf-8") as fh:
        for raw in fh:
            if raw.strip():
                records.append(ProofRecord(**json.loads(raw)))
    return records


def verify_claim(records: Iterable[ProofRecord], claim: str, minimum_state: str = "VERIFIED") -> bool:
    rank = ["FOUND", "STARTED", "VERIFIED", "SUBMITTED", "ACCEPTED", "FUNDED", "COMPLETED", "PAID"]
    if minimum_state not in rank:
        raise ValueError("unknown minimum_state")
    floor = rank.index(minimum_state)
    return any(r.claim == claim and r.state in rank and rank.index(r.state) >= floor and bool(r.evidence_ref) for r in records)

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class FailureRule:
    id: str
    title: str
    trigger_tags: tuple[str, ...]
    failure: str
    prevention: str
    regression_test: str
    evidence_ref: str

    def validate(self) -> None:
        if not self.id.strip():
            raise ValueError("id is required")
        if not self.trigger_tags:
            raise ValueError("trigger_tags are required")
        if not self.regression_test.strip():
            raise ValueError("regression_test is required")


class FailureMemory:
    def __init__(self, rules: list[FailureRule] | None = None) -> None:
        self.rules = list(rules or [])

    def add(self, rule: FailureRule) -> None:
        rule.validate()
        if any(existing.id == rule.id for existing in self.rules):
            raise ValueError(f"duplicate failure rule: {rule.id}")
        self.rules.append(rule)

    def applicable(self, tags: set[str]) -> list[FailureRule]:
        return [
            rule
            for rule in self.rules
            if set(rule.trigger_tags).intersection(tags)
        ]

    def save(self, path: str | Path) -> None:
        payload = [asdict(rule) for rule in self.rules]
        Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "FailureMemory":
        p = Path(path)
        if not p.exists():
            return cls()
        raw = json.loads(p.read_text(encoding="utf-8"))
        return cls([FailureRule(**item) for item in raw])

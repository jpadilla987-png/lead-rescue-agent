from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class EqualFieldRule:
    left: str
    right: str
    name: str = "field_equality"


def _get_path(item: dict[str, Any], path: str) -> tuple[bool, Any]:
    cur: Any = item
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False, None
        cur = cur[part]
    return True, cur


def check_equal_fields(
    items: Iterable[dict[str, Any]],
    rules: Iterable[EqualFieldRule],
) -> list[dict[str, Any]]:
    """Enforce explicit relational invariants inside one execution result.

    This intentionally does not infer meaning. It checks contracts such as
    request.id == result.id that a history/shape monitor cannot infer.
    """
    violations: list[dict[str, Any]] = []
    rows = list(items)

    for idx, item in enumerate(rows):
        for rule in rules:
            left_ok, left_value = _get_path(item, rule.left)
            right_ok, right_value = _get_path(item, rule.right)

            if not left_ok or not right_ok:
                violations.append({
                    "kind": "contract_unverifiable",
                    "rule": rule.name,
                    "row": idx,
                    "left": rule.left,
                    "right": rule.right,
                    "missing": [
                        path
                        for path, ok in ((rule.left, left_ok), (rule.right, right_ok))
                        if not ok
                    ],
                })
                continue

            if left_value != right_value:
                violations.append({
                    "kind": "contract_mismatch",
                    "rule": rule.name,
                    "row": idx,
                    "left": rule.left,
                    "right": rule.right,
                    "left_value": left_value,
                    "right_value": right_value,
                })

    return violations

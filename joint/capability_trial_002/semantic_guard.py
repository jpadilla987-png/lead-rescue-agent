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


def _normalize_identity(value: Any) -> tuple[bool, str | None]:
    """Normalize identifier-like values without Python's bool/int equality trap.

    Returns (valid, normalized). Null is invalid. Booleans are kept distinct from
    numbers. Numbers and strings are compared by their textual representation so
    42 and "42" can match, while True and 1 cannot.
    """
    if value is None:
        return False, None
    if isinstance(value, bool):
        return True, f"bool:{str(value).lower()}"
    if isinstance(value, (int, float)):
        return True, f"num:{value}"
    if isinstance(value, str):
        stripped = value.strip()
        if stripped == "":
            return False, None
        # Numeric-looking strings compare to numbers by canonical text.
        try:
            num = float(stripped)
            if num.is_integer():
                return True, f"num:{int(num)}"
            return True, f"num:{num}"
        except ValueError:
            return True, f"str:{stripped}"
    return True, f"{type(value).__name__}:{value}"


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
    rules = list(rules)

    if rules and not rows:
        return [{
            "kind": "contract_unverifiable",
            "rule": "*",
            "row": None,
            "missing": ["execution output"],
            "detail": "rule configured but execution returned zero rows",
        }]

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

            left_valid, left_norm = _normalize_identity(left_value)
            right_valid, right_norm = _normalize_identity(right_value)

            if not left_valid or not right_valid:
                violations.append({
                    "kind": "contract_unverifiable",
                    "rule": rule.name,
                    "row": idx,
                    "left": rule.left,
                    "right": rule.right,
                    "missing": [
                        path
                        for path, valid in ((rule.left, left_valid), (rule.right, right_valid))
                        if not valid
                    ],
                    "detail": "null or empty contract value cannot prove equality",
                })
                continue

            if left_norm != right_norm:
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

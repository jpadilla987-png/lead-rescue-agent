from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RequirementSnapshot:
    key: str
    label: str
    required: bool
    options: tuple[str, ...] = ()
    description: str = ""


def diff_requirements(
    old: list[RequirementSnapshot],
    new: list[RequirementSnapshot],
) -> dict:
    before = {item.key: item for item in old}
    after = {item.key: item for item in new}

    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed: list[dict] = []

    for key in sorted(set(before).intersection(after)):
        a, b = before[key], after[key]
        fields = {}
        for name in ("label", "required", "options", "description"):
            old_value = getattr(a, name)
            new_value = getattr(b, name)
            if old_value != new_value:
                fields[name] = {"old": old_value, "new": new_value}
        if fields:
            changed.append({"key": key, "changes": fields})

    return {
        "changed": bool(added or removed or changed),
        "added": added,
        "removed": removed,
        "modified": changed,
    }

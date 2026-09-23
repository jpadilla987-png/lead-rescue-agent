from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Asset:
    path: str
    created_on: date
    materially_changed: bool
    change_note: str = ""


def classify(asset: Asset, submission_start: date) -> dict:
    preexisting = asset.created_on < submission_start
    if not preexisting:
        status = "new"
    elif asset.materially_changed and asset.change_note.strip():
        status = "preexisting_significantly_updated"
    else:
        status = "preexisting_requires_disclosure"

    return {
        "path": asset.path,
        "status": status,
        "disclosure_required": preexisting,
        "change_note": asset.change_note,
    }

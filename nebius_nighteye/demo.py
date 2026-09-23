from __future__ import annotations

import json

from .core import AnalysisRequest, EvidenceItem
from .nebius_client import analyze


DEMO = AnalysisRequest(
    topic="Has the monitored supplier situation materially changed?",
    evidence=(
        EvidenceItem(
            id="ev-001",
            source="supplier-status",
            observed_at="2026-09-22T08:00:00Z",
            text="Supplier status page reports normal operations.",
        ),
        EvidenceItem(
            id="ev-002",
            source="shipping-update",
            observed_at="2026-09-22T14:10:00Z",
            text="Two scheduled shipments moved from Tuesday to Friday.",
        ),
        EvidenceItem(
            id="ev-003",
            source="account-manager-note",
            observed_at="2026-09-22T15:05:00Z",
            text="Account manager says a temporary component shortage is affecting new outbound orders.",
        ),
    ),
)


def main() -> None:
    print(json.dumps(analyze(DEMO), indent=2))


if __name__ == "__main__":
    main()

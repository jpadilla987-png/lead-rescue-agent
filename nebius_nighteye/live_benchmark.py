from __future__ import annotations

import json
from statistics import mean

from .benchmark import CASES, evaluate_analysis
from .nebius_client import analyze


def main() -> None:
    rows = []
    for case in CASES:
        result = analyze(case.request)
        row = evaluate_analysis(case, result["analysis"])
        row["model"] = result["model"]
        row["provider"] = result["provider"]
        rows.append(row)

    report = {
        "case_count": len(rows),
        "average_structural_score": round(mean(row["score"] for row in rows), 3),
        "model": rows[0]["model"] if rows else None,
        "provider": rows[0]["provider"] if rows else None,
        "cases": rows,
    }

    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

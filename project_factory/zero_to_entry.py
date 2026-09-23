from __future__ import annotations


def skeleton(project_name: str, competition: str) -> dict[str, str]:
    if not project_name.strip() or not competition.strip():
        raise ValueError("project_name and competition are required")

    readme = f"""# {project_name}

Competition: {competition}

## Problem

TODO

## Solution

TODO

## Run

TODO

## Test

TODO

## Evidence

See PROOF.md.

## Disclosure

Document all pre-existing code and all work created during the submission window.
"""

    return {
        "README.md": readme,
        "LICENSE": "Choose an OSI-approved license before public submission.\n",
        "PROOF.md": "# Proof Vault\n\nNo claims verified yet.\n",
        "RELEASE_CHECKLIST.md": (
            "# Release Checklist\n\n"
            "- [ ] Requirements snapshot current\n"
            "- [ ] Functional tests pass\n"
            "- [ ] Adversarial tests pass\n"
            "- [ ] Security review passes\n"
            "- [ ] Six-role review complete\n"
            "- [ ] Demo evidence captured\n"
            "- [ ] Submission compiler reports READY\n"
            "- [ ] Significant-update disclosure accurate\n"
        ),
        "MONEY_FORK.md": (
            "# Commercial Fork\n\n"
            "Payer:\n\nPain with measurable cost:\n\nCurrent alternative:\n\n"
            "Proposed price:\n\nFirst 10 customer path:\n"
        ),
    }

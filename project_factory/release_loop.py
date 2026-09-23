from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

REQUIRED_ROLES = (
    "builder",
    "tester",
    "critic",
    "rules_auditor",
    "user_reviewer",
    "judge",
)

BLOCKING_SEVERITIES = {"blocker", "high"}


@dataclass(frozen=True)
class ReviewFinding:
    role: str
    severity: str
    finding: str
    evidence: str
    fix: str = ""
    resolved: bool = False

    def validate(self) -> None:
        if self.role not in REQUIRED_ROLES:
            raise ValueError(f"unknown role: {self.role}")
        if self.severity not in {"blocker", "high", "medium", "low", "info"}:
            raise ValueError(f"unknown severity: {self.severity}")
        if not self.finding.strip():
            raise ValueError("finding is required")
        if not self.evidence.strip():
            raise ValueError("evidence is required")


@dataclass
class ReleaseCandidate:
    project: str
    version: str
    findings: list[ReviewFinding] = field(default_factory=list)
    test_evidence: list[str] = field(default_factory=list)
    proof_refs: list[str] = field(default_factory=list)

    def add_findings(self, findings: Iterable[ReviewFinding]) -> None:
        for finding in findings:
            finding.validate()
            self.findings.append(finding)

    def add_test_evidence(self, *refs: str) -> None:
        self.test_evidence.extend(ref.strip() for ref in refs if ref.strip())

    def add_proof_refs(self, *refs: str) -> None:
        self.proof_refs.extend(ref.strip() for ref in refs if ref.strip())

    def role_coverage(self) -> dict[str, bool]:
        covered = {role: False for role in REQUIRED_ROLES}
        for item in self.findings:
            covered[item.role] = True
        return covered

    def unresolved_blockers(self) -> list[ReviewFinding]:
        return [
            item
            for item in self.findings
            if item.severity in BLOCKING_SEVERITIES and not item.resolved
        ]

    def release_gate(self) -> dict:
        coverage = self.role_coverage()
        missing_roles = [role for role, present in coverage.items() if not present]
        blockers = self.unresolved_blockers()

        reasons: list[str] = []
        if missing_roles:
            reasons.append("missing reviewer roles: " + ", ".join(missing_roles))
        if blockers:
            reasons.append(f"{len(blockers)} unresolved blocker/high finding(s)")
        if not self.test_evidence:
            reasons.append("no test evidence")
        if not self.proof_refs:
            reasons.append("no proof-vault references")

        return {
            "project": self.project,
            "version": self.version,
            "ready": not reasons,
            "missing_roles": missing_roles,
            "unresolved_blockers": [
                {
                    "role": item.role,
                    "severity": item.severity,
                    "finding": item.finding,
                    "evidence": item.evidence,
                }
                for item in blockers
            ],
            "test_evidence_count": len(self.test_evidence),
            "proof_ref_count": len(self.proof_refs),
            "reasons": reasons,
        }


def review_round(candidate: ReleaseCandidate, findings: Iterable[ReviewFinding]) -> dict:
    """Apply one Builder->Tester->Critic->Auditor->User->Judge review round and return the gate."""
    candidate.add_findings(findings)
    return candidate.release_gate()

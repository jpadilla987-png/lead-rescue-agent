from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class Requirement:
    key: str
    label: str
    required: bool = True
    evidence_refs: tuple[str, ...] = ()
    answer: str = ""

    @property
    def satisfied(self) -> bool:
        if not self.required:
            return True
        return bool(self.answer.strip()) and bool(self.evidence_refs)


@dataclass(frozen=True)
class SubmissionContext:
    project: str
    track: str
    one_liner: str
    problem: str
    solution: str
    architecture: tuple[str, ...]
    requirements: tuple[Requirement, ...]
    product_feedback: tuple[str, ...] = ()
    disclosure: str = ""
    repo_url: str = ""
    demo_url: str = ""
    video_url: str = ""


@dataclass(frozen=True)
class SubmissionPacket:
    ready: bool
    markdown: str
    missing_required: tuple[str, ...]
    evidence_count: int
    claim_count: int


def compile_submission(ctx: SubmissionContext) -> SubmissionPacket:
    missing = tuple(req.key for req in ctx.requirements if req.required and not req.satisfied)
    evidence_count = sum(len(req.evidence_refs) for req in ctx.requirements)
    claim_count = sum(1 for req in ctx.requirements if req.answer.strip())

    lines = [
        f"# {ctx.project}",
        "",
        f"**Track:** {ctx.track}",
        "",
        f"**One-line value:** {ctx.one_liner}",
        "",
        "## Problem",
        ctx.problem,
        "",
        "## Solution",
        ctx.solution,
        "",
        "## Architecture",
    ]
    lines.extend(f"- {item}" for item in ctx.architecture)

    lines.extend(["", "## Requirement evidence matrix"])
    for req in ctx.requirements:
        status = "PASS" if req.satisfied else ("OPTIONAL" if not req.required else "MISSING")
        refs = ", ".join(req.evidence_refs) if req.evidence_refs else "none"
        answer = req.answer.strip() or "not supplied"
        lines.extend([
            f"### {req.label} — {status}",
            answer,
            f"Evidence: {refs}",
            "",
        ])

    if ctx.product_feedback:
        lines.append("## Product feedback")
        lines.extend(f"- {item}" for item in ctx.product_feedback)
        lines.append("")

    if ctx.disclosure:
        lines.extend(["## Significant-update disclosure", ctx.disclosure, ""])

    lines.extend([
        "## Links",
        f"- Repository: {ctx.repo_url or 'MISSING'}",
        f"- Working demo: {ctx.demo_url or 'MISSING'}",
        f"- Demo video: {ctx.video_url or 'MISSING'}",
        "",
        "## Release status",
        "READY" if not missing else "NOT READY",
    ])

    return SubmissionPacket(
        ready=not missing,
        markdown="\n".join(lines).strip() + "\n",
        missing_required=missing,
        evidence_count=evidence_count,
        claim_count=claim_count,
    )


def missing_evidence(requirements: Iterable[Requirement]) -> tuple[str, ...]:
    return tuple(
        req.key
        for req in requirements
        if req.required and (not req.answer.strip() or not req.evidence_refs)
    )

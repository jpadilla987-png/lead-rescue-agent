from __future__ import annotations

from project_factory.demo_factory import DemoBeat, build_demo_plan
from project_factory.submission_compiler import Requirement, SubmissionContext, compile_submission


def context() -> SubmissionContext:
    requirements = (
        Requirement(
            key="working_mcp",
            label="Working Alexa+ MCP implementation",
            answer="Self-hosted MCP server using Streamable HTTP with lead-priority, inspection, and guarded follow-up tools.",
            evidence_refs=(
                "github-actions:35812772639",
                "repo:amazon_alexa/server.py",
            ),
        ),
        Requirement(
            key="public_repo",
            label="Public code repository with license and setup instructions",
            answer="Public GitHub repository, MIT licensed, with Amazon-specific README and reproducible commands.",
            evidence_refs=(
                "repo:https://github.com/jpadilla987-png/lead-rescue-agent/tree/amazon-alexa",
                "repo:LICENSE",
                "repo:amazon_alexa/README.md",
            ),
        ),
        Requirement(
            key="demo_video",
            label="Public English demo video under 3 minutes",
            answer="",
            evidence_refs=(),
        ),
        Requirement(
            key="product_feedback",
            label="Product feedback for tools/APIs/SDKs used",
            answer="",
            evidence_refs=(),
        ),
        Requirement(
            key="significant_update",
            label="Explain significant update to pre-existing project",
            answer="Amazon-specific MCP implementation is isolated on amazon-alexa and was created during the submission period.",
            evidence_refs=(
                "git:2bb2fc7eb22b4e7a0678333a41159361fffab4c7",
                "repo:amazon_alexa/README.md",
            ),
        ),
        Requirement(
            key="security_review",
            label="Independent security review",
            answer="Dependency audit, Bandit static analysis, and CodeQL all pass after fixing the default network-bind finding.",
            evidence_refs=("github-actions:35812772437",),
        ),
    )

    return SubmissionContext(
        project="Lead Rescue Voice",
        track="Alexa+",
        one_liner="An Alexa+ style agent that finds leads going cold and turns them into safe, actionable follow-ups.",
        problem="Small service businesses lose valuable leads when owners cannot respond quickly while doing the actual work.",
        solution="A bounded lead-recovery agent ranks stale or urgent opportunities, explains why they matter, and prepares the safest next action while escalating pricing authority to the owner.",
        architecture=(
            "MCP Python SDK v2 server",
            "Streamable HTTP endpoint at /mcp",
            "Transparent deterministic lead scoring",
            "Guarded follow-up drafting with owner escalation",
            "Automated functional, adversarial, and security tests",
        ),
        requirements=requirements,
        disclosure="The repository predates the Amazon hackathon. The Alexa+/MCP implementation on the amazon-alexa branch is a significant new build created during the submission window.",
        repo_url="https://github.com/jpadilla987-png/lead-rescue-agent/tree/amazon-alexa",
    )


def packet():
    return compile_submission(context())


def demo_180():
    return build_demo_plan(
        opening="A good lead should not die because the owner is on a ladder, in a truck, or helping another customer.",
        total_seconds=180,
        beats=[
            DemoBeat("Problem", 20, "Show four incoming leads and ask which are going cold.", "The queue is visible and understandable."),
            DemoBeat("MCP ranking", 35, "Call prioritize_leads through MCP.", "Ranked leads appear with scores and reasons.", "Use saved CI output if the live client fails."),
            DemoBeat("Safety", 35, "Open the price-match lead and request a follow-up.", "The agent refuses to invent a discount and escalates owner approval."),
            DemoBeat("Urgent rescue", 30, "Open the critical no-cooling lead.", "The agent explains the urgent reason and prepares a bounded response."),
            DemoBeat("Proof", 30, "Show GitHub Actions functional + adversarial + security passes.", "Judges see reproducible evidence."),
            DemoBeat("Close", 15, "Summarize commercial path for service businesses.", "Value proposition is explicit."),
        ],
    )

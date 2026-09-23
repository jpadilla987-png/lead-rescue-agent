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
                "github-actions:35815021522",
                "repo:amazon_alexa/server.py",
            ),
        ),
        Requirement(
            key="protocol_version",
            label="MCP protocol 2025-11-25 or later",
            answer="The real HTTP smoke test fails if the negotiated client.protocol_version is older than 2025-11-25.",
            evidence_refs=(
                "github-actions:35815021522",
                "repo:amazon_alexa/http_smoke.py",
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
            key="browser_demo_source",
            label="Alexa+ style browser simulation source",
            answer="Self-contained HTML/CSS/JavaScript simulation mirrors the MCP tools, rescue queue, and owner-approval boundary.",
            evidence_refs=(
                "repo:amazon_alexa/demo/index.html",
                "repo:amazon_alexa/tests/test_demo_assets.py",
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
            answer="Factual feedback draft covers MCP Python SDK v2, Python testing, GitHub Actions, and the browser simulation.",
            evidence_refs=("repo:amazon_alexa/PRODUCT_FEEDBACK.md",),
        ),
        Requirement(
            key="friction_log",
            label="Optional friction log for judging bonus",
            answer="Two evidence-backed friction entries cover protocol-version proof and deployment-safe host defaults.",
            evidence_refs=("repo:amazon_alexa/FRICTION_LOG.md",),
        ),
        Requirement(
            key="open_source_mini",
            label="Open Source Mini Challenge contribution",
            answer="The public amazon-alexa branch was created during the hackathon window as a new open-source contribution.",
            evidence_refs=(
                "repo:amazon_alexa/OPEN_SOURCE_MINI.md",
                "git:2bb2fc7eb22b4e7a0678333a41159361fffab4c7",
            ),
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
            label="Independent automated security review",
            answer="Dependency audit, Bandit static analysis, and CodeQL pass after fixing the default network-bind finding.",
            evidence_refs=("github-actions:35815021550",),
        ),
        Requirement(
            key="submitter_country",
            label="Submitter country of residence",
            answer="",
            evidence_refs=(),
        ),
        Requirement(
            key="canada_province",
            label="Canada province or N/A",
            answer="",
            evidence_refs=(),
        ),
        Requirement(
            key="age_attestation",
            label="Age-of-majority attestation",
            answer="",
            evidence_refs=(),
        ),
        Requirement(
            key="eligible_jurisdiction_attestation",
            label="Eligible-jurisdiction attestation",
            answer="",
            evidence_refs=(),
        ),
        Requirement(
            key="employee_attestation",
            label="Promotion-entity employee attestation",
            answer="",
            evidence_refs=(),
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
            "Protocol-version compatibility assertion",
            "Transparent deterministic lead scoring",
            "Guarded follow-up drafting with owner escalation",
            "Browser simulation for judge-facing demo",
            "Automated functional, adversarial, and security tests",
        ),
        requirements=requirements,
        product_feedback=(
            "MCP Python SDK v2 made the tool surface compact and testable.",
            "Exact protocol-revision proof required an explicit client.protocol_version assertion.",
            "Security review found and corrected an unsafe default all-interface bind.",
        ),
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
            DemoBeat("Problem", 18, "Show incoming leads and ask which are going cold.", "The queue is immediately understandable."),
            DemoBeat("MCP ranking", 30, "Run the morning brief.", "Ranked leads appear with transparent scores and reasons."),
            DemoBeat("Urgent rescue", 30, "Open the critical no-cooling lead.", "The agent prepares a bounded response without inventing availability."),
            DemoBeat("Safety", 34, "Open the price-match lead and request a follow-up.", "The agent refuses to invent a discount and escalates owner approval."),
            DemoBeat("Proof", 28, "Show functional, protocol, adversarial, and security passes.", "Judges see reproducible evidence."),
            DemoBeat("Close", 15, "Summarize the commercial path for service businesses.", "Value proposition is explicit."),
        ],
    )

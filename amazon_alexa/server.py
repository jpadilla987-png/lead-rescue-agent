from __future__ import annotations

import os
from typing import Any

from mcp.server import MCPServer

from lead_rescue_core import draft_follow_up, get_lead, prioritized_leads

mcp = MCPServer("Lead Rescue Voice")


@mcp.tool()
def prioritize_leads(limit: int = 3) -> dict[str, Any]:
    """Rank leads by rescue urgency and explain why each one needs attention now."""
    leads = prioritized_leads(limit)
    return {"count": len(leads), "leads": leads}


@mcp.tool()
def inspect_lead(lead_id: str) -> dict[str, Any]:
    """Inspect a lead, including its transparent rescue score and urgency explanation."""
    return get_lead(lead_id)


@mcp.tool()
def prepare_follow_up(lead_id: str, tone: str = "warm") -> dict[str, Any]:
    """Prepare a safe follow-up draft, escalating pricing authority and unusual commitments to the owner."""
    return draft_follow_up(lead_id, tone)


@mcp.prompt()
def morning_rescue_brief() -> str:
    """Prompt an Alexa+ style host to run a short lead-rescue morning briefing."""
    return (
        "Use the Lead Rescue Voice tools to identify the three leads most at risk, explain why each matters, "
        "and prepare the safest next follow-up. Never invent pricing, discounts, availability, or commitments."
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    mcp.run(
        transport="streamable-http",
        host=host,
        port=port,
        streamable_http_path="/mcp",
        stateless_http=True,
        json_response=True,
    )

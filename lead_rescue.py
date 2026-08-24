"""Lead Rescue — autonomous small-business lead follow-up with Strands + Amazon Bedrock.

Run:
    pip install -r requirements.txt
    python lead_rescue.py

AWS credentials must be configured for Amazon Bedrock. Strands uses Bedrock natively.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from strands import Agent, tool
from strands.models import BedrockModel


BUSINESS = {
    "name": "Desert Air HVAC",
    "service_area": ["Palmdale", "Lancaster", "Quartz Hill"],
    "hours": "Mon-Sat 7am-7pm",
    "published_offers": ["$89 tune-up", "free replacement estimate"],
    "rules": {
        "same_day_emergency": True,
        "discounts_need_owner": True,
        "price_matching_needs_owner": True,
        "never_invent_availability": True,
    },
}

STATE: dict[str, Any] = {
    "leads": [
        {
            "id": "L-101",
            "name": "Maria",
            "city": "Palmdale",
            "request": "AC stopped cooling and the house is getting hot. Can someone come today?",
            "timing": "today afternoon",
            "status": "new",
        },
        {
            "id": "L-102",
            "name": "Derek",
            "city": "Lancaster",
            "request": "Another company quoted $79. Can you beat that price?",
            "timing": "this week",
            "status": "new",
        },
        {
            "id": "L-103",
            "name": "Ana",
            "city": "Quartz Hill",
            "request": "I want the advertised tune-up. Morning is best.",
            "timing": "morning",
            "status": "new",
        },
    ],
    "calendar": [
        {"slot": "Today 3:30 PM", "available": True},
        {"slot": "Tomorrow 9:00 AM", "available": True},
        {"slot": "Tomorrow 11:30 AM", "available": False},
    ],
    "actions": [],
    "owner_decisions": [],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@tool
def get_business_context() -> str:
    """Load service area, operating rules, hours, and published offers before customer-facing action."""
    return json.dumps(BUSINESS)


@tool
def get_new_leads() -> str:
    """Return every currently unprocessed inbound lead."""
    return json.dumps([lead for lead in STATE["leads"] if lead["status"] == "new"])


@tool
def check_availability(preference: str) -> str:
    """Check real appointment availability for a customer's timing preference. Never invent a slot."""
    slots = [item["slot"] for item in STATE["calendar"] if item["available"]]
    return json.dumps({"preference": preference, "available_slots": slots})


@tool
def send_customer_reply(lead_id: str, message: str, offered_slot: str = "") -> str:
    """Send a warm routine reply when no owner-only price, discount, legal, or warranty decision is required."""
    lead = next((item for item in STATE["leads"] if item["id"] == lead_id), None)
    if not lead:
        return "ERROR: lead not found"
    lead["status"] = "scheduled" if offered_slot else "replied"
    STATE["actions"].append(
        {
            "at": now_iso(),
            "lead_id": lead_id,
            "kind": "schedule" if offered_slot else "reply",
            "message": message,
            "offered_slot": offered_slot or None,
        }
    )
    return f"Reply recorded for {lead_id}"


@tool
def schedule_follow_up(lead_id: str, when: str, reason: str) -> str:
    """Schedule a future follow-up so a lead is not forgotten."""
    STATE["actions"].append(
        {"at": now_iso(), "lead_id": lead_id, "kind": "follow_up", "when": when, "reason": reason}
    )
    return f"Follow-up scheduled for {lead_id}"


@tool
def escalate_to_owner(lead_id: str, question: str, options: list[str]) -> str:
    """Pause automation and surface a real business decision that only the owner should make."""
    lead = next((item for item in STATE["leads"] if item["id"] == lead_id), None)
    if not lead:
        return "ERROR: lead not found"
    lead["status"] = "needs_owner"
    decision = {"lead_id": lead_id, "question": question, "options": options[:4]}
    STATE["owner_decisions"].append(decision)
    STATE["actions"].append({"at": now_iso(), "lead_id": lead_id, "kind": "decision", **decision})
    return f"Owner decision requested for {lead_id}"


@tool
def mark_lead_closed(lead_id: str, reason: str) -> str:
    """Close a lead only when it is clearly outside the service area or no longer actionable."""
    lead = next((item for item in STATE["leads"] if item["id"] == lead_id), None)
    if not lead:
        return "ERROR: lead not found"
    lead["status"] = "closed"
    STATE["actions"].append({"at": now_iso(), "lead_id": lead_id, "kind": "closed", "reason": reason})
    return f"Lead {lead_id} closed"


SYSTEM_PROMPT = """
You are Lead Rescue, an autonomous professional agent for a busy local-service business owner.
Your job is to process the full inbound lead queue end-to-end rather than merely chat about it.

Rules:
1. Load business context first, then load all new leads.
2. Process EVERY new lead before finishing.
3. Check actual calendar availability before offering any appointment time. Never invent a slot.
4. Handle routine inquiries yourself with concise, warm, human replies and useful follow-up.
5. Never negotiate a discount, price match, custom price, unusual warranty, legal commitment, or unsupported promise.
   Escalate those decisions to the owner with 2-4 concise options.
6. Treat loss-of-cooling requests as urgent when policy permits same-day service.
7. Surface only decisions that truly require the owner; routine work should stay quiet and autonomous.
8. When finished, summarize leads processed, actions completed, and owner decisions waiting.
""".strip()


def main() -> None:
    model = BedrockModel(
        model_id="global.anthropic.claude-sonnet-4-6",
        region_name="us-west-2",
        temperature=0.2,
    )

    agent = Agent(
        model=model,
        tools=[
            get_business_context,
            get_new_leads,
            check_availability,
            send_customer_reply,
            schedule_follow_up,
            escalate_to_owner,
            mark_lead_closed,
        ],
        system_prompt=SYSTEM_PROMPT,
    )

    print("\n=== LEAD RESCUE: RUNNING NEW-LEAD QUEUE ===\n")
    response = agent(
        "Process the entire new-lead queue now. Take permitted actions, schedule follow-ups, "
        "and escalate only true owner decisions."
    )

    print("\n=== AGENT SUMMARY ===")
    print(response)
    print("\n=== ACTION LOG ===")
    print(json.dumps(STATE["actions"], indent=2))
    print("\n=== OWNER DECISIONS ===")
    print(json.dumps(STATE["owner_decisions"], indent=2))


if __name__ == "__main__":
    main()

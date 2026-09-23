from __future__ import annotations

from copy import deepcopy
from typing import Any

LEADS: list[dict[str, Any]] = [
    {
        "id": "lead-001",
        "name": "Maya Chen",
        "service": "AC no-cooling repair",
        "age_hours": 1.4,
        "estimated_value": 420,
        "urgency": "critical",
        "stage": "new",
        "last_message": "The house is 87 degrees and we have a toddler. Can anyone come today?",
    },
    {
        "id": "lead-002",
        "name": "Andre Ruiz",
        "service": "HVAC replacement estimate",
        "age_hours": 19.0,
        "estimated_value": 9200,
        "urgency": "high",
        "stage": "quoted",
        "last_message": "We have another quote. Can you match it?",
    },
    {
        "id": "lead-003",
        "name": "Sam Patel",
        "service": "Seasonal tune-up",
        "age_hours": 31.0,
        "estimated_value": 189,
        "urgency": "normal",
        "stage": "new",
        "last_message": "Looking for a tune-up sometime next week.",
    },
    {
        "id": "lead-004",
        "name": "Jordan Brooks",
        "service": "Ductless mini-split",
        "age_hours": 54.0,
        "estimated_value": 4800,
        "urgency": "normal",
        "stage": "contacted",
        "last_message": "Still interested, but I have not heard back since Friday.",
    },
]

URGENCY_WEIGHT = {"normal": 0, "high": 28, "critical": 48}
STAGE_WEIGHT = {"new": 12, "contacted": 8, "quoted": 16}


def lead_score(lead: dict[str, Any]) -> int:
    """Return a transparent 0-100 rescue priority score."""
    age = min(float(lead["age_hours"]) / 48.0, 1.0) * 30
    value = min(float(lead["estimated_value"]) / 5000.0, 1.0) * 22
    urgency = URGENCY_WEIGHT.get(str(lead.get("urgency", "normal")), 0)
    stage = STAGE_WEIGHT.get(str(lead.get("stage", "new")), 0)
    return max(0, min(100, round(age + value + urgency + stage)))


def _reason(lead: dict[str, Any], score: int) -> str:
    reasons: list[str] = []
    if lead["urgency"] == "critical":
        reasons.append("critical service need")
    elif lead["urgency"] == "high":
        reasons.append("high urgency")
    if float(lead["age_hours"]) >= 24:
        reasons.append("response delay over 24 hours")
    if float(lead["estimated_value"]) >= 3000:
        reasons.append("high-value opportunity")
    if lead["stage"] == "quoted":
        reasons.append("active buying decision")
    if not reasons:
        reasons.append("new lead awaiting a timely response")
    return f"Priority {score}/100: " + ", ".join(reasons) + "."


def prioritized_leads(limit: int = 3) -> list[dict[str, Any]]:
    if limit < 1 or limit > 10:
        raise ValueError("limit must be between 1 and 10")
    ranked: list[dict[str, Any]] = []
    for lead in LEADS:
        item = deepcopy(lead)
        score = lead_score(item)
        item["priority_score"] = score
        item["why_now"] = _reason(item, score)
        ranked.append(item)
    ranked.sort(key=lambda x: (-x["priority_score"], -float(x["estimated_value"])))
    return ranked[:limit]


def get_lead(lead_id: str) -> dict[str, Any]:
    for lead in LEADS:
        if lead["id"] == lead_id:
            item = deepcopy(lead)
            score = lead_score(item)
            item["priority_score"] = score
            item["why_now"] = _reason(item, score)
            return item
    raise ValueError(f"Unknown lead_id: {lead_id}")


def draft_follow_up(lead_id: str, tone: str = "warm") -> dict[str, Any]:
    if tone not in {"warm", "direct", "concise"}:
        raise ValueError("tone must be warm, direct, or concise")
    lead = get_lead(lead_id)
    first_name = str(lead["name"]).split()[0]

    if lead["stage"] == "quoted" and "match" in str(lead["last_message"]).lower():
        return {
            "lead_id": lead_id,
            "requires_owner_approval": True,
            "reason": "The customer requested a price match. The agent must not invent discounts or alter pricing authority.",
            "draft": f"Hi {first_name}, thanks for sending that over. I can get the quote comparison in front of the owner and come back to you with a clear answer. I won't promise a price change before it is approved.",
        }

    if lead["urgency"] == "critical":
        draft = f"Hi {first_name}, I saw your urgent {lead['service']} request. We are treating this as time-sensitive and are checking the earliest available service window now."
    elif tone == "direct":
        draft = f"Hi {first_name}, following up on your {lead['service']} request. Are you still looking to get this scheduled?"
    elif tone == "concise":
        draft = f"Hi {first_name} — checking in on your {lead['service']} request. Want me to help with the next step?"
    else:
        draft = f"Hi {first_name}, thanks for reaching out about {lead['service']}. I wanted to make sure your request did not get lost. If you are still interested, I can help move the next step forward."

    return {
        "lead_id": lead_id,
        "requires_owner_approval": False,
        "reason": "Routine follow-up within published service boundaries.",
        "draft": draft,
    }

from __future__ import annotations

import asyncio

from mcp import Client

from server import mcp


async def main() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("prioritize_leads", {"limit": 2})
        payload = result.structured_content
        assert isinstance(payload, dict)
        assert payload["count"] == 2
        assert payload["leads"][0]["priority_score"] >= payload["leads"][1]["priority_score"]

        follow_up = await client.call_tool("prepare_follow_up", {"lead_id": "lead-002", "tone": "warm"})
        follow_payload = follow_up.structured_content
        assert isinstance(follow_payload, dict)
        assert follow_payload["requires_owner_approval"] is True
        print("In-process MCP smoke test passed")
        print(payload)


if __name__ == "__main__":
    asyncio.run(main())

from __future__ import annotations

import asyncio

from mcp import Client


async def main() -> None:
    async with Client("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("prioritize_leads", {"limit": 1})
        payload = result.structured_content
        assert isinstance(payload, dict)
        assert payload["count"] == 1
        assert payload["leads"][0]["id"]
        print("Streamable HTTP MCP smoke test passed")
        print(payload)


if __name__ == "__main__":
    asyncio.run(main())

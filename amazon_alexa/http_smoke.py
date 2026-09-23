from __future__ import annotations

import asyncio

from mcp import Client


MIN_PROTOCOL_VERSION = "2025-11-25"


async def main() -> None:
    async with Client("http://127.0.0.1:8000/mcp") as client:
        negotiated = client.protocol_version
        assert negotiated is not None
        assert negotiated >= MIN_PROTOCOL_VERSION, (
            f"Negotiated MCP protocol {negotiated} is older than required {MIN_PROTOCOL_VERSION}"
        )

        result = await client.call_tool("prioritize_leads", {"limit": 1})
        payload = result.structured_content
        assert isinstance(payload, dict)
        assert payload["count"] == 1
        assert payload["leads"][0]["id"]

        print("Streamable HTTP MCP smoke test passed")
        print(f"Negotiated MCP protocol: {negotiated}")
        print(payload)


if __name__ == "__main__":
    asyncio.run(main())

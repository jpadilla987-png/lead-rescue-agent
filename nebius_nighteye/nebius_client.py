from __future__ import annotations

import os
from typing import Any, Protocol

from openai import OpenAI

from .core import AnalysisRequest, build_messages, parse_analysis


DEFAULT_BASE_URL = "https://api.tokenfactory.us-central1.nebius.com/v1/"
DEFAULT_MODEL = "nvidia/nemotron-3-super-120b-a12b"


class ChatBackend(Protocol):
    def complete(self, *, messages: list[dict[str, str]], model: str) -> str: ...


class NebiusBackend:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ) -> None:
        key = api_key or os.getenv("NEBIUS_API_KEY")
        if not key:
            raise RuntimeError("NEBIUS_API_KEY is required for live inference")
        self.model = model or os.getenv("NEBIUS_MODEL", DEFAULT_MODEL)
        self.client = OpenAI(
            api_key=key,
            base_url=base_url or os.getenv("NEBIUS_BASE_URL", DEFAULT_BASE_URL),
            timeout=60.0,
            max_retries=2,
        )

    def complete(self, *, messages: list[dict[str, str]], model: str) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,
            max_tokens=1800,
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("Nebius returned an empty response")
        return content


def analyze(req: AnalysisRequest, backend: ChatBackend | None = None, model: str | None = None) -> dict[str, Any]:
    active = backend or NebiusBackend(model=model)
    selected_model = model or getattr(active, "model", DEFAULT_MODEL)
    messages = build_messages(req)
    raw = active.complete(messages=messages, model=selected_model)
    result = parse_analysis(raw, (item.id for item in req.evidence))
    return {
        "model": selected_model,
        "provider": "Nebius Token Factory",
        "analysis": result,
    }

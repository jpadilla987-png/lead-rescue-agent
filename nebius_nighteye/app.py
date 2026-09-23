from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .core import AnalysisRequest, EvidenceItem
from .nebius_client import analyze


app = FastAPI(title="NIGHTEYE Evidence Engine", version="0.1.0")


class EvidenceIn(BaseModel):
    id: str = Field(min_length=1, max_length=80)
    source: str = Field(min_length=1, max_length=200)
    observed_at: str = Field(min_length=1, max_length=80)
    text: str = Field(min_length=1, max_length=5000)


class AnalyzeIn(BaseModel):
    topic: str = Field(min_length=1, max_length=500)
    evidence: list[EvidenceIn] = Field(min_length=1, max_length=30)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "NIGHTEYE Evidence Engine"}


@app.post("/analyze")
def analyze_route(payload: AnalyzeIn) -> dict:
    req = AnalysisRequest(
        topic=payload.topic,
        evidence=tuple(
            EvidenceItem(
                id=item.id,
                source=item.source,
                observed_at=item.observed_at,
                text=item.text,
            )
            for item in payload.evidence
        ),
    )
    try:
        return analyze(req)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

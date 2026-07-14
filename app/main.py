"""FastAPI entrypoint for nyxara-core (open-source, MIT).

Minimal skeleton after the 2026-07 reset — only a liveness probe.
Each phase of the roadmap adds its own routers/adapters on top of this.

Run locally:
    uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="nyxara-core",
    description="MIT-licensed AI engineering core — RAG, agents, evaluation. Built from scratch.",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Liveness probe. No auth, no tenant context required."""
    return {"status": "ok", "service": "nyxara-core"}

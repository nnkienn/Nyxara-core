"""FastAPI entrypoint for n-assistant-core (open-source).

Run locally:
    uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

import logging

import structlog
from fastapi import FastAPI

from app.core.config import settings
from app.core.llm_client import LLMClientBase
from app.infrastructure.adapters.embedder.bge_embedder import BGEEmbedder
from app.infrastructure.adapters.vectorstore.qdrant_store import QdrantStore
from app.infrastructure.adapters.reranker.bge_reranker import BGEReranker
from app.application.retrieval.bm25_index import BM25Index
from app.application.retrieval.hybrid_retriever import HybridRetriever
from app.application.generation.grader import RelevanceGrader
from app.application.generation.graph import build_crag_graph
from app.presentation.api.routes.ask import router as ask_router

# ── Structlog configuration ────────────────────────────────────────────────
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        (
            structlog.dev.ConsoleRenderer()
            if settings.DEBUG
            else structlog.processors.JSONRenderer()
        ),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(
        logging.getLevelName(settings.LOG_LEVEL),
    ),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# ── FastAPI application ────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description="MIT-licensed AI & backend core: RAG pipeline, agent orchestration.",
    version=settings.APP_VERSION,
)


@app.on_event("startup")
async def _on_startup() -> None:
    logger.info(
        "startup",
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        inference_provider=settings.INFERENCE_PROVIDER,
        inference_model=settings.INFERENCE_MODEL,
        debug=settings.DEBUG,
    )

    # ── Composition root: dựng CRAG graph MỘT LẦN (model nặng, không dựng/request) ──
    llm = LLMClientBase()
    embedder = BGEEmbedder()
    store = QdrantStore()
    bm25 = BM25Index()
    retriever = HybridRetriever(embedder, store, bm25)
    reranker = BGEReranker()
    grader = RelevanceGrader(llm)

    # Cất vào app.state → route /ask lấy ra dùng chung.
    app.state.crag_graph = build_crag_graph(
        retriever=retriever, reranker=reranker, grader=grader
    )
    logger.info("crag_graph_ready")


app.include_router(ask_router)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Liveness probe. No auth, no tenant context required."""
    return {"status": "ok", "service": "core-api-opensource"}

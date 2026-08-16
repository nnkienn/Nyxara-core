"""FastAPI entrypoint for nyxara-core (open-source, MIT).

Phase: `/ask` wired up (2026-08-14) — lifespan builds the 4 real adapters
(Embedder, VectorStore, BM25Index, DocStore -> HybridRetriever, Grader,
Generator) once at startup and compiles the CRAG graph, stored on
`app.state` so request handlers reuse it instead of rebuilding per call.

Run locally:
    uvicorn app.main:app --reload --port 8000

Requires env var OLLAMA_BASE_URL (e.g. http://100.78.59.56:11434 via Tailscale).
"""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from qdrant_client import QdrantClient

from app.application.generation.graph import build_graph
from app.application.retrieval.bm25_index import BM25Index
from app.application.retrieval.hybrid_retriever import HybridRetriever
from app.application.retrieval.reranking_retriever import RerankingRetriever
from app.infrastructure.adapters.docstore.in_memory_doc_store import InMemoryDocStore
from app.infrastructure.adapters.embedder.bge_embedder import BGEEmbedder
from app.infrastructure.adapters.generator.ollama_generator import OllamaGenerator
from app.infrastructure.adapters.grader.ollama_grader import OllamaGrader
from app.infrastructure.adapters.reranker.bge_reranker import BGEReranker
from app.infrastructure.adapters.vectorstore.qdrant_store import QdrantStore
from app.presentation.api.ask import router as ask_router
from app.presentation.api.ingest import router as ingest_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    embedder = BGEEmbedder()
    client = QdrantClient(location=":memory:")
    vector_store = QdrantStore(client=client, collection="docs", dim=embedder.dim)
    bm25_index = BM25Index()
    doc_store = InMemoryDocStore()
    hybrid_retriever = HybridRetriever(embedder, vector_store, bm25_index)
    reranker = BGEReranker()
    # retrieve_node (node.py) gọi .search(tenant_id, query, candidate_k, top_k) — 4 tham số,
    # đúng chữ ký RerankingRetriever, không phải HybridRetriever (chỉ có 3, tự tính candidate_k)
    retriever = RerankingRetriever(hybrid_retriever, doc_store, reranker)

    ollama_base_url = os.environ["OLLAMA_BASE_URL"]
    grader = OllamaGrader(base_url=ollama_base_url)
    generator = OllamaGenerator(base_url=ollama_base_url)

    manifest_path = os.environ.get("MANIFEST_PATH", "data/manifest.json")
    os.makedirs(os.path.dirname(manifest_path) or ".", exist_ok=True)

    # lưu lại để /ingest và /ask dùng chung đúng 4 instance này,
    # không dựng mới mỗi request
    app.state.embedder = embedder
    app.state.vector_store = vector_store
    app.state.bm25_index = bm25_index
    app.state.doc_store = doc_store
    app.state.manifest_path = manifest_path
    app.state.graph = build_graph(retriever, doc_store, grader, generator)

    yield


app = FastAPI(
    title="nyxara-core",
    description="MIT-licensed AI engineering core — RAG, agents, evaluation. Built from scratch.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(ingest_router)
app.include_router(ask_router)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Liveness probe. No auth, no tenant context required."""
    return {"status": "ok", "service": "nyxara-core"}

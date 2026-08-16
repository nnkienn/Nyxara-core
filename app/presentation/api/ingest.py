"""POST /ingest — write a document into all 3 stores (BM25 + Qdrant + DocStore)."""

from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.application.chunking.recursive_chunker import recursive_chunk
from app.application.ingestion.pipeline import ingest_document

router = APIRouter()


class IngestRequest(BaseModel):
    tenant_id: str
    doc_id: str
    text: str
    chunk_size: int = 200
    chunk_overlap: int = 20


class IngestResponse(BaseModel):
    chunk_count: int


@router.post("/ingest", response_model=IngestResponse, tags=["ingest"])
def ingest(payload: IngestRequest, request: Request) -> IngestResponse:
    # `def` thường, không `async def` — ingest_document gọi embedder.embed() (model thật,
    # đồng bộ) + vector_store.upsert() (qdrant-client đồng bộ), cùng lý do với /ask.
    chunks = recursive_chunk(payload.text, payload.chunk_size, payload.chunk_overlap)

    ingest_document(
        payload.tenant_id,
        payload.doc_id,
        chunks,
        request.app.state.manifest_path,
        request.app.state.bm25_index,
        request.app.state.vector_store,
        request.app.state.doc_store,
        request.app.state.embedder,
    )

    return IngestResponse(chunk_count=len(chunks))

"""QdrantStore — Qdrant implementation of the VectorStore port.

Two things to notice while reading:
  1. ``ensure_collection`` uses ``collection_exists`` + ``create_collection`` —
     NEVER ``recreate_collection`` (which silently wipes data — the prototype trap).
  2. ``search`` enforces a mandatory ``tenant_id`` filter — this is the
     "namespace isolation" the project mandates: one install holds many niches,
     and a query NEVER sees another niche's vectors.
"""

from __future__ import annotations

import uuid

import structlog
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.core.config import settings
from app.domain.ports.vector_store import SearchHit

logger = structlog.get_logger(__name__)


class QdrantStore:
    """Implements the VectorStore port against a Qdrant server."""

    def __init__(self, url: str | None = None) -> None:
        # URL comes from config (QDRANT_URL): localhost:6353 on the host,
        # http://core-qdrant:6333 inside the compose network — never hardcoded.
        self._client = QdrantClient(url or settings.QDRANT_URL)

    def ensure_collection(self, collection: str, dim: int) -> None:
        if not self._client.collection_exists(collection):
            self._client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )
            logger.info("collection_created", collection=collection, dim=dim)

    def upsert(self, collection, vectors, payloads) -> int:
        points: list[PointStruct] = []
        for vector, payload in zip(vectors, payloads):
            # Deterministic ID from tenant_id + text → re-ingesting the same chunk
            # OVERWRITES instead of duplicating (idempotent ingest).
            key = f"{payload.get('tenant_id', '')}:{payload.get('text', '')}"
            point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, key))
            points.append(PointStruct(id=point_id, vector=vector, payload=payload))
        self._client.upsert(collection_name=collection, points=points)
        return len(points)

    def search(self, collection, query_vector, *, tenant_id, top_k=5) -> list[SearchHit]:
        # The namespace moat: only points whose payload.tenant_id == this tenant.
        namespace_filter = Filter(
            must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))]
        )
        results = self._client.query_points(
            collection_name=collection,
            query=query_vector,
            query_filter=namespace_filter,
            limit=top_k,
        ).points
        return [
            SearchHit(id=p.id, score=p.score, payload=p.payload or {}) for p in results
        ]

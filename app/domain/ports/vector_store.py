"""VectorStore port — store vectors + payload, search by similarity.

Hexagonal: the RAG pipeline depends on THIS abstract contract, never on Qdrant
directly. Swap Qdrant for Milvus/pgvector by writing a new adapter — no caller
changes. ``SearchHit`` is a plain domain type so Qdrant's classes never leak out.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class SearchHit:
    """One retrieval result: which point, how similar, and its stored payload."""

    id: str | int
    score: float                 # cosine similarity in [-1, 1] (here, normalized → [0,1])
    payload: dict[str, Any]


class VectorStore(Protocol):
    def ensure_collection(self, collection: str, dim: int) -> None:
        """Create the collection IF MISSING (idempotent, Cosine distance).

        Deliberately NOT ``recreate`` — re-creating wipes existing data (the trap
        from the prototype). Safe to call on every ingest.
        """
        ...

    def upsert(
        self, collection: str, vectors: list[list[float]], payloads: list[dict[str, Any]]
    ) -> int:
        """Store/replace points. Each payload MUST carry ``tenant_id``. Returns count."""
        ...

    def search(
        self,
        collection: str,
        query_vector: list[float],
        *,
        tenant_id: str,
        top_k: int = 5,
    ) -> list[SearchHit]:
        """Nearest vectors WITHIN the ``tenant_id`` namespace (mandatory filter)."""
        ...

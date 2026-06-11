"""Tests for IngestionService.

The whole point: we test the ingestion LOGIC with a FAKE embedder and a FAKE
store — no 4.5GB bge-m3 model, no running Qdrant. That's the payoff of depending
on ports (Embedder / VectorStore) instead of concrete classes.
"""

import json

from app.application.services.ingestion import IngestionService


class FakeEmbedder:
    """Satisfies the Embedder port structurally (has dim + embed) — no model."""

    dim = 4

    def embed(self, texts):
        return [[0.0, 0.1, 0.2, 0.3] for _ in texts]  # dummy 4-dim vector each


class FakeStore:
    """Satisfies the VectorStore port — records calls in memory, no Qdrant."""

    def __init__(self):
        self.collections: dict[str, int] = {}
        self.upserts: list[tuple] = []

    def ensure_collection(self, collection, dim):
        self.collections[collection] = dim

    def upsert(self, collection, vectors, payloads):
        self.upserts.append((collection, vectors, payloads))
        return len(vectors)

    def search(self, *args, **kwargs):
        return []


def _write_approved(tmp_path, items):
    path = tmp_path / "approved.json"
    path.write_text(json.dumps(items), encoding="utf-8")
    return path


def test_ingest_stamps_tenant_id_on_every_chunk(tmp_path):
    items = [
        {"clean_content": "Short tweet one.", "tenant_id": "niche_a", "source_url": "u1"},
        {"clean_content": "Short tweet two.", "source_url": "u2"},  # no tenant_id
    ]
    path = _write_approved(tmp_path, items)

    store = FakeStore()
    service = IngestionService(FakeEmbedder(), store)   # ← inject fakes, no real deps

    n = service.ingest_file(path, collection="memory", tenant_id="fallback")

    assert n == 2  # two short items → two chunks
    _, vectors, payloads = store.upserts[0]
    assert len(vectors) == 2
    # item with its own tenant_id keeps it; the one without → falls back
    assert payloads[0]["tenant_id"] == "niche_a"
    assert payloads[1]["tenant_id"] == "fallback"


def test_ingest_sizes_collection_from_embedder_dim(tmp_path):
    path = _write_approved(tmp_path, [{"clean_content": "hello world"}])
    store = FakeStore()

    IngestionService(FakeEmbedder(), store).ingest_file(path, collection="c", tenant_id="t")

    # dim comes from the embedder (4), never hardcoded as 1024
    assert store.collections["c"] == FakeEmbedder.dim


def test_ingest_empty_file_stores_nothing(tmp_path):
    path = _write_approved(tmp_path, [])
    store = FakeStore()

    n = IngestionService(FakeEmbedder(), store).ingest_file(path, collection="c", tenant_id="t")

    assert n == 0
    assert store.upserts == []

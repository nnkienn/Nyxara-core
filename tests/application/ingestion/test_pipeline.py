import pytest

from app.application.ingestion.pipeline import (
    diff_manifest,
    get_doc_manifest,
    incremental_ingest,
    ingest_document,
    load_manifest,
    load_seen,
    save_manifest,
    save_seen,
)
from app.application.retrieval.bm25_index import BM25Index
from app.infrastructure.adapters.docstore.in_memory_doc_store import InMemoryDocStore


class FakeEmbedder:
    dim = 3

    def __init__(self):
        self.calls: list[list[str]] = []

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(list(texts))
        return [[float(len(t)), 0.0, 0.0] for t in texts]


class FakeVectorStore:
    def __init__(self):
        self.data: dict[str, dict[str, str]] = {}

    def upsert(self, tenant_id, ids, texts, vectors) -> None:
        self.data.setdefault(tenant_id, {})
        for id_, text in zip(ids, texts):
            self.data[tenant_id][id_] = text

    def delete(self, tenant_id, chunk_id) -> None:
        self.data.get(tenant_id, {}).pop(chunk_id, None)

    def search(self, tenant_id, query_vector, top_k):
        raise NotImplementedError("không cần cho test này")


def test_second_run_only_returns_new_chunks(tmp_path):
    seen_path = str(tmp_path / "seen.json")

    incremental_ingest(["mèo", "gà", "chó"], seen_path)
    new_chunks = incremental_ingest(["mèo", "gà", "chó", "chim"], seen_path)

    assert new_chunks == ["chim"]




def test_get_doc_manifest_survives_json_roundtrip(tmp_path):
    path = str(tmp_path / "manifest.json")
    manifest = {"t1": {"d1": {"0": "hash0", "1": "hash1"}}}
    save_manifest(path, manifest)
    loaded = load_manifest(path)
    assert get_doc_manifest(loaded, "t1", "d1") == {"0": "hash0", "1": "hash1"}


def test_get_doc_manifest_returns_empty_dict_for_unknown_doc():
    assert get_doc_manifest({}, "t1", "d1") == {}

def test_diff_manifest_categorizes_new_changed_deleted_unchanged():
    old = {"0": "hashA", "1": "hashB", "2": "hashC"}
    new = {"0": "hashA", "1": "hashB_CHANGED", "3": "hashD"}

    to_upsert, to_skip, to_delete = diff_manifest(old, new)

    assert sorted(to_upsert) == ["1", "3"]
    assert sorted(to_skip) == ["0"]
    assert sorted(to_delete) == ["2"]


def _new_stores():
    return BM25Index(), InMemoryDocStore(), FakeVectorStore(), FakeEmbedder()


def test_ingest_document_writes_to_all_three_stores(tmp_path):
    manifest_path = str(tmp_path / "manifest.json")
    bm25, doc_store, vector_store, embedder = _new_stores()

    ingest_document(
        "t1", "doc1", ["mèo đen", "chó nâu", "chim xanh"],
        manifest_path, bm25, vector_store, doc_store, embedder,
    )

    assert bm25.doc_count["t1"] == 3
    assert doc_store.get("t1", "doc1:0") == "mèo đen"
    assert vector_store.data["t1"]["doc1:2"] == "chim xanh"
    # embed phải gọi 1 lần cho cả batch, không loop từng chunk
    # (không so đúng thứ tự: `to_upsert` xuất phát từ `set()` trong diff_manifest,
    # nên thứ tự batch không đảm bảo — chỉ cần đúng NỘI DUNG được gửi đi)
    assert len(embedder.calls) == 1
    assert sorted(embedder.calls[0]) == sorted(["mèo đen", "chó nâu", "chim xanh"])


def test_ingest_document_second_run_diffs_correctly(tmp_path):
    manifest_path = str(tmp_path / "manifest.json")
    bm25, doc_store, vector_store, embedder = _new_stores()

    ingest_document(
        "t1", "doc1", ["mèo đen", "chó nâu", "chim xanh"],
        manifest_path, bm25, vector_store, doc_store, embedder,
    )
    # lần 2: chunk 0 giữ nguyên, chunk 1 đổi nội dung, chunk 2 (chim xanh) biến mất
    ingest_document(
        "t1", "doc1", ["mèo đen", "chó nâu ĐỔI"],
        manifest_path, bm25, vector_store, doc_store, embedder,
    )

    # chunk 2 phải bị xoá khỏi cả 3 store
    assert "doc1:2" not in vector_store.data["t1"]
    with pytest.raises(KeyError):
        doc_store.get("t1", "doc1:2")
    assert "doc1" not in bm25.index["t1"].get("chim", {})

    # chunk 1 phải được cập nhật nội dung mới
    assert doc_store.get("t1", "doc1:1") == "chó nâu ĐỔI"

    # chunk 0 KHÔNG đổi -> lần embed thứ 2 chỉ gồm chunk 1 (to_skip không embed lại)
    assert embedder.calls[1] == ["chó nâu ĐỔI"]


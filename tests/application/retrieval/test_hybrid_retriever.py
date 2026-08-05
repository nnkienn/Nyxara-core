import pytest

from app.application.retrieval.bm25_index import BM25Index
from app.application.retrieval.hybrid_retriever import HybridRetriever
from app.domain.ports.vector_store import SearchHit


class FakeEmbedder:
    dim = 3

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0, 0.0] for _ in texts]


class FakeVectorStore:
    def __init__(self, hits: list[SearchHit]):
        self._hits = hits

    def upsert(self, tenant_id, ids, texts, vectors) -> None:
        raise NotImplementedError("không cần cho test này")

    def search(self, tenant_id: str, query_vector: list[float], top_k: int) -> list[SearchHit]:
        return self._hits[:top_k]


def _build_bm25() -> BM25Index:
    bm25 = BM25Index()
    bm25.add_document("t1", "doc1", "con mèo đen")
    bm25.add_document("t1", "doc2", "con chó nâu")
    return bm25


def test_doc_found_in_both_sources_beats_doc_only_in_dense():
    # doc2 đứng hạng 1 ở dense (điểm cao nhất) nhưng KHÔNG khớp từ khoá nào trong BM25.
    # doc1 đứng hạng 2 ở dense nhưng khớp cả 2 từ trong BM25 -> phải thắng chung cuộc.
    dense_hits = [
        SearchHit(id="doc2", text="con chó nâu", score=0.9),
        SearchHit(id="doc1", text="con mèo đen", score=0.8),
    ]
    retriever = HybridRetriever(FakeEmbedder(), FakeVectorStore(dense_hits), _build_bm25())

    result = retriever.search("t1", "mèo đen", top_k=5)
    doc_ids = [doc_id for doc_id, _ in result]

    assert doc_ids[0] == "doc1"
    assert doc_ids[1] == "doc2"


def test_score_matches_hand_calculation():
    dense_hits = [
        SearchHit(id="doc2", text="con chó nâu", score=0.9),
        SearchHit(id="doc1", text="con mèo đen", score=0.8),
    ]
    retriever = HybridRetriever(FakeEmbedder(), FakeVectorStore(dense_hits), _build_bm25())

    result = dict(retriever.search("t1", "mèo đen", top_k=5))

    # doc1: rank 2 (dense) + rank 1 (bm25) -> 1/62 + 1/61
    assert result["doc1"] == pytest.approx(1 / 62 + 1 / 61, abs=1e-9)
    # doc2: chỉ rank 1 (dense), không khớp bm25 -> chỉ 1/61
    assert result["doc2"] == pytest.approx(1 / 61, abs=1e-9)


def test_top_k_truncates_final_result():
    dense_hits = [
        SearchHit(id="doc2", text="con chó nâu", score=0.9),
        SearchHit(id="doc1", text="con mèo đen", score=0.8),
    ]
    retriever = HybridRetriever(FakeEmbedder(), FakeVectorStore(dense_hits), _build_bm25())

    result = retriever.search("t1", "mèo đen", top_k=1)

    assert len(result) == 1
    assert result[0][0] == "doc1"

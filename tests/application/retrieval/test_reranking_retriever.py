import pytest

from app.application.retrieval.bm25_index import BM25Index
from app.application.retrieval.hybrid_retriever import HybridRetriever
from app.application.retrieval.reranking_retriever import RerankingRetriever
from app.domain.ports.vector_store import SearchHit
from app.infrastructure.adapters.docstore.in_memory_doc_store import InMemoryDocStore


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


class FakeReranker:
    def __init__(self, score_by_text: dict[str, float]):
        self._score_by_text = score_by_text

    def score(self, query: str, docs: list[str]) -> list[float]:
        return [self._score_by_text[doc] for doc in docs]


def _build_pipeline(reranker) -> RerankingRetriever:
    dense_hits = [
        SearchHit(id="doc2", text="con chó nâu", score=0.9),
        SearchHit(id="doc1", text="con mèo đen", score=0.8),
    ]

    bm25 = BM25Index()
    bm25.add_document("t1", "doc1", "con mèo đen")
    bm25.add_document("t1", "doc2", "con chó nâu")

    doc_store = InMemoryDocStore()
    doc_store.save("t1", "doc1", "con mèo đen")
    doc_store.save("t1", "doc2", "con chó nâu")

    hybrid = HybridRetriever(FakeEmbedder(), FakeVectorStore(dense_hits), bm25)
    return RerankingRetriever(hybrid, doc_store, reranker)


def test_rerank_score_overrides_rrf_order():
    # RRF (đã verify trước đó) xếp doc1 > doc2. Cố tình cho reranker chấm NGƯỢC LẠI
    # (doc2 cao hơn doc1) để chứng minh: thứ hạng CUỐI CÙNG theo cross-encoder,
    # không phải theo RRF -- đúng note đã ghi "RRF score bị THAY bằng cross-encoder score".
    reranker = FakeReranker({"con mèo đen": 0.1, "con chó nâu": 9.9})
    retriever = _build_pipeline(reranker)

    result = retriever.search("t1", "mèo đen", candidate_k=10, top_k=5)
    doc_ids = [doc_id for doc_id, _ in result]

    assert doc_ids[0] == "doc2"
    assert doc_ids[1] == "doc1"


def test_top_k_truncates_final_result():
    reranker = FakeReranker({"con mèo đen": 5.0, "con chó nâu": 1.0})
    retriever = _build_pipeline(reranker)

    result = retriever.search("t1", "mèo đen", candidate_k=10, top_k=1)

    assert len(result) == 1
    assert result[0][0] == "doc1"

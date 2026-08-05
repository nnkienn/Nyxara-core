from app.application.retrieval.bm25_index import BM25Index
from app.application.retrieval.rrf import reciprocal_rank_fusion
from app.domain.ports.embedder import Embedder
from app.domain.ports.vector_store import VectorStore


class HybridRetriever:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore,
        bm25_index: BM25Index,
        rrf_k: int = 60,
    ) -> None:
        self.embedder = embedder
        self.vector_store = vector_store
        self.bm25_index = bm25_index
        self.rrf_k = rrf_k

    def search(self, tenant_id: str, query: str, top_k: int) -> list[tuple[str, float]]:
        candidate_k = top_k * 2

        query_vector = self.embedder.embed([query])[0]
        dense_hits = self.vector_store.search(tenant_id, query_vector, candidate_k)
        dense_ranked = [hit.id for hit in dense_hits]

        bm25_hits = self.bm25_index.search(tenant_id, query, candidate_k)
        bm25_ranked = [doc_id for doc_id, _ in bm25_hits]

        return reciprocal_rank_fusion(
            [dense_ranked, bm25_ranked], k=self.rrf_k, top_k=top_k
        )

from app.application.retrieval.hybrid_retriever import HybridRetriever
from app.domain.ports.doc_store import DocStore
from app.domain.ports.reranker import Reranker


class RerankingRetriever:
    def __init__(
        self,
        hybrid_retriever: HybridRetriever,
        doc_store: DocStore,
        reranker: Reranker,
    ) -> None:
        self.hybrid_retriever = hybrid_retriever
        self.doc_store = doc_store
        self.reranker = reranker

    def search(
        self, tenant_id: str, query: str, candidate_k: int, top_k: int
    ) -> list[tuple[str, float]]:
        candidates = self.hybrid_retriever.search(tenant_id, query, candidate_k)
        doc_ids = [doc_id for doc_id, _ in candidates]
        texts = [self.doc_store.get(tenant_id, doc_id) for doc_id in doc_ids]

        scores = self.reranker.score(query, texts)

        reranked = sorted(zip(doc_ids, scores), key=lambda pair: pair[1], reverse=True)
        return reranked[:top_k]

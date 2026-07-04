from __future__ import annotations
from app.domain.ports.retriever import RetrievalHit
from app.domain.ports.embedder import Embedder
from app.domain.ports.vector_store import VectorStore
from app.application.retrieval.bm25_index import BM25Index
from app.application.retrieval.rrf import reciprocal_rank_fusion


class HybridRetriever:
    def __init__(self, embedder: Embedder, store: VectorStore, bm25: BM25Index) -> None:
        self._embedder = embedder
        self._store = store
        self._bm25 = bm25

    def retrieve(self, query: str, *, tenant_id: str, top_k: int = 5) -> list[RetrievalHit]:
        # Step 1: dense search
        query_vec = self._embedder.embed([query])[0]
        dense_hits = self._store.search("chunks", query_vec, tenant_id=tenant_id, top_k=top_k * 2)
        dense_ranked = [h.id for h in dense_hits]

        # Step 2: BM25 search
        bm25_hits = self._bm25.search(query, tenant_id=tenant_id, top_k=top_k * 2)
        bm25_ranked = [doc_id for doc_id, _ in bm25_hits]

        # Step 3: RRF fusion
        fused = reciprocal_rank_fusion([dense_ranked, bm25_ranked])

        # Step 4: build result
        id_to_hit = {h.id: h for h in dense_hits}
        results = []
        for doc_id, score in fused[:top_k]:
            if doc_id not in id_to_hit:
                continue
            h = id_to_hit[doc_id]
            results.append(RetrievalHit(
                doc_id=doc_id,
                text=h.payload.get("text", ""),
                score=score,
                source=h.payload.get("source_url", ""),
            ))
        return results

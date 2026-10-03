import math
from threading import Lock
from typing import Optional

from app.application.retrieval.metadata_filter import matches


class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.index: dict[str, dict[str, dict[str, int]]] = {}
        self.doc_len: dict[str, dict[str, int]] = {}
        self.doc_count: dict[str, int] = {}
        # metadata[tenant][doc_id] = {"loai": "Nghị định", "nam": 2020} — để search lọc theo cây trung lập
        self.metadata: dict[str, dict[str, dict]] = {}
        self._lock = Lock()

    def add_document(
        self, tenant_id: str, doc_id: str, text: str, metadata: Optional[dict] = None
    ) -> None:
        with self._lock:
            tokens = text.lower().split()
            self.metadata.setdefault(tenant_id, {})[doc_id] = metadata or {}
            self.doc_len.setdefault(tenant_id, {})[doc_id] = len(tokens)
            self.doc_count.setdefault(tenant_id, 0)
            self.doc_count[tenant_id] += 1

            freq: dict[str, int] = {}
            for tok in tokens:
                freq[tok] = freq.get(tok, 0) + 1

            for term, tf in freq.items():
                self.index.setdefault(tenant_id, {}).setdefault(term, {})[doc_id] = tf
    def _idf(self, tenant_id: str, term: str) -> float:
        doc_freq = len(self.index.get(tenant_id, {}).get(term, {}))
        if doc_freq == 0:
            return 0.0
        return math.log((self.doc_count[tenant_id] - doc_freq + 0.5) / (doc_freq + 0.5) + 1)
    def _score(self, tenant_id: str, term: str, doc_id: str) -> float:
        tf = self.index.get(tenant_id, {}).get(term, {}).get(doc_id, 0)
        if tf == 0:
            return 0.0

        doc_len = self.doc_len[tenant_id][doc_id]
        avg_doc_len = sum(self.doc_len[tenant_id].values()) / self.doc_count[tenant_id]

        idf = self._idf(tenant_id, term)
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / avg_doc_len))

        return idf * (numerator / denominator)

    def search(
        self, tenant_id: str, query: str, top_k: int, filter_tree: Optional[dict] = None
    ) -> list[tuple[str, float]]:
        tokens = query.lower().split()
        scores: dict[str, float] = {}

        for term in tokens:
            for doc_id in self.index.get(tenant_id, {}).get(term, {}):
                score = self._score(tenant_id, term, doc_id)
                scores[doc_id] = scores.get(doc_id, 0.0) + score

        # BM25 không có bộ lọc riêng -> chấm xong mới lọc (post-filter), cùng cây với Qdrant.
        # Lọc TRƯỚC khi cắt top_k: cắt trước rồi mới lọc thì có thể còn thiếu (hoặc 0) kết quả.
        if filter_tree is not None:
            tenant_meta = self.metadata[tenant_id]
            scores = {
                doc_id: score
                for doc_id, score in scores.items()
                if matches(filter_tree, tenant_meta[doc_id])
            }

        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return ranked[:top_k]
    def remove_document(self, tenant_id : str , doc_id : str) -> None :
        with self._lock:
            if tenant_id in self.doc_len and doc_id in self.doc_len[tenant_id]:
                del self.doc_len[tenant_id][doc_id]
                self.doc_count[tenant_id] -= 1
            self.metadata.get(tenant_id, {}).pop(doc_id, None)

            for term in list(self.index.get(tenant_id, {})):
                if doc_id in self.index[tenant_id][term]:
                    del self.index[tenant_id][term][doc_id]
                    if not self.index[tenant_id][term]:
                        del self.index[tenant_id][term]
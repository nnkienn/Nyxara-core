import math


class BM25Index:
    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.index: dict[str, dict[str, dict[str, int]]] = {}
        self.doc_len: dict[str, dict[str, int]] = {}
        self.doc_count: dict[str, int] = {}

    def add_document(self, tenant_id: str, doc_id: str, text: str) -> None:
        tokens = text.lower().split()

        self.doc_len.setdefault(tenant_id, {})[doc_id] = len(tokens)
        self.doc_count[tenant_id] = self.doc_count.get(tenant_id, 0) + 1

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

    def search(self, tenant_id: str, query: str, top_k: int) -> list[tuple[str, float]]:
        tokens = query.lower().split()
        scores: dict[str, float] = {}

        for term in tokens:
            for doc_id in self.index.get(tenant_id, {}).get(term, {}):
                score = self._score(tenant_id, term, doc_id)
                scores[doc_id] = scores.get(doc_id, 0.0) + score

        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return ranked[:top_k]
from FlagEmbedding import FlagReranker


class BGEReranker:
    def __init__(self):
        self.model = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=False)

    def score(self, query: str, docs: list[str]) -> list[float]:
        pairs = [[query, doc] for doc in docs]
        return self.model.compute_score(pairs)

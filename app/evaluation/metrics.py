"""Retrieval metrics — chấm điểm danh sách máy khoanh so với đáp án (lát 1)."""


def hit_at_k(results: list[list[str]], answers: list[str], k: int) -> float:
    hits = 0 
    for i in range(len(results)):
        top_k = results[i][:k]
        if answers[i] in top_k:
            hits= hits+1
    return hits / len(results)
def mrr(results: list[list[str]], answers: list[str], k: int) -> float:
    hits = 0 
    for i in range(len(results)):
        top_k = results[i][:k]
        if answers[i] in top_k:
            hits= hits+(1/(len(results) + 1))
    return hits / len(results)
"""Retrieval metrics — chấm điểm danh sách máy khoanh so với đáp án (lát 1)."""

import math


def hit_at_k(results: list[list[str]], answers: list[list[str]], k: int) -> float:
    hits = 0 
    for i in range(len(results)):
        top_k = results[i][:k]
        for answer in answers[i]:
            if answer in top_k:
                hits= hits+1
                break
    return hits / len(results)
def mrr(results: list[list[str]], answers: list[list[str]], k: int) -> float:
    total_rr = 0 
    for i in range(len(results)):
        top_k = results[i][:k]
        for doc in top_k:
            if doc in answers[i]:
                rank = top_k.index(doc) + 1
                rr = 1 /rank
                total_rr += rr
                break
    return total_rr / len(results)


def ndcg_at_k(results: list[list[str]], answers: list[list[str]], k: int) -> float:
    total_ndcg = 0 
    for i in range(len(results)):
        dcg = 0
        top_k= results[i][:k]
        for doc in top_k:
            if doc in answers[i]:
                rank = top_k.index(doc)+1
                dcg+=1/math.log2(rank+1)
        idcg = 0
        ideal_hits = min(len(answers[i]),k)
        for rank in range(1, ideal_hits + 1):
            idcg +=1/math.log2(rank+1)
        total_ndcg += dcg/idcg
    return total_ndcg / len(results)
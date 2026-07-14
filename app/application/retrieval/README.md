# application/retrieval

Phase 2.1 — Hybrid Retrieval. `query → [dense (Qdrant cosine) + BM25] → RRF merge → top_k`.

| File (sẽ build) | Kỹ thuật | CTDLGT |
|---|---|---|
| `bm25_index.py` | Okapi BM25 (k1=1.5, b=0.75) — term→posting list | Hash map / inverted index |
| `rrf.py` | Reciprocal Rank Fusion, `k=60` (Cormack 2009) — scale-invariant merge | Two-pointer / merge N ranked lists |
| `hybrid_retriever.py` | orchestrate dense + BM25 + RRF | — |

Interface: `app/domain/ports/retriever.py`.

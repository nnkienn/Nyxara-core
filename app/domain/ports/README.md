# domain/ports

Interfaces thuần Python (`typing.Protocol`), zero framework/library import. Đây là "hợp đồng"
mà mọi adapter ở `infrastructure/` phải tuân theo — domain không biết Qdrant hay BGE là gì.

| File (sẽ build) | Phase | Ghi chú |
|---|---|---|
| `chunker.py` | 0 | Protocol cho recursive/semantic chunker |
| `embedder.py` | 1 | `dim` property + `embed()` |
| `vector_store.py` | 1 | `SearchHit` dataclass + upsert/search |
| `retriever.py` | 2.1 | Hybrid retriever interface |
| `reranker.py` | 2.2 | Cross-encoder rerank interface |
| `metering.py` | 9 | 0 import stripe — chỉ đo, không tính tiền |
| `entitlement.py` | 9 | Feature flag theo gói khách (cloud enforce) |
| `null_adapters.py` | 9 | Fake/no-op adapter để core chạy standalone không cần cloud |

Xem [LEARNING_ROADMAP.md](../../../Learning-document/LEARNING_ROADMAP.md) để biết method signature chi tiết từng port.

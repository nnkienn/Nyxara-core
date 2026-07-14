# infrastructure/adapters

Cắm implementation thật vào `domain/ports/`. Domain/application không bao giờ import thẳng
thư viện bên thứ 3 — chỉ adapter mới được.

| Thư mục | Phase | File (sẽ build) |
|---|---|---|
| `embedder/` | 1 | `bge_embedder.py` — load `BAAI/bge-m3`, embed batch → `list[list[float]]` |
| `vectorstore/` | 1 | `qdrant_store.py` — ensure_collection, upsert idempotent (UUID5), search với **tenant filter bắt buộc** |
| `reranker/` | 2.2 | `bge_reranker.py` — cross-encoder `bge-reranker-v2-m3`, đọc query+doc cùng 1 forward pass |

**Debug drill Phase 1:** cố tình bỏ `tenant_id` filter trong 1 test → chứng minh nó *không*
crash mà trả nhầm dữ liệu tenant khác (silent failure đắt giá nhất của multi-tenancy).

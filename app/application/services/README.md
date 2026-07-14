# application/services

Phase 2.4 — phần mở rộng của Advanced Retrieval, bật sau khi lõi (hybrid/rerank/CRAG) chạy được.

| File (sẽ build) | Kỹ thuật | Ưu tiên | CTDLGT |
|---|---|---|---|---|
| `mmr.py` | Maximal Marginal Relevance — `λ·relevance − (1−λ)·max_sim_to_selected` | 🟡 | Priority queue |
| `query_transform.py` | multi-query, HyDE, step-back | 🟡 | — |
| `context_compressor.py` | cắt nhiễu, xử lý Lost-in-the-Middle | 🟡 | — |

**Bug cố ý MMR:** đảo dấu `λ` → top-k toàn bản trùng. Debug bằng cách in điểm marginal từng ứng viên mỗi vòng.

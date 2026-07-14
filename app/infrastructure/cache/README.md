# infrastructure/cache

Phase 3.5 — Query Performance. Chỉ mở sau khi profiling thấy chỗ nghẽn thật (premature
optimization = bẫy kinh điển).

| File (sẽ build) | Kỹ thuật | Ưu tiên |
|---|---|---|
| `semantic_cache.py` | cache theo *ý nghĩa* (cosine sim giữa query mới và query đã cache) | 🟢 |

**Bug cố ý:** ngưỡng cosine quá thấp (0.7) → trả cache cho câu khác ý. Debug bằng cách log
`(query, matched_cache_query, sim)` để thấy false-hit.

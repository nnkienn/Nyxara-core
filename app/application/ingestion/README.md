# application/ingestion

Phase 0. Pipeline có trạng thái: cùng 1 doc chạy lại không được nhân đôi (idempotent).

| File (sẽ build) | Kỹ thuật | Ưu tiên |
|---|---|---|
| `pipeline.py` | dedup (SHA-256 exact trước, near-dup sau) + incremental ingest (seen-set theo hash) + versioning | 🔴 |

**Code tay trước:** SHA-256 exact-dedup, rồi near-dup bằng MinHash/edit-distance để thấy DP thật.

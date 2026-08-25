# 🗺️ Pipeline — sổ tay trace luồng (document → CRAG → answer)

> Gộp lại từ 3 file cũ (`retrieval-pipeline.md` · `crag-pipeline.md` · `ingest-to-crag-pipeline.md`,
> nay đã xoá) thành **1 bộ theo đúng thứ tự chạy thật**, để trace không bị nhảy lung tung giữa
> nhiều file. Đọc theo số thứ tự — mỗi file là 1 chặng, chặng sau giả định bạn đã hiểu chặng trước.

> 🚩 **Đang trace lại toàn luồng?** Dùng [00-trace-exercises.md](./00-trace-exercises.md) —
> bộ câu hỏi tự kiểm tra theo 4 trạm, kèm cảnh báo: 4 file note bên dưới có ít nhất **3 chỗ
> mô tả lệch với code thật**. Đừng đọc để nhớ, đọc để bắt lỗi.

## Thứ tự đọc (khớp đúng thứ tự 1 request chạy qua)

| # | File | Chặng | Trace bằng cách nào |
|---|---|---|---|
| 1 | [01-ingest.md](./01-ingest.md) | Document thô → chunk → ghi vào 3 kho | Gọi `POST /ingest`, đọc `pipeline.py::ingest_document` |
| 2 | [02-retrieval.md](./02-retrieval.md) | Query → tìm trong 3 kho → top-k đoạn liên quan | Đọc `HybridRetriever` + `RerankingRetriever` |
| 3 | [03-crag.md](./03-crag.md) | Retrieval đó chấm điểm, lặp lại nếu tệ, rồi sinh câu trả lời | Đọc `graph.py`/`node.py`, gọi `POST /ask` |
| 4 | [04-api.md](./04-api.md) | 2 chặng trên được bọc thành HTTP endpoint thế nào | Đọc `main.py` (lifespan) + `ask.py`/`ingest.py` |

**Muốn trace nhanh nhất:** chạy `uvicorn` thật (xem [04-api.md](./04-api.md)), gọi `/ingest` rồi
`/ask` bằng `curl`, vừa đọc log terminal vừa mở đúng file theo thứ tự 1→4 ở trên, khớp từng dòng
log với đúng hàm đang chạy.

---

## Sơ đồ tổng (rút gọn — chi tiết từng chặng xem file tương ứng)

```
Document thô
    │
    ▼  [01] chunk + ingest_document (so hash cũ/mới, chỉ ghi phần đổi)
┌─────────────────────────────────────────────┐
│   3 KHO:  BM25Index · QdrantStore · DocStore  │
└─────────────────────────────────────────────┘
    ▲                                    │
    │ ghi (ingest)              đọc (retrieval)
    │                                    ▼
[04] POST /ingest                [02] RerankingRetriever
                                  (Hybrid: dense+sparse+RRF
                                   → rerank cross-encoder)
                                          │
                                          ▼  candidate_docs (đã có text)
                                  [03] CRAG: retrieve → grade → generate
                                  (lặp lại retrieve nếu grade = INCORRECT,
                                   có `attempts` chặn lặp vô hạn)
                                          │
                                          ▼
                                  [04] POST /ask  →  {answer}
```

---

## 2 bug thật gặp khi trace qua HTTP (không cái nào `pytest` bắt được — đọc trước khi tự trace)

- **#24** — thiếu tầng `RerankingRetriever` khi wiring (`main.py` truyền thẳng `HybridRetriever` có
  3 tham số `.search()`, nhưng CRAG `retrieve_node` cần đúng 4 tham số). Xem [02-retrieval.md](./02-retrieval.md)
  và [04-api.md](./04-api.md).
- **#25** — `manifest.json` (bền, trên đĩa) lệch pha với 3 kho in-memory (mất khi restart) → ingest
  lại tưởng thành công nhưng thực ra bị bỏ qua (`to_skip` oan). Xem [01-ingest.md](./01-ingest.md).

Chi tiết đầy đủ (triệu chứng/nguyên nhân/fix) ở [../bug-log.md](../bug-log.md), bug #20-#25.

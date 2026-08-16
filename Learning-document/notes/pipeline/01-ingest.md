# 1️⃣ Ingest — document thô → 3 kho

> Chặng đầu tiên. Bắt đầu khi có 1 tài liệu, kết thúc khi cả 3 kho (BM25 + Qdrant + DocStore)
> có đúng dữ liệu mới nhất. File chính: `app/application/ingestion/pipeline.py::ingest_document`.

---

## Kể chuyện trước

1. Có 1 tài liệu thô (`text`), gọi `POST /ingest` (xem [04-api.md](./04-api.md)) hoặc gọi thẳng
   `ingest_document(...)` nếu test tay.
2. `recursive_chunk(text, size, overlap)` cắt thành `chunks: list[str]`.
3. `ingest_document` **không ghi mù** — nó so với lần ingest trước (`manifest`) để biết chunk nào
   thật sự cần làm gì:
   - **Mới hoặc đổi nội dung** → `to_upsert` — phải embed lại, ghi vào cả 3 kho.
   - **Giữ nguyên** → `to_skip` — bỏ qua, không tốn embed (bước đắt nhất).
   - **Đã biến mất** (doc bị rút ngắn) → `to_delete` — xoá khỏi cả 3 kho.
4. Ghi xong, lưu lại `manifest` mới để lần sau so tiếp.

---

## Sơ đồ

```
                          Document thô (text)
                                  │
                                  ▼
                    recursive_chunk(text, size, overlap)
                                  │
                                  ▼
                          chunks: list[str]
                                  │
                                  ▼
   ┌───────────────────────────────────────────────────────────┐
   │  ingest_document(tenant_id, doc_id, chunks, manifest_path,   │
   │                   bm25_index, vector_store, doc_store,        │
   │                   embedder)                                    │
   └───────────────────────────────────────────────────────────┘
                                  │
        1. manifest = load_manifest(manifest_path)
        2. old_doc  = get_doc_manifest(manifest, tenant_id, doc_id)
        3. new_doc  = {str(i): hash(chunk) for i, chunk in enumerate(chunks)}
        4. to_upsert, to_skip, to_delete = diff_manifest(old_doc, new_doc)
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼ to_delete                                          ▼ to_upsert
  .remove_document()                              embedder.embed(texts)  ← 1 lần/batch
  .delete()  (Qdrant)                                        │
  .delete()  (DocStore)                                     vectors
  (gọi trên cả 3 kho)                                        │
        │                                          doc_store.save() +
        │                                          bm25_index.add_document()
        │                                          vector_store.upsert()
        └─────────────────────────┬─────────────────────────┘
                                  ▼
              manifest[tenant_id][doc_id] = new_doc
              save_manifest(manifest_path, manifest)
```

---

## ⚠️ Bẫy khi trace: `manifest.json` bền, 3 kho không bền (bug #25)

`manifest.json` ghi **xuống đĩa** (`data/manifest.json`), sống sót qua restart server. Nhưng
`BM25Index`, `QdrantStore(":memory:")`, `InMemoryDocStore` chỉ sống **trong RAM** — mất sạch mỗi
khi `uvicorn --reload` restart. Hậu quả: restart xong, gọi `/ingest` lại **cùng 1 doc** →
`diff_manifest` thấy hash khớp với `manifest.json` cũ → xếp vào `to_skip` → **không ghi gì vào 3
kho vừa rỗng** — dù response vẫn báo `200 OK`.

**Khi trace mà thấy retrieval trả rỗng dù vừa `/ingest`:** việc đầu tiên phải nghi là
`rm data/manifest.json` rồi ingest lại, trước khi nghi ngờ logic retrieval.

---

## Test tương ứng (chạy để xác nhận từng bước còn đúng)

```bash
.venv/bin/python3 -m pytest tests/application/ingestion/test_pipeline.py -v
```

`test_ingest_document_writes_to_all_three_stores` và
`test_ingest_document_second_run_diffs_correctly` verify đúng luồng trên (bằng fake
`VectorStore`/`Embedder`, không cần model/Qdrant thật).

**Tiếp theo:** [02-retrieval.md](./02-retrieval.md) — dữ liệu vừa ghi vào 3 kho được đọc lại
như thế nào khi có 1 câu hỏi.

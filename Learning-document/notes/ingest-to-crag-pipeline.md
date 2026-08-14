# 🗺️ Ingest → CRAG — bức tranh toàn cảnh + chỗ cắm Port

> Vẽ sau khi xong Việc 1 (ingest hợp nhất, 2026-08-14), trước khi làm `/ask` API.
> Gộp lại **toàn bộ đường đi** của 1 tài liệu — từ lúc còn là text thô, qua ingest,
> nằm trong 3 kho, tới lúc 1 câu hỏi HTTP đi vào CRAG và có câu trả lời đi ra.
> Đánh dấu rõ **🔌 Port** (interface đã tách, đổi adapter không sửa code gọi nó) vs
> **⚠️ chưa có Port** (class cụ thể, đổi implementation phải sửa chỗ gọi).

---

## Kể chuyện trước (đọc nếu sơ đồ dưới còn rối)

**Nửa đầu — INGEST (ghi vào kho, làm ở Việc 1):**
1. Có 1 tài liệu thô → chunk thành nhiều đoạn nhỏ (`chunks: list[str]`).
2. `ingest_document(...)` so sánh với lần ingest trước (`diff_manifest`) → biết đoạn nào
   mới/đổi (`to_upsert`), đoạn nào biến mất (`to_delete`), đoạn nào giữ nguyên (`to_skip`, bỏ qua).
3. Ghi đồng thời vào **3 kho**: `BM25Index` (từ khoá), `VectorStore`/Qdrant (vector), `DocStore`
   (text gốc) — chỉ đoạn `to_upsert` mới cần gọi `Embedder` (bước đắt tiền nhất).

**Nửa sau — QUERY / CRAG (đọc ra, trả lời, làm ở Việc 2):**
1. HTTP `POST /ask` gửi `{tenant_id, query}` vào.
2. `retrieve` — tìm trong `VectorStore` + `BM25Index` (qua `HybridRetriever`), rồi tra text
   thật từ `DocStore`.
3. `grade` — LLM (`Grader`) chấm từng đoạn có liên quan không → `verdict`.
4. Đủ tốt → `generate` (LLM `Generator` sinh câu trả lời). Tệ → quay lại `retrieve` (tìm rộng
   hơn), có `attempts` chặn lặp vô hạn — xem chi tiết nhánh này ở [crag-pipeline.md](./crag-pipeline.md).
5. Trả `{answer}` ra HTTP response.

---

## Sơ đồ đầy đủ

```
                              Document thô (text)
                                      │
                                      ▼
                        chunking (recursive_chunker.py)
                     ⚠️ CHƯA CÓ PORT — domain/ports/chunker.py
                     chỉ mới là ý định trong roadmap, chưa build
                                      │
                                      ▼
                            chunks: list[str]
                                      │
                                      ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │  ingest_document(tenant_id, doc_id, chunks, manifest_path,          │
   │                   bm25_index, vector_store, doc_store, embedder)    │
   │  — hàm ĐIỀU PHỐI, không phải Port, chỉ gọi các Port bên dưới đúng   │
   │  thứ tự (xem load_manifest/diff_manifest ở pipeline.py)             │
   └───────────────────────────────────────────────────────────────────┘
                                      │
                to_delete             │             to_upsert (mới/đổi)
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             │                             ▼
  .remove_document()          (to_skip: bỏ qua,           🔌 Embedder (Port)
  .delete()                    không đụng gì cả)          BGEEmbedder (adapter)
  .delete()                                                        │
  (gọi trên cả 3 kho                                          vectors
   bên dưới)                                                       │
        │                                                          ▼
        └──────────────────────────┬───────────────────────────────┘
                                    ▼
        ┌─────────────────────────────────────────────────────────┐
        │                      3 KHO (storage)                      │
        │                                                           │
        │   🔌 VectorStore (Port)        ⚠️ BM25Index               │
        │   domain/ports/vector_store.py  (class cụ thể — roadmap:  │
        │   → QdrantStore (adapter)        "để lại Port khi thật    │
        │                                    sự cần đổi impl khác") │
        │                                                           │
        │            🔌 DocStore (Port)                             │
        │            domain/ports/doc_store.py                      │
        │            → InMemoryDocStore (adapter)                   │
        └─────────────────────────────────────────────────────────┘

╔═══════════════════════ ranh giới INGEST | QUERY ═══════════════════════╗

                     HTTP  POST /ask {tenant_id, query}
                                      │
                                      ▼
   ┌───────────────────────────────────────────────────────────────────┐
   │  graph.invoke({query, tenant_id, attempts: 0})                      │
   │  build_graph(retriever, doc_store, grader, generator)  — graph.py    │
   └───────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                          NODE: retrieve (node.py)
        ┌─────────────────────────────────────────────────────────┐
        │  ⚠️ HybridRetriever / RerankingRetriever                   │
        │  (class cụ thể — CHƯA CÓ Port riêng, roadmap Phase 2.1:    │
        │   "để lại khi thật sự cần đổi implementation khác")        │
        │  bọc bên trong: 🔌 Embedder + 🔌 VectorStore + ⚠️ BM25Index  │
        └─────────────────────────────────────────────────────────┘
                                      │  (doc_id, score) → tra text
                                      ▼
                       🔌 DocStore.get(tenant_id, doc_id)
                                      │
                                      ▼
                            NODE: grade (node.py)
                       🔌 Grader (Port) — domain/ports/grader.py
                       → OllamaGrader (adapter, qwen2.5:3b qua Tailscale)
                                      │
                                      ▼
                                verdict là gì?
                         ┌────────────┴────────────┐
                  CORRECT/AMBIGUOUS          INCORRECT (attempts<max)
                         │                    → quay lại NODE: retrieve
                         ▼
                          NODE: generate (node.py)
                       🔌 Generator (Port) — domain/ports/generator.py
                       → OllamaGenerator (adapter, cùng model)
                                      │
                                      ▼
                         HTTP response {answer}
```

---

## Bảng Port — chỗ nào cắm được, đổi sang gì thì cần

| Port (interface) | File | Adapter hiện tại | Đổi sang gì thì cần Port này |
|---|---|---|---|
| 🔌 `Embedder` | `domain/ports/embedder.py` | `BGEEmbedder` | model embedding khác (OpenAI, Cohere, model fine-tune riêng) |
| 🔌 `VectorStore` | `domain/ports/vector_store.py` | `QdrantStore` | Pinecone, Weaviate, pgvector |
| 🔌 `DocStore` | `domain/ports/doc_store.py` | `InMemoryDocStore` | Postgres, Redis, S3 (mất data khi restart nếu còn in-memory) |
| 🔌 `Grader` | `domain/ports/grader.py` | `OllamaGrader` | LLM khác làm giám khảo (OpenAI, Claude) |
| 🔌 `Generator` | `domain/ports/generator.py` | `OllamaGenerator` | LLM khác sinh câu trả lời |
| 🔌 `Reranker` | `domain/ports/reranker.py` | `BGEReranker` | Cohere rerank API, cross-encoder khác |
| ⚠️ *(chưa có Port)* | — | `BM25Index` (tự viết tay) | Elasticsearch, Tantivy, Qdrant sparse vector native |
| ⚠️ *(chưa có Port)* | — | `HybridRetriever`/`RerankingRetriever` | thay hẳn chiến lược retrieval (vd Elasticsearch lo cả hybrid) |
| ⚠️ *(chưa có Port)* | — | `recursive_chunker.py` (hàm thuần) | semantic chunking, LLM-based chunking |

**Vì sao 3 dòng cuối chưa có Port mà vẫn ổn:** đúng nguyên tắc "tránh abstraction sớm" đã ghi
trong roadmap Phase 2.1 — chỉ tách Port khi **thật sự** cần đổi implementation, không tách
trước "cho chắc". Ingest/CRAG hiện chỉ có 1 cách làm (`BM25Index` tự viết, `HybridRetriever`
cụ thể) nên chưa cần Port; sẽ tách khi Eval (Phase 3) chứng minh cần đổi.

---

## 1 điểm dễ nhầm

**`BM25Index` và `HybridRetriever` KHÔNG có Port**, khác với `Embedder`/`VectorStore`/`DocStore`/
`Grader`/`Generator` (5 cái đó đều đã tách Port từ đầu). Nhìn sơ đồ trên: `ingest_document` và
`retrieve_node` vẫn gọi thẳng `bm25_index.add_document(...)`/`bm25_index.search(...)` như 1 class
cụ thể, không qua interface nào — nếu sau này đổi sang Elasticsearch, phải sửa trực tiếp những
chỗ gọi này (không chỉ đổi 1 dòng khởi tạo adapter như 5 Port kia).

---

## Xem thêm

- [crag-pipeline.md](./crag-pipeline.md) — chi tiết nhánh lặp `retrieve ↔ grade` bên trong CRAG.
- [retrieval-pipeline.md](./retrieval-pipeline.md) — chi tiết luồng Dense + BM25 + RRF + Rerank.
- [bug-log.md](./bug-log.md) — bug #20-#23 gặp phải khi xây phần ingest ở sơ đồ trên.

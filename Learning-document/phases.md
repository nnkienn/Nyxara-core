# 📚 Kho kiến thức — 10 Phase

> Tách khỏi `LEARNING_ROADMAP.md` ngày 2026-09-18. Đây là **kho tra cứu**: công thức, WHY,
> gợi ý bug cố ý, file gợi ý. **Không phải thứ tự làm.**
>
> ⚠️ **Thứ tự làm = lát cắt 0→6** ở [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md).
> Các Phase viết từ tháng 8, bảng lát cắt viết 17/09 — **đá nhau thì lấy bảng lát cắt**.
> Mỗi Phase chỉ có *một phần* được học sâu (🔴), phần còn lại 🟡 hoặc 🟢 — xem bản đồ ngay dưới.

## Bản đồ Phase → lát cắt

Các Phase **không bị xoá** — chúng là **kho kiến thức** (công thức, WHY, bug cố ý gợi ý). Thứ tự làm = lát 0→6.
Mỗi Phase giờ chỉ có **một phần** được học sâu; phần còn lại ở mức 🟡 hoặc 🟢. Số `#` = số dòng trong bảng của Phase đó.

| Phase | Đã xong | 🔴 Học sâu (lát) | 🟡 Nhỏ (lát) | 🟢 Chỉ nói được |
|---|---|---|---|---|
| **0** Ingestion | #1 recursive · #6 dedup · #7 incremental | #9 Document-based theo Điều/Khoản · #11 parse văn bản *(lát 2)* | #4 Parent-Child · #10 Contextual *(lát 2)* · #8 Versioning *(lát 4)* | #2 Semantic · #3 Proposition · #5 Multi-vector |
| **1** Vector | ✅ toàn bộ | — | — | — |
| **2** Retrieval | Hybrid · RRF · Rerank · CRAG | #1 Metadata filter *(lát 0)* · #2 Query Transform *(lát 2)* | #4 MMR *(lát 2)* · #5 Compression / Lost-in-the-Middle *(lát 3)* · #3 Temporal *(lát 4)* | #6 Adaptive-RAG · #7 GraphRAG · #8 Multimodal |
| **3** Eval ⭐ | — | #1 Hit@k/MRR/NDCG · #4 Golden · #5 Regression · #6 A/B *(lát 1)* · #2 Judge · #3 Faithfulness *(lát 3)* | #7 Hiệu chỉnh judge *(lát 3)* · #9 Chi phí/latency *(lát 6)* | #8 Online eval · #10 Bias · #11 RAG vs long-context |
| **3.5** Performance | — | — | #1 Đo latency từng chặng · #6 Cache + prompt caching *(lát 6)* | #2 Payload index · #3 HNSW · #4 Quantization · #5 Budget 2 tầng · #7 Async batching · #8 Semantic cache |
| **4** Agent | — | #1 Supervisor · #2 Tool calling · #7 Tracing · #8 MCP · #12 Đo đường đi *(lát 5)* · #5 Từ chối *(lát 3)* | #4 Memory · #6 HITL *(lát 5)* | #3 Intent triage · #10 Routing · #11 Feedback → train · #9 Prompt craft *(luyện xuyên suốt, không thành mốc)* |
| **5** Safety | — | #1 Chống prompt injection *(lát 3)* | — | #2 PII · #3 Moderation · #4 Output sanitization · #5 Red-team · #6-#11 |
| **6** Fine-tune | — | — | — | Toàn bộ: LoRA/QLoRA · quantization · synthetic data · embedding FT |
| **7** MLOps | Vector delete/sync (kéo lên P0) | — | CI/CD chạy regression eval · deploy + demo URL · Load test p50/p95 *(lát 6)* | Model serving (vLLM) · LGTM · Drift · Embedding migration · Retrain · Canary |
| **8** Community | — | — | — | Toàn bộ (plugin registry, entry-points) |
| **9** SaaS Bridge | Multi-tenancy (P1) | — | — | Toàn bộ (Metering/Entitlement Port) — xét lại khi quay về N Assistant |

**Tóm lại, học sâu thật ở 5 Phase:** **0** (phần còn lại) · **2** (phần còn lại) · **3** · **4** · **5** (một mục).
**3.5 và 7** học ở mức nhỏ trong lát 6. **6, 8, 9** chỉ học để nói được trong phỏng vấn.


## Phase 0 — Foundation & Ingestion Pipeline

> 🧭 **Mức học từ 17/09:** 🔴 #9 #11 · 🟡 #4 #8 #10 · 🟢 #2 #3 #5 · ✅ #1 #6 #7 — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

> **Rác vào = rác ra.** Retrieval giỏi tới đâu cũng vô nghĩa nếu chunk sai. Đây là nền.

### Kiến thức cốt lõi
- **Chunking granularity** quyết định chất lượng retrieval: chunk quá to → nhiễu; quá nhỏ → mất ngữ cảnh.
- Ingestion là **pipeline có trạng thái**: cùng 1 doc chạy lại không được nhân đôi (idempotent).
- Doc thay đổi theo thời gian → cần **versioning** + **incremental ingest** thay vì re-ingest toàn bộ.

> **🔨 Trạng thái (2026-08-14):** Mở rộng ingest từ "chỉ append-only" (Incremental ✅ cũ, chỉ
> dedupe theo hash) thành **multi-store CRUD đồng bộ** (BM25 + Qdrant + DocStore ghi/xoá cùng lúc).
> Lý do: ingest lại doc đã sửa/xoá đang để lại **orphan** trong BM25/Qdrant vì `pipeline.py` cũ
> chưa có thao tác xoá — đúng ra thuộc Phase 7 (Data lifecycle: vector CRUD/delete/sync) nhưng
> kéo sớm lên đây vì ingest cần nó ngay để không nợ kỹ thuật.
> **Thứ tự (theo vòng 6 bước):**
> 1. ✅ `BM25Index.remove_document` — **XONG 2026-08-14** (9 test pass, bug #20 — quên trừ
>    `doc_count`, xem [bug-log](notes/bug-log.md))
> 2. ✅ `VectorStore.delete` / `QdrantStore.delete` — **XONG 2026-08-14** (3 test pass, bug #21
>    — `delete_points` không tồn tại, đúng là `client.delete`)
> 3. ✅ `DocStore.delete(tenant_id, doc_id)` — **XONG 2026-08-14** (3 test pass, không bug —
>    tiện thể tạo luôn `tests/infrastructure/adapters/docstore/` vì trước đó `InMemoryDocStore`
>    chưa từng có test, kể cả `save`/`get`)
> 4. ✅ Redesign manifest: `(tenant_id, doc_id) → {chunk_index: content_hash}` — **XONG
>    2026-08-14** (`load_manifest`/`save_manifest`/`get_doc_manifest` trong `pipeline.py`,
>    3 test pass, bug #22 — 2 lần thụt lề sai liên tiếp; giữ song song `load_seen`/`incremental_ingest`
>    cũ, gộp lại ở bước 6 ráp orchestrator)
> 5. ✅ Hàm diff thuần: `to_upsert` / `to_skip` / `to_delete` — **XONG 2026-08-14** (`diff_manifest`
>    trong `pipeline.py`, so 2 manifest bằng `set` union + so hash từng `chunk_index`, 4 test pass,
>    không bug — verify tay trước bằng ví dụ 4 case rồi mới viết test chính thức)
> 6. ✅ Ráp `ingest_document` orchestrator (BM25Index + VectorStore + DocStore + Embedder) —
>    **XONG 2026-08-14** (2 test integration pass: ghi đủ 3 store lần đầu + diff đúng lần 2
>    (xoá/đổi/giữ nguyên), embed batch 1 lần không loop từng chunk; bug #23 — giả định sai thứ
>    tự của `set()` khi viết assert, không phải bug ở `ingest_document`). **66/66 test toàn
>    project pass.**
> Toàn bộ pipeline ingest hợp nhất (Việc 1 của buổi) đã xong.
>
> **🔨 Trạng thái (2026-09-06) — Phase 0 gần đóng, còn 3 việc:**
> - ✅ **Bug #25 FIX THẬT** (treo 14/08 → 06/09, 23 ngày). Manifest bỏ file trên đĩa, thành
>   `dict` trong RAM (`app.state.manifest`) — chọn hướng *"cùng dễ vỡ"* thay vì *"cùng bền"*;
>   hướng bền (Qdrant server thật + persistence cho BM25/DocStore) đẩy sang **Phase 5**.
>   Test chặn tái phát: `test_restart_thi_quen_sach_khong_skip_oan` (2 khối `with TestClient`
>   ngang hàng = 2 đời tiến trình), đã chứng minh đỏ được.
> - ✅ **Bug #30** — `/ingest` báo cáo trung thực: `ingest_document` trả `dict[str,int]`,
>   response thêm `chunk_upserted`/`chunk_skipped`/`chunk_deleted` (additive change).
> - ✅ **Bug #31** — `lifespan` có phần shutdown, nhả model khỏi VRAM.
> - ⬜ **Bug #29** — race condition `BM25Index.doc_count` (`threading.Lock`). Đã chẩn đoán xong
>   05/09 (mất 56.9% số lần cộng khi 4 luồng), **chưa fix**.
> - ⬜ **Trạm 4d** — `def` vs `async def` trong handler.
> - ⬜ Nối `split_by_separators` vào pipeline (hàm mồ côi từ 17/07, có test xanh, không ai gọi).
> Suite đo thật 06/09 trên Fedora 44 / Python 3.14.7: **70 passed in 127.34s**.
>
> ✅ **Việc 2 — `/ask` API (bọc `graph.py` vào FastAPI) — XONG 2026-08-14, verify qua HTTP
> thật (không phải chỉ `pytest`):**
> - `app/presentation/api/ask.py` — `POST /ask {tenant_id, query}` → `{answer}`.
> - `app/presentation/api/ingest.py` — `POST /ingest {tenant_id, doc_id, text}` → tái dùng
>   `ingest_document`, để có cách nạp data qua HTTP (không chỉ `pytest`).
> - `app/main.py` — `lifespan` dựng 1 lần: `BGEEmbedder` → `QdrantStore`(`:memory:`) →
>   `BM25Index` → `InMemoryDocStore` → `HybridRetriever` → **`BGEReranker` + `RerankingRetriever`**
>   (bọc ngoài Hybrid, bắt buộc — `retrieve_node` cần `.search(tenant_id, query, candidate_k,
>   top_k)` 4 tham số, không phải `HybridRetriever` trần chỉ có 3) → `OllamaGrader`/
>   `OllamaGenerator` → `build_graph(...)`, lưu vào `app.state`.
> - Cả 2 handler viết `def` (không `async def`) — tránh chặn event loop khi gọi model/HTTP
>   đồng bộ bên trong (`graph.invoke`, `embedder.embed`, `vector_store.upsert`).
> - **Verify thật:** `curl /ingest` rồi `curl /ask` với Ollama thật (qua Tailscale) → trả lời
>   đúng bám nội dung đã ingest, không bịa.
> - **3 bug thật gặp khi trace qua HTTP** (không cái nào `pytest` bắt được — bài học lớn nhất
>   buổi này): #24 (thiếu tầng `RerankingRetriever`, `pytest` xanh vì Fake khớp sai giả định),
>   #25 (`manifest.json` bền lệch pha 3 kho dễ vỡ khi `--reload` restart). Xem chi tiết
>   [bug-log.md](notes/bug-log.md).
> - Sơ đồ tổng thể (trace theo thứ tự): [notes/pipeline/](notes/pipeline/README.md).

### Danh sách kỹ thuật

| # | Kỹ thuật | Học được gì | Ưu tiên | CTDLGT |
|---|----------|------------|---------|--------|
| 1 | **Recursive character chunking** | tách theo phân cấp separator (`\n\n`→`\n`→` `) | 🔴 | Sliding window |
| 2 | **Semantic chunking** | cắt theo điểm gãy ngữ nghĩa (embedding distance giữa câu) | 🟡 | — |
| 3 | **Proposition chunking** | LLM tách doc thành mệnh đề độc lập, atomic | 🟢 | — |
| 4 | **Parent-Child retrieval** | match chunk nhỏ, trả parent lớn → context đủ | 🟡 | Hash map (child→parent) |
| 5 | **Multi-vector** | 1 doc → nhiều vector (summary + chunks) | 🟢 | — |
| 6 | **Deduplication** | chặn chunk trùng/gần trùng (hash + near-dup) | 🔴 | Set / Bloom / edit-distance DP |
| 7 | **Incremental ingest** | chỉ ingest phần mới/đổi (seen-check theo hash) | 🔴 | Hash set |
| 8 | **Versioning** | giữ lịch sử chunk, rollback được | 🟡 | — |
| 9 | **Document-based chunking** | cắt theo cấu trúc doc (heading → section → subsection). Heading do NGƯỜI viết = ranh giới ngữ nghĩa có sẵn → thường thắng Semantic mà rẻ hơn hàng trăm lần. Hợp Markdown/HTML/legal/technical doc | 🔴 | Cây phân cấp / stack (theo dõi heading level) |
| 10 | **Contextual Retrieval** | LLM sinh 1–2 câu định vị chunk trong document → prepend vào chunk TRƯỚC khi embed. Trả giá lúc ingest thay vì lúc query | 🟡 | — |
| 11 | **Document parsing — đọc file thật** (PDF có bảng · DOCX · HTML · scan cần OCR) | ⭐ **THÊM 2026-09-06 — lỗ hổng lớn nhất của roadmap.** Cả pipeline hiện bắt đầu từ `text: str` sẵn có, tức bỏ qua đúng chỗ RAG thật chết nhiều nhất. Học: layout-aware parsing · **bảng phải giữ cấu trúc** (bảng flatten thành text là mất nghĩa hoàn toàn) · header/footer/số trang là rác phải lọc · khi nào cần OCR và OCR sai thì hỏng gì downstream · chọn giữa parser rẻ (pypdf) vs layout-aware (Unstructured/Docling) và **cái giá từng cái** | 🔴 | Cây layout · state machine đọc bảng |

### Cách học hiệu quả (code tay)
- **CODE TAY:** viết `recursive_chunk(text, size, overlap)` bằng tay TRƯỚC — đừng gọi
  `RecursiveCharacterTextSplitter`. Tự xử overlap bằng sliding window.
- **BUG CỐ Ý:** đặt overlap > size, hoặc quên cộng offset → chunk mất chữ giữa 2 mảnh.
- **DEBUG:** in `[(start, end)]` từng chunk, kiểm tra `chunk[i].end - overlap == chunk[i+1].start`.
- **Dedup:** tự viết SHA-256 exact-dedup trước; rồi near-dup bằng MinHash/edit-distance để thấy DP thật.

### Files gợi ý
```
app/application/chunking/recursive_chunker.py
app/application/chunking/semantic_chunker.py
app/application/ingestion/pipeline.py        # dedup + incremental + versioning
app/domain/ports/chunker.py
tests/application/test_recursive_chunker.py   # test overlap boundary
```

### Next steps
Chunk đúng → embed → nạp Qdrant (Phase 1). Sau khi có Eval (Phase 3), quay lại A/B
so recursive vs semantic chunking trên chính niche của bạn.

> **Góc nhìn gom nhóm (2026-08-25):** #4 Parent-Child, #10 Contextual Retrieval (và *Late
> Chunking* — đã cân nhắc và **loại**) đều chữa **cùng một bệnh**: chunk bị cắt rời khỏi document
> nên vector mất ngữ cảnh. Khác nhau ở chỗ trả giá bằng gì (lúc query / lúc ingest / đổi interface).
> *Late Chunking* loại vì phá hợp đồng port `Embedder` (`embed(texts) -> vectors` phải đổi thành
> `embed_document(text, spans)`) — chi phí kiến trúc lớn, lợi ích chưa chứng minh.
> *LLM-based chunking* loại: trùng lợi ích với #3 Proposition chunking nhưng đắt hơn.
>
> **Biến cần A/B ở Phase 3 (đừng để thành hằng số thiêng):** `chunk_size=200` ký tự và
> `chunk_overlap=20` trong `app/presentation/api/ingest.py` là số gõ đại lúc dựng API, chưa ai đo.
> BGE-M3 nuốt được 8192 token — 200 ký tự (~50 token) là *một lựa chọn*, không phải chân lý.

---

## ✅ Phase 1 — Vector Memory (Embedding + Qdrant + Tenant Isolation)

> 🧭 **Mức học từ 17/09:** ✅ xong toàn bộ — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

**Trạng thái: ✅ XONG (2026-07-19)** — port Embedder/VectorStore + cosine similarity (tay) +
BGEEmbedder + QdrantStore (DI constructor · upsert idempotent UUID5 · `search` có tenant filter
→ `SearchHit`). Đã có test tenant-isolation + drill "silent failure" (bug #13). Bug đã ghi:
#8 cosine · #10 ensure_collection · #11 rename biến · #12 point id UUID · #13 tenant leak · #14 API `.search`→`.query_points`.

### Kiến thức học được
- **Vector Embedding**: ánh xạ text → vector 1024 chiều bằng contrastive learning. Không phải hash — là learned representation từ hàng tỷ cặp câu.
- **Cosine Similarity**: đo góc giữa 2 vector, invariant với magnitude. L2-normalized → rút gọn thành dot product.
- **Tenant Isolation**: single-collection multi-tenancy với mandatory `tenant_id` filter. **Silent failure nếu bỏ filter** — đây là bug bảo mật tệ nhất: không crash, chỉ rò dữ liệu tenant khác.

### Files sẽ build (gõ lại bằng tay)

| File dự kiến | Mô tả |
|------|-------|
| `app/domain/ports/embedder.py` | Embedder Protocol — dim property + embed() method |
| `app/domain/ports/vector_store.py` | VectorStore Protocol — SearchHit dataclass |
| `app/infrastructure/adapters/embedder/bge_embedder.py` | BGEEmbedder — load BAAI/bge-m3, embed batch → list[list[float]] |
| `app/infrastructure/adapters/vectorstore/qdrant_store.py` | QdrantStore — ensure_collection, upsert (idempotent UUID5), search với tenant filter |

### Tests sẽ viết (mục tiêu)
- `test_bge_embedder.py`: dim, empty guard, 1024 dims, batch
- `test_qdrant_store.py`: ensure idempotent, upsert count, UUID5 deterministic, **tenant filter**, None payload

### Debug drill (bước 2–3 của vòng học)
Cố tình bỏ `tenant_id` filter trong 1 test → chứng minh nó *không* crash mà trả nhầm
dữ liệu tenant khác. Bài học "silent failure" đắt giá nhất của multi-tenancy.

---

## 🔨 Phase 2 — Advanced Retrieval (Hybrid + Rerank + CRAG + …)

> 🧭 **Mức học từ 17/09:** ✅ Hybrid/RRF/Rerank/CRAG · 🔴 #1 #2 · 🟡 #3 #4 #5 · 🟢 #6 #7 #8 — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

> **Trạng thái:** 2.1 và 2.2 đã build lại xong bằng tay (2026-08-03/04), full trace +
> test pass. 2.3 (CRAG) chưa bắt đầu — xem [🎯 Next Action](#-bảng-theo-dõi-tiến-độ-checklist).

### 2.1 BM25 + Hybrid Retrieval + RRF — ✅ XONG 2026-08-03

**Kiến thức học được:**
- **TF-IDF vs BM25**: TF-IDF có 2 vấn đề — TF không saturation + không chuẩn hóa độ dài doc.
  BM25 sửa bằng `k1` (TF saturation) và `b` (length normalization).
```
score(d,t) = IDF(t) × TF×(k1+1) / (TF + k1×(1-b+b×dl/avgdl))
IDF(t)     = log((N - df + 0.5) / (df + 0.5) + 1)
k1 = 1.5 (TF saturation)   ·   b = 0.75 (length normalization)
```
- **RRF — Reciprocal Rank Fusion**: cosine ∈ [0,1], BM25 ∈ [0,∞) — khác đơn vị, không cộng
  trực tiếp. RRF chuyển cả 2 về **rank** → scale-invariant.
```
RRF(d) = Σ 1/(k + rank_i(d))    k=60 (Cormack 2009)
```
- **HybridRetriever flow:**
```
query
  ├─→ embed(query) → Qdrant cosine (top 2k) → dense_ranked
  ├─→ BM25.search(query, tenant_id) (top 2k) → bm25_ranked
  └─→ RRF([dense_ranked, bm25_ranked]) → top_k RetrievalHit
```

**Files đã build:** `app/application/retrieval/bm25_index.py` · `rrf.py` · `hybrid_retriever.py`
(⚠️ `app/domain/ports/retriever.py` — **chưa build**, `HybridRetriever` hiện là class cụ thể,
chưa có Port riêng; để lại khi thật sự cần đổi implementation khác, tránh abstraction sớm)
**Tests:** 16 test (`test_bm25_index.py` 8 · `test_rrf.py` 5 · `test_hybrid_retriever.py` 3) — pass, khớp tay
**CTDLGT chạm tay:** inverted index (hash map term→postings), merge N ranked lists (two-pointer).
**Bug thật gặp (xem [bug-log](notes/bug-log.md)):** #15 (`int | None` cần Python 3.10, dự án chạy 3.9)
· #16 (thụt lề 2 lần: dead code chặn trước + unexpected indent) · #17 (`QdrantStore.search`
trả UUID nội bộ thay vì `doc_id` gốc — phát hiện lúc ghép `HybridRetriever`, không phải lúc chạy).
**Sơ đồ tổng:** [notes/pipeline/02-retrieval.md](notes/pipeline/02-retrieval.md).

### 2.2 Cross-encoder Reranking (bge-reranker-v2-m3) — ✅ XONG 2026-08-04
- **Bi-encoder vs Cross-encoder**: bi-encoder encode query/doc riêng rồi so vector.
  Cross-encoder đọc query+doc **cùng 1 forward pass** → chính xác hơn nhưng chậm hơn.
- **Vì sao 2 bước:** Hybrid lọc nhanh top-20/50 → cross-encoder chấm kỹ. Không thể
  chạy cross-encoder trên 10,000 docs. RRF score bị **thay** bằng cross-encoder score.
- **Lỗ hổng phát hiện khi ghép (không có trong kế hoạch ban đầu):** `HybridRetriever` chỉ trả
  `(doc_id, score)`, không có text để đưa vào reranker → thêm `DocStore` (Port) +
  `InMemoryDocStore` (adapter) + `RerankingRetriever` (nối Hybrid → tra text → rerank → sort)
  để giải quyết. Production thật sẽ thay `InMemoryDocStore` bằng Postgres/Redis, giữ nguyên Port.

**Files đã build:** `app/domain/ports/reranker.py` · `app/infrastructure/adapters/reranker/bge_reranker.py`
· `app/domain/ports/doc_store.py` · `app/infrastructure/adapters/docstore/in_memory_doc_store.py`
· `app/application/retrieval/reranking_retriever.py`
**Tests:** 5 test (`test_bge_reranker.py` 2, model thật · `test_reranking_retriever.py` 2 ·
`test_qdrant_store.py` +1 regression cho bug #17) — pass
**Bug thật gặp:** nhầm model (`bge-m3` thay vì `bge-reranker-v2-m3`, khiến classifier head
random-init) · gọi nhầm method (`.rerank()` không tồn tại, đúng là `compute_score()`).

### 2.3 CRAG (Corrective RAG via LangGraph) — ✅ XONG 2026-08-12
- **State machine**: `state` = "tờ giấy" chạy qua các **node** (trạm), điền dần từng ô.
- **Node = hàm** (`state → dict`); **edge** = ray cố định; **conditional edge** = rẽ theo **router**.
- **grade → verdict → correct**: LLM-as-judge chấm YES/NO từng doc → `decide()` đếm ra
  CORRECT/AMBIGUOUS/INCORRECT (ngưỡng `>=0.6`/`<=0.0`, là tham số) → INCORRECT thì quay lại
  `retrieve` (tìm rộng hơn). `attempts` (tăng trong `grade_node`, vì conditional edge không
  được sửa state) guard chặn lặp vô hạn — verify bằng graph thật: luôn CORRECT → đi thẳng;
  luôn INCORRECT → lặp đúng `max_attempts` lần rồi van an toàn cưỡng bức generate.
- **Hạ tầng LLM thật lần đầu dùng trong dự án:** Ollama (`qwen2.5:3b`, CPU 4-core/16GB) chạy
  trên server riêng, nối qua Tailscale (mesh VPN, không cần mở port ra Internet) — `grader.py`
  (chấm YES/NO) và `generator.py` (sinh câu trả lời) đều gọi qua HTTP (`httpx`) tới cùng model.

**Files đã build:** `app/application/generation/` → `state.py · node.py (retrieve/grade/generate) ·
decision.py (decide/route) · graph.py` + `app/domain/ports/grader.py`, `generator.py` +
`app/infrastructure/adapters/grader/ollama_grader.py`, `adapters/generator/ollama_generator.py`
**Tests:** 17 test (`test_decision.py` 6 · `test_node.py` 4 · `test_graph.py` 2 e2e ·
`test_ollama_grader.py` 5 mock · `test_ollama_generator.py` 3 mock) — tất cả pass, không cần mạng
**Bug thật gặp:** `#18` httpx timeout mặc định 5s quá ngắn cho LLM · `#19` `.upper()` xong so
sánh với chuỗi chữ thường → luôn `False` (xem [bug-log](notes/bug-log.md)).
**CTDLGT chạm tay:** graph (node/edge, conditional routing, cycle guard qua `attempts`), closure
(node "nhớ" dependency đã inject).

### 2.4 Còn lại của Advanced RAG — ⏳ chưa build

> 🧭 **Đồng bộ 2026-09-18:** cột **Ưu tiên** dưới đây đã chỉnh lại cho khớp **bản đồ lát cắt 17/09 (mục F)** —
> mục F là nguồn sự thật, bảng này trước đó còn giữ mức cũ. Thêm cột **Lát** để khỏi phải dò lại.
> Thay đổi thật: **#2 Query Transformation 🟡 → 🔴** · **#6 Adaptive-RAG 🟡 → 🟢**.

| # | Kỹ thuật | Học được gì | Ưu tiên | Lát | CTDLGT |
|---|----------|------------|---------|-----|--------|
| 1 | **Metadata filtering** | lọc trước semantic search (dùng thật trong Comment Assistant) | 🔴 | **0** | Filter predicate tree |
| 2 | **Query Transformation** (Multi-Query · HyDE · **Step-back**) | query↔doc space mismatch; mở rộng/nâng cấp query. **Miền luật:** dân hỏi *"mở quán cà phê cần giấy gì"*, luật viết *"đăng ký kinh doanh hộ cá thể"* | 🔴 | **2** | — |
| 3 | **Temporal / Freshness-aware** + **time-decay** | `harvested_at` → payload Qdrant → recency scoring; chunk cũ = rác dù đúng topic. **Miền luật:** gắn với trạng thái **còn/hết hiệu lực**, không chỉ là mới/cũ | 🟡 | **4** | — |
| 4 | **MMR** (Maximal Marginal Relevance) | tránh top-k gần trùng → bao phủ nhiều khía cạnh | 🟡 | **2** | Priority queue |
| 5 | **Context Compression** + **Lost-in-the-Middle** | cắt nhiễu; LLM quên phần giữa → đặt chunk quan trọng ở đầu/cuối | 🟡 | **3** | — |
| 6 | **Adaptive-RAG / Self-RAG** | quyết định *có nên retrieve không* ngay từ đầu (anh em ruột CRAG) | 🟢 | — | — |
| 7 | **GraphRAG** (Knowledge Graph + multi-hop) | câu hỏi nối nhiều mẩu; vector thuần yếu chỗ này | 🟢 | — | **Graph BFS/DFS** |
| 8 | **Multimodal RAG** | ảnh sản phẩm / bảng / PDF, transcript | 🟢 | — | — |

### Cách học hiệu quả (code tay) cho 2.4
- **MMR — bài CTDLGT đẹp nhất:** tự viết vòng chọn k phần tử, mỗi bước maximize
  `λ·relevance − (1−λ)·max_sim_to_selected`. **BUG CỐ Ý:** đảo dấu `λ` → top-k quay ra
  toàn bản trùng. **DEBUG:** in điểm marginal từng ứng viên mỗi vòng.
- **Metadata filtering:** tự viết filter predicate trước khi đẩy xuống Qdrant `Filter` — hiểu
  pre-filter (lọc rồi search) vs post-filter (search rồi lọc) khác nhau về recall thế nào.
- **HyDE:** LLM sinh câu trả lời giả → embed *nó* thay vì query. In ra để thấy vì sao vá được mismatch.

### Files gợi ý
```
app/application/services/mmr.py
app/application/services/query_transform.py    # multi_query, hyde, step_back
app/application/services/context_compressor.py
app/application/graphrag/                       # entity extract → graph → multi-hop
```

### Next steps
*(cập nhật 18/09 — theo lát cắt, không theo thứ tự bảng)* **Lát 0:** metadata filtering.
**Lát 2:** Query Transformation (🔴) rồi MMR (🟡). **Lát 3:** compression. **Lát 4:** temporal theo hiệu lực.
Adaptive-RAG / GraphRAG / Multimodal chỉ cần **nói được** — đọc ~1h, trả lời 3-5 câu đóng sách, không build.
**Đừng build hết rồi mới đo** — mỗi cái xong đẩy qua Phase 3 (lát 1 dựng sẵn harness để làm đúng việc đó).

---

## Phase 3 — Evaluation Framework (đo trước, tin sau) ⭐ PHASE QUAN TRỌNG NHẤT

> 🧭 **Mức học từ 17/09:** 🔴 #1-#6 · 🟡 #7 #9 · 🟢 #8 #10 #11 — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

> **Không có eval = bay mù.** Mọi kỹ thuật ở Phase 2 chỉ được **bật** khi eval chứng minh
> nó *thật sự* cải thiện. Đây là kỹ năng **phân biệt Senior với junior** rõ nhất: junior
> "nghe nói kỹ thuật X hay nên bật", Senior "đo thấy X +6% context-recall trên golden set
> nên bật, nhưng nó −40ms latency nên tắt cho niche realtime". **Câu phỏng vấn Senior kinh
> điển: "Làm sao bạn biết thay đổi này tốt hơn?" — không trả lời được = trượt.**

### Hai loại eval phải tách bạch (đừng lẫn)
| | **Retrieval eval** (tầng tìm) | **Generation eval** (tầng sinh) |
|---|---|---|
| Đo cái gì | kho trả về đúng doc không | câu trả lời có đúng/bám context không |
| Metric | Hit@k, MRR, NDCG, context-precision/recall | faithfulness, answer-relevancy, correctness |
| Cần nhãn | doc nào đúng (relevance label) | câu trả lời chuẩn (hoặc LLM-judge) |
| Rẻ/đắt | rẻ, deterministic — **chạy mỗi commit** | đắt (gọi LLM) — chạy theo mốc |

> **Nguyên tắc:** debug retrieval eval TRƯỚC. Nếu kho trả sai doc thì LLM giỏi mấy cũng bịa.

### Kiến thức cốt lõi (hiểu công thức, không chỉ gọi hàm)
- **Hit@k / Recall@k**: trong top-k có ít nhất 1 doc đúng không / bắt được bao nhiêu % doc đúng.
- **MRR** (Mean Reciprocal Rank) = trung bình `1/rank` của doc đúng đầu tiên — thưởng xếp hạng cao.
- **NDCG**: có phân biệt mức độ liên quan (không chỉ đúng/sai) + phạt theo vị trí (log discount).
- **RAGAS**: `faithfulness` = tỉ lệ claim trong answer *được context hậu thuẫn*;
  `answer_relevancy` = answer có trả đúng câu hỏi; `context_precision` = doc đúng có xếp trên đầu không.
- **Golden dataset**: (query, doc_đúng, answer_chuẩn) cố định + **versioned** (`golden/v1.jsonl`) —
  đổi golden phải bump version, không sửa lén (nếu không A/B mất ý nghĩa).
- **Regression set**: mỗi bug production → 1 ca vĩnh viễn ở đây, chống tái phát.
- **A/B testing**: bật/tắt đúng **1 biến**, chạy cùng golden, so delta metric + **significance**
  (n nhỏ thì +2% có thể là nhiễu — cần đủ mẫu).
- **Online eval**: traffic thật, implicit feedback (click / user sửa / thumbs) — khác offline.
- **LLM-judge calibration**: judge cũng lệch (thiên vị câu dài, vị trí) → phải đo agreement với
  nhãn người (Cohen's κ) trước khi tin judge.
- **Cost-Quality trade-off** (tư duy Senior cốt tử): eval **KHÔNG chỉ đo accuracy**. Mỗi kỹ thuật
  còn có giá — `cost/query` (token), `latency` (p50/p95), `throughput`. Reranker +5% recall nhưng
  +120ms có thể *không đáng* cho niche realtime. Senior quyết bằng **cả 2 trục** chất lượng ↔ chi phí.

### Danh sách kỹ thuật

| # | Kỹ thuật | Học được gì | Ưu tiên | CTDLGT / Code tay |
|---|----------|------------|---------|--------|
| 1 | **Retrieval metrics** (Hit@k · MRR · NDCG) | đo tầng tìm, deterministic, chạy mỗi commit | 🔴 | sort + log-discount |
| 2 | **Custom LLM Judge** | tự viết prompt chấm + parse **structured** (JSON), retry | 🔴 | prompt eng + JSON parse |
| 3 | **RAGAS** (faithfulness · relevancy · context precision/recall · answer correctness) | metric chuẩn ngành cho generation | 🔴 | — |
| 4 | **Golden dataset** + versioning | chuẩn cố định, versioned (không sửa tùy hứng) | 🔴 | data management |
| 5 | **Regression set** | mỗi bug → 1 test vĩnh viễn | 🔴 | — |
| 6 | **A/B harness** + significance | so 2 cấu hình (vd: with/without MMR) | 🔴 | statistical testing |
| 7 | **Judge calibration** (κ / Pearson vs nhãn người) | biết judge có đáng tin không | 🟡 | correlation metrics |
| 8 | **Online eval** | traffic thật (click · dwell time · thumbs) | 🟡 | feedback loop |
| 9 | **Cost & Efficiency metrics** | tokens · latency (p50/p95) · cost/query · throughput | 🔴 | profiling |
| 10 | **Bias & Fairness check** | model có lệch theo niche / độ dài query không | 🟢 | statistical fairness |
| 11 | **RAG vs long-context — đo để biết khi nào KHÔNG cần RAG** | ⭐ **THÊM 2026-09-06.** Context window đã dài ra rất nhiều, nên *"khi nào KHÔNG nên dùng RAG?"* là câu phân loại Senior. Dựng cùng một golden set, chạy 2 nhánh: (a) RAG top-k · (b) nhét thẳng cả document vào context. So **4 trục**: chất lượng · chi phí/query · độ trễ p95 · khả năng trích dẫn nguồn. Kết luận phải là **một ngưỡng cụ thể** ("dưới N nghìn token thì long-context thắng"), không phải cảm tính | 🔴 | — |

### Cách học hiệu quả (code tay) — làm theo thứ tự
1. **CODE TAY retrieval metrics TRƯỚC** (rẻ, deterministic): tự viết `hit_at_k`, `mrr`, `ndcg`
   trên list rank + set doc đúng. Đây là bài **sort + reciprocal + log-discount** thuần.
   → chạy được ngay trên pipeline đã có, chưa cần LLM.
2. **CODE TAY `faithfulness_score()`**: tách answer thành claim, mỗi claim hỏi judge "có trong
   context không", đếm tỉ lệ. RỒI mới so với `ragas` để kiểm chứng bản tay.
3. **CODE TAY A/B harness**: hàm nhận `(pipeline_A, pipeline_B, golden)` → trả bảng delta metric.

**BUG CỐ Ý (bắt buộc, 3 ca kinh điển):**
- **Judge parse lỏng:** `"yes" in text` → câu *"No, this is not yes-worthy"* bị chấm YES.
  **DEBUG:** log (raw_output, parsed) → thấy vì sao phải parse structured JSON/regex chặt.
- **NDCG sai log base / off-by-one rank:** rank bắt đầu từ 0 thay vì 1 → discount lệch toàn bộ.
  **DEBUG:** tính tay 3 doc, so với hàm.
- **A/B rò biến:** đổi *2 thứ* cùng lúc (reranker + chunk size) → không biết cái nào gây delta.
  **DEBUG:** kỷ luật "1 biến / 1 lần đo".
- **Golden sửa ngầm:** đổi golden mà không bump version → A/B trước/sau so trên 2 bộ khác nhau,
  kết luận vô nghĩa. **DEBUG:** log hash của dataset mỗi lần chạy, so hash trước/sau.

### 🎯 Bài tập thực hành (làm đủ 4 — đây là "đồ án" của Phase 3)
1. Xây **golden dataset 50–100 cặp** `(query, context, ideal_answer)` cho **niche của bạn**.
2. Viết **custom judge** (code tay) → chạy → **so kết quả với RAGAS** để kiểm chứng bản tay.
3. Chạy **A/B test** thật: `HybridRetriever` vs `Hybrid + MMR` trên golden → giữ/bỏ MMR theo số.
4. Thêm **regression test** cho đúng bug bạn từng gặp (vd "Lost-in-the-Middle" ở Phase 2) →
   nó thành lưới chống tái phát vĩnh viễn.

### Files gợi ý
```
app/evaluation/
├── judge.py                    # Custom LLM Judge + structured parse + retry
├── metrics.py                  # faithfulness, relevancy — TỰ implement trước
├── retrieval_metrics.py        # hit@k, mrr, ndcg — code tay, deterministic
├── ragas_runner.py             # đối chiếu với bản tay
├── ab_harness.py               # A/B + statistical significance
├── calibration.py              # human vs LLM judge agreement (κ / Pearson)
├── cost_metrics.py             # tokens · latency · cost/query · throughput
├── golden/
│   ├── v1.jsonl                # versioned — bump version khi đổi, không sửa lén
│   └── v2.jsonl
└── regression/
    └── test_lost_in_middle.py  # mỗi bug production → 1 file ở đây
tests/evaluation/test_retrieval_metrics.py   # tính tay đối chiếu
```

### Next steps
1. **Tuần này:** xây Golden Dataset + Custom Judge (bài tập 1–2).
2. Implement **A/B Harness** (bài tập 3).
3. **Quay lại Phase 2** đo từng kỹ thuật (metadata filter, MMR, temporal, rerank…) →
   **chỉ giữ cái thắng rõ rệt** trên golden của niche bạn (cả trục chất lượng ↔ cost).
4. **Tích hợp eval vào CI:** mỗi PR phải **pass regression set** + không tụt metric quá ngưỡng.
   → biến "đo trước, tin sau" thành **cổng tự động**, không phụ thuộc kỷ luật con người.             
> Đây là **vòng lặp trung tâm của cả dự án**: *thêm kỹ thuật → eval → giữ/bỏ*.
> Không có bước này, roadmap chỉ là sưu tầm kỹ thuật.

---

## Phase 3.5 — Query Performance (đo trước, tối ưu sau)

> 🧭 **Mức học từ 17/09:** 🟡 #1 #6 (+ prompt caching) · 🟢 phần còn lại — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

> **Premature optimization = bẫy kinh điển.** Chỉ tối ưu khi pipeline chạy đúng VÀ đã
> profiling thấy chỗ nghẽn thật.

| # | Kỹ thuật | Học được gì | Ưu tiên |
|---|----------|------------|---------|
| 1 | **Latency profiling** | đo từng chặng (embed/dense/sparse/rerank) trước khi đụng | 🔴 |
| 2 | **Qdrant payload indexing** | index `tenant_id`/`timestamp`/`parent_id` → filter nhanh | 🟡 |
| 3 | **HNSW tuning** (`m`, `ef_construct`, `ef_search`) | đánh đổi recall ↔ latency | 🟡 |
| 4 | **Vector quantization** (scalar/product) | giảm RAM + tăng tốc, mất ít recall | 🟡 |
| 5 | **Two-stage budget tuning** | cân `top_k` retrieve vs rerank (rerank đắt nhất) | 🟡 |
| 6 | **Caching (Redis)** | cache embedding query + kết quả lặp | 🟡 |
| 7 | **Async + batching** | embed/search song song, gộp batch | 🟡 |
| 8 | **Semantic caching** | cache theo *ý nghĩa* (2 câu khác chữ cùng ý → hit) | 🟢 |

### Cách học hiệu quả
- **CODE TAY:** tự viết decorator `@timed` gom latency từng chặng vào dict trước khi
  cắm LangFuse. Profiling bằng số thật, không đoán.
- **BUG CỐ Ý:** semantic cache đặt ngưỡng cosine quá thấp (0.7) → trả cache cho câu khác ý.
  **DEBUG:** log (query, matched_cache_query, sim) → thấy false-hit.

**Files gợi ý:** `app/infrastructure/cache/semantic_cache.py` · `app/observability/timing.py`

---

## Phase 4 — Agentic Orchestrator (LangGraph)

> 🧭 **Mức học từ 17/09:** 🔴 #1 #2 #5 #7 #8 #12 · 🟡 #4 #6 · 🟢 #3 #10 #11 — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

> Từ RAG một phát → **agent nhiều bước** biết dùng tool, nhớ ngữ cảnh, có người gác cổng.

### Kiến thức cốt lõi
- **Multi-agent**: Supervisor điều phối → Researcher → Creator → Critic → Human gate.
- **Tool calling** cần **structured output / constrained decoding**: ép JSON hợp lệ, retry khi lỗi.
- **Memory**: multi-turn / thread memory — nhớ hội thoại, không single-shot.
- **HITL** (human-in-the-loop): chặn hành động rủi ro chờ người duyệt.
- **Tracing (LangFuse)**: soi agent nhiều bước chạy gì, hỏng ở node nào — KHÔNG thể thiếu.
- **MCP (Model Context Protocol)**: chuẩn hiện đại gắn tool/context — học sớm, đừng tự chế.

### Danh sách kỹ thuật

| # | Kỹ thuật | Học được gì | Ưu tiên | CTDLGT |
|---|----------|------------|---------|--------|
| 1 | **Supervisor multi-agent** | điều phối nhiều agent | 🔴 | Graph |
| 2 | **Tool calling** + structured output | ép JSON, retry | 🔴 | — |
| 3 | **Intent triage** | phân loại comment: trả lời/lờ/đẩy người → tiết kiệm LLM | 🔴 | — |
| 4 | **Multi-turn memory** | nhớ thread hội thoại | 🔴 | Ring buffer |
| 5 | **Abstention "tôi không biết"** | từ chối có hiệu chỉnh thay vì đoán bừa | 🔴 | — |
| 6 | **HITL gate** | người duyệt trước khi gửi | 🟡 | — |
| 7 | **Tracing (LangFuse)** | step-level observability | 🔴 | — |
| 8 | **MCP** | chuẩn gắn tool/context | 🟡 | — |
| 9 | **Prompt engineering craft** (CoT, few-shot, dynamic example selection) | kỹ năng nền nhất | 🔴 | — |
| 10 | **Query routing** (multi-source/multi-tool) | chọn kho/tool nào — sâu hơn intent triage | 🟡 | — |
| 11 | **Human-feedback → training loop** | edit của người duyệt → data train (active learning) | 📡 🟢 | — |
| 12 | **Agent evaluation — đo ĐƯỜNG ĐI, không chỉ đo câu trả lời** | ⭐ **THÊM 2026-09-06.** Phase 3 đo RAG = đo **kết quả cuối**; agent nhiều bước phải đo **trajectory**: chọn đúng tool không · số bước tới khi xong · có lặp/quẩn không · chi phí + token mỗi task · tỉ lệ chạm HITL gate. Cùng một bài học với bug #26/#29: **assert kết quả cuối là mù với bug nằm trong quá trình** — agent trả lời đúng bằng đường đi ngu ngốc vẫn là hỏng | 🔴 | Graph traversal · so khớp chuỗi hành động |

### Cách học hiệu quả (code tay)
- **CODE TAY:** tự dựng StateGraph supervisor bằng LangGraph (bạn đã làm CRAG — tái dùng skill).
  Tự viết retry-loop cho tool call lỗi JSON TRƯỚC khi dùng structured-output helper.
- **BUG CỐ Ý:** để supervisor không có điều kiện dừng → agent loop vô hạn gọi tool.
  **DEBUG:** đọc LangFuse trace, đếm số vòng, thêm `max_steps` guard (như `attempts` ở CRAG).

**Files gợi ý:** `app/application/agent/supervisor.py` · `app/application/agent/tools/` · `app/application/agent/memory.py`

### Next steps
Cắm LangFuse ngay từ agent đầu tiên — debug agent không trace = tự trói tay.

---

## Phase 5 — Safety & Guardrails (áo giáp)

> 🧭 **Mức học từ 17/09:** 🔴 #1 · 🟢 phần còn lại — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

> UGC (user-generated content) **không tin được**. Agent phơi ra internet cần giáp 2 chiều.

### Danh sách kỹ thuật

| # | Kỹ thuật | Học được gì | Lớp | Ưu tiên |
|---|----------|------------|-----|---------|
| 1 | **Prompt injection defense** | chặn input độc lái agent | core | 🔴 |
| 2 | **PII redaction** | phát hiện + che SĐT/địa chỉ (PDPD/GDPR) | core | 🔴 |
| 3 | **Toxicity / moderation** (in + out) | lọc chửi bới 2 chiều | core | 🟡 |
| 4 | **Output sanitization** (XSS/markdown injection) | làm sạch *output* trước render — khác injection input | core | 🔴 |
| 5 | **Red-teaming / jailbreak** | tự tấn công tìm lỗ trước kẻ xấu | core | 🟡 |
| 6 | **Output guardrail framework** | tầng policy có hệ thống (ngoài Critic) | core | 🟡 |
| 7 | **Self-consistency / SelfCheckGPT** | phát hiện bịa bằng sample nhiều lần so chéo | core | 🟢 |
| 8 | **Graceful degradation** | Qdrant/LLM sập → xuống cấp êm | core | 🟡 |
| 9 | **Rate limiting** | chặn spam | core *đo* · **cloud** *enforce* | 🟡 |
| 10 | **Cost guard + circuit breaker** | chặn nổ bill | core *đo* · **cloud** *enforce* | 🔴 |
| 11 | **SAST — quét lỗ hổng code tĩnh** (Fortify, Semgrep, Bandit) | khác hẳn 1-10 (an toàn *AI*) — đây là an toàn *code truyền thống* (SQL injection, dependency CVE...), quét trước khi build/deploy | CI/CD (không phải core AI) | 🟡 |

### Cách học hiệu quả (code tay)
- **CODE TAY PII:** tự viết Trie/regex matcher cho SĐT VN + email TRƯỚC khi dùng Presidio.
  → luyện đúng CTDLGT **Trie/pattern matching**.
- **BUG CỐ Ý (injection):** để prompt template nối thẳng UGC → nhét "ignore previous
  instructions" thấy agent bị lái. **DEBUG:** thấy vì sao phải tách data/instruction (delimiter, role).
- **Circuit breaker:** tự viết state machine CLOSED→OPEN→HALF_OPEN — lại là bài **state machine**.

**Files gợi ý:** `app/safety/pii.py` · `app/safety/injection.py` · `app/safety/circuit_breaker.py` · `app/safety/sanitize.py`

---

## Phase 6 — Fine-tuning

> 🧭 **Mức học từ 17/09:** 🟢 toàn bộ — chỉ nói được — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

| Kỹ thuật | Học được gì | Ưu tiên |
|---|---|---|
| **LoRA / QLoRA** trên `Qwen2.5-7B` | low-rank update math (tự tính ΔW = BA) | 🛠️ 🔴 |
| **Synthetic data generation** | sinh data train khi data thật ít | 🛠️ 🟡 |
| **GGUF quantization** (Q4/Q5/Q8) merge | nén model chạy local | 🛠️ 🟡 |
| **Embedding / domain fine-tuning** | chỉnh bge-m3 cho niche | 🛠️ 🟡 |

### Cách học hiệu quả (code tay)
- **CODE TAY:** tự implement LoRA layer thuần PyTorch (`W + (B@A)*scale`) trên 1 linear nhỏ,
  train toy task → hiểu vì sao chỉ update rank thấp mà vẫn học được. RỒI mới dùng PEFT.
- **BUG CỐ Ý:** quên freeze base weights → mất điểm low-rank. **DEBUG:** đếm trainable params.

**Files gợi ý:** `experiments/lora/manual_lora.py` · `experiments/lora/train_qwen.py`

---

## Phase 7 — MLOps & Production

> 🧭 **Mức học từ 17/09:** 🟡 CI/CD · deploy + demo · load test · 🟢 phần còn lại — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

> Phần **vector CRUD/delete/sync** của "Data lifecycle" bên dưới đã kéo sớm lên
> [Phase 0](#phase-0--foundation--ingestion-pipeline) (2026-08-14) vì ingest cần nó ngay;
> phần còn lại (embedding migration khi đổi model) vẫn nằm ở đây.

| Kỹ thuật | Học được gì | Ưu tiên |
|---|---|---|
| **Model serving** (vLLM / TGI cho LLM · **NVIDIA Triton** cho model vision/đa dạng hơn, vd YOLO) | phục vụ inference throughput cao (paged attention, dynamic batching) | 🛠️ 🔴 |
| **Observability stack** — **LGTM**: Prometheus (metric) + **Loki** (log) + **Tempo** (trace) + Grafana (dashboard), thu thập qua **Grafana Alloy/OpenTelemetry** (chuẩn chung, không lệ thuộc 1 hãng) | metric/log/trace/alert hạ tầng — 3 trụ observability tách bạch (metric đo *bao nhiêu*, log đo *chuyện gì xảy ra*, trace đo *chậm ở đâu trong chuỗi service*) | 🛠️ 🔴 |
| **Load testing** (Locust) | giả lập nhiều user gọi `/ask` cùng lúc, đo hệ thống chịu được bao nhiêu request/s trước khi thật sự deploy | 🛠️ 🟡 |
| **Data lifecycle** | vector CRUD/delete/sync · dedup · incremental · **embedding migration** (re-embed khi đổi model) | 🛠️ 🔴 |
| **Drift detection** | data / embedding / concept drift — chất lượng tụt âm thầm | 🛠️ 🟡 |
| **Eval-at-scale** | online eval · regression · prompt versioning · judge calibration | 🛠️ 🟡 |
| **CI/CD** (Jenkins/GitHub Actions — build/test/deploy tự động mỗi lần push) | nền tảng đưa code lên production an toàn, lặp lại được | 🛠️ 🔴 |
| **CI/CD retrain** + experiment tracking (W&B/MLflow) · versioning (DVC/HF) | reproducible ML — khác CI/CD ở trên (đây riêng cho vòng lặp retrain model) | 📡 🟢 |
| **Canary / blue-green deploy** · DR/backup · scaling/backpressure | tung model an toàn, chịu tải | 📡 🟢 (nhiều phần **cloud**) |

### Cách học hiệu quả
- Phân biệt rạch ròi: **agent tracing (LangFuse, Phase 4)** ≠ **observability hạ tầng (Prometheus/Loki/Tempo)**.
  Cái đầu cần lúc BUILD agent (soi 1 lần chạy agent cụ thể); cái sau đo cả hệ thống theo thời gian.
- **Drift:** tự viết so phân bố embedding tuần này vs tuần trước (PSI / KL divergence) trước khi dùng tool.
- **Load test:** chạy Locust nhắm vào `/ask` sau khi có endpoint thật (Việc 2 hôm nay) — đo p50/p95
  latency khi có 10/50/100 user cùng hỏi, thấy điểm nghẽn thật (LLM call thường là nút cổ chai).

**Files gợi ý:** `app/observability/metrics.py` · `ops/serving/vllm.yaml` · `app/lifecycle/reembed.py` · `ops/loadtest/locustfile.py`

---

## Phase 8 — Extensibility & Community (Open Source)

> 🧭 **Mức học từ 17/09:** 🟢 toàn bộ — chỉ nói được — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

> Open source thắng/thua ở chỗ **người lạ có mở rộng được không**. Lõi khó hiểu = chết.

| Kỹ thuật | Học được gì | Ưu tiên |
|---|---|---|
| **Plugin system** (scraper / LLM client / retriever) | Port + Adapter, đăng ký động | 🛠️ 🔴 |
| **Niche templates** | onboard 1 lĩnh vực mới bằng config | 🛠️ 🟡 |
| **Benchmark suite** | so pipeline giữa các fork/niche | 🛠️ 🟡 |
| **Documentation** (kiến trúc, WHY, sơ đồ) | contributor hiểu được lõi | 🔴 |
| **Contributing guide** + code of conduct | hạ rào đóng góp | 🔴 |
| **Examples** (runnable, copy-paste được) | người mới chạy được trong 5 phút | 🔴 |
| **Analytics feedback loop** (Analyst role) | engagement → "cái gì hiệu quả" vào memory niche | 📡 🟢 |
| **AI disclosure / watermarking** | ghi rõ nội dung AI (luật/nền tảng) | 📡 (**cloud**) |
| **Bias / fairness audit** | model đối xử công bằng giữa nhóm | 📡 🟢 |

### Cách học hiệu quả (code tay) — Plugin system từng bước
> Đây là bài **Port/Adapter + Registry** thật, cực đáng làm tay vì open source sống nhờ nó.

1. **CODE TAY registry đơn giản** (dict + decorator) trước khi nghĩ tới entry-points:
```python
# app/plugins/registry.py
_REGISTRY: dict[str, dict[str, type]] = {}          # kind → {name → class}

def register(kind: str, name: str):
    def deco(cls):
        if name in _REGISTRY.setdefault(kind, {}):    # ← chặn trùng tên
            raise ValueError(f"plugin {kind}:{name} đã tồn tại")
        _REGISTRY[kind][name] = cls
        return cls
    return deco

def get(kind: str, name: str) -> type:
    return _REGISTRY[kind][name]                       # KeyError = tên sai/chưa load
```
2. **Bắt plugin phải tuân Port:** trong `register`, assert `issubclass(cls, PORTS[kind])` →
   plugin không implement đúng interface bị chặn *lúc đăng ký*, không phải lúc chạy giữa production.
3. **Nâng lên entry-point discovery** (`importlib.metadata.entry_points`) để plugin ở *package
   ngoài* tự nạp — đây là cách contributor cắm scraper mới mà không sửa core.

**BUG CỐ Ý (3 ca thật của plugin system):**
- **Trùng tên im lặng:** bỏ dòng chặn trùng → plugin B ghi đè A, A biến mất không báo.
  **DEBUG:** thấy vì sao registry phải fail-loud khi trùng.
- **Import side-effect:** decorator chạy lúc import → quên `import` module plugin thì `get()`
  KeyError dù class có tồn tại. **DEBUG:** hiểu registration = side-effect của import.
- **Plugin sai interface:** đăng ký class thiếu method của Port → chỉ nổ khi pipeline gọi tới.
  **FIX:** kiểm ở bước 2 (assert issubclass) → chuyển lỗi runtime thành lỗi đăng ký.

**Files gợi ý:** `app/plugins/registry.py` · `app/plugins/ports.py` · `tests/plugins/test_registry.py` (test trùng tên, tên sai, sai interface)

- Mỗi kỹ thuật đã học ở Phase 0–7 → viết 1 **example runnable** + 1 đoạn doc WHY. Doc là
  sản phẩm phụ của việc bạn đã hiểu thật.

---

## Phase 9 — SaaS Bridge (Cloud layer)

> 🧭 **Mức học từ 17/09:** 🟢 toàn bộ — xét lại khi quay về N Assistant — xem [Bản đồ Phase → lát](#bản-đồ-phase--lát-cắt).

> **Không đụng bộ não.** Core phơi **Port**, cloud cắm **Adapter**. CI cấm import billing vào core.

| Kỹ thuật | Học được gì | Lớp | Ưu tiên |
|---|---|---|---|
| **Usage metering** | đếm token/request/tenant → hóa đơn | Port ở core · enforce ở cloud | 🔴 |
| **Feature guard / Entitlement Port** | bật/tắt kỹ thuật theo gói khách | Port ở core · policy ở cloud | 🔴 |
| **Multi-tenancy enforcement** | siết `tenant_id` xuyên suốt, chống rò | core (đã có filter) + cloud (map customer) | 🔴 |
| **Wallet / Credit + 2-pha hold/settle** | trừ tiền theo ngữ cảnh (xem memory authz-billing) | cloud | 🟡 |
| **Rate/cost enforce theo customer** | chặn nổ bill từng khách | cloud | 🟡 |
| **Data retention / right-to-be-forgotten** | xóa data theo yêu cầu (luật) | cloud | 📡 |

### MeteringPort — hình dạng interface (core chỉ *đo*, không *tính tiền*)
```python
# app/domain/ports/metering.py — 0 import stripe, 0 khái niệm tiền
class MeteringPort(Protocol):
    def record(self, tenant_id: str, unit: str, qty: int, meta: dict) -> None: ...
    # unit ∈ {"llm_input_token","llm_output_token","embed_call","rerank_call","search"}
```
- Core **emit sự kiện dùng** (bao nhiêu token, bao nhiêu search) theo `tenant_id`. Hết.
- Cloud cắm adapter: gom event → tính tiền theo bảng giá gói → xuất hóa đơn. **Bảng giá KHÔNG
  bao giờ ở core** (đổi giá không được rebuild bộ não). Core dùng `NullMeteringAdapter` khi chạy
  standalone (fork MIT không cần billing vẫn chạy).

### 2-phase hold/settle (cloud) — vì sao cần 2 pha
> LLM streaming: **biết chi phí thật SAU khi sinh xong**, nhưng phải chặn TRƯỚC nếu hết credit.
```
1. HOLD (trước khi gọi LLM):  ước lượng max cost → giữ tạm trong ví (reserve).
   ├─ ví đủ  → giữ, cho chạy
   └─ ví thiếu → từ chối NGAY (chưa tốn LLM) → tránh "âm ví"
2. SETTLE (sau khi LLM xong): biết token thật → trừ đúng số, HOÀN phần giữ dư.
   └─ nếu request lỗi/hủy giữa chừng → RELEASE toàn bộ hold (không trừ oan).
```
- **Vì sao không trừ 1 pha:** trừ trước → không biết số thật, trừ thừa/thiếu; trừ sau → khách
  hết tiền vẫn gọi được LLM (thủng bill). Hold/settle giải đúng cả 2.
- Đây là **state machine** `HELD → SETTLED | RELEASED` — cùng họ với circuit breaker (Phase 5)
  và CRAG (Phase 2). Idempotency key chống settle 2 lần khi retry. Xem memory `authz-billing-plan`.

### Cách học hiệu quả (code tay)
- **CODE TAY (core):** định nghĩa `MeteringPort` + `EntitlementPort` (interface thuần, 0 import
  stripe). Viết **fake adapter** in-memory để test core; adapter thật (Stripe) ở repo cloud.
- **CODE TAY (cloud):** tự viết ví hold/settle bằng dict `{tenant: balance, holds: {id: amount}}`
  trước khi nghĩ tới DB. Test các đường: đủ tiền, thiếu tiền (từ chối ở HOLD), hủy giữa chừng (RELEASE).
- **BUG CỐ Ý:**
  - Đặt enforcement/bảng giá *trong* core → CI phải reject `import stripe`. Ranh giới sống nhờ test.
  - Quên RELEASE khi request lỗi → tiền "kẹt hold" vĩnh viễn, ví tụt dần dù không tiêu.
    **DEBUG:** log balance + holds mỗi request → thấy hold không được dọn.
  - Settle 2 lần khi client retry (thiếu idempotency key) → trừ tiền gấp đôi.

**Files gợi ý (core):** `app/domain/ports/metering.py` · `app/domain/ports/entitlement.py` · `app/domain/ports/null_adapters.py`
**Files (cloud, repo khác):** `wallet/hold_settle.py` · adapter Stripe/billing · dashboard · gateway.

---

## ★ OPTIONAL — Visual & Character Engine (cần GPU, off main path)
ComfyUI · Flux/SDXL · ControlNet · IP-Adapter/FaceID · character LoRA · img/text→video ·
TTS clone (XTTS/CosyVoice) · ffmpeg auto-edit. Làm khi có nhu cầu thật + GPU.

---


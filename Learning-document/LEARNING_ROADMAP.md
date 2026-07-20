# Learning Roadmap — Nyxara Open (AI Engineering Toolkit)

> Tài liệu chính thức. Ghi lại **những gì đã học, file đã build, kiến thức WHY**, và
> **bản đồ còn lại** để trở thành Senior AI Engineer qua việc xây một toolkit RAG/Agent
> production-grade, open source (Core MIT).
> Cập nhật mỗi khi hoàn thành một kỹ thuật mới.

> ## 🔁 RESET — 2026-07-13
> Đã **xóa sạch** code cũ (harvester + toàn bộ bộ não RAG + 74 test) và bắt đầu lại từ đầu:
> giữ Docker + khung hexagonal rỗng, code lại từng phase theo **vòng 6 bước** (tự tay + tự hiểu).
> **Kiến thức/công thức bên dưới GIỮ LẠI** (đã học rồi) — nhưng mọi trạng thái ✅ cũ đã về ⏳:
> phải **build lại bằng tay**, KHÔNG copy từ git history (`817d2d1` chỉ để tham khảo khi bí).
> Notes học kèm: [notes/](notes/) — design-system · algorithms · glossary · bug-log.

---

## 🎯 Tầm nhìn dự án

**Nyxara Open** = AI Engineering Toolkit mã nguồn mở (Core MIT), phục vụ 3 mục tiêu cùng lúc:

1. **Giáo trình sống** — học *đủ* mọi kỹ thuật RAG / Agent / MLOps hiện đại, không bỏ sót,
   để có **phán đoán** chọn đúng cái đáng dùng.
2. **Sản phẩm cộng đồng** — Core niche-agnostic, fork được, dùng thật.
3. **Nền SaaS kiếm tiền** — lớp cloud bọc ngoài (billing, metering, entitlement) *không* đụng bộ não AI.

Đích cá nhân: **pass phỏng vấn Senior AI Engineer**. Muốn vậy phải chứng minh được
2 thứ mà mọi thư viện che mất: **tự implement được lõi** và **debug được khi nó hỏng**.

---

## 🧭 Phương pháp học (Senior mindset)

> **Bối cảnh 2026:** AI gõ boilerplate hộ bạn. Giá trị còn lại của một kỹ sư là
> **đọc-hiểu flow sâu + soi bug** (AI cũng viết bug như `>= 0` lẽ ra `>= 0.5`).
> ❌ BỎ "nhớ hết code rồi gõ lại từ trí nhớ" — vô nghĩa. ✅ Hiểu để soi AI đúng/sai.

**⚠️ Luật thép (không thương lượng):**
> **Không code tay giỏi + không debug tốt → KHÔNG pass phỏng vấn Senior, và dự án
> open source SẼ THẤT BẠI.** Contributor bỏ đi khi lõi là hộp đen không ai hiểu.
> Vì vậy: **mọi kỹ thuật cốt lõi phải tự implement TRƯỚC khi cho phép dùng thư viện.**

### 4 nguyên tắc gốc
1. **Không pass, không hiểu → không đi tiếp.** Sai thì ở lại, giải thích, hỏi lại tới khi rõ.
2. **Học = XÂY.** Mỗi kỹ thuật phải chạm tay vào code chạy được — không chỉ đọc hiểu.
3. **Kỹ thuật là flag, mặc định TẮT.** Học ≠ phải bật. Eval mới quyết cái nào đáng bật.
4. **Ghi WHY ngay** vào [notes/algorithms.md](notes/algorithms.md) + từ mới vào [notes/glossary.md](notes/glossary.md) — mỗi bước.

### 🔨 Vòng 6 bước cho MỖI kỹ thuật cốt lõi (bắt buộc)
```
1. CODE TAY        ← tự viết lõi từ đầu (naive OK), KHÔNG import thư viện làm hộ
2. BUG CỐ Ý        ← tự phá 1 chỗ (off-by-one, sai dấu, quên normalize, thiếu await)
3. DEBUG BẰNG TAY  ← đọc trace, in số thật, tự tìm ra chỗ hỏng — KHÔNG hỏi AI ngay
4. FIX             ← sửa, giải thích tại sao bug đó gây sai kết quả gì
5. TEST            ← viết test bắt đúng ca bug vừa rồi (regression) + happy path
6. DOCUMENT        ← WHY vào notes/algorithms.md · từ mới vào notes/glossary.md · bug vào notes/bug-log.md
```
> Sau khi PASS 6 bước → *mới* được thay bằng thư viện chuẩn (FlagEmbedding, rank-bm25…)
> và so kết quả với bản tay. Thư viện là để **production**, bản tay là để **hiểu**.

### 🧮 CTDLGT phải luyện song song (không tách rời)
Mỗi kỹ thuật RAG là một bài CTDLGT trá hình — gọi tên hẳn ra để luyện có chủ đích:

| Cấu trúc / thuật toán | Xuất hiện ở kỹ thuật nào |
|---|---|
| **Hash map / inverted index** | BM25 (term → posting list), dedup |
| **Priority Queue / Heap** | top-k retrieval, MMR (chọn k phần tử tốt nhất) |
| **Sliding Window** | chunking, context-window budgeting |
| **Trie / prefix tree** | tokenizer, autocomplete, PII pattern matching |
| **Graph (BFS/DFS, topo-sort)** | LangGraph state machine, GraphRAG multi-hop |
| **Dynamic Programming** | edit distance (dedup near-duplicate), LCS |
| **Set / Bloom filter** | dedup ở scale lớn, seen-check incremental ingest |
| **Two-pointer / merge** | RRF (merge N ranked lists) |

### Vòng chạy-sửa + 2 lớp lưới (luôn đúng)
```
viết/sửa → chạy → lỗi (còn gợi ý) → sửa → chạy lại → xanh → TEST vài ca
```
| Lỗi cú pháp | Lỗi logic |
|---|---|
| **Chạy** bắt (Python chỉ `^`) | **Test** bắt (gọi thử, so kết quả) — mắt người không bắt nổi |

→ Không cần gõ đúng phát đầu. Senior cũng sửa 5 lần/30s. **Quen loop = kỹ năng thật.**

**Nhịp:** 1 hàm nhỏ / ngày (code tay → soi → sửa → test) > đọc 5 file.

---

## 🏛️ Ranh giới Core ↔ Cloud (SaaS)

> **2 lớp tách bạch — không trộn.** SaaS *thêm* lớp ngoài, không *thay* gì bên trong core.

| | `nyxara-core` (repo này, MIT) | `nyxara-cloud` (lớp SaaS) |
|---|---|---|
| Vai trò | **Bộ não AI** — RAG, CRAG, agent, fine-tune, eval | **Vỏ thương mại** — bán được |
| Chứa | Toàn bộ lộ trình AI engineer, niche-agnostic | auth, billing, account, dashboard, API gateway, metering |
| `tenant_id` | **namespace** (kho của 1 niche) | **customer** (map account → namespace) |
| Quan hệ | *bị gọi* — phơi API | *gọi vào* API của core |
| License | MIT, fork tự do | đóng được, thương mại |

**Cầu nối:** 1 *customer* (cloud) → ánh xạ thành 1 *tenant_id namespace* (core).
Core không biết tới tiền/account; cloud không chứa logic AI.

**CI enforce constitution:** reject `import stripe` / auth / billing trong core.
Core phơi **Port** (interface), cloud cắm **Adapter** — ví dụ `EntitlementPort`, `MeteringPort`.

**Vì sao tách:** (1) core sạch → học không nhiễu, fork được; (2) đổi mô hình kinh doanh
không đụng bộ não; (3) "mọi lĩnh vực" = core niche-agnostic sẵn, cloud chỉ onboard theo niche.

---

# 📚 CÁC PHASE

> Nhãn: 🛠️ **code tay** (học sâu, đủ 6 bước) · 📡 **radar** (biết để sau, làm khi gặp lỗi thật).
> Độ ưu tiên: 🔴 Cao · 🟡 Trung bình · 🟢 Thấp/optional.
> Trạng thái: ✅ Xong · 🔨 Đang làm · ⏳ Chưa bắt đầu.

Thứ tự logic: **Foundation & Ingestion → Advanced RAG → Evaluation → Performance →
Agent → Safety → Fine-tuning → MLOps → Community → SaaS Bridge.**

---

## Phase 0 — Foundation & Ingestion Pipeline

> **Rác vào = rác ra.** Retrieval giỏi tới đâu cũng vô nghĩa nếu chunk sai. Đây là nền.

### Kiến thức cốt lõi
- **Chunking granularity** quyết định chất lượng retrieval: chunk quá to → nhiễu; quá nhỏ → mất ngữ cảnh.
- Ingestion là **pipeline có trạng thái**: cùng 1 doc chạy lại không được nhân đôi (idempotent).
- Doc thay đổi theo thời gian → cần **versioning** + **incremental ingest** thay vì re-ingest toàn bộ.

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

---

## ✅ Phase 1 — Vector Memory (Embedding + Qdrant + Tenant Isolation)

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

## ⏳ Phase 2 — Advanced Retrieval (Hybrid + Rerank + CRAG + …)

> **Trạng thái sau reset:** kiến thức/công thức GIỮ LẠI (đã học). Code (bm25/rrf/hybrid/rerank/CRAG)
> đã xóa → build lại bằng tay theo 6 bước. Đường link file cũ đã gỡ vì file không còn.

### 2.1 BM25 + Hybrid Retrieval + RRF — ⏳ build lại (kiến thức ✔)

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

**Files sẽ build:** `app/application/retrieval/bm25_index.py` · `rrf.py` · `hybrid_retriever.py` · `app/domain/ports/retriever.py`
**Tests mục tiêu:** BM25 · RRF · HybridRetriever
**CTDLGT chạm tay:** inverted index (hash map term→postings), merge N ranked lists (two-pointer).

### 2.2 Cross-encoder Reranking (bge-reranker-v2-m3) — ⏳ build lại (kiến thức ✔)
- **Bi-encoder vs Cross-encoder**: bi-encoder encode query/doc riêng rồi so vector.
  Cross-encoder đọc query+doc **cùng 1 forward pass** → chính xác hơn nhưng chậm hơn.
- **Vì sao 2 bước:** Hybrid lọc nhanh top-20 → cross-encoder chấm kỹ top-5. Không thể
  chạy cross-encoder trên 10,000 docs. RRF score bị **thay** bằng cross-encoder score.

**Files sẽ build:** `app/domain/ports/reranker.py` · `app/infrastructure/adapters/reranker/bge_reranker.py`

### 2.3 CRAG (Corrective RAG via LangGraph) — ⏳ build lại (kiến thức ✔)
- **State machine**: `state` = "tờ giấy" chạy qua các **node** (trạm), điền dần từng ô.
- **Node = hàm** (`state → dict`); **edge** = ray cố định; **conditional edge** = rẽ theo **router**.
- **grade → verdict → correct**: LLM-as-judge chấm CÓ/KHÔNG → đếm ra CORRECT/AMBIGUOUS/INCORRECT
  → INCORRECT thì tìm lại **rộng hơn trong kho** (in-store). `attempts` guard chặn lặp vô hạn.

**Files sẽ build:** `app/application/generation/` → `state.py · node.py · grader.py · decision.py · graph.py`
**Tests mục tiêu:** grader · decision · graph e2e (vòng tự sửa + chốt chặn)
**Bug đã từng gặp (nhớ để né lại — ghi vào [bug-log](notes/bug-log.md)):** HybridRetriever thiếu `await` (async lây cả chuỗi) · `attempts` KeyError ở đường thành công (init `attempts=0`) · cần `extra_hosts` cho core-api reach Ollama grader.
**CTDLGT chạm tay:** graph (node/edge, conditional routing, cycle guard qua `attempts`).

### 2.4 Còn lại của Advanced RAG — ⏳ chưa build

| # | Kỹ thuật | Học được gì | Ưu tiên | CTDLGT |
|---|----------|------------|---------|--------|
| 1 | **Metadata filtering** | lọc trước semantic search (dùng thật trong Comment Assistant) | 🔴 | Filter predicate tree |
| 2 | **Query Transformation** (Multi-Query · HyDE · **Step-back**) | query↔doc space mismatch; mở rộng/nâng cấp query | 🟡 | — |
| 3 | **Temporal / Freshness-aware** + **time-decay** | `harvested_at` → payload Qdrant → recency scoring; chunk cũ = rác dù đúng topic. **Flag niche:** tài chính/news bật gắt | 🟡 (🔴 news) | — |
| 4 | **MMR** (Maximal Marginal Relevance) | tránh top-k gần trùng → bao phủ nhiều khía cạnh | 🟡 | Priority queue |
| 5 | **Context Compression** + **Lost-in-the-Middle** | cắt nhiễu; LLM quên phần giữa → đặt chunk quan trọng ở đầu/cuối | 🟡 | — |
| 6 | **Adaptive-RAG / Self-RAG** | quyết định *có nên retrieve không* ngay từ đầu (anh em ruột CRAG) | 🟡 | — |
| 7 | **GraphRAG** (Knowledge Graph + multi-hop) | câu hỏi nối nhiều mẩu; vector thuần yếu chỗ này | 🟢 | **Graph BFS/DFS** |
| 8 | **Multimodal RAG** | ảnh sản phẩm / bảng / PDF, transcript | 🟢 | — |

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
Metadata filtering + MMR trước (🔴/🟡 dùng thật). GraphRAG/Multimodal để radar tới khi
gặp câu hỏi multi-hop thật. **Đừng build hết rồi mới đo** — mỗi cái xong đẩy qua Phase 3.

---

## Phase 3 — Evaluation Framework (đo trước, tin sau) ⭐ PHASE QUAN TRỌNG NHẤT

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

### Cách học hiệu quả (code tay)
- **CODE TAY PII:** tự viết Trie/regex matcher cho SĐT VN + email TRƯỚC khi dùng Presidio.
  → luyện đúng CTDLGT **Trie/pattern matching**.
- **BUG CỐ Ý (injection):** để prompt template nối thẳng UGC → nhét "ignore previous
  instructions" thấy agent bị lái. **DEBUG:** thấy vì sao phải tách data/instruction (delimiter, role).
- **Circuit breaker:** tự viết state machine CLOSED→OPEN→HALF_OPEN — lại là bài **state machine**.

**Files gợi ý:** `app/safety/pii.py` · `app/safety/injection.py` · `app/safety/circuit_breaker.py` · `app/safety/sanitize.py`

---

## Phase 6 — Fine-tuning

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

| Kỹ thuật | Học được gì | Ưu tiên |
|---|---|---|
| **Model serving** (vLLM / TGI) | phục vụ LLM throughput cao (paged attention) | 🛠️ 🔴 |
| **Observability stack** (Prometheus + Grafana) | metric/log/alert hạ tầng (latency, error rate, uptime) | 🛠️ 🔴 |
| **Data lifecycle** | vector CRUD/delete/sync · dedup · incremental · **embedding migration** (re-embed khi đổi model) | 🛠️ 🔴 |
| **Drift detection** | data / embedding / concept drift — chất lượng tụt âm thầm | 🛠️ 🟡 |
| **Eval-at-scale** | online eval · regression · prompt versioning · judge calibration | 🛠️ 🟡 |
| **CI/CD retrain** + experiment tracking (W&B/MLflow) · versioning (DVC/HF) | reproducible ML | 📡 🟢 |
| **Canary / blue-green deploy** · DR/backup · scaling/backpressure | tung model an toàn, chịu tải | 📡 🟢 (nhiều phần **cloud**) |

### Cách học hiệu quả
- Phân biệt rạch ròi: **agent tracing (LangFuse, Phase 4)** ≠ **observability hạ tầng (Prometheus)**.
  Cái đầu cần lúc BUILD agent; cái sau đo cả hệ thống.
- **Drift:** tự viết so phân bố embedding tuần này vs tuần trước (PSI / KL divergence) trước khi dùng tool.

**Files gợi ý:** `app/observability/metrics.py` · `ops/serving/vllm.yaml` · `app/lifecycle/reembed.py`

---

## Phase 8 — Extensibility & Community (Open Source)

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

## 🎯 Nguyên tắc bao trùm: Học vs. Production

> Project build **tất cả** kỹ thuật để **HỌC cho biết** — nhưng một sản phẩm thật
> **KHÔNG dùng hết**. Mỗi fork chỉ **bật đúng subset** niche cần (mọi kỹ thuật là
> *flag, mặc định TẮT*). Học hết là để **có phán đoán** chọn đúng. **Eval (Phase 3)**
> cho biết cái nào *thật sự đáng bật*. **Học một kỹ thuật ≠ phải deploy nó.**

---

## 📊 Tổng kết Tests

```
15 tests (2026-07-19) — Chunker 2 · Dedup 2 · Edit distance 5 · Pipeline 1 · Similarity 1 · BGEEmbedder 3 · QdrantStore 1
đếm lại bất cứ lúc nào bằng:  grep -rc "def test_" tests
```
> Trước reset có 74 test xanh (P1 vector 15 · BM25 13 · RRF 10 · Hybrid 11 · Reranker 6 · CRAG 12 · Chunker 4 · Ingestion 3).
> Build lại tới đâu, con số bò lên tới đó. Cập nhật sau MỖI lần thêm test — lệch số = tài liệu mất tin cậy.
> Quy ước: mỗi bug sửa ở bất kỳ phase nào → +1 regression test (nguyên tắc gốc #4) + ghi [notes/bug-log.md](notes/bug-log.md).

---

## ✅ Bảng theo dõi tiến độ (checklist)

| Phase | Kỹ thuật | Trạng thái | 🎯 Next Action (việc kế tiếp cụ thể) |
|---|---|---|---|
| 0 | **Recursive** chunking ✅ · Semantic/Proposition ⏳ | 🔨 | Recursive xong; Semantic (cắt theo embedding distance) để radar, giờ có embedder rồi |
| 0 | **Dedup (exact+near) ✅ · Incremental ✅** · Parent-Child/Multi-vector/Versioning ⏳ | 🔨 | Lõi 🔴 xong (edit_distance DP + pipeline seen-check). Còn lại 🟡🟢 radar |
| 1 | Embedding · Qdrant · Tenant Isolation | ✅ | **XONG 2026-07-19** — search + tenant filter + drill silent-failure (bug #13). 15 test |
| 2 | BM25 · Hybrid · RRF | ⏳ | ⭐ **BẮT ĐẦU TẠI ĐÂY** — code tay BM25 (inverted index) → RRF (merge) → HybridRetriever |
| 2 | Cross-encoder Rerank | ⏳ | Port Reranker → BGEReranker; 2 bước retrieve→rerank |
| 2 | CRAG (+ API) | ⏳ | StateGraph LangGraph; né lại 3 bug cũ (await, attempts, extra_hosts) |
| 2 | Metadata filter · Query transform · Temporal · MMR · Compression · Adaptive/Self-RAG · GraphRAG · Multimodal | ⏳ | Sau khi khôi phục xong lõi 2.1–2.3: Metadata filtering → MMR |
| 3 | Eval: Retrieval metrics · Judge · RAGAS · Golden · Regression · A/B · Cost/Efficiency · Calibration · Online · Bias · **CI gate** | ⏳ | **Ưu tiên song song P2:** code tay `hit@k/mrr/ndcg` → golden 50–100 cặp → A/B Hybrid vs Hybrid+MMR |
| 3.5 | Profiling · Indexing · HNSW · Quantization · Caching · Semantic cache | ⏳ | Chỉ mở sau khi có eval — viết `@timed` đo từng chặng trước |
| 4 | Agent: Supervisor · Tool · Triage · Memory · Abstention · HITL · Tracing · MCP | ⏳ | Tái dùng skill CRAG → dựng StateGraph supervisor + cắm LangFuse ngay |
| 5 | Safety: Injection · PII · Toxicity · Sanitization · Red-team · Rate · Cost · Circuit breaker · Degradation | ⏳ | Code tay Trie/regex PII (SĐT VN) + circuit breaker state machine |
| 6 | Fine-tune: LoRA/QLoRA · Synthetic · GGUF · Domain | ⏳ | Manual LoRA layer PyTorch (`W+BA·scale`) trên 1 linear toy |
| 7 | MLOps: Serving · Observability · Data lifecycle · Drift · Canary | ⏳ | vLLM serve local + Prometheus metric cơ bản |
| 8 | Extensibility: Plugin · Templates · Benchmark · Docs · Examples | ⏳ | Code tay registry dict+decorator (chặn trùng + assert Port) |
| 9 | SaaS Bridge: Metering · Entitlement · Multi-tenancy enforce | ⏳ | Định nghĩa `MeteringPort`+`EntitlementPort` (0 stripe) + fake adapter |

> **Nhịp sau reset:** đi tuần tự **P0 chunking → P1 vector → P2 lõi (bm25/rrf/hybrid/rerank/CRAG)**.
> Khôi phục lõi cũ bằng tay trước (đã có kiến thức, nhanh hơn lần đầu). Tới **P3 eval** thì mở
> song song để bắt đầu đo các kỹ thuật P2 mở rộng. Mỗi phần xong → cập nhật notes + số test.

---

## 📚 Tài liệu tham khảo

| Tài liệu | Nội dung |
|----------|---------|
| [notes/](notes/) | Sổ tay học: design-system · algorithms · glossary · bug-log (viết ở bước 6 mỗi kỹ thuật) |
| [README.vi.md](../README.vi.md) | Giới thiệu dự án, kiến trúc hệ thống |
| Cormack et al. 2009 | Paper gốc RRF — `k=60` từ đây |
| Robertson et al. 1994 | Paper gốc Okapi BM25 |
| BAAI/bge-m3 | Model embedding 1024-dim, 100+ ngôn ngữ |
| Lewis et al. 2020 | RAG paper gốc |
| Yan et al. 2024 | CRAG (Corrective RAG) |
| Asai et al. 2023 | Self-RAG |
| Carbonell & Goldstein 1998 | MMR gốc |

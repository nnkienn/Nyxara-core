<div align="center">

# Nyxara 🤖🚀

### Bộ công cụ AI Engineering bạn tự build từ đầu — RAG nâng cao, agent, fine-tuning & evaluation — hướng tới một ngách thật

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-DC244C.svg?logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C.svg)](https://langchain-ai.github.io/langgraph/)
[![Status](https://img.shields.io/badge/status-rebuilding_from_scratch-orange.svg)](./Learning-document/LEARNING_ROADMAP.md)

**Phần lớn dự án "học AI" chết yểu vì là một mớ tutorial ghép lại — không người dùng, không cách nào biết thứ mình làm có chạy đúng không, và một lõi hộp đen chẳng ai hiểu. Nyxara đặt cược ngược lại: bạn **tự tay xây từng tầng** — toán embedding, công thức RRF, reranker, CRAG, cập nhật LoRA, các chỉ số eval — và hướng nó vào một công việc thật: một *Comment Assistant* cho seller-affiliate TikTok Shop / Shopee. Có người duyệt (human-in-the-loop), KHÔNG bao giờ tự đăng.**

🌐 🇬🇧 [English](./README.md) · 🇻🇳 **Tiếng Việt** · 🇩🇪 [Deutsch](./README.de.md) · 🇨🇳 [中文](./README.zh.md)

</div>

---

> ### 🔁 Trạng thái: đang build lại từ đầu (reset 2026-07)
> Repo đã được reset về **khung skeleton chạy được** — Docker + khung hexagonal rỗng + endpoint
> `/health`. Harvester và bộ não RAG cũ (cùng 74 test) đã bị xóa **có chủ đích**, để mỗi tầng
> được **gõ lại bằng tay và hiểu thật**, không thừa kế một hộp đen. Mọi thứ dưới mục "Vì sao"
> mô tả **hệ thống mục tiêu và con đường học tới đó** — theo dõi trạng thái thật ở [roadmap](#-lộ-trình--con-đường-học).

---

## 🎯 Vì sao có dự án này

Hai thứ giết chết hầu hết dự án "tôi đang học AI engineering":

1. **Chúng được khâu từ tutorial.** Bạn ráp một retriever LangChain, ra được câu trả lời, nhưng không bao giờ hiểu *vì sao* dense retrieval trượt, RRF thực sự tính cái gì, hay reranker có giúp ích không. Sự hiểu biết không bao giờ đọng lại.
2. **Chúng không có đích đến.** Không tác vụ thật, không người dùng thật, không cách nào đo "tốt hơn". Động lực bốc hơi.

**Nyxara sửa cả hai.** Đây là một động cơ **RAG + agentic đa ngôn ngữ mà bạn tự build từ đầu** — sở hữu toán embedding, công thức RRF, cross-encoder rerank, cập nhật LoRA, các chỉ số eval — và nó hướng tới một **ngách cụ thể có người dùng thật (dù nhỏ):** tự động hóa content & social cho **seller-affiliate trên TikTok Shop / Shopee tại Việt Nam.**

> **Bối cảnh 2026:** AI gõ boilerplate hộ bạn rồi. Kỹ năng còn giá trị là *đọc-hiểu flow sâu và soi ra bug* — vì AI cũng ship bug tinh vi (`>= 0` lẽ ra `>= 0.5`). Nên Nyxara chạy trên một luật bất di bất dịch: **mọi kỹ thuật cốt lõi phải tự implement TRƯỚC, chỉ sau đó mới thay bằng thư viện.** Nếu bạn không tự build được và không debug được, bạn không thể biết thư viện có đang "nói dối" mình hay không.

Nó được thiết kế để chạy **100% local** mặc định (không byte nào rời máy bạn trừ khi bạn chọn tầng cloud), và một `tenant_id` **namespace** cho phép một bản cài chứa nhiều niche song song — *một folder cho mỗi niche*, không phải *một tenant cho mỗi khách trả tiền*. Lõi MIT không có billing, auth hay dashboard; những thứ đó nằm ở một **lớp cloud tách riêng** (xem [Phase 9](#-lộ-trình--con-đường-học)).

---

## 🧭 Cách bạn học ở đây — kỷ luật

Repo này trước hết là **một cỗ máy để học**, sau đó mới là công cụ ngách. Phương pháp không phải "đọc code rồi gật gù". Mỗi kỹ thuật cốt lõi phải đi qua một **vòng 6 bước** trước khi một thư viện được phép lại gần:

```
1. CODE TAY        ← tự viết lõi từ đầu (naive cũng được); KHÔNG có thư viện làm hộ
2. BUG CỐ Ý        ← tự phá 1 chỗ (off-by-one, sai dấu, quên normalize / await)
3. DEBUG BẰNG TAY  ← đọc trace, in số thật, tự tìm ra — ĐỪNG hỏi AI ngay
4. FIX             ← sửa, giải thích chính xác bug đó gây sai kết quả gì
5. TEST            ← viết test bắt đúng ca bug vừa rồi (regression) + happy path
6. DOCUMENT        ← WHY vào notes/, từ mới vào glossary, bug vào bug-log
```

Chỉ sau 6 bước đó bạn mới thay bằng thư viện chuẩn (FlagEmbedding, rank-bm25…) **và so kết quả với bản tay.** Thư viện là để **production**; bản tay là để **hiểu**.

**Cấu trúc dữ liệu không phải bài tập tách rời** — mỗi kỹ thuật RAG *chính là* một bài CTDLGT trá hình:

| Cấu trúc / thuật toán | Xuất hiện ở đâu |
|---|---|
| Hash map / inverted index | BM25 (term → posting list), dedup |
| Priority queue / heap | top-k retrieval, MMR |
| Sliding window | chunking, context-window budgeting |
| Trie / prefix tree | tokenizer, PII pattern matching |
| Graph (BFS/DFS) | state machine LangGraph, GraphRAG multi-hop |
| Quy hoạch động (DP) | edit distance cho dedup gần-trùng |
| Two-pointer / merge | RRF (gộp N ranked list) |

> **Tài liệu học nằm ở [`Learning-document/`](./Learning-document/):**
> [LEARNING_ROADMAP.md](./Learning-document/LEARNING_ROADMAP.md) (con đường đầy đủ + bài code tay) và
> [`notes/`](./Learning-document/notes/) — **design-system**, **algorithms**, **glossary**, **bug-log**.

---

## 🛍️ Sản phẩm-lõi đầu tiên — Comment Assistant

Đây là đích ngách khiến mọi kỹ thuật có lý do tồn tại.

Một seller-affiliate đăng video bán hàng lên TikTok Shop / Shopee. Bên dưới, hàng chục comment dồn về: *"giá bao nhiêu?"*, *"da dầu dùng được không?"*, *"ship mấy ngày?"*. Comment Assistant biến cơn lũ đó thành các câu trả lời đúng giọng, đã được duyệt:

1. **Đọc** comment công khai dưới video.
2. **Truy xuất** đúng thông tin sản phẩm — giá, thành phần, công dụng, link chính thức — **lọc đúng *sản phẩm đó*** (lọc metadata trước, *rồi mới* semantic search — không phải "vector gần nhất thắng").
3. **Soạn** câu trả lời đúng giọng và đúng ngôn ngữ của seller.
4. **Phê bình:** một **Critic agent chặn thông tin bịa và claim công dụng chưa kiểm chứng** — bất di bất dịch với mỹ phẩm/sức khỏe, nơi một claim sai là vấn đề niềm tin và pháp lý.
5. **Người duyệt** trước khi bất cứ thứ gì được gửi. **Nyxara không bao giờ tự đăng.** Khi một câu trả lời *thật sự* được gửi, nó đi qua **API chính thức** của nền tảng — không bao giờ qua trình duyệt lén.

Mọi kỹ thuật RAG/agent/eval trong roadmap đều giành được chỗ đứng bằng cách trả lời một câu hỏi thật ở đây: *retrieval có lấy đúng sản phẩm không? rerank có thật sự nâng câu trả lời không? Critic có bắt được claim sai không?* — và evaluation ở Phase 3 là cách bạn **chứng minh** thay vì đoán.

---

## 🧱 Hệ thống bạn sẽ build (kiến trúc mục tiêu)

> Đây là các mảnh mà roadmap dựng lên, từng phase. **Code hiện tại = skeleton;** mỗi mục dưới
> là mục tiêu build, chưa phải tính năng đã có. Trạng thái xem ở [bảng roadmap](#-lộ-trình--con-đường-học).

- **Pipeline nạp dữ liệu (Phase 0):** connector cắm-được (thả 1 file / nguồn) + chunking → dedup → incremental upsert. Thu thập dữ liệu tách khỏi suy luận — *tầng nạp không bao giờ gọi LLM*.
- **Bộ nhớ vector (Phase 1):** `BAAI/bge-m3` (1024 chiều, 100+ ngôn ngữ) vào [Qdrant](https://qdrant.tech/), một chỉ mục xuyên ngôn ngữ chung. Mọi `upsert`/`search` mang filter `tenant_id` bắt buộc — **zero lẫn dữ liệu chéo niche** như một bảo đảm kiến trúc. (Bỏ filter → *âm thầm* rò dữ liệu niche khác, không crash. Đó là bài debug ở Phase 1.)
- **Retrieval nâng cao (Phase 2):** Hybrid (dense + BM25) → RRF → cross-encoder rerank → CRAG, rồi metadata filtering, MMR, query transformation, temporal, Adaptive/Self-RAG, GraphRAG — mỗi cái **tự build bằng tay** và bật/tắt theo query.
- **Evaluation (Phase 3):** Hit@k/MRR/NDCG tự viết + RAGAS + custom LLM judge + golden/regression set + A/B — vòng lặp quyết định kỹ thuật nào thật sự được giữ.
- **Dual-engine LLM router:** một `LLMClientBase` (tương thích OpenAI) để mọi agent chạy trên Ollama/MLX (local dev) hoặc vLLM/cloud (scale) mà không sửa code — định tuyến là quyết định cấu hình lúc runtime.
- **Agent Supervisor–Worker (Phase 4):** Supervisor → Researcher → Creator → **Critic** → cổng người. **Critic kiểm chứng grounding trước khi bản nháp tới tay người**, và con người là cổng cuối. Không có agent tự-đăng.
- **Safety (Phase 5), Fine-tuning (Phase 6), MLOps (Phase 7), Mở rộng (Phase 8)** — xem roadmap.

---

## 🏗️ Kiến trúc Hexagonal — và ranh giới Core ↔ Cloud

Lõi domain không phụ thuộc gì cả; thế giới bên ngoài cắm vào qua các port. Bạn có thể thay Qdrant, engine LLM hay web framework mà không cần động đến logic nghiệp vụ.

> **Core (repo này) vs. lớp Cloud.** Repo này là **bộ não AI thuần, MIT, niche-agnostic** — cố ý *không có* billing, auth, hay tài khoản khách (`tenant_id` là **namespace**, không phải customer). Mọi việc thương mại hóa (auth, billing, dashboard, API gateway, đo dùng theo khách, ví/credit) thuộc về một **lớp cloud riêng gọi vào HTTP API của engine này** và ánh xạ mỗi *customer → tenant_id namespace*. Core phơi **port** (vd `MeteringPort`, `EntitlementPort`); cloud cắm **adapter**. CI từ chối `import stripe` / auth / billing bên trong core. Bộ não giữ nguyên tính fork-được và học-được; vỏ thương mại không bao giờ rò vào trong. Cây cầu đó là [Phase 9](#-lộ-trình--con-đường-học).

Skeleton hiện tại (lớn dần khi build từng phase):

```
nyxara-core/
├── app/
│   ├── domain/                  # Thực thể & port thuần — không phụ thuộc framework   (rỗng)
│   ├── application/             # Use case / orchestration                            (rỗng)
│   ├── infrastructure/          # Adapter cắm vào port                                (rỗng)
│   ├── presentation/api/        # Router & schema FastAPI                             (rỗng)
│   └── main.py                  # Composition root — hiện chỉ có /health
├── Learning-document/
│   ├── LEARNING_ROADMAP.md      # ★ con đường học đầy đủ
│   └── notes/                   # design-system · algorithms · glossary · bug-log
├── tests/                       # (rỗng — build lại từng test, TDD)
├── docker-compose.yml           # redis + qdrant + core-api
├── Dockerfile                   # image core-API tối giản
├── requirements.txt             # slim; mỗi phase tự thêm dep
└── LICENSE                      # MIT
```

---

## ⚡ Ngăn xếp công nghệ (mục tiêu)

| Tầng | Công nghệ |
|---|---|
| API | FastAPI (Python 3.11) · Pydantic v2 |
| Vector / RAG | **Qdrant** · embedding `BAAI/bge-m3` (1024 chiều, đa ngôn ngữ) · Hybrid + RRF + cross-encoder rerank (`bge-reranker-v2-m3`) + CRAG · lọc metadata · semantic chunking |
| Suy luận | `LLMClientBase` → Ollama / Apple MLX (dev) · vLLM / Cloud API (scale) |
| Agent framework | LangGraph (Supervisor–Worker, multi-agent, human-in-the-loop, tracing, MCP) |
| Evaluation | **RAGAS** + retrieval metrics tự viết (Hit@k/MRR/NDCG) + custom LLM judge + A/B |
| Fine-tuning | LoRA/QLoRA trên `Qwen2.5-7B` · lượng tử hóa GGUF · fine-tune embedding/domain |
| An toàn | chống prompt-injection · PII redaction · toxicity moderation · output sanitization · circuit breaker |
| Tác vụ async | Celery 5 + broker Redis 7 |
| MLOps | vLLM/TGI serving · LangFuse · Prometheus + Grafana · CI/CD retrain |
| Hình ảnh / Video — *TÙY CHỌN* | ComfyUI · Flux / SDXL · ControlNet · XTTS / CosyVoice · ffmpeg *(cần GPU)* |
| Container | Docker Compose |
| Giấy phép | MIT |

---

## 🗺️ Lộ trình — Con đường Học

Các phase được sắp xếp để mỗi phase dạy bạn một tầng của hệ thống từ đầu. **Trạng thái là thật, không phải mơ ước — sau reset 2026-07, mọi thứ đang được build lại bằng tay.** Đánh số khớp với **[LEARNING_ROADMAP.md](./Learning-document/LEARNING_ROADMAP.md)** chi tiết. **CORE** là con đường chính; **CLOUD** (Phase 9) là lớp thương mại tách riêng; **OPTIONAL** Visual nằm bên lề.

| Phase | Nhánh | Chủ đề | Bạn xây & học gì | Trạng thái |
|---|---|---|---|---|
| **0. Nền móng & Ingestion** | CORE | Connector dữ liệu → làm sạch → **chunk · dedup · incremental ingest** | Kiến trúc plugin, recursive/semantic chunking, dedup (hash + edit-distance) | ⏳ **Bắt đầu ở đây** |
| **1. Bộ nhớ Vector** | CORE | `bge-m3` + Qdrant + đa namespace | Toán embedding, **tự tay** code cosine similarity, cô lập bắt-buộc-`tenant_id` | ⏳ Build lại |
| **2. Retrieval Nâng cao** | CORE | Hybrid + RRF + rerank + CRAG, rồi metadata filter · MMR · query transform · temporal · Adaptive/Self-RAG · GraphRAG | Toán RRF & rerank, bi- vs cross-encoder, graph workflow — mỗi retriever **tự build bằng tay** | ⏳ Build lại |
| **3. Evaluation Framework** ⭐ | CORE | RAGAS + custom LLM judge + Hit@k/MRR/NDCG tự viết + golden/regression + A/B + cost/latency | **Mỗi kỹ thuật Phase 2 có thật sự giúp không** — vòng lặp trung tâm | ⏳ Dự kiến |
| **3.5 Tối ưu tốc độ** | CORE | Latency profiling · HNSW tuning · quantization · payload indexing · semantic caching | Đo trước, tối ưu sau; đánh đổi recall ↔ latency | ⏳ Dự kiến |
| **4. Agentic Orchestrator** | CORE | LangGraph Supervisor–Worker (Researcher → Creator → **Critic**) · **Comment Assistant** e2e · HITL · intent triage · memory · abstention · tracing (LangFuse) · MCP | Thiết kế multi-agent, grounding & chống ảo giác, HITL | ⏳ Dự kiến |
| **5. Safety & Guardrails** | CORE | Chống prompt-injection · PII redaction · toxicity moderation · output sanitization · red-teaming · circuit breaker | Gia cố một LLM ăn comment không tin được | ⏳ Dự kiến |
| **6. Fine-tuning** | CORE | **LoRA/QLoRA** trên `Qwen2.5-7B` · synthetic data · merge GGUF · fine-tune embedding/domain | Toán cập nhật low-rank (tự viết LoRA layer bằng PyTorch), lượng tử hóa | ⏳ Dự kiến |
| **7. Production & MLOps** | CORE | vLLM/TGI serving · Prometheus + Grafana · data lifecycle · drift detection · CI/CD · canary | Observability, ML tái lập được, giữ KB đúng theo thời gian | ⏳ Dự kiến |
| **8. Mở rộng & Cộng đồng** | CORE | Plugin system · template niche · benchmark suite · docs · ví dụ chạy được | Khả năng mở rộng OSS, thiết kế registry port/adapter | ⏳ Dự kiến |
| **9. SaaS Bridge** | **CLOUD** | Usage metering · feature/entitlement port · siết multi-tenancy · ví (2-pha hold/settle) | Vỏ thương mại — **một lớp tách riêng, không bao giờ nằm trong bộ não core** | ⏳ Tương lai · repo riêng |
| **★ Visual & Character Engine** | **OPTIONAL** | ComfyUI + IP-Adapter/FaceID + character LoRA · Flux/SDXL + ControlNet · image/text→video · TTS clone · ffmpeg | Kỹ thuật nhất quán, điều khiển diffusion, pipeline video | 🧩 Add-on · cần GPU |

### Phase 2 chi tiết — RAG nâng cao, mọi kỹ thuật bật/tắt theo từng query

Cốt lõi là tự tay build từng kỹ thuật **bằng tay** (pure Python trên `LLMClientBase` + `qdrant-client`, LangGraph chỉ lo flow) rồi **đo xem nó có thật sự giúp ích không** ở Phase 3 — *học RAG mà không đo là học mù.*

| Kỹ thuật | Làm gì | Học được gì |
|---|---|---|
| **Hybrid Search** (dense + sparse/BM25) | chạy retrieval semantic + từ khóa cùng lúc | khi nào dense thắng sparse và ngược lại |
| **RRF** (Reciprocal Rank Fusion) | gộp nhiều bảng xếp hạng thành một | công thức RRF bằng tay; cách gộp ranking |
| **Cross-encoder reranking** (`bge-reranker-v2-m3`) | chấm lại top-k bằng cách đọc query+doc *cùng nhau* | vì sao rerank nâng top-k mạnh nhất; **bi- vs cross-encoder** |
| **CRAG** (Corrective RAG) qua LangGraph | chấm điểm context rồi retry / mở rộng | tự chấm context; vòng lặp tự sửa; state machine |
| **Metadata filtering** (vector + filter) | lọc đúng sản phẩm *trước* semantic search | lọc cấu trúc + vector search — **dùng thật trong Comment Assistant** |
| **MMR** (đa dạng kết quả) | tránh top-k toàn chunk gần trùng nhau | maximal marginal relevance (một bài priority-queue) |
| **Query Transformation** (Multi-Query · HyDE · Step-back) | mở rộng / viết lại truy vấn trước khi search | lệch không gian query↔document |
| **Temporal / freshness-aware** | cân độ mới, không chỉ độ liên quan | time-decay scoring; flag theo niche |
| **Context Compression** + lost-in-the-middle | cắt còn câu trả lời; sắp xếp cho vừa cửa sổ | cắt nhiễu; token budgeting |
| **Adaptive-RAG / Self-RAG** | quyết định *có nên retrieve không* ngay từ đầu | anh em ruột của CRAG; routing trước retrieval |
| **GraphRAG** (knowledge graph + multi-hop) | trả lời câu hỏi nối nhiều mẩu tin | nơi vector thuần yếu; duyệt graph |

Mỗi kỹ thuật là một **flag theo từng query, mặc định tắt**, nên bạn có thể A/B *có* vs *không* và đọc số liệu. **Evaluation framework** được kéo lên sớm (Phase 3) vì không có nó thì không thể chọn flag một cách khôn ngoan.

---

## 🚀 Bắt đầu nhanh

Hiện tại lệnh này chạy **skeleton** — một health endpoint cùng Redis + Qdrant, sẵn sàng cho các phase build lên trên.

```bash
git clone https://github.com/nnkienn/nyxara-core.git
cd nyxara-core
cp .env.example .env
docker compose up -d --build      # khởi chạy redis + qdrant + core-api

curl http://localhost:8100/health
# {"status":"ok","service":"nyxara-core"}
```

| Dịch vụ | URL |
|---|---|
| Core API | http://localhost:8100 |
| Qdrant (vector DB) | http://localhost:6353 |
| Redis (broker) | localhost:6399 |

> **Tiếp theo:** mở [LEARNING_ROADMAP.md](./Learning-document/LEARNING_ROADMAP.md) và bắt đầu ở **Phase 0** —
> tự build chunker, gài bug, debug, test, ghi notes. Tính năng sáng đèn dần theo lúc bạn build.

---

## 🔐 Quy tắc Kỹ thuật Bất di Bất dịch

Đây là các quy tắc **hiến định**. PR vi phạm sẽ bị tự động từ chối.

- ✋ **Tự build trước khi import.** Mỗi kỹ thuật cốt lõi phải có bản implement từ đầu + test của nó *trước khi* một thư viện thay thế. Một lõi hộp đen giết chết dự án open source.
- 📏 **Đo trước khi bật.** Mỗi kỹ thuật RAG là flag theo từng query, mặc định **tắt**; chỉ bật khi eval Phase 3 chứng minh nó giúp ích trên golden set. Không có kiểu "nghe nói nó hay".
- 🛡️ **Namespace ở khắp nơi.** Mọi thao tác Vector DB, cache key và audit log đều PHẢI mang namespace `tenant_id` để các niche không bao giờ lẫn vào nhau.
- 🧠 **Một model embedding duy nhất.** `BAAI/bge-m3` là embedding duy nhất được phép — không model riêng theo ngôn ngữ, không OpenAI ada.
- 🔌 **Trừu tượng `LLMClientBase`.** Agent gọi `client.complete(...)` — không bao giờ gọi trực tiếp `openai.ChatCompletion.*` hay `transformers`.
- ✅ **TDD bắt buộc.** Red → Green → Refactor. Logic RAG/Agent cần **test xuyên ngôn ngữ** (VN, EN, DE, CN); mỗi bug sửa xong thành một regression test vĩnh viễn.
- 🏛️ **Core giữ nguyên sự thuần khiết.** Không `import stripe`, auth hay billing trong core — lớp thương mại là riêng biệt (Phase 9).
- 🙋 **Human-in-the-loop, không auto-đăng.** Bản nháp tới tay một con người để duyệt, sửa, hoặc từ chối. Không gì được gửi tự động; khi nội dung *thật sự* được gửi, nó dùng **API chính thức** của nền tảng — không bao giờ tự động hóa trình duyệt / đăng lén.
- 🌾 **Nguồn dữ liệu zero-hardcode.** Mục tiêu cào/nạp nằm trong config, chỉ trang công khai, tôn trọng robots.txt.

---

<div align="center">

**Giấy phép:** [MIT](LICENSE) · Tự do sử dụng, fork, chỉnh sửa và tự host. Xây cho cộng đồng AI mã nguồn mở. 🌍

📞 **nnkienn@gmail.com**

</div>

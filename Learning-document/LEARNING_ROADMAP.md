# Learning Roadmap — Nyxara Open (AI Engineering Toolkit)

> 🧹 **Dọn 2026-09-18:** file này từng 1.202 dòng. Đã tách làm 3:
> **(a)** kho kiến thức 10 Phase → [phases.md](phases.md) — tra cứu, không đọc mỗi buổi ·
> **(b)** kế hoạch cũ đã hết hiệu lực (RESET 13/07 · DEADLINE 28/08) và mục "Phương pháp học"
> trùng với CLAUDE.md → [archive/2026-09-18-LEARNING_ROADMAP.md](archive/2026-09-18-LEARNING_ROADMAP.md) ·
> **(c)** phần còn lại — **thiết kế lại 17/09 là nguồn sự thật duy nhất** — giữ nguyên ở đây.
>
> ⚠️ Phase nào trong `phases.md` đá nhau với **mục F** dưới đây thì **lấy mục F**.


> Tài liệu chính thức. Ghi lại **những gì đã học, file đã build, kiến thức WHY**, và
> **bản đồ còn lại** để trở thành Senior AI Engineer qua việc xây một toolkit RAG/Agent
> production-grade, open source (Core MIT).
> Cập nhật mỗi khi hoàn thành một kỹ thuật mới.

> # 🧭 THIẾT KẾ LẠI — 2026-09-17 (NGUỒN SỰ THẬT HIỆN HÀNH)
> **Thay thế** các phần *DEADLINE ÉP TIẾN ĐỘ 28/08*, *RE-PLAN 10/09*, *RECALC 13/09* — đã chuyển vào
> [archive/2026-09-18-LEARNING_ROADMAP.md](archive/2026-09-18-LEARNING_ROADMAP.md) ngày 18/09.
> Các Phase 0→9 vẫn là **kho kiến thức**, nay ở [phases.md](phases.md); thứ tự làm và độ sâu theo mục này.

> ## A. Vì sao thiết kế lại (số thật)
> - Checkpoint 17/09: **1/4 mốc**. Mốc 1 tốn **6h30** / hộp 3h; mốc 2 đã **≥5h25** / hộp 8h mà chưa xong.
> - Kế hoạch cũ cần ~70 mốc × ~10h ≈ **700h** trong ~20 tuần — **không khả thi từ đầu**, không phải do lười.
> - Chậm nhất là **gõ cú pháp**, không phải logic: note 16/09 *"ruột đúng ngay lần đầu, mọi vòng đỏ là vỏ cú pháp"*.
> - Sổ nợ giờ có lãi/trần biến mỗi sự kiện đời thường (sinh nhật, OT) thành "nợ" → nản dần.
> - Rà thị trường (6.964 tin tuyển quốc tế + tin VN, 17/09): **chatbot RAG đã quá phổ thông**; thứ làm nổi là **số eval
>   thật, chi phí, deploy, chiều sâu 1-2 mảng**. **Senior** (VN lẫn remote) đòi 4-5+ năm + ≥2 năm LLM production —
>   side project **không thay được**.

> ## B. Quyết định user chốt 17/09
> | | Chốt |
> |---|---|
> | **Đích qua Tết** | **Bậc thang: AI Engineer mức Mid** (VN hoặc remote hợp đồng) để lấy 1-2 năm LLM production → **Senior remote ~2028** |
> | **Hồ sơ hiện tại** | Backend/fullstack < 3 năm · công ty **không** có cơ hội làm AI · tiếng Anh nói **cơ bản** |
> | **Nghỉ việc** | **Phỏng vấn khi vẫn đi làm**, nộp từ ~tháng 1/2027, chỉ nghỉ khi có offer |
> | **Project chính** | **Nyxara-core miền pháp luật Việt Nam** (dữ liệu công khai, có baseline) + **Nyxara-Orchestrator** (agent + chi phí token) |
> | **N Assistant** (`nyxara`) | **Tạm gác** — quay lại sau khi có việc AI |
> | **Cách code** | **Cách A** (mục D). Test + nối dây: **Claude viết**, user đọc/trace — user không cần viết nhiều test |
> | **Giờ** | Sáng **1h30** · công ty **1h** · tối **2h bắt buộc** · OT mệt → **30' trace** + Claude **phải cảnh báo** hụt giờ |
> | **Ôn** | Câu phỏng vấn nói to + bài bảng trắng 5', hẹn lại ❌+2 · ⚠️+5 · ✅+14 ngày — bắt đầu tối 17/09 |
> | **Nhánh song song** | Code Python thực tế · Tiếng Anh phỏng vấn · Portfolio · Orchestrator (~1h/ngày) |
> | **Độ sâu** | **Vẫn học kỹ như cách đang làm** — vòng 6 bước cho mọi kỹ thuật 🔴, không cắt bước để kịp mốc |

> ## C. Dữ liệu (đã kiểm chứng tồn tại 17/09)
> - **Zalo AI Legal Text Retrieval** — HF `GreenNode/zalo-ai-legal-text-retrieval-vn`: **61,4K điều luật · 818 câu hỏi test có qrels**,
>   có trong MTEB (`ZacLegalTextRetrieval`). **SOTA công khai NDCG@10 = 0.8488** → baseline để so số của mình.
> - Văn bản gốc có metadata (loại văn bản, cơ quan, năm, hiệu lực): các bộ `vbpl` / `vietnamese-legal-documents` trên HF.
> - ⚠️ Kiểm license từng bộ trước khi đưa lên demo công khai.

> ## D. Cách học mới — "Cách A" cho lõi thuật toán
> 1. Claude **giảng** kỹ thuật (là gì, WHY, cấu trúc dữ liệu) — như cũ.
> 2. User viết **mã giả tiếng Việt**, từng bước — **logic 100% của user**.
> 3. Claude **dịch nguyên văn** mỗi bước → đúng 1 dòng Python, **giữ nguyên cả chỗ sai**, không sửa logic hộ, không gợi ý thuật toán.
> 4. User chạy (Claude chạy hộ nếu vướng thao tác) → thấy sai → **tự sửa bước mã giả** hoặc sửa thẳng dòng Python.
> 5. Bug cố ý · debug · fix · document: **như vòng 6 bước cũ**. Test do **Claude viết**, user đọc để biết test bắt gì.
> - **Nối dây** (adapter, API, Qdrant, Docker, CI): Claude viết, user **trace** 1 lượt + giải thích lại bằng lời.
> - **Bảng trắng** (trong giờ ôn) giữ phản xạ tự gõ lõi mà không tốn vòng sửa dấu.

> ## E. Mức độ sâu (theo đích Mid + miền pháp luật)
> | Mức | Nghĩa | ~Giờ/mốc |
> |---|---|---|
> | 🔴 Sâu | Đủ vòng 6 bước + A/B trên golden set → **ra số** | ~5h *(chưa kiểm chứng — đo ở mốc đầu tiên theo cách A)* |
> | 🟡 Nhỏ | Một bản chạy được + một phép đo | ~3h |
> | 🟢 Nói được | Đọc ~1h + trả lời 3-5 câu phỏng vấn đóng sách | ~1h |

> ## F. Lộ trình theo LÁT CẮT (mỗi lát ra một tính năng + một bảng số)
> | Lát | Tính năng | 🔴 Sâu | 🟡 Nhỏ | Phase gốc |
> |---|---|---|---|---|
> | **0** | Đóng mốc 2 đang dở | Metadata filter (cây `and/or/not` → nối Qdrant **và** BM25, dùng metadata văn bản luật) | — | P2 |
> | **1** | **Nền đo** — nạp 61K điều luật, đo baseline | Hit@k · MRR · NDCG@10 (code tay) · A/B harness · regression set (gộp 36 bug cũ) | Bảng BM25 / dense / hybrid / +rerank so SOTA 0.8488 | P3 #1 #4 #5 #6 |
> | **2** | **Retrieval pháp luật** | Chunk theo cấu trúc **Điều/Khoản** (Document-based) · Query Transform (câu đời thường → ngôn ngữ luật, HyDE) · Parse văn bản (HTML/PDF) | MMR · overlap ([bug #34](notes/bug-log.md)) · Parent-Child (khớp Khoản, trả cả Điều) · Contextual (gắn tên Luật/Chương vào chunk) | P0 #4 #9 #10 #11 · P2 #2 #4 |
> | **3** | **Trả lời có trích dẫn, không bịa** | Trích dẫn Điều/Khoản (offset, C2) · Judge tự viết + faithfulness · Từ chối "không có căn cứ" (gộp [bug #33](notes/bug-log.md)) · Chống prompt injection | Hiệu chỉnh judge vs 50 nhãn tay · Lost-in-the-Middle / compression | P3 #2 #3 #7 · P4 #5 · P5 #1 |
> | **4** | **Hiệu lực văn bản** — không trích điều đã hết hiệu lực / bị thay thế | — | Temporal + versioning theo trạng thái hiệu lực | P2 #3 |
> | **5** | **Agent pháp lý + MCP** | Tool calling + structured output · Supervisor nhỏ · Tracing · Đo đường đi (trajectory) · **MCP server** tra cứu luật | Memory hội thoại · HITL | P4 |
> | **6** | **Production + portfolio** | — | Docker + CI chạy regression eval · deploy + **demo URL** · latency p50/p95 + cache + chi phí/query · README dạng spec + bảng số · bài viết tiếng Anh | P3.5 · P7 |
> | 🟢 | **Nói được** | Fine-tune (LoRA, khi nào FT vs RAG) · Quantization · K8s · Drift · GraphRAG · Multimodal · Phase 8, 9 | | |

> ### Bản đồ: 10 Phase bên dưới → thực chất học gì (thêm 17/09)
> Các Phase **không bị xoá** — chúng là **kho kiến thức** (công thức, WHY, bug cố ý gợi ý). Thứ tự làm = lát 0→6.
> Mỗi Phase giờ chỉ có **một phần** được học sâu; phần còn lại ở mức 🟡 hoặc 🟢. Số `#` = số dòng trong bảng của Phase đó.
>
> | Phase | Đã xong | 🔴 Học sâu (lát) | 🟡 Nhỏ (lát) | 🟢 Chỉ nói được |
> |---|---|---|---|---|
> | **0** Ingestion | #1 recursive · #6 dedup · #7 incremental | #9 Document-based theo Điều/Khoản · #11 parse văn bản *(lát 2)* | #4 Parent-Child · #10 Contextual *(lát 2)* · #8 Versioning *(lát 4)* | #2 Semantic · #3 Proposition · #5 Multi-vector |
> | **1** Vector | ✅ toàn bộ | — | — | — |
> | **2** Retrieval | Hybrid · RRF · Rerank · CRAG | #1 Metadata filter *(lát 0)* · #2 Query Transform *(lát 2)* | #4 MMR *(lát 2)* · #5 Compression / Lost-in-the-Middle *(lát 3)* · #3 Temporal *(lát 4)* | #6 Adaptive-RAG · #7 GraphRAG · #8 Multimodal |
> | **3** Eval ⭐ | — | #1 Hit@k/MRR/NDCG · #4 Golden · #5 Regression · #6 A/B *(lát 1)* · #2 Judge · #3 Faithfulness *(lát 3)* | #7 Hiệu chỉnh judge *(lát 3)* · #9 Chi phí/latency *(lát 6)* | #8 Online eval · #10 Bias · #11 RAG vs long-context |
> | **3.5** Performance | — | — | #1 Đo latency từng chặng · #6 Cache + prompt caching *(lát 6)* | #2 Payload index · #3 HNSW · #4 Quantization · #5 Budget 2 tầng · #7 Async batching · #8 Semantic cache |
> | **4** Agent | — | #1 Supervisor · #2 Tool calling · #7 Tracing · #8 MCP · #12 Đo đường đi *(lát 5)* · #5 Từ chối *(lát 3)* | #4 Memory · #6 HITL *(lát 5)* | #3 Intent triage · #10 Routing · #11 Feedback → train · #9 Prompt craft *(luyện xuyên suốt, không thành mốc)* |
> | **5** Safety | — | #1 Chống prompt injection *(lát 3)* | — | #2 PII · #3 Moderation · #4 Output sanitization · #5 Red-team · #6-#11 |
> | **6** Fine-tune | — | — | — | Toàn bộ: LoRA/QLoRA · quantization · synthetic data · embedding FT |
> | **7** MLOps | Vector delete/sync (kéo lên P0) | — | CI/CD chạy regression eval · deploy + demo URL · Load test p50/p95 *(lát 6)* | Model serving (vLLM) · LGTM · Drift · Embedding migration · Retrain · Canary |
> | **8** Community | — | — | — | Toàn bộ (plugin registry, entry-points) |
> | **9** SaaS Bridge | Multi-tenancy (P1) | — | — | Toàn bộ (Metering/Entitlement Port) — xét lại khi quay về N Assistant |
>
> **Tóm lại, học sâu thật ở 5 Phase:** **0** (phần còn lại) · **2** (phần còn lại) · **3** · **4** · **5** (một mục).
> **3.5 và 7** học ở mức nhỏ trong lát 6. **6, 8, 9** chỉ học để nói được trong phỏng vấn.

> **Tạm ước:** 🔴 ~16 × 5h = 80h · 🟡 ~11 × 3h = 33h · 🟢 ~10h · trace Orchestrator ~4h → **~120h**.

> ## G. Toán thời gian tới lúc nộp đơn (~15/01/2027, ~17 tuần)
> | | Giờ-mốc có (sáng 1h30 + tối 1h40, 5 ngày/tuần, trừ 25% OT/đời thường) |
> |---|---|
> | Orchestrator 1h/ngày **nằm ngoài** 4h30 | **~200h** → đủ ~120h, dư ~80h (kể cả khi 🔴 tốn 8h: ~168h, vẫn đủ) |
> | Orchestrator 1h/ngày **trừ vào** 4h30 | **~135h** → đủ ở 5h/🔴, **thiếu** nếu 🔴 tốn 8h |
> ✅ **User chốt 17/09: Orchestrator 1h/ngày NẰM NGOÀI** → tổng **5h30/ngày**, giờ-mốc Nyxara-core ~200h. Slot công ty 1h (tiếng Anh + câu phỏng vấn + Python thực tế) tính riêng.

> ## H. Mốc theo tháng
> | Tháng | Mục tiêu |
> |---|---|
> | **09** (18→30) | Lát 0 đóng · Lát 1 xong (có bảng baseline đầu tiên) |
> | **10** | Lát 2 · Lát 3 nửa đầu |
> | **11** | Lát 3 xong · Lát 4 · Lát 5 nửa đầu · trace Orchestrator |
> | **12** | Lát 5 xong · Lát 6 (deploy, demo, README, bài viết) · CV |
> | **01/2027** | Nộp đơn khi vẫn đi làm · mock interview (tiếng Anh + tiếng Việt) · 🟢 nói được |

> ## I. Nhánh song song (slot công ty 1h/ngày)
> - **Tiếng Anh (~30') — cách làm user chốt 18/09:** user **tự viết text ra** (kể project 60 giây, câu trả lời phỏng vấn) →
>   **Claude chỉnh lại** (ngữ pháp, từ dùng sai, câu Việt-hoá, cách diễn đạt tự nhiên hơn — giữ nguyên ý của user, chỉ sửa
>   cách nói) → user **đọc nhẩm** bản đã chỉnh cho quen miệng. Không bắt nói ngẫu hứng khi chưa có bản viết.
> - **Python thực tế (~15-20'):** 1 bài ngắn dict/chuỗi/logic đời thường — trị thẳng lỗ cú pháp.
> - **Câu phỏng vấn (~10-15'):** [interview-questions.md](interview-questions.md), theo lịch hẹn ❌/⚠️/✅.
> - **Orchestrator:** agent làm, user định hướng nghiên cứu. Muốn đưa vào CV cần **số benchmark thật**
>   (token/task thành công so với agent trực tiếp) + **user tự giảng lại được vòng Planner → Repair**.

> ## J. Luật giờ mới (bỏ sổ nợ có lãi/trần)
> - Mục tiêu mỗi ngày: sáng 1h30 · công ty 1h · tối 2h. **Không lãi, không trần.**
> - Ngày OT mệt: **30' trace**, ưu tiên code viết trong ngày. **Claude phải nói rõ**: hôm nay hụt bao nhiêu,
>   tuần này đã hụt bao nhiêu, ảnh hưởng mốc tháng nào — **không im lặng**.
> - Ngày bận biết trước (sinh nhật…) ghi sẵn là ngày nghỉ.
> - Tối Chủ Nhật 10': đếm **lát/mốc đóng + số câu phỏng vấn đã trả lời**, so với bảng H.
>
> ## K. Chuẩn bị phỏng vấn — 5 vòng thật (rà 17/09 từ bộ câu hỏi phỏng vấn thật 2026)
> Ngân hàng câu hỏi: [interview-questions.md](interview-questions.md) (mục 11-18 thêm 17/09).
> | Vòng | Cần gì | Đến từ đâu trong kế hoạch |
> |---|---|---|
> | **1. Lý thuyết** (45-90') | RAG · eval · agent · chi phí/latency · guardrails · monitoring · fine-tune · **lý thuyết LLM** | Lát 0-6 + 🟢 + ⚠️ **lý thuyết LLM (mới)** |
> | **2. Code** (45-60') | Code thực tế (dict/chuỗi/retry/parse) · cosine NumPy · Python sâu (race, GIL, async) · **DSA easy/medium** | Nhánh Python thực tế · ✅ bug #29 · ⚠️ **DSA (mới)** |
> | **3. System design AI** (60') | Làm rõ yêu cầu → kiến trúc → đi sâu 1 khối → đánh đổi, điểm hỏng · ước chi phí | ⚠️ **Luyện nói (mới)** |
> | **4. Trình bày project** (30-60') | Vì sao chọn · cái gì hỏng · debug thế nào · con số · làm lại đổi gì · 60 giây · tiếng Anh | ✅ bug-log 36 bug + bảng số lát 1-6 · ⚠️ **kịch bản (mới)** |
> | **5. Hành vi** (30-60') | 5-6 câu chuyện STAR: thử thách kỹ thuật, việc mơ hồ, vì sao sang AI | ⚠️ **Mới** |
>
> **5 việc bổ sung** — gần hết nằm trong **slot công ty 1h/ngày** (~85h/17 tuần), không ăn giờ lát cắt:
> | Việc | Làm thế nào | Khi nào | ~Giờ |
> |---|---|---|---|
> | Lý thuyết LLM (transformer, attention, KV cache, tokenization, temperature/top-p, context window) | 🟢 đọc + trả lời mục 11 ngân hàng câu hỏi | 10 → 11/2026 | ~8h |
> | DSA cơ bản (hash map, sort, two pointers, stack/queue) | 1 bài easy/medium/ngày, **thay phiên** với bài Python thực tế | từ 11/2026 | ~25h |
> | System design nói | 1 đề/tuần: tự nói 45' → Claude chấm theo 4 bước | 12/2026 → 01/2027 | ~10h |
> | Trình bày project (60 giây + bản 30' hỏi dồn), tiếng Việt + tiếng Anh | Soạn khung từ tháng 11, hoàn thiện sau lát 6, tự ghi âm | 11/2026 → 01/2027 | ~6h |
> | Hành vi STAR (5-6 chuyện, lấy từ bug-log + chuyện đổi nghề) | Soạn + nói to | 01/2027 | ~4h |
> **Tổng thêm ~53h.**
>
> ## L. Nyxara-Orchestrator — làn song song (chốt 17/09)
> - **Là sản phẩm thật, không chỉ bài thử nghiệm/benchmark** (user nói rõ 17/09). Repo: `~/My-project/Nyxara-Orchestrator`
>   (TypeScript, agent code là chính, user định hướng + kiểm). Roadmap riêng: `docs/ROADMAP.md` của repo đó (M0 → M7 ước 23-41 tuần).
> - **Giờ:** 1h/ngày, **nằm ngoài** 4h30 của Nyxara-core → tổng 5h30/ngày.
> - **Luật Nyxara-core (Cách A, không code hộ) KHÔNG áp cho repo này** — ở đó agent code.
>
> | Thời gian | Orchestrator | Ra được gì |
> |---|---|---|
> | **09-10/2026** | M0 Baseline (tái hiện lỗi task lớn, chụp số N0) → M1 Đo lường (một lệnh so D1 agent trực tiếp vs N0) · **user trace + giảng lại được kiến trúc và harness benchmark (~4h)** | Bảng số đầu tiên |
> | **11-12/2026** | M2 — lát đầu (ngân sách theo model sau feature flag) → so D1 / N0 / N1 | Token cho mỗi task thành công, số thật |
> | **01-02/2027** | Chuẩn bị phát hành: chọn license (roadmap repo gợi ý Apache-2.0) · `SECURITY.md` + giải thích quyền ghi file/chạy lệnh · quickstart · CI kiểm VSIX · README chỉ ghi số đã đo | Đưa vào CV lúc phỏng vấn: repo + số benchmark + *"Marketplace preview Q1/2027"* |
> | **03/2027** | **Preview trên VS Code Marketplace** | Link Marketplace |
> | Sau đó | M3 → M7 | |
>
> - **Cộng hưởng không tốn giờ:** kỷ luật đo học bằng tay ở lát 1 Nyxara-core (golden, A/B một biến, regression) = kỷ luật M1 cần.
> - **Chưa nối kỹ thuật core ↔ Orchestrator** (vd MCP) trước Tết — khác ngôn ngữ, tốn giờ; xét lại cùng M5.
> - **Kể trong phỏng vấn:** *"tôi thiết kế nghiên cứu + benchmark + kiến trúc, dùng AI agent để code, tự kiểm chứng bằng số"* — chỉ nói được khi đã trace ở mốc 09-10.
> - ✅ **Luật ưu tiên khi ngày ngắn — user chốt 17/09:** tối 2h core → sáng 1h30 → slot công ty → **Orchestrator cắt đầu tiên, không tính hụt**.
>   Tối CN: 2 tuần liền Orchestrator ăn vào giờ core → hạ xuống 3 buổi/tuần.


## 🎯 Tầm nhìn dự án

**Nyxara Open** = AI Engineering Toolkit mã nguồn mở (Core MIT), phục vụ 3 mục tiêu cùng lúc:

1. **Giáo trình sống** — học *đủ* mọi kỹ thuật RAG / Agent / MLOps hiện đại, không bỏ sót,
   để có **phán đoán** chọn đúng cái đáng dùng.
2. **Sản phẩm cộng đồng** — Core niche-agnostic, fork được, dùng thật.
3. **Nền SaaS kiếm tiền** — lớp cloud bọc ngoài (billing, metering, entitlement) *không* đụng bộ não AI.

Đích cá nhân: **pass phỏng vấn Senior AI Engineer**. Muốn vậy phải chứng minh được
2 thứ mà mọi thư viện che mất: **tự implement được lõi** và **debug được khi nó hỏng**.

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


## 🎯 Nguyên tắc bao trùm: Học vs. Production

> Project build **tất cả** kỹ thuật để **HỌC cho biết** — nhưng một sản phẩm thật
> **KHÔNG dùng hết**. Mỗi fork chỉ **bật đúng subset** niche cần (mọi kỹ thuật là
> *flag, mặc định TẮT*). Học hết là để **có phán đoán** chọn đúng. **Eval (Phase 3)**
> cho biết cái nào *thật sự đáng bật*. **Học một kỹ thuật ≠ phải deploy nó.**

---

## 📊 Tổng kết Tests

```
66 tests (2026-08-14) — Chunker 2 · Dedup 2 · Edit distance 5 · Pipeline 6 (+2 ingest_document,
bug #22 #23) · Similarity 1 · BGEEmbedder 3 · QdrantStore 3 (+1 delete, bug #21) · BM25 9
(+1 remove_document, bug #20) · InMemoryDocStore 3 (mới — chưa từng có test) · RRF 5 ·
HybridRetriever 3 · Reranker 2 · RerankingRetriever 2 · CRAG: decision 6 · node 4 · graph 2 ·
grader 5 · generator 3
đếm lại bất cứ lúc nào bằng:  grep -rc "def test_" tests
```
> Trước reset có 74 test xanh (P1 vector 15 · BM25 13 · RRF 10 · Hybrid 11 · Reranker 6 · CRAG 12 · Chunker 4 · Ingestion 3).
> Build lại tới đâu, con số bò lên tới đó. Cập nhật sau MỖI lần thêm test — lệch số = tài liệu mất tin cậy.
> Quy ước: mỗi bug sửa ở bất kỳ phase nào → +1 regression test (nguyên tắc gốc #4) + ghi [notes/bug-log.md](notes/bug-log.md).

---

## ✅ Bảng theo dõi tiến độ (checklist)

| Phase | Kỹ thuật | Trạng thái | 🎯 Next Action (việc kế tiếp cụ thể) |
|---|---|---|---|
| 0 | **Recursive** chunking ⚠️ · Document-based ⏳ · Semantic/Proposition ⏳ · Contextual Retrieval ⏳ | 🔨 | ⚠️ **Đã verify 2026-08-25: `/ingest` chạy Fixed-Size, KHÔNG phải Recursive** — `recursive_chunk` chỉ là sliding window theo chỉ số; `split_by_separators` (recursive thật) có test xanh nhưng không nơi nào trong `app/` gọi. Phải nối vào pipeline mới được đánh ✅. Sau đó: **Document-based** (Markdown heading; corpus thật sẵn = `Learning-document/`) |
| 0 | Dedup (exact+near) ✅ · Incremental (append-only) ✅ · **Multi-store delete-aware ingest** 🔨 (kéo sớm từ Phase 7) | 🔨 | Đang làm `BM25Index.remove_document` (1/6 bước) → DocStore/VectorStore delete → manifest theo tenant/doc → diff → ingest orchestrator |
| 1 | Embedding · Qdrant · Tenant Isolation | ✅ | **XONG 2026-07-19** — search + tenant filter + drill silent-failure (bug #13). 15 test |
| 2 | BM25 · Hybrid · RRF | ✅ | **XONG 2026-08-03** — BM25 + RRF + HybridRetriever, 18 test. Phát hiện + fix bug #17 (QdrantStore trả UUID thay vì doc_id gốc) lúc ghép |
| 2 | Cross-encoder Rerank | ✅ | **XONG 2026-08-04** — `Reranker`+`BGEReranker` (model thật, verify điểm 4.75/-2.07) · `DocStore`+`InMemoryDocStore` (lỗ hổng doc_id→text phát hiện khi ghép, đã vá) · `RerankingRetriever` nối Hybrid→text→rerank→sort. 22 test pass (18 retrieval + 2 reranker + 2 vectorstore regression) |
| 2 | CRAG | ✅ | **XONG 2026-08-12** — `state.py`/`node.py`(retrieve+grade+generate)/`decision.py`/`graph.py` (`StateGraph`) + Ollama thật (`qwen2.5:3b` qua Tailscale) cho `grader.py`/`generator.py`. 17 test, verify e2e cả 2 nhánh (CORRECT đi thẳng, INCORRECT lặp rồi van an toàn). Bug #18 (timeout), #19 (case-sensitivity) |
| 2 | Metadata filter · Query transform · Temporal · MMR · Compression · Adaptive/Self-RAG · GraphRAG · Multimodal | ⏳ | ⭐ **BẮT ĐẦU TẠI ĐÂY** — Metadata filtering → MMR |
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

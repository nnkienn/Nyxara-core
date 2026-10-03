# 🛤️ Các làn phụ — tra cứu, không đọc mỗi buổi

> Tách khỏi `LEARNING_ROADMAP.md` ngày **2026-09-24** (dọn "học lan man"). Nội dung giữ nguyên bản 17-18/09.
> Làn chính và thứ tự làm: [LEARNING_ROADMAP.md](LEARNING_ROADMAP.md). **Làn phụ không bao giờ ăn vào giờ XÂY lát cắt.**
>
> | Làn | Giờ | Khi nào mở |
> |---|---|---|
> | Slot công ty (mục I) | 1h/ngày | đang chạy |
> | Chuẩn bị phỏng vấn (mục K) | nằm trong slot công ty | lý thuyết LLM 10/2026 · DSA 11/2026 · system design 12/2026 |
> | Dự án số 2 — trợ lý tư vấn phòng khám (mục L) | 1h/ngày, **cắt đầu tiên** khi ngày ngắn | **sau khi lát 1 đóng** (Orchestrator bỏ 02/10) |
> | RA NGOÀI (mục M) | ~2h/tuần | **khi lát 1 có số** (10/2026) — trước đó không làm |

## I. Nhánh song song (slot công ty 1h/ngày)
- **Tiếng Anh (~30') — cách làm user chốt 18/09:** user **tự viết text ra** (kể project 60 giây, câu trả lời phỏng vấn) →
  **Claude chỉnh lại** (ngữ pháp, từ dùng sai, câu Việt-hoá, cách diễn đạt tự nhiên hơn — giữ nguyên ý của user, chỉ sửa
  cách nói) → user **đọc nhẩm** bản đã chỉnh cho quen miệng. Không bắt nói ngẫu hứng khi chưa có bản viết.
- **Python thực tế (~15-20'):** 1 bài ngắn dict/chuỗi/logic đời thường — trị thẳng lỗ cú pháp.
- **Câu phỏng vấn (~10-15'):** [interview-questions.md](interview-questions.md), theo lịch hẹn ❌/⚠️/✅.
## K. Chuẩn bị phỏng vấn — 5 vòng thật (rà 17/09 từ bộ câu hỏi phỏng vấn thật 2026)
Ngân hàng câu hỏi: [interview-questions.md](interview-questions.md) (mục 11-18 thêm 17/09).

### K0. CHỨC DANH NHẮM — chốt 18/09 sau khi rà thị trường thật
**Hồ sơ thật:** 2 năm fullstack (Python backend + React). **Không** có năm kinh nghiệm AI/ML.

| Nhắm | Vì sao |
|---|---|
| ✅ **AI Backend Engineer · LLM Engineer · AI Software Engineer** | JD loại này = *dựng RAG workflow · indexing/embeddings · tích hợp LLM API vào backend (Django/FastAPI)*. **2 năm backend được tính đủ**, phần AI là phần đang xây |
| ❌ **AI Engineer / ML Engineer thuần** | JD đòi 3-5 năm AI/ML. 2 năm fullstack ở đây bị tính gần như 0 — đấu với người 4 năm ML là tự thua |

**Số thật:** phân tích 43.500 tin AI engineering — phần lớn nhắm **2-6 năm**, phổ biến 4-6, nhưng **chỉ 33% tin
ghi yêu cầu số năm**. Portfolio ăn đứt số năm: *"xây một thứ thật mà người lạ dùng được là đủ lấy ghế mid;
người mất hai năm thường là người đi học thay vì đi ship"*.
**Lương nhắm hợp lý:** 25-35tr (Mid VN 30-45tr yêu cầu 3-5 năm; khung AI-backend đẩy bạn lên đầu trên).

**Hai lỗ so với chuẩn Mid, phải vá bằng lát cắt chứ không bằng học thêm:**
1. *"Đã ship cho người dùng thật"* → deploy tháng 10 (mục H), UI React tự làm.
2. *"3-5 dự án end-to-end"* → Nyxara-core + **trợ lý tư vấn phòng khám (mục L) là dự án số 2** — có người dùng thật (đổi 02/10).

**Từ khoá phải có trên CV** (JD Việt Nam gọi tên đích danh, thiếu là rớt vòng lọc trước khi ai nghe bạn nói):
`LangChain` / `LangGraph` / `LlamaIndex` · `RAGAS` · `Graph RAG` · `Qdrant` · `FastAPI` · `Docker`.
Cả ba cái đầu đã được cắm vào lát 1/4/6 — **không cần học thêm gì ngoài lộ trình**.
| Vòng | Cần gì | Đến từ đâu trong kế hoạch |
|---|---|---|
| **1. Lý thuyết** (45-90') | RAG · eval · agent · chi phí/latency · guardrails · monitoring · fine-tune · **lý thuyết LLM** | Lát 0-6 + 🟢 + ⚠️ **lý thuyết LLM (mới)** |
| **2. Code** (45-60') | Code thực tế (dict/chuỗi/retry/parse) · cosine NumPy · Python sâu (race, GIL, async) · **DSA easy/medium** | Nhánh Python thực tế · ✅ bug #29 · ⚠️ **DSA (mới)** |
| **3. System design AI** (60') | Làm rõ yêu cầu → kiến trúc → đi sâu 1 khối → đánh đổi, điểm hỏng · ước chi phí | ⚠️ **Luyện nói (mới)** |
| **4. Trình bày project** (30-60') | Vì sao chọn · cái gì hỏng · debug thế nào · con số · làm lại đổi gì · 60 giây · tiếng Anh | ✅ bug-log 36 bug + bảng số lát 1-6 · ⚠️ **kịch bản (mới)** |
| **5. Hành vi** (30-60') | 5-6 câu chuyện STAR: thử thách kỹ thuật, việc mơ hồ, vì sao sang AI | ⚠️ **Mới** |

**5 việc bổ sung** — gần hết nằm trong **slot công ty 1h/ngày** (~85h/17 tuần), không ăn giờ lát cắt:
| Việc | Làm thế nào | Khi nào | ~Giờ |
|---|---|---|---|
| Lý thuyết LLM (transformer, attention, KV cache, tokenization, temperature/top-p, context window) | 🟢 đọc + trả lời mục 11 ngân hàng câu hỏi | 10 → 11/2026 | ~8h |
| DSA cơ bản (hash map, sort, two pointers, stack/queue) | 1 bài easy/medium/ngày, **thay phiên** với bài Python thực tế | từ 11/2026 | ~25h |
| System design nói | 1 đề/tuần: tự nói 45' → Claude chấm theo 4 bước | 12/2026 → 01/2027 | ~10h |
| Trình bày project (60 giây + bản 30' hỏi dồn), tiếng Việt + tiếng Anh | Soạn khung từ tháng 11, hoàn thiện sau lát 6, tự ghi âm | 11/2026 → 01/2027 | ~6h |
| Hành vi STAR (5-6 chuyện, lấy từ bug-log + chuyện đổi nghề) | Soạn + nói to | 01/2027 | ~4h |
**Tổng thêm ~53h.**
## L. Dự án số 2 — Trợ lý tư vấn phòng khám (repo `nyxara`) · chốt 02/10, thay Orchestrator

**Vì sao đổi:** Orchestrator bị chê *"không nhắm đúng thị trường, chả ai xài"* — user đồng ý (TypeScript trong khi 7/10 tin
đòi Python · thị trường extension code đã bão hoà · agent code nên khó nhận là của mình). Bản cũ: git history trước 02/10.
Căn cứ chọn: [thi-truong-2026-10.md](notes/thi-truong-2026-10.md) — agent + tool calling là yêu cầu số 1 (8/10).

- **Là gì:** agent trả lời tin nhắn bệnh nhân cho **một phòng khám THẬT** user đang làm (đang tư vấn qua FB Ads + Zalo).
  Đây là năng lực "AI Tư vấn Bệnh nhân" đã có trong README `nyxara`, **cắt gọn**.
- **Phạm vi bản đầu — đúng 3 tool:** ① tra dịch vụ / bảng giá / giờ khám (RAG trên tài liệu phòng khám — dùng lõi `nyxara-core`)
  · ② đặt / dời lịch hẹn (Postgres) · ③ chuyển lễ tân thật (HITL) khi hỏi triệu chứng, khiếu nại, hoặc agent không chắc.
  Kênh: **giả lập trước**, nối Messenger / Zalo OA sau khi agent qua bộ đo.
- **Bộ đo:** hội thoại thật của phòng khám **đã ẩn danh** → 100-200 ca có đáp án (tool đúng · tham số đúng · có chuyển người
  khi phải chuyển). Chấm **tỉ lệ xong việc** + **số bước sai** + **số ca lẽ ra phải chuyển người mà không chuyển** (lỗi nặng nhất).
- **Lấp lỗ tin tuyển:** agent + tool calling · structured output · API OpenAI/Anthropic · Postgres · async webhook · HITL ·
  guardrails · **"đã ship cho người dùng thật"**.
- ⚠️ **Luật không thương lượng:** không chẩn đoán, không kê đơn, luôn có disclaimer (README `nyxara`) · dữ liệu sức khoẻ là
  **dữ liệu cá nhân nhạy cảm** (NĐ 13/2023) → phòng khám đồng ý bằng văn bản trước khi lấy hội thoại · **ẩn danh trước khi
  rời máy phòng khám** · hội thoại thật **không bao giờ vào git**.
- **Giờ:** slot 1h/ngày cũ của Orchestrator (~90h tới 15/02), ước **40-50h**. Cắt đầu tiên khi ngày ngắn.
  **Bắt đầu SAU KHI LÁT 1 ĐÓNG** — dùng lại khung eval của lát 1. Trước đó: chỉ xin phép phòng khám + gom hội thoại (việc của user).
  ✅ **03/10: đã xin phép xong** · lấy hội thoại **T7 10/10** → ẩn danh **trên máy phòng khám** trước khi mang ra.
- **Còn chốt ở buổi mở dự án:** lõi agent (luật chuyển người, chấm bộ đo) áp **Cách A** hay agent code — gợi ý Cách A cho lõi,
  Claude viết nối kênh / webhook / UI, vì "agent code hết" là điểm yếu đã làm Orchestrator bị chê.

## M. RA NGOÀI — làn thứ tư, thêm 18/09 (~2h/tuần, cắt vào giờ Orchestrator khi cần)

> **Vì sao thêm:** user nói *"phỏng vấn + project thực tế + hiểu sâu... vẫn cảm thấy chưa đủ"*.
> Đúng — vì cả ba đều là **chuẩn bị**. Không có cái nào khiến người ta **gọi bạn**.
> Ba làn kia làm bạn sẵn sàng khi chuông reo; làn này làm chuông reo.

| Việc | Làm gì | Khi nào |
|---|---|---|
| **Repo public + README dạng spec** | Bảng số thật (BM25/dense/hybrid/+rerank so SOTA 0.8488), kiến trúc, 1 GIF demo. README **là CV kỹ thuật** | ngay khi lát 1 có số (10/2026) |
| **Demo URL người lạ dùng được** | UI React tối giản, 1 ô hỏi + trích dẫn Điều/Khoản | 10/2026 |
| **Viết bài trong lúc làm, không để cuối** | 1 bài/tháng, tiếng Việt trước (cộng đồng AI VN), bản tiếng Anh sau. Chủ đề có sẵn: *vì sao BM25 trượt `"o to"`* · *tự viết NDCG@10 rồi đối chiếu RAGAS* · *36 bug khi tự xây RAG* | từ 10/2026 |
| **Nộp đơn thăm dò SỚM** | 3-5 chỗ từ **11/2026**, không đợi 01/2027. Mục đích là **lấy phản hồi thật**, không phải để đậu. Rớt sớm rẻ hơn rớt muộn | 11/2026 |
| **Mock interview người thật** | 1-2 buổi, tiếng Việt + tiếng Anh. Claude chấm được nội dung, **không** chấm được áp lực người thật | 12/2026 |

**Luật:** bài viết và README ăn theo việc đang làm, **không** thành mốc riêng ngốn giờ.
Viết về đúng thứ vừa xây xong trong tuần — nếu phải nghiên cứu thêm để viết thì chọn sai chủ đề.

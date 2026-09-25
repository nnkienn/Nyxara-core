# 🧭 Lộ trình — Nyxara-core

> **Dọn 2026-09-24** vì bị chê *"học lan man"* — và đúng: bản cũ 364 dòng chạy 4 làn song song, còn sót
> tầm nhìn Senior/SaaS đá nhau với đích Mid, và từ 01/09 có **77 commit tài liệu, 10 commit vào `app/`** —
> commit `app/` cuối cùng là 13/09.
> File này giờ chỉ trả lời **làm gì, theo thứ tự nào**. Bản đầy đủ: [archive/2026-09-24-LEARNING_ROADMAP.md](archive/2026-09-24-LEARNING_ROADMAP.md).
>
> Tra cứu, **không đọc mỗi buổi**: [phases.md](phases.md) (kiến thức 10 Phase + bản đồ Phase → lát) ·
> [side-lanes.md](side-lanes.md) (slot công ty · phỏng vấn · Orchestrator · RA NGOÀI).
> Chỗ dừng từng buổi: [notes/review-schedule.md](notes/review-schedule.md).

---

## 1. Đích — một câu

**AI Backend / LLM Engineer mức Mid**, nộp đơn **~15/02/2027** (sau Tết) khi vẫn đi làm — **hạn thật duy nhất**.
Bằng chứng: Nyxara-core miền **pháp luật VN** (Zalo Legal 61,4K điều · 818 câu test có qrels · SOTA NDCG@10 **0.8488**,
HF `GreenNode/zalo-ai-legal-text-retrieval-vn`) + **bảng số thật** + **demo người lạ dùng được**.
Độ sâu **giữ nguyên** (vòng 6 bước cho mọi 🔴) — thiếu giờ thì việc trôi nguyên vẹn, không cắt bước.

---

## 2. ĐANG LÀM — lát 0: Metadata filter

Cây `and/or/not` → bộ lọc Qdrant **và** lọc BM25, trên metadata văn bản luật (loại · cơ quan · năm).
Đã có (drill, user tự gõ): `to_and_clause` · `to_or_clause` · `to_not_clause` phẳng · `post_filter`.

> ⚠️ **LUẬT ĐÓNG LÁT (mới 24/09):** một lát chỉ **ĐÓNG** khi code nằm trong **`app/`**, có test, và
> `.venv/bin/python -m pytest -q` **toàn bộ xanh**. Drill là phòng tập, **không phải sản phẩm** —
> drill sạch mà `app/` trống thì lát vẫn MỞ.

Kế hoạch đóng lát 0: xem **tuần 28/09** ở [chỗ dừng](notes/review-schedule.md).

---

## 3. Các lát (mỗi lát = một tính năng + một bảng số)

| Lát | Tính năng | 🔴 Sâu | 🟡 Nhỏ |
|---|---|---|---|
| **0** | **Metadata filter** ← đang ở đây | cây `and/or/not` → Qdrant + BM25 | — |
| **1** | **Nền đo + LÊN MẠNG** — nạp 61K điều, đo baseline, deploy demo | Hit@k · MRR · NDCG@10 (code tay) · A/B harness · regression set (gộp bug cũ) | Bảng BM25 / dense / hybrid / +rerank so 0.8488 · RAGAS 1 lần đối chiếu · so 2-3 embedding · demo URL + UI React |
| **2** | **Retrieval pháp luật** | Chunk theo **Điều/Khoản** · Query Transform (đời thường → ngôn ngữ luật, HyDE) · Parse HTML/PDF | MMR · overlap (bug #34) · Parent-Child · Contextual |
| **3** | **Trích dẫn, không bịa** | Trích Điều/Khoản (offset) · Judge + faithfulness · Từ chối "không có căn cứ" · Chống prompt injection | Hiệu chỉnh judge vs 50 nhãn tay · Lost-in-the-Middle |
| **4** | **Hiệu lực + tham chiếu chéo** | — | Temporal/versioning theo hiệu lực · GraphRAG multi-hop trên dẫn chiếu pháp lý |
| **5** | **Agent pháp lý + MCP** | Tool calling + structured output · Supervisor nhỏ · Tracing · Đo trajectory · MCP server tra luật | Memory hội thoại · HITL |
| **6** | **Production + portfolio** | — | Docker + CI chạy regression eval · latency p50/p95 + cache + chi phí/query · README dạng spec · port lõi sang LangChain một lần · bài viết tiếng Anh |

**Mức:** 🔴 = đủ 6 bước + A/B ra số (~5h, chưa kiểm chứng) · 🟡 = một bản chạy + một phép đo (~3h) ·
🟢 = đọc ~1h + trả lời 3-5 câu phỏng vấn đóng sách (Fine-tune, Quantization, K8s, Drift… — xem bản đồ trong phases.md).
**Tạm ước ~120h việc / ~200h giờ-mốc có tới 15/02.**

**Mốc tháng = CHỈ HƯỚNG, không phải hạn:**

| Tháng | Mục tiêu | Thực tế |
|---|---|---|
| 09 | Lát 0 đóng · Lát 1 xong | ⚠️ 24/09: lát 0 chưa vào `app/` — trễ ~1 tuần |
| 10 | 🚀 Demo lên mạng + repo public + bài viết đầu · Lát 2 | |
| 11 | Lát 3 · nộp đơn thăm dò 3-5 chỗ · Lát 4 | |
| 12 | Lát 5 · Lát 6 · CV · mock interview người thật | |
| 01/2027 | Tháng đệm — bù phần trễ | |
| 02/2027 | **Nộp đơn diện rộng ~15/02** | |

---

## 4. TUẦN MẪU CỐ ĐỊNH — mỗi tuần giống hệt nhau

Mục đích: **không phải quyết định "hôm nay học gì"**. Mở máy là biết.

| Ca | Phút | Làm gì — cố định |
|---|---|---|
| **Sáng 1h30** (T2-T6) | 10' | Vấn đáp đóng sách 2-3 câu tới hạn |
| | 75' | **XÂY** — đúng một việc tiếp theo của lát hiện hành (chỗ dừng) |
| | 5' | Note ≤15 dòng + chỗ dừng |
| **Công ty 1h** (T2-T6) | 20' | Gym cú pháp Python thuần (không domain RAG) |
| | 20' | Vấn đáp đóng sách 3 câu + hẹn lại (❌+2 · ⚠️+5 · ✅+14) |
| | 20' | Tiếng Anh — user viết → Claude chỉnh → đọc to |
| **Tối, bắt đầu ≤20:30, không OT** | 105' + 15' | **XÂY** tiếp việc của ca sáng + note |
| **Tối, bắt đầu >21:00 hoặc vừa OT** | 30' + 15' | Drill ép chọn · gõ ruột ngắn trên code **viết trong ngày**. **45' là DỪNG** |

**Cố định theo thứ trong tuần:**
- **Sáng T4 = bài thiết kế** (CLAUDE.md §4 loại 3) — gắn vào đúng việc XÂY của tuần, không bài rời.
- **T7 = ca tối XÂY nếu rảnh**, không thì nghỉ — không tính hụt.
- **Tối CN 10-20' = TỔNG KẾT TUẦN**: đếm lát đóng (theo luật §2) + số câu vấn đáp + số lần tắc cứng ·
  viết kế hoạch tuần sau vào chỗ dừng. **Đây là chỗ DUY NHẤT được sửa phương pháp / luật / roadmap.**

**Tỷ lệ:** XÂY ~70% · DRILL ~20% · META ≤5%. Ca sáng không bao giờ drill suông.
**Thứ tự cắt khi ngày ngắn:** Orchestrator → slot công ty → sáng → **tối giữ đến cùng**.
Ngày OT: Claude **phải nói rõ** hụt bao nhiêu, tuần này hụt bao nhiêu — không im lặng.

---

## 5. CHẾ ĐỘ CÔNG TÁC / NGÀY BẬN BIẾT TRƯỚC

Ghi sẵn là **ngày nghỉ, không tính hụt**. Có 15-20' rảnh thì tranh thủ, chọn **một** trong thực đơn —
tất cả làm được **không cần repo, không cần GPU**, chỉ cần điện thoại hoặc laptop:

| Món | Cần gì | Ghi lại |
|---|---|---|
| **Vấn đáp 1 câu tới hạn** — nói to, đóng sách, rồi mới mở đáp án | điện thoại | điểm ✅/⚠️/❌ vào ghi chú điện thoại, về nhà chép vào sổ |
| **Đọc to bản tiếng Anh đã chỉnh** 2 lượt ([english-speaking.md](notes/english-speaking.md)) | điện thoại | tick |
| **Gym cú pháp** — 1 ván trên file drill | laptop có Python | kết quả chạy |
| **Viết nháp tiếng Anh** câu phỏng vấn kế tiếp (chưa chỉnh) | điện thoại | để Claude chỉnh khi về |

**Cấm khi công tác:** mở kỹ thuật mới · đọc code lạ · trace code cũ · sửa kế hoạch/luật.
**Ngày đầu về:** không bù giờ — chạy đúng tuần mẫu §4 từ ca kế tiếp.

---

## 6. Luật chống lan man (24/09)

1. **Một lát tại một thời điểm.** Không mở lát sau khi lát trước chưa đóng theo luật §2.
2. **Làn phụ** ([side-lanes.md](side-lanes.md)) **không ăn giờ XÂY**. RA NGOÀI chỉ mở khi lát 1 có số.
3. **Phương pháp chỉ đổi ở tối CN**, sửa thì phải bỏ một luật khác (CLAUDE.md ≤150 dòng).
   Lỗi phương pháp thấy giữa buổi → ghi 1 dòng vào note, **không vá ngay**.
4. **Mỗi lát tạo tối đa ~1 file drill/buổi.** Drill phục vụ việc XÂY đang làm, không thành việc riêng.
   Drill cũ hơn 1 tuần → `drills/archive/`.
5. **Đo sản phẩm bằng `git log -- app tests`**, không bằng số commit tài liệu. Tổng kết CN đếm cả hai.

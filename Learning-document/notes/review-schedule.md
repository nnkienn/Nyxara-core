# 🔁 Lịch ôn + nhật ký buổi

> 🧹 **Dọn 2026-09-18:** file này từng 1.300 dòng (nhật ký từ 04/09, cộng bảng ôn +1/+3/+7/+14 đã bị
> thay từ 17/09). Toàn bộ bản cũ: [archive/2026-09-18-review-schedule.md](../archive/2026-09-18-review-schedule.md).
>
> **Luật mới (18/09): mỗi buổi tối đa ~15 dòng** — drill gì · điểm · hỏng chỗ nào · mai bắt đầu từ đâu.
> Giữ ~2 tuần gần nhất, cũ hơn thì đẩy vào `archive/`. **Note dài hơn buổi học là note sai.**

---

## 📅 Đang tới hạn (hẹn theo kết quả vấn đáp: ❌ +2 · ⚠️ +5 · ✅ +14)

| Hạn | Câu | Lần trước hỏng gì |
|---|---|---|
| **20/09** | 3.9 tenant filtering | *"search xong mới lọc"* — thực ra BM25 chặn bằng **khoá ngoài cùng**, doc tenant khác **không vào nổi** vòng chấm điểm. Tối 18/09 drill lại đúng 3/3, vẫn đo lại cho chắc |
| **20/09** | 3.8 BM25 khớp theo cái gì | **Đảo nhãn hoàn toàn** (nói BM25 khớp *ngữ nghĩa*). Drill tối 18/09 đã lật lại 11/12 — đo lại đóng sách |
| **23/09** | 3.5 RRF | WHY sạch, nhưng công thức lệch: nói *"1/k+60"*, đúng là `1/(k + rank)` với `k=60`; thiếu chữ **cộng dồn theo `doc_id`** |
| **23/09** | 1.4 Recursive chunker | Đúng 2 bước split+merge nhưng **thiếu hậu quả** (mẩu 1 chữ → vector vô nghĩa) |

**Cách ôn:** đóng sách, nói to, trả lời hết khả năng **rồi mới** mở note đối chiếu → chấm ✅/⚠️/❌ →
ghi vào [interview-questions.md § Nhật ký vấn đáp](../interview-questions.md) → hẹn lại.
⚠️ Đọc câu rồi đọc luôn đáp án là **vô ích** — cảm giác "à mình biết mà" là ảo giác quen thuộc.

**Hai luật ôn rút ra từ thực tế, đừng quên:**
1. **Lỗi "lẫn 2 thứ na ná nhau" → drill ép chọn, KHÔNG giảng lại.** Đo được: 1/4 → 11/12 trong một vòng
   (03/09) · BM25 đảo nhãn → 11/12 sau một ngày (18/09). Giảng lại lần hai thì 12h sau vẫn lẫn.
   Cặp mới ghi vào [the-phan-biet.md](./the-phan-biet.md).
2. **Trượt thì không tick**, và không mở kỹ thuật mới trong buổi mốc ôn bị trượt — vá nền trước.

---

## 📓 Nhật ký buổi

### 2026-09-19 (T7) — 1 ca tối 20:40-22:50 (~2h10) · LÁT 0 · **BUỔI HỎNG**

- Việc: pre-filter — dịch cây `and/or/not` sang `Filter` Qdrant. **Không hoàn thành.**
- **0 lượt gõ code thật trong 100 phút đầu** — Claude cho đoán liên tiếp thay vì cho làm. Đúng loại
  "buổi hỏng" mà CLAUDE.md §4 cấm. Lỗi ở cách dạy, không ở user.
- **5 lần lỗi ĐỌC/CHÉP** (không phải lỗi hiểu): `năm` thay `nam` (3 lần) · `"Bộ Tài Chính"` C hoa
  thay `"Bộ Tài chính"` · thiếu `}` đóng. → luật mới: **giá trị lấy từ dữ liệu thì COPY-PASTE, không gõ tay.**
- Lẫn mới: **`must_not` bị hiểu thành ngăn CHỌN RA** (đúng là ngăn LOẠI RA) → the-phan-biet.
- Lẫn mới: **`danh_gia` (chấm, cần metadata, ra True/False) ↔ `to_qdrant_filter` (dịch đơn, không cần
  metadata, ra dict)** — user nói "tồn tại thì must, không tồn tại thì must_not" = giọng của hàm chấm.
- Hai thứ học được thật: **bộ lọc sai không bao giờ nổ**, chỉ lặng lẽ trả sai → phải chạy trên kho nhỏ
  đã biết đáp án. Và `unexpected EOF while parsing` = thiếu ngoặc đóng, con trỏ chỉ cuối file, không chỉ đúng chỗ.
- User dừng buổi: *"không hiểu quả và cực kì mệt, suy sụp vì không đọc được code"*.

**⚙️ ĐỔI PHƯƠNG PHÁP (chốt 19/09, KHOÁ tới 27/09 mới bàn lại):**
Kỹ thuật **mới** → **PRIMM** (Claude viết bản chạy được → user đoán → chạy → soi → sửa vặt → gõ lại từ trắng).
Kỹ thuật **đã đọc qua** → giữ **Cách A** (user mã giả, Claude dịch). Cách A không sai, 18/09 đo tốt —
sai là dùng nó cho thứ user chưa đọc bao giờ. Căn cứ: PRIMM (~500 học sinh) + Parsons problems
(ghép code có sẵn ≈ hiệu quả ngang viết từ đầu, tải nhận thức thấp hơn nhiều).
**Chấm bằng 2 số, tới 27/09:** (1) số lần tắc cứng phải hỏi Claude mới đi tiếp được ·
(2) cuối mỗi kỹ thuật đóng file gõ lại từ trắng được hay không. Không khá hơn thì bỏ PRIMM.

---

### 2026-09-18 (T6) — 3 ca, ~2h55 · LÁT 0

**Ca sáng 06:01-07:05 (~55' giờ-mốc) — ngày đo chuẩn của Cách A**
- Trả xong vòng đoán `not` (thẻ đổi sang metadata văn bản luật thật) · thêm guard `not` phải đúng 1 con.
- **Lỗi logic duy nhất: VÀ ↔ HOẶC** — vá bằng kho 3 văn bản chạy cả hai chiều.
- **`loc_sau`** (post-filter): user viết mã giả tiếng Việt → Claude dịch. Thiếu `list_out = []` và `return`,
  cả hai lòi ra bằng chạy thật. Rồi **gõ tay `post_filter`, tên tiếng Anh, XANH NGAY LẦN ĐẦU**.
- Đo: **3 lỗi logic · 1 lỗi cú pháp · 0 vòng đỏ do gõ** ⇒ Cách A đúng như giả định, giữ.

**Slot công ty (~1h) — vòng vấn đáp đóng sách ĐẦU TIÊN: 0 ✅ · 2 ⚠️ · 1 ❌**
- Lỗ nặng nhất: **BM25 đảo nhãn** → [Cặp 15](./the-phan-biet.md). Vá bằng bài đo, không giảng.
- Mẩu 1 Python `doc_dong` xong — 5 vòng đỏ, **không vòng nào là lỗi logic**, hỏng toàn ở vỏ cú pháp.
  Đáng nhớ nhất: `so[temp[0]] = temp=[1]` — một dấu `=` lạc chỗ, **không nổ phát nào**, sai sạch mà chạy trơn.
- English: pitch 60s lần đầu. Đóng sách nhớ đoạn 1, **rơi 3/4 còn lại**. Ôn bằng 4 móc:
  `BY HAND` · `PIVOT` · `NUMBER` · `BUG LOG`.
- User tự nhận: *"tôi chưa hoàn toàn trả lời thuần thục phỏng vấn được"* → slot công ty **không được cắt**.

**Ca tối 22:07-22:55 (~50', vừa OT về) — hụt ~1h10 so với slot tối 2h**
- Áp §6 CLAUDE.md: không đọc code lạ, pre-filter đẩy sang ca sáng. Drill ép chọn **11/12**
  ([drill](../drills/2026-09-18-toi-ep-chon-bm25-tenant.py)) — Cặp 15 lật đúng chiều, tenant 3/3.
- Sai 1 ô: **số hiệu văn bản `15/2022/ND-CP` là ca của BM25**, không phải dense (IDF 0.981 vs 0.470).
  **Hai cảnh phải nhớ thay cho nhãn:** `"o to"` = DENSE · `15/2022/ND-CP` = BM25.
- **Lỗi ĐỌC ĐỀ lần thứ 3** — trả `CÓ/RỖNG` cho câu hỏi `BM25/DENSE`, hai đáp án ngược nhau cho cùng một cảnh.
- `dem_luot`: thuật toán đầu tiên user nói ra **sai** (đếm dãy liên tiếp, chỉ đúng nếu log đã xếp).
  Gỡ bằng một câu hỏi một ô: *"`count = 0` giữ được mấy con số?"*. **Ruột do Claude gõ** (ngoại lệ mệt)
  ⇒ **buổi này KHÔNG tính là có lượt gõ thật**.
- ⭐ Bug im lặng: `def` thụt 4 dấu cách → `dem_luot` lọt **vào trong** `doc_dong`, chạy file không lỗi
  không kết quả. **User tự tìm ra và tự sửa** — lượt debug thật của buổi.
- Cuối buổi: dọn lại toàn bộ tài liệu (3.324 → ~1.100 dòng, phần cắt vào `archive/`).

---

### 2026-09-20 (CN) chiều 16:49-17:30 (~40', buổi NHẸ sau nghỉ, user báo chán)

- Không đọc code lạ, không thiết kế. Chỉ: vá 1 chỗ lẫn + drill ép chọn + gõ ruột ngắn.
- **Lẫn 1:** ô trong `{"range": {___: 2015}}` điền `"nam"` (tên trường) thay vì `"gte"` (phép so sánh).
  Vá bằng in thật 3 biến → **drill ép chọn 3/3** ngay sau đó.
- **Gõ ruột `to_range_clause`** ([drill](../drills/2026-09-20-chieu-go-ruot-range.py)) — **4/4 ca đúng**.
  Hai vòng đỏ, cả hai là lỗi **chép máy móc từ file PRIMM**: `pred.keys()[0]` (quên bọc `list`) và
  biến `phep` không tồn tại (file này đặt tên `op`). Không vòng nào là lỗi logic.
- ⭐ **Tay đúng, miệng sai:** gõ đúng `pred[op][0]` nhưng hỏi *"`pred[op]` chứa gì"* thì trả `"gte"`.
  → [Cặp 16](./the-phan-biet.md) — tái phát của "lỗi A" 15/09. Lần sau gặp: **dựng bài đo, cấm giảng lại.**
- Chưa làm: vấn đáp 3.8/3.9 · PRIMM `to_qdrant_filter` (mục SOI + SỬA VẶT) · nợ cũ 18/09.

---

## ⏸️ CHỖ DỪNG — buổi sau làm từ đây

1. **Bài Parsons pre-filter** (Claude soạn sẵn tối 19/09): `to_qdrant_filter` bản ĐÃ CHẠY ĐƯỢC +
   bản xáo dòng để user sắp lại. Chạy theo PRIMM: đoán → chạy → soi → sửa vặt → gõ lại từ trắng.
   File: [drills/2026-09-19-to-qdrant-filter.py](../drills/2026-09-19-to-qdrant-filter.py) (bản ✍️ trắng, 0/8).
2. **Vấn đáp tới hạn 20/09** — 3.9 tenant filtering · 3.8 BM25 khớp theo cái gì. Đóng sách, 10' đầu buổi.
3. **Nợ cũ còn nguyên:** gõ ruột `cham_nhat` ([drill 18/09](../drills/2026-09-18-congty-python.py)) ·
   `eq/ne/gt/gte/lt/lte` vào glossary · pitch 4 móc đọc to.
4. **Theo dõi:** lỗi đọc đề/chép sai đã **8 lần** cộng dồn. Bắt buộc copy-paste giá trị, cấm gõ tay.

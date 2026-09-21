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
| **25/09** | 3.8 BM25 khớp theo cái gì | 20/09 ⚠️: nói nhầm *"rank"* (rank là đầu vào của RRF, không phải của BM25), không nêu được **mặt chữ + TF/IDF**. Đo bằng drill ép chọn, không hỏi lại trần |
| **04/10** | 3.9 tenant filtering | 20/09 ✅ đủ đáp án + lý do (khoá ngầm ngoài cùng, BM25 chỉ chấm doc đã qua lọc) |
| **05/10** | 3.5 RRF | 21/09 ✅ công thức + WHY + số hạng + **tự nói ra "cùng `doc_id`"** cuối buổi. Lần sau hỏi thẳng, không cho tính thay |
| **05/10** | 1.4 Recursive chunker | 21/09 ✅ tự nói được hậu quả: vector rác toàn "thì/là/ở" vẫn chiếm chỗ top-k |

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

### 2026-09-20 (CN) tối 18:43-20:05 (~1h20) · LÁT 0 · PRIMM buổi đầu

- **Vấn đáp tới hạn:** 3.9 ✅ (tự nói đúng cả cơ chế: khoá ngầm ngoài cùng, BM25 chỉ chấm phần đã
  qua lọc → +14, hẹn 04/10) · 3.8 ⚠️ (nói nhầm *"rank"*; rank là đầu vào RRF, không phải BM25 → 25/09).
- **Trượt 3 lượt liên tiếp, cả 3 cùng MỘT lỗ: quên CÁI GỐC.** Đoán cây `and` → trả 2 dict rời, thiếu
  `{"must": [...]}` bọc ngoài · đếm số lần gọi → nói 2, đúng là **3**. Lượt thứ 3 **không tính**:
  bản in của Claude căn lề sai (dòng `trả ra` của #1 thụt 12 dấu, của #2/#3 thụt 14) → lỗi của Claude.
- ⭐ **Miệng trượt nhưng TAY GÕ ĐÚNG.** [Gõ ruột gốc](../drills/2026-09-20-toi-go-ruot-goc.py) **4/6** —
  và ca đúng bao gồm đúng cái ca đầu buổi đoán sai, có đủ `{"must": [...]}`. Ca `and` 3 lá cũng đúng.
- 2 ca đỏ chung một gốc: ruột `or` thiếu `danh_sach_con = []`. **User tự tìm ra** bằng cách đặt ruột 1
  cạnh ruột 2 — lượt debug thật của buổi. Chưa kịp sửa.
- 🔴 **Nút thật của buổi:** *"viết xong cũng không biết hàm này đang làm gì"* → gõ được mà không có nghĩa.
  Gỡ bằng kho 5 văn bản chạy thật: 5 vào, **2 sống**, `vb5` "Thông tư về thuế" đúng chủ đề vẫn bị cắt
  vì `loai != Nghị định`. User tự gọi đúng tên: **metadata filtering**. Đúng luật 09/09 — số thật vào, lời nói không.
- Lỗi chép cộng dồn: **10 lần** (tối nay thêm 2: `nghi_dinh` gõ tay · `2015` thay `2020`).
- Lẫn mới: [Cặp 17](./the-phan-biet.md) — `match` khoá chết cứng `"value"` ↔ `range` điền tên phép.
  Là chiều ngược của Cặp 16 **cùng ngày** ⇒ lần sau dựng bài đo, cấm giảng.
- **Chấm PRIMM (số 1/2, hẹn 27/09):** tắc cứng phải hỏi Claude = **1 lần** (câu "hàm này làm gì").

---

### 2026-09-21 (T2) ca công ty 15:20-16:30 (~1h10) · Python thuần + drill

- **Trả xong nợ `cham_nhat`** ([drill 18/09](../drills/2026-09-18-congty-python.py)) — **3/3 ca** kể cả ca bẫy
  (lượt chậm nhất nằm giữa). **Ruột user gõ** ⇒ lượt gõ thật. Bài thiết kế chuỗi↔số chọn đúng, lý do tự nói.
- User xin *"nói ra các bước"* → Claude KHÔNG cho danh sách bước, đổi thành **bảng 5 lượt 2 cột** (ms lớn nhất
  tới giờ / tên lượt đó); điền xong thuật toán tự lộ. **Giữ cách này dùng lần sau.**
- 2 bug, **user tự sửa sau khi Claude in số**: `'120' > 0` nổ `TypeError` (mọi giá trị ra từ `doc_dong` là
  **chuỗi**) · `name = dong["user"]` đặt **ngoài** `if` → trả tên **lượt cuối**; bản gốc vẫn ra `'binh'`, chỉ
  lòi khi **đảo ngược log** (ra `'kien'`) — sai mà xanh.
- **Trượt 2 lượt liên tiếp, cả 2 lỗi ĐỌC** (trả lời theo `dem_luot` chứ không theo `cham_nhat`) → áp §6,
  dừng hỏi, in bảng biến từng lượt. Vào ngay.
- **Drill ép chọn Cặp 16+17: 9/10.** ⭐ **Cặp 16 SẠCH** (6/6, kể cả `d[list(d.keys())[0]]`). Sai câu `match`
  ⇒ **Cặp 17 vẫn hở** → đo bằng Qdrant thật rồi ép chọn 2 câu → **2/2**.
- ⚠️ **Lỗi Claude:** 3 câu drill dùng tên lớp thư viện (`MatchValue`, `Range`) user chưa gặp → *"không hiểu
  câu hỏi"*. Đo một cặp thì cấm kéo từ vựng mới vào.
- **Vấn đáp (làm sớm 2 ngày): 3.5 ✅ · 1.4 ✅**, cả hai từ ⚠️ lên, hẹn **05/10**. Lỗ còn lại là lỗ **miệng**:
  tính đúng `vb7`=2 số hạng / `vb3`=1 nhưng phải nhắc mới nói ra *"cùng `doc_id`"* — **cuối buổi tự nói lại được**.
  Luật rút ra: loại câu này **cấm trả lời bằng con số**, bắt nói tiêu chí thành lời.
- **Tiếng Anh (bản viết đầu tiên, ~10')**: user tự viết 5 câu "what are you building" → Claude chỉnh, giữ ý.
  3 lỗi lặp: `a` trước nguyên âm · `half past year` (chỉ dùng cho giờ) → `six months ago` · 3 động từ chồng nhau.
  Nợ: **đọc to bản đã chỉnh 2 lượt**.
- **Hạn nộp đơn đổi 15/01 → ~15/02/2027** ("qua Tết", user chốt hôm nay) — ghi ở [roadmap mục G+H](../LEARNING_ROADMAP.md).
  Giữ độ sâu, dời hạn, không cắt bước. Mốc tháng từ đây là **mốc chỉ hướng**, hạn thật chỉ còn 15/02.
- Lỗi chép cộng dồn **12** (+2). Slot Python ăn 35'/20' nên tiếng Anh bị dồn xuống ~10'.

---

## ⏸️ CHỖ DỪNG — buổi sau làm từ đây

1. **Sửa ruột `or` cho 6/6** ([drill tối 20/09](../drills/2026-09-20-toi-go-ruot-goc.py), đang 4/6).
   Thiếu đúng 1 dòng, user đã tự khoanh đúng chỗ — **để user tự thêm, Claude không gõ hộ.**
   Xong 6/6 thì sang **GÕ LẠI TỪ TRẮNG** (bước 5 PRIMM) = số đo thứ 2 của PRIMM, hẹn chấm 27/09.
2. **Mục SỬA VẶT** trong [file PRIMM](../drills/2026-09-20-primm-to-qdrant-filter.py): V1 thêm phép
   `in` · V2 gộp thân `and`/`or` · V3 bắt `{"not": [con1, con2]}` phải nổ.
3. **Dọn `cham_nhat`** (2 dòng, 1 phút): `name = {}` khai dict nhưng giữ chuỗi · `max` trùng tên hàm
   sẵn có của Python. Đặt lại 2 tên tiếng Anh.
4. **Nợ cũ:** `eq/ne/gt/gte/lt/lte` vào glossary. Tiếng Anh bản 1 **đã đọc to ✅** —
   buổi sau viết bản 2: *"why did you switch to AI?"* ([english-speaking.md](./english-speaking.md)).
5. **Theo dõi:** lỗi đọc đề/chép sai **12 lần** cộng dồn. Bắt buộc copy-paste giá trị, cấm gõ tay.
6. ⚠️ **Nhắc Claude:** nghĩa (hàm này để làm gì, nằm ở đâu trong luồng) phải nói **TRƯỚC** khi bắt gõ ruột.
7. ⚠️ **Nhắc Claude — 2 cách đã đo là ăn, dùng lại:** (a) user xin "cho các bước" → đưa **bảng số 2 cột
   để user điền**, không đưa danh sách bước; (b) bài đo một cặp thì **cấm kéo từ vựng mới** vào câu hỏi.
8. **Cặp 17 (`match` ↔ `range`)** mới chỉ 2/2 sau khi đo — chưa coi là sạch, **xen 2 câu ép chọn vào
   đầu buổi sau**; sạch thì mới gỡ. Cặp 16 đã sạch, khỏi hỏi lại.

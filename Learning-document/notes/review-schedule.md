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
| **04/10** | 3.8 BM25 khớp theo cái gì | 29/09 ⚠️: ép chọn 4/5, câu lời có TF nhưng nói *"khớp theo văn bản"* (thiếu **mặt chữ**) + **thiếu IDF**. Lần sau: chỉ hỏi câu lời, phải đủ 3 ý |
| **04/10** | 10.10 vì sao port nhận cây trung lập, không nhận dict Qdrant | 02/10 ❌: không nói được 2 hậu quả (BM25 phải dịch lần 2 · đổi DB sửa 4 chỗ thay vì 1) |
| **04/10** | 3.9 tenant filtering | 20/09 ✅ đủ đáp án + lý do (khoá ngầm ngoài cùng, BM25 chỉ chấm doc đã qua lọc) |
| **05/10** | 3.5 RRF | 21/09 ✅ công thức + WHY + số hạng + **tự nói ra "cùng `doc_id`"** cuối buổi. Lần sau hỏi thẳng, không cho tính thay |
| **07/10** | 10.11 port / adapter là gì | 02/10 ⚠️: giảng lại đúng nhưng **ngay sau khi đọc** — lần sau đóng sách hẳn |
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

### 2026-09-22 (T3) ca sáng 05:00-05:55 (~55') · LÁT 0 · **ĐỔI BẬC BÀI**

- Xen Cặp 17 đầu buổi: **1/2**, sai lại ô `match`. Dựng [bài đo Qdrant thật](../drills/2026-09-22-sang-do-cap17.py)
  (`match: {"eq": ...}` **nổ lúc dựng tờ đơn**, chưa kịp đi tìm) → vòng 2 chứng minh `eq` trên **số** cũng nổ
  ⇒ chữ *"chuỗi"* trong tiêu chí user là thứ làm hỏng. Ép chọn lại **3/3**.
- **Sửa ruột `or` → 6/6.** `danh_sach_con = []` chỉ nằm trong nhánh `and`, nhánh `or` không thấy →
  `UnboundLocalError`. User **không gỡ được, yêu cầu Claude viết hộ** — Claude sửa (đúng ngoại lệ §2).
- 🔴 **User nổ giữa buổi:** *"đọc này tôi hiểu gì chết liền, mất cả buổi sáng để hỏi linh tinh"*. Hỏi lại thì
  tắc **cả 4 chỗ cùng lúc**: đệ quy · dict lồng · cú pháp Python · không rõ hàm để làm gì.
  ⇒ **Bài đệ quy là quá tầm**, lỗi ở Claude đã ném nó ra quá sớm. Bỏ đệ quy giữa buổi, lùi 1 bậc.
- **Trạm mới 1 — [bóc lớp](../drills/2026-09-22-sang-boc-lop.py) 4/4**, kể cả ô 5 tầng ngoặc, tự gõ.
  Claude in sẵn bảng `LOP 0..4` kèm cột `type`; luật một câu: *dict bóc bằng `["khoá"]`, list bóc bằng `[số]`*.
- **Trạm mới 2 — [`to_and_clause` phẳng](../drills/2026-09-22-sang-and-phang.py) 3/3**, vòng `for` gọi
  `to_leaf_clause`, **không đệ quy**. Lỗi duy nhất không-phải-cú-pháp: **quên cái bọc `{"must": ...}`** —
  đúng lỗ đã trượt 3 lượt tối 20/09.
- ⚠️ **Tất cả lỗi còn lại của buổi đều là VỎ CÚ PHÁP**, không lỗi logic nào: `list_out[]` thiếu `=` ·
  thiếu `:` sau `for` · `list_out()` gọi biến như hàm · `{"must": list_out"}` nháy thừa · xoá nhầm dòng
  comment của Claude. ⇒ [Cặp 18](./the-phan-biet.md) (tên biến ↔ tên hàm trước `(...)`), sai **3 lần/buổi**.
- **Thêm 30' (07:05-07:25) — [`to_or_clause` + `to_not_clause` phẳng](../drills/2026-09-22-sang-or-not-phang.py) 4/4.**
  `or` **xanh ngay lần đầu, 0 vòng đỏ** (lần đầu trong ngày). `not` 3 vòng đỏ nhưng **cả 3 là lỗi bóc lớp/chỉ số**,
  không lỗi cú pháp nào: đưa cả list cho `to_leaf_clause` → `AttributeError: 'list' has no keys` ·
  `pred["not"][1]` trên list 1 phần tử → `IndexError` (tái phát lỗi "đếm `[1]` từ 1" của 15/09) · quên bọc list.
  ⇒ Vỏ cú pháp chặt lại thấy rõ trong 2h: đầu buổi 5 lỗi cú pháp liên tiếp, cuối buổi 0.
- **Kết luận phương pháp:** user nói *"đọc không hiểu"* nhưng bóc 5 tầng ngoặc đúng ngay ⇒ nút thật là
  **cú pháp trong tay**, không phải đầu. Hợp với ghi nhận cũ "hiểu nhưng không code lại được".

---

### 2026-09-23 (T4) ca công ty 15:17 (~30', hụt giờ) · gym cú pháp ván 1

- 22/09 chỉ có ca sáng, **ca công ty + ca tối không ghi → tính hụt**.
- Gym ván 1: ô 1·2·5·9 đúng. **Hỏng chủ yếu vì ĐỌC ĐỀ, không phải logic:** ô 3 + ô 8 lấy nhầm từ `bag`
  (đề bảo `D` / `CAY`) · đặt `key1` thay `key_1` · ô 6 `XS[2]` (đề bảo số âm). Vỏ cú pháp: `count == 0` ·
  `XS.len()` · ô 10 thiếu `return`. User hết giờ, xin đáp án → Claude đưa (ngoại lệ §2), **user chưa gõ vào file**.
- Luật mới: **copy-paste tên biến từ comment đề**, không gõ tay. Lỗi đọc/chép cộng dồn **15** (+3).

---

### 2026-09-24 (T5) — **DỌN "HỌC LAN MAN"** (không có ca học)

- Bạn của user đọc roadmap, chê *"lan man"*. Đo lại: từ 01/09 có **77 commit tài liệu, 10 commit `app/`**, commit
  `app/` cuối là 13/09 · lát 0 ăn ~12-15h / hộp 8h mà **chưa dòng nào vào `app/`** · phương pháp đổi 4 lần trong 1 tuần.
- Dọn: roadmap 364 → ~120 dòng (một lát, một tuần mẫu cố định, chế độ công tác) · 4 làn phụ → `side-lanes.md` ·
  bản đồ Phase → `phases.md` · 19 drill cũ → `drills/archive/`. Bản đủ: `archive/2026-09-24-LEARNING_ROADMAP.md`.
- **Luật mới: lát chỉ ĐÓNG khi code ở trong `app/` + pytest toàn bộ xanh.** Drill sạch mà `app/` trống thì lát vẫn MỞ.
- 25-27/09 user đi công tác → **ngày nghỉ, không tính hụt** ([roadmap §5](../LEARNING_ROADMAP.md)).

---

### 2026-09-25 (T6) ca tối 20:53-21:40 (~45', ngày công tác — không tính hụt) · ca tối muộn: drill + gõ ruột

- **Drill ép chọn BM25 10 câu → 10/10** (mặt chữ↔nghĩa 6/6 · IDF chữ hiếm · chuẩn hoá độ dài · ô "tính BM25 có cần rank không" = `S`). Cặp 15 vẫn sạch, lỗi *"rank"* của 20/09 đã hết.
- **Nhưng đóng sách kể ra thì rơi 1/3 đại lượng** → 3.8 chấm **⚠️**, hẹn 30/09 hỏi miệng. Bài học phương pháp: **10/10 ép chọn KHÔNG chứng minh dựng lại được** — có 2 phương án trước mắt thì chọn đúng, từ đầu trống thì thiếu. Trùng ghi nhận cũ "hiểu nhưng không code lại được", lần này ở mức nói.
- Vào được sau khi chạy `BM25Index` thật: cùng `tf=2`, cùng `idf=0.1823`, `doc_len` **8 vs 170** → **0.3682 vs 0.2015**.
- **Gym ván 1 chưa xong 10/10.** 3 vòng đỏ, gốc là **ô 8**: bóc được `CAY["and"]` rồi vẫn dùng giọng dict cho cái list vừa bóc (`key.Keys()` · `key["key_con"]`) ⇒ [Cặp 19](./the-phan-biet.md) mới, trượt 3 lượt, chỉ vào sau khi in đường đi.
- Lỗi vỏ/chép của buổi: `XS.len()` · `.Keys()` K hoa · nháy quanh tên biến · **sửa `key1`→`key_1` ở ô 3 mà quên chỗ dùng ở ô 4** · `XS[2]` bỏ sót yêu cầu "số âm". Lỗi đọc đề/chép cộng dồn **→ 18** (+3).
- ⚠️ User báo *"done tôi nghĩ vậy"* nhưng file vẫn nổ — **luật: chưa dán output thì chưa gọi là xong.**

---

### 2026-09-29 (T3) ca công ty 09:50-10:05 (~15') · hàng đợi mẩu lần đầu

- Về sau 3 ngày công tác, không tranh thủ được món nào. Ca công ty giờ **không cố định** → chạy cột N.
- **N1 gym ván 1: 10/10** ✅. Ô 3·4·7 sửa đúng ngay (tên `key_1`, `len(XS)`). Ô 6 `XS[-2]` → in bảng `-1/-2/-3` → đúng.
  **Ô 8 trượt 2 lượt, cả 2 là lỗi ĐỌC**: chỉ đổi số cuối, để nguyên đoạn `list(bag.key[0])` dù đã bảo xoá hết.
- **N3 Cặp 17: 2/2 → SẠCH** (giữ qua 7 ngày). **N2 vấn đáp 3.8: ⚠️** — ép chọn 4/5 (sai câu TF, chạy thật A 0.904 / B 0.47). Câu lời có TF, **thiếu mặt chữ
  + IDF** → hẹn 04/10, lần sau chỉ hỏi câu lời.
- **N5 gym ván 2: 10/10** (tới 11:55, xen việc công ty). ⭐ **0 lỗi cú pháp** trong 2 hàm `if/elif/else` + `for/append/return` —
  đủ `:` mọi dòng mở khối. Vòng đỏ: ô 2 `stock = ["12"]` (ghi đè thay vì gán khoá) · ô 5 `list[...]` (**Cặp 18** tái phát, 1 lần) ·
  ô 8 nhánh `>= 8` trả `"kha"` (lỗi chép, tự sửa sau khi xem bảng in). Đề không dấu → user khó đọc → **đề drill từ nay có dấu**.
- N4 tiếng Anh **dời sang ca tối** (user chọn). Lỗi đọc/chép cộng dồn **21** (+2 ô 8 gym 1, +1 ô 8 gym 2).

---

### 2026-09-30 (T4) ca tối 20:37-21:10 (~35', dừng sớm vì mệt) · X1 xong

- Đầu buổi: rebase máy nhà, gộp ghi chú 25/09 (chưa commit) với 5 commit 29/09 của máy công ty. Lỗi đọc/chép gộp lại = **21**.
- **X1 `to_qdrant_filter` (cây 1 tầng + lá trần bọc `must`): 5/5** ✅ — [drill](../drills/2026-09-30-toi-x1-gop-ham.py). ⭐ **0 vòng đỏ cú pháp.**
- Tắc trước khi gõ: không nhớ `op` giữ gì; với cây `and` trả lời *"eq và gte"* (khoá của CON) → in thật từng bước → ép chọn 3/3 ⇒ [Cặp 20](./the-phan-biet.md).
- 2 vòng đỏ logic: nhánh 3 chép lặp `op == "or"` (tự sửa) · nhánh cuối gọi `to_not_clause` cho lá trần → `KeyError: 'not'`. Thấy *"khác chữ must"* nhưng không viết ra được → vào sau khi đặt cạnh `to_not_clause` của chính mình 22/09 + mã giả 4 bước.
- Nợ tên: nhánh `else` đặt `value = []` · `key = <tờ đơn>` (tên ngược với thứ nó giữ) · `if(...)` thừa ngoặc → sửa khi gõ lại ở X2.
- **X2 đã dựng khung, CHƯA gõ**: [qdrant_filter.py](../../app/infrastructure/adapters/vectorstore/qdrant_filter.py) ruột trống + 6 test đang đỏ. → 02/10 X2 xong, `pytest -q` toàn bộ **86 passed**.

---

### 2026-10-02 (T6) ca sáng 05:15-06:20 (~65') · LÁT 0 · về sau công tác + bão 01/10 (BKK, không tính hụt)

- **X2 ✅** `to_qdrant_filter` gõ lại từ trắng vào `app/` — logic chia đường đúng ngay; **6/6, suite 82 → 86 passed**.
- Vòng đỏ: `pred.key()` (thiếu `s`) · rồi **4 lượt liền `{'must': None}`** — `.append()` nằm trong `return`/bên phải `=`.
  Ép chọn lộ gốc: tưởng **cả list cũng `None`** sau append ⇒ [Cặp 21](./the-phan-biet.md). Lần 4 thêm `"value"` có nháy (chữ thay biến).
- Câu đoán `like` → chọn `to_not_clause` ✗ → in đường đi → đúng `to_leaf_clause`; ô kiểm `gte` đúng.
- **X3 ✅ chốt A — cây trung lập** (Claude chốt theo yêu cầu user). User không nói được lý do → 10.10 ❌ hẹn 04/10.
- **X4 ✅** Claude viết: port có `metadatas`/`filter_tree` (mặc định `None`) · `QdrantStore` nối cây **cạnh** khoá tenant · 4 test kho nhỏ.
  User *"từ khúc này không hiểu gì"* → tắc **3 chỗ** (lớp thư viện · tenant · port/adapter) → gỡ từng chỗ bằng chạy thật:
  tenant (lộ hợp đồng công ty A cho B) ✅ · port/adapter (cắm `ListStore` 6 dòng vào cùng `HybridRetriever`) ✅ giảng lại 2 câu.
- ⚠️ **Lỗi Claude:** đố cú pháp `FieldCondition`/`MatchValue` — nối dây là việc của Claude (§2). User: *"bớt kiểu hỏi này, tốn thời gian"*.
- **Mai/tối:** X5 — BM25 nhận cùng cây; **lúc đó mới nối `filter_tree` vào `HybridRetriever`** (nối sớm = Qdrant lọc, BM25 không → lệch im lặng).

---

## ⏸️ CHỖ DỪNG — buổi sau làm từ đây

### A. Từ 29/09 — ca sáng + tối CỐ ĐỊNH chạy cột X · ca công ty KHÔNG cố định chạy cột N

User báo sau công tác: **ca sáng và ca tối vẫn bình thường** (roadmap §4). Chỉ **ca công ty** là
*"tranh thủ được lúc nào tôi nhắn lúc đó"* — không biết trước mấy phút.

- **Ca sáng / tối** → mẩu XÂY kế tiếp (cột X), **đi đúng thứ tự, không theo ngày** — xong X nào làm X kế.
  ⭐ X3 thiết kế rơi vào ca sáng (hoặc tối bắt đầu ≤19:30, không OT) — CLAUDE.md §6.
  Tối >21h hoặc OT → không làm X, chạy cột N (45' là DỪNG).
- **Ca công ty** → user nhắn **`rảnh mấy phút`**, Claude lấy mẩu NHỎ (cột N) từ trên xuống, nhét vừa số phút.
  Mỗi mẩu **tự đóng được**: hết mẩu thì file chạy được + 1 dòng nhật ký. Bị gọi đi giữa chừng → lần sau làm lại mẩu đó.

| # | Mẩu XÂY (X) — lát 0 vào `app/` | User làm | Claude làm |
|---|---|---|---|
| ~~X1~~ | ✅ 30/09 **5/5** · Gộp 3 hàm phẳng → `to_qdrant_filter(pred)`, nhìn `op` rẽ sang đúng hàm (cây 1 tầng) | gõ ruột `if/elif/return` | khung drill + ca thử |
| ~~X2~~ | ✅ 02/10 **6/6** · Vào `app/`: **gõ lại TỪ TRẮNG** `to_qdrant_filter` (bước 5 PRIMM, số đo 2) — khung + 6 test đã có; hỏi lại câu đoán *"`ValueError` của `like` do hàm nào ném"* | gõ ruột | file khung adapter Qdrant + test |
| ~~X3~~ | ✅ 02/10 chốt **A** · Bài thiết kế: port `VectorStore.search` nhận **cây trung lập** hay **dict Qdrant đã dịch**? | chốt + lý do + cái giá | giảng 2-3 phương án kèm giá **trước khi hỏi** |
| ~~X4~~ | ✅ 02/10 (chưa nối `HybridRetriever` — dời sang X5) · Nối dây: `upsert` lưu metadata vào payload · `search` nhận filter | trace 1 lượt + giảng lại | viết nối dây |
| **X5 ← ca kế** | Phía BM25 + nối `filter_tree` qua `HybridRetriever` cho **cả hai** nhánh · `danh_gia` + `post_filter` → `app/`, tên tiếng Anh | gõ lại từ trắng | khung + test + nối vào nhánh BM25 |
| X6 | Test đầu-cuối trên kho 5 văn bản (ca `vb5` Thông tư bị cắt) | **đoán trước**, chạy, đọc test | test · `pytest -q` toàn bộ xanh → commit → **LÁT 0 ĐÓNG** |

| # | Mẩu NHỎ (N) — 10-20' | Ghi chú |
|---|---|---|
| ~~N1~~ | ✅ 29/09 Gym ván 1 **10/10** | |
| ~~N2~~ | ✅ 29/09 Vấn đáp 3.8 làm xong (⚠️, hẹn 04/10) | |
| ~~N3~~ | ✅ 29/09 Cặp 17 **2/2 — SẠCH** | |
| N4 | Tiếng Anh: đọc to bản 21/09 → viết bản 2 *"why did you switch to AI?"* — **29/09 dời sang ca tối** | user viết, Claude chỉnh |
| ~~N5~~ | ✅ 29/09 Gym ván 2 **10/10**, 0 lỗi cú pháp trong hàm | |
| N6 | Gym ván 3 (Claude soạn khi cần) — nhắm chỗ còn hở: gán khoá vào dict · `list(...)` ngoặc tròn | đề có dấu |
| **N8 ← ca công ty 02/10** | **Ôn toàn cảnh lát 0** (user: *"còn mơ hồ quá mức"*). Claude in **một** đường đi thật: cây → `to_qdrant_filter` → `conditions` (tenant + cây) → Qdrant → kết quả kho 5 vb; user đọc rồi **tự vẽ lại bằng chữ** 4 mũi tên. Sau đó ép chọn Cặp 21 (2 ô). **Cấm** chuỗi câu đố cú pháp thư viện | không mở X5 trong ca này |
| — | **04/10: vấn đáp 3.9** · **05/10: 3.5 + 1.4** | chèn lên đầu cột N khi tới hạn |
| N7 | Ép chọn **[Cặp 19](./the-phan-biet.md)** (dict↔list) 2 câu — nợ từ tối 25/09 | cấm giảng lại |

- **User hẹn 30/09:** sáng 01/10 gõ lại X2 · tối 01/10 muốn đóng hết phần còn lại của lát (X3→X6; X3 thiết kế cần ca sáng hoặc tối ≤19:30).
- Lát 0 đóng ở **cây 1 tầng** là đủ. Đệ quy = nâng cấp **một chữ**, chỉ mở khi user tự hỏi *"nếu con lại là cây thì sao"*.
- **CN 04/10** vẫn tổng kết tuần + chấm PRIMM 2 số (nếu có tin nhắn tối CN). Hàng đợi này chạy tới khi giờ cố định trở lại.

### A1b. ✅ USER CHỐT 02/10 — bỏ Orchestrator, làm cả A + B + C (sửa roadmap ở tổng kết CN 04/10, theo luật §4)

- **Bỏ Nyxara-Orchestrator** (bị chê *"không nhắm đúng thị trường, chả ai xài"*; user đồng ý: TypeScript · thị trường extension
  code đã bão hoà · agent code nên khó nhận là của mình).
- **A** — `nyxara-core` lấp 4 lỗ tin tuyển: cloud · adapter OpenAI/Anthropic · Docker kéo lên lát 1 · `PgVectorStore`. ~15-20h, lấy từ ~60h trống.
- **C** — MCP server tra luật cho người ngoài dùng (Claude Desktop/Cursor), gắn lát 5. ~10-15h, lấy từ ~60h trống.
- **B = DỰ ÁN SỐ 2 mới** — agent text-to-SQL trên Postgres (hỏi tiếng Việt → SQL → kết quả + câu SQL đã chạy; đo tỉ lệ đúng).
  ~30-40h, **ăn slot 1h/ngày cũ của Orchestrator**, không đụng giờ core. Python/FastAPI, dùng lại khung eval lát 1.
- ✅ **B bắt đầu SAU LÁT 1** (user chốt 02/10). Bộ đo có sẵn: **ViText2SQL** (VinAI, ~10K câu tiếng Việt, chỉ dùng nghiên cứu/học) — vai trò như Zalo Legal ở core.
- **Còn phải chốt ở CN 04/10:** tên B · B áp **Cách A** cho lõi hay agent code
  (agent code = đúng điểm yếu đã khiến Orchestrator bị chê) · B dùng dữ liệu bảng nào.

### A2. Bài thiết kế chờ — MẢNG DỮ LIỆU (user nêu 02/10, chưa sửa roadmap)

User thấy lộ trình **thiếu kỹ năng xử lý dữ liệu**: ETL/pipeline · làm sạch · **SQL/Postgres** · crawl · queue · **chạy theo lịch**.
Còn ~60h chưa phân (35 mục ≈ 137h / ~200h tới 15/02). **Cách chốt:** ca sáng, user mang **2-3 tin tuyển thật**
→ Claude đối chiếu từng dòng với ~90 mục hiện có → chỉ thêm thứ tin tuyển đòi. Ba phương án Claude soạn sẵn
(giảng kèm giá trước khi hỏi): **P1** gộp vào lát 1 (nạp 61K bằng pipeline thật: Postgres giữ metadata + job theo lịch) ·
**P2** lát data riêng sau lát 1 (crawl vbpl văn bản mới → làm sạch → Postgres → queue embed) · **P3** chỉ 🟢 nói được.
⭐ **Đã rà 10 tin thật 02/10 → [thi-truong-2026-10.md](./thi-truong-2026-10.md): ETL/Airflow 0 tin bắt buộc ⇒ nghiêng bỏ P2.** X5/X6 lát 0 **chạy tiếp bình thường** — mảng này chỉ ảnh hưởng từ lát 1 trở đi.

### B. Giữ nguyên

- **Nợ cũ:** `eq/ne/gt/gte/lt/lte` vào glossary · dọn 2 tên trong `cham_nhat` (`name = {}` · `max`).
- ⚠️ **Nhắc Claude:** user tắc 4 chỗ cùng lúc thì **hạ bậc bài, đừng hạ tốc độ hỏi** (22/09).
- **Theo dõi:** lỗi đọc đề/chép sai **21 lần**. Tên biến lấy từ đề → **copy-paste**, không gõ tay.

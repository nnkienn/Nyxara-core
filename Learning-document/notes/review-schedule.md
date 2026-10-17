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
| **21/10** | 3.8 BM25 khớp theo cái gì | 16/10 ⚠️ (lên từ ❌): mặt chữ · TF · IDF · độ dài ✅ · **IDF chữ hiếm 40/61K → cao ✅ (lần đầu đúng chiều đóng sách)**. Sai: rỗng "vì IDF = 0" (đúng: **không điều nào chứa chữ → 0 ứng viên được chấm**) · ví dụ `ma túy đá` không rỗng (tách `ma`/`túy`/`đá` đều có trong sổ — chạy thật kho 3 điều: điều "khai thác đá" đứng đầu). Câu kiểm `chất methamphetamine` ✅ không rỗng nhờ `chất` (chưa nêu tên điều + điểm thấp). Lần sau: ví dụ rỗng = `methamphetamine` · ví dụ "trả về nhưng sai điều" = `ma túy đá` |
| **21/10** | 10.10 vì sao port nhận cây trung lập, không nhận dict Qdrant | 16/10 ⚠️ (giữ như 07/10): (a) BM25 không hiểu ✅ · (b) "không có chỗ đổi" — **lần 2 chưa gọi tên file** (đúng: sửa `HybridRetriever` trong core + `PgVectorStore` phải đọc cú pháp Qdrant). Trả lời 1 câu, quá ngắn. Claude giảng sơ đồ 2 nhánh + câu mẫu |
| **20/10** | 3.9 tenant filtering | 15/10 ⚠️ (lên từ ❌): "không cùng cơ chế" ✅ · bảo mật ✅ · BM25 thiếu chữ **phân vùng** (`self.index[tenant_id]`), lẫn với `filter_tree` · thiếu ý post-filter làm `top_k` rỗng. Lần sau: hỏi lại nguyên câu |
| **20/10** | 3.5 RRF | 15/10 ⚠️: công thức ✅ · khác đại lượng ✅ · BM25 trần "2" (10/10 nói 1) — **không có trần**, cộng theo số chữ query · hậu quả mơ hồ, thiếu "BM25 lấn át vector". Nói lại câu mẫu 3/4 (thiếu giới hạn, gọi "nhánh Qdrant"). Ca X/Y (10 chữ × 1 BM25 + cosine) ❌: lấy 1 điểm cho cả văn bản → "cosine quyết định". **20/10: làm lại ca P/Q (6 chữ × 1.5, cosine 0.40 vs 0.98) TRƯỚC khi hỏi 3.5** |
| **21/10** | Vì sao `HybridRetriever` chuyền cây xuống **cả hai** nhánh | 16/10 tối ⚠️ (tụt từ ✅): câu 1 trả "BM25 giỏi khớp chính xác" — **lẫn giá trị nhánh BM25 ↔ lọc trên nhánh BM25**, chiều ngược ("tốt lọt ra" thay vì "bị cấm lọt vào"). Chạy thật `ND100_2019` → đảo nhánh ✅. Lọc sau RRF: không nhớ → giảng (cắt trước, lọc sau = **thiếu**, có khi 0) → ca 5 nghị định cũ ra **0** ✅. Lần sau: hỏi nguyên câu, đóng sách, cả 2 ý |
| **21/10** | 10.11 port / adapter là gì | 16/10 ⚠️ (lên từ ❌): định nghĩa port/adapter ✅ · dịch 2 chiều ✅ · đổi DB = **thêm** adapter ✅ · tự thêm test bằng fake + cái giá ✅. **Thiếu cả phần ví dụ** (lần 2): không nêu `VectorStore`/`QdrantStore`, `query_points`, `SearchHit`; "dịch thô ngược lên" thiếu "của Qdrant → `SearchHit`". Lần sau: bắt đầu câu trả lời BẰNG ví dụ |
| **21/10** | 1.4 Recursive chunker | 07/10 ✅ hỏi trần: CẮT → GỘP + hậu quả "mẩu lẻ tẻ vô nghĩa" (gọi nhầm là "cây" — là danh sách mẩu) |

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

### 2026-10-02 (T6) ca tối 21:11-21:55 (~45', ca muộn, user báo còn sung) · ca công ty KHÔNG có (hụt ~1h)

- **Cặp 21 trượt lại 2 vòng (0/2, 0/3)** — hình dung ổn định: *".append tạo list mới, gốc giữ nguyên"* = đúng là của **dấu `+`**.
  Gỡ bằng in `+` cạnh `.append` + **user tự gõ ở REPL** → vào. Kiểm lại cuối ca: hiểu đúng (đọc đề sai: trả "list" cho câu hỏi số).
- **N8 ôn toàn cảnh lát 0** — viết lại 4 bước VÀO→DỊCH→GHÉP→RA: đúng ý. Lẫn mới: tưởng `QdrantStore.search` chạy cả dense + BM25
  → ép chọn 2/2 (dense · nhánh BM25 chưa lọc).
- ⭐ **Gõ lại `to_qdrant_filter` từ trắng (+15h): 6/6 xanh lượt đầu, 0 vòng đỏ** (sáng: 5 lượt). Nợ tên `value`/`key` ngược.
- ⭐ **Cặp 19 ép chọn 6/6 — SẠCH** (25/09 trượt 3 lượt).
- X5a mở: khung `matches` + `leaf_matches` + 17 test → user tắc từ dòng đầu, hạ bậc còn `leaf_matches` (in đường đi 1 lá) → user dừng *"nghĩ không nổi"*.
  ⚠️ **`pytest -q` toàn bộ hiện 17 failed** cho tới khi X5a xong.
- Lỗi đọc đề cộng dồn **22**. Gym ván 3 đã soạn, chưa làm.

### 2026-10-03 (T7) ca công ty từ 10:11 · LÁT 0 · ✅ X5a xong

- ✅ **`leaf_matches` 8/8** (Claude thêm ca `gt 2015` — ca `gt 2020` cũ pass nhờ may) → ✅ **`matches` 18/18 · suite 104 passed, 0 failed**.
- `matches`: chép nguyên bộ dịch Qdrant sang (ra `{'must': [True, False]}`) ⇒ **[Cặp 22](./the-phan-biet.md)**. Sau đó `and` vướng
  `"andor"` · `out == False` (so cả list) · `return True` trong vòng `for`; **`or` tự lật đúng lượt đầu**; `not` 3 lượt (`child` không tồn tại · thiếu `return` · đưa cả cây).
- Tắc từ đầu → hạ bậc 3 câu 1 dòng → vẫn tắc ở **dấu so sánh** + **quên `lt/lte` là gì** → Claude giảng thẳng + khung so le với `to_leaf_clause` (user: *"đừng hỏi vòng vo"*).
- Vòng đỏ cú pháp: `metadata(fields)` (ngoặc tròn sau tên biến — lặp 22/09) · thiếu `:` sau `if`.
- Lỗi logic: hàm bỏ quên `op` (luôn so `>=`) · `gt`↔`lt` đảo chiều dấu → in 2 ca fail, user tự sửa.
- **X5b ✅ nối dây (Claude):** `BM25Index` lưu metadata + lọc bằng `matches` **trước** cắt `top_k` · `Hybrid`/`Reranking` chuyền
  `filter_tree` xuống cả 2 nhánh · **109 passed**. Trace in thật: ô kiểm `top_k=1` ✗ (quên cắt) → `top_k=2` ✅.
  Giảng lại "lọc trước cắt" ✅ (thiếu hậu quả *rỗng*) · "chuyền cả 2 nhánh" ⚠️ (nói "lọt vào cây khác", thiếu **RRF trộn** + **im lặng**).
- ⚠️ **Chưa xử lý:** văn bản **thiếu trường** → `leaf_matches` nổ `KeyError`, Qdrant thì lặng lẽ loại ⇒ 2 nhánh lệch — **bài thiết kế
  ca sáng** (lõi của user). · `pipeline.py` chưa truyền metadata cho 2 store (cần cho lát 1).
- Bàn dự án 2: **đã xin phép phòng khám**, lấy hội thoại **T7 10/10** (ghi side-lanes L). User hỏi fine-tune → giữ 🟢, ứng viên nâng = FT `bge-m3`.
- **Tiếp:** X6 = đóng lát 0. Nợ tên: `fields` → `field` · `child = leaf_matches(child, ...)` dùng 1 tên cho 2 thứ.

### 2026-10-05 (T2) ca công ty từ 09:13 · (máy cty chưa thấy log tối 04/10 ở trên — gộp 06/10)

- Gym ván 3 trên máy này **còn trắng** (tối 03/10 làm dở rồi ngủ quên, không lưu) → làm lại từ đầu.
- **10.10 ❌ lần 2** → [Cặp 23](./the-phan-biet.md). In thật `matches(dict Qdrant)` nổ `TypeError` + ép chọn → nói lại đủ 2 hậu quả. Hẹn 07/10.
- **3.8 ⚠️** đủ 3 ý nhưng IDF ngược chiều ("của" cao) → in IDF thật 0.1466 vs 1.9924 → đúng. Hẹn 10/10.
- **3.9 ⚠️** đúng `tenant_id` + trước chấm, thiếu vì sao → cảnh `top_k=5` toàn của A → "rỗng". Hẹn 10/10.
- **3.5 ⚠️** công thức + số hạng đúng; tưởng cosine/BM25 "cùng đại lượng" → in BM25 thật 3.741 vs cosine ≤1. Hẹn 10/10.
- **1.4 ❌** không nhớ CẮT → GỘP → in 30 mẩu vs 3 mẩu → nói đúng hậu quả. Hẹn 07/10. **Vấn đáp: 0 ✅ · 3 ⚠️ · 2 ❌** — 21/09 các câu ✅ sau 14 ngày rơi hết.
- ⚠️ Lỗi Claude: hỏi "rảnh mấy phút" 2 lần — ca công ty không có số phút, đã ghi ở mục A.

---

### 2026-10-04 (CN) ca tối 19:50-21:40 (~1h50) · LÁT 0 · X6 dựng, chưa đóng

- Vấn đáp 3 câu tới hạn: **3.8 ⚠️** (lẫn tên TF/IDF, thiếu mặt chữ + độ dài) · **10.10 ⚠️** (từ ❌; không gọi tên chỗ sửa) · **3.9 ✅** (câu (a) Claude phải hỏi lại bằng filter in thật; câu (b) đề lệch code — BM25 đã tách theo tenant, không tính).
- Nợ tên: `fields` → `field` ✅ · `child` → `matched` **chưa làm** (user: *"chả biết đặt tên gì"*; Claude đưa luật "tên = câu hỏi biến trả lời").
- **X6:** Claude viết [test đầu-cuối](../../tests/application/retrieval/test_hybrid_filter_end_to_end.py) — Qdrant `:memory:` + BM25 thật + `HybridRetriever`, kho 5 vb + 1 vb tenant B → **9/10**.
  Ca đỏ = **lỗi thật**: cây có `tenant_id` → BM25 `leaf_matches` nổ `KeyError` (metadata BM25 không có trường đó), Qdrant chạy đúng. ⇒ bài thiết kế "thiếu trường" **ca sáng 05/10**.
- User *"chưa hiểu gì phần nối port"* → Claude mở bằng script "camera" + 5 câu đoán → user: **"giảng nghiêm túc đi, kiểu này không học được"** → giảng thẳng 6 mục (bài toán · cây trung lập · port/adapter · pre/post-filter · Hybrid 2 nhánh · ai viết gì).
- Giảng lại ngay sau đó: đúng khung 6 mục, **thiếu WHY** (BM25 vì sao lọc sau + lọc trước khi cắt · vì sao phải lọc cả 2 nhánh) · thiếu tenant · mục 2 nói ngược (mỗi kho tự dịch cây, không phải cây hiểu ngôn ngữ kho) · chưa ghép **hàm nào ở nhánh nào**. Giảng ngay sau khi đọc ⇒ chưa tính là nhớ.
- Tổng kết tuần ✅ · chốt B = **Nyxara Care, repo riêng `nyxara-care`**, Cách A, dữ liệu Pancake · khung 3 loại project vào roadmap §1.
  Repo `nyxara` cũ: user thấy nhà tuyển dụng không cần → đề xuất **chuyển private** (chưa làm, chờ user). Gym ván 3 mở 22:05 → dừng, **chưa gõ ô nào** (mệt).

---

### 2026-10-06 (T3) ca sáng từ 06:45 ~45' (mệt sau OT tối 05/10) · **LÁT 0 ĐÓNG**

- Gộp git: tối 04/10 (máy nhà, chưa commit) + ca cty 05/10 → bảng hạn lấy bản 05/10.
- X6: in thật trường thiếu → Qdrant `eq` không khớp / `not` khớp, BM25 nổ `KeyError`. Giảng A nổ · B `False` · C `True` + giá.
- User hỏi "chuẩn là gì" → B (khớp kho ghép cặp; SQL khác). Lần đầu hướng dẫn "chưa chuyên nghiệp" → giảng lại 5 mục (bài toán · `in` · guard · trace · việc) thì gõ được.
- User gõ guard `if field not in metadata: return False` → **119 passed**.
- Nợ: kiểm tên trường ở cửa vào (gõ sai `"nma"` hiện ra rỗng im lặng) · ~~tên `child`~~ ✅ 07:15 → `matched` (and + or).

---

### 2026-10-07 (T4) ca tối 21:47-23:10 (~80', ca muộn) · **LÁT 1 MỞ** (dữ liệu)

- Hụt: 06/10 chỉ 45' sáng, không ca cty/tối · 07/10 không ca sáng/cty → ~1,5 ngày trống.
- Vấn đáp đóng sách: **1.4 ✅** (→21/10) · **10.10 ⚠️** lên từ ❌ (→12/10) · **10.11 ❌** (→09/10).
- 10.11: Claude giảng bằng code dự án (Qdrant + `Filter`) → user *"khó hiểu quá"* ⇒ **hạ bậc** về ví dụ
  20 dòng `Store`/`ListStore`/`DictStore`, chạy thật in ra → ép chọn a/b/c ✅ → gõ `TupleStore` ✅.
- Lỗi cú pháp: `Class` hoa · `def __init__` gõ 2 lần. Tự bỏ `.values()` khi đổi sang tuple ✅.
- Bỏ Cặp 19. User đòi **mở lát 1 luôn** (22:15): Claude tải Zalo Legal → `data/` (gitignore) — 61.425 điều ·
  **788 câu test** (roadmap ghi 818 — sửa) · 793 cặp qrels. Giảng Hit@k (YouTube + bảng 3 lần tìm) → **chưa thông
  sau 3 lượt**, quá 45' ⇒ dừng; in thật `results[:k]` k=1..3 cho đọc, không hỏi.
- Mai sáng: **mở đầu bằng bản in `hit_show`** (1 câu, k=1..3), user tự nói Hit@1/Hit@3 → rồi gõ `hit_at_k`
  trên 788 câu. Cộng vấn đáp Hybrid 2 nhánh. Đừng giảng Hit@k lần 4 bằng lời — cho làm.
- User không chịu dừng → chạy thật `BM25Index` trên 61K × 100 câu: A text Hit@5 0.71 · B title+text 0.75 → vẫn
  *"mông lung"* (dồn 5 thứ 1 lần). Hạ về **"điểm thi"** (đề 788 câu · máy khoanh k điều · đúng/sai · điểm) → user
  tự nói **"câu đúng chia tổng câu"** ✅. Phát hiện: `BM25Index` gốc **chạy 61K không nổi** — để user tự soi (lát 1).
- User đòi học tiếp (22:50) → gõ `hit_at_k` ([drill](../drills/hit-at-k.py)): đúng B1 đếm · B4 chia; sai `.len()`
  + **2 vòng `for` lồng, so list `==` chuỗi, không dùng `k`** → in 9 dòng False. User xin đáp án → Claude đưa lời
  giải + trace; user *"vẫn chưa hiểu lắm"*, dừng ~23:10. **Chưa gõ lại.** Nút thật: **list lồng list + chỉ số `i`**.
- Mai sáng: (1) chấm tay 3 câu trên giấy · (2) in `results[i]`, `results[i][:k]`, `answers[i]` cho i=0..2 ·
  (3) gõ lại 5 dòng từ trắng. Nếu `[i][:k]` còn rối → drill riêng list lồng 10' trước.

### 2026-10-08 (T5) ca tối 21:20-22:10 (~50', ca muộn, không OT) · LÁT 1
- Ca sáng + cty 08/10 không có. Vấn đáp Hybrid 2 nhánh **❌** (→10/10) — giảng bằng bảng RRF k=60.
- Hit@k đoán `0 · 1/3 · 0` → lẫn 2 cặp: **"k dòng đầu" ↔ "dòng thứ k"** · **Hit 1 câu (0/1) ↔ điểm cả đề (chia)**.
  Ép chọn 3/4 (còn hở cặp 1) → 4/4 ✅.
- Gõ lại `hit_at_k` (vào file cũ [hit-at-k.py](../drills/hit-at-k.py)): 2 thiếu `:` · `result` thiếu `s` · `==` → `in`;
  **tự sửa `hits = top_k + 1`** → xanh 0.333/0.666.
- Claude nối [hit-real.py](../drills/hit-real.py): BM25 tối giản 61K × 788 câu, cache `data/zalo_legal/bm25_top10_test.json`.
- Dừng ~22:10: user *"chưa hiểu phép toán Hit@k, tự nghiền ngẫm"*. Mẩu 5 (vòng `for` k=1,3,5,10 + đoán chiều x/y/z) chưa gõ.

### 2026-10-09 (T6) — ca 16:15 (đứt quãng) + ca tối 21:10-22:30 (~1h20, user chọn "buổi mới 2h") · LÁT 1
- Vấn đáp 10.11 **⚠️** (→14/10): port ✅ · adapter chỉ "bộ chuyển đổi" — thiếu *dịch lời gọi core sang API công nghệ cụ thể*.
- Hit@k chấm tay 3 câu (chữ cái, có câu mẫu) ✅ sau khi đề mã dài bị *"không hiểu đề"*. Vòng `for` k=1,3,5,10: `:` · `k`↔`x` · chép `4` thay `5`.
- Giảng toàn cảnh lát 1 (câu 7 thật: "hầm" kéo Điều 47 lên dòng 1) → giảng lại 4 bước ✅, nhưng nói *"không có xe máy"* = tưởng máy đọc nội dung — **máy chỉ so mã qrels**.
- Câu 42: đọc đúng dòng 1 nhưng ghi Hit = **1/42** → lẫn lần 2 *1 câu ↔ cả đề* (lấy `i` làm mẫu số) → ép chọn 4/4 → [Cặp 24](./the-phan-biet.md).
- **`hit_at_k` vào `app/evaluation/metrics.py`** — closed-book **không gõ được** ("không biết gõ gì") → Claude giảng 5 mục, user gõ **có nhìn**; thiếu `:` → **5 passed · suite 124**. Hỏi được `[:k]` là gì → in thật.
- Baseline BM25 tối giản 788 câu: **Hit@1 0.42 · @3 0.66 · @5 0.75 · @10 0.82**.
- Drill `:` — 2/4 rồi 3/4: **sót `else` cả 2 ván**, sót `def` 1 lần. Câu "từ khoá nào kéo Điều sai lên" bỏ qua 3 lần.
- Học thêm 22:30-22:50 (user chưa buồn ngủ): mã giả 4 bước đóng sách ✅ (thiếu `i`) · điền ô `i=1`: **đếm từ 1** (`results[1]` → lấy hàng 0) + `[:2]` ra 1 chữ → ép chọn `[1]`/`[:1]` 4/4 · `i=2` 3/4: `results[2]` ra **`"remix"`** = lẫn **list lồng: `[2]` lấy CẢ HÀNG (1 câu) ↔ `[2][x]` lấy 1 điều**.
- 22:55 user hỏi trễ bao nhiêu → Claude tính ~44h ≈ 29 ca XÂY (lạc quan; Hit@k thật ~2× ước) · **user chốt: GIỮ NGUYÊN kế hoạch, tự bù giờ** — tổng kết CN 11/10 chỉ đo giờ thật, không mở lại câu re-plan.
- **T7 10/10:** xem [A0 ở chỗ dừng](#-chỗ-dừng--buổi-sau-làm-từ-đây) — (0) 3' ép chọn list lồng `results[i]` ↔ `results[i][j]` · (1) 2' ép chọn `:` có `else`/`def` · (2) **CỬA: gõ lại `hit_at_k` ĐÓNG SÁCH** vào file trắng, chạy 5 test · qua → mở **MRR** (giảng 5 mục trước). Trượt cửa → mã giả tiếng Việt 4 bước trước rồi gõ.

### 2026-10-10 (T7) ca sáng 06:02-07:40 (98') · LÁT 1
- Ép chọn list lồng 3/4 + `:` 2/2 (`def`/`else` sạch) · chỉ số↔dòng: `results[1][2]` ra `"remix"` (đếm từ 1) → ép chọn 2/2.
- Vấn đáp 3.8 ❌ · 3.9 ❌ (→12/10, chi tiết ở bảng trên). Ép chọn IDF/phân vùng 5/6 + 2/3 → [Cặp 27](./the-phan-biet.md).
- **CỬA `hit_at_k` đóng sách: QUA** — 4 bước logic đúng ngay; 1 gõ nhầm `hits-hits+1` · 1 `return` thụt trong `for` (tự tìm từ bản in) → 5/5.
- MRR: giảng 5 mục → *"chưa hiểu"* → cảnh 1 câu → chấm tay cột dòng 4/4 nhưng mẫu số luôn `1/3` → ép chọn 4/4 →
  [Cặp 26](./the-phan-biet.md). Giảng thêm: phân bố dòng thật 788 câu · Lan/Minh · vì sao `1/dòng` · reranker không làm Hit@10 nhúc nhích.
- Gõ `mrr` vào `app/`: dòng cộng `1/(len(results)+1)` (hỏi "đề mấy câu" thay vì "đáp án ở đâu"). Claude viết 5 test MRR → **2 đỏ / 10**.
  User tự chỉ đúng dòng cộng sai. Hết giờ, chưa sửa xong.
- ⚠️ User nói nhiều lần **"thuật toán OK, còn mù mờ MRR khác Hit@k chỗ nào"** — 4 cách giảng chưa đọng; cách cuối: **đậu/rớt ↔ bao nhiêu điểm**.
- **Tối nay bắt đầu:** (0) 2 ô Hit/MRR của sếp (đã hỏi cuối ca sáng) · (1) sửa cụm `len(results)` → `.index` → 10 passed ·
  (2) chạy `mrr` trên 788 câu thật cạnh Hit@1/3/5/10 — **để số thật làm rõ khái niệm** · rồi mới BUG CỐ Ý theo A0.

- **Chiều 10/10, học ngoài với ChatGPT (~2h, user báo cáo):** Hit@k + MRR. Nắm thêm: **1 lần tìm → 1 RR** (đúng đầu tiên rồi dừng,
  từng trả 1/2 + 1/5) · mẫu số tính cả lần trượt · MRR 0.65 ≠ "65%". Còn hở: lẫn **k · rank · số lần tìm** · index↔rank (+1 thừa/thiếu)
  · `rr`↔`total_rr` · tự viết vẫn `total_rr == 0`, `results.index`. Hẹn **11/10 kiểm tra không gợi ý**: lời → tính tay → tự viết → trace.
  Cách dạy user xin: 1 câu/lượt · bài ngắn · cố định dữ liệu · nói rõ "1 lần tìm" hay "cả bộ" + k bao nhiêu · **không dùng "dòng" cho lần tìm**.

### 2026-10-10 (T7) ca tối 20:10-22:20 · LÁT 1 · áp cách dạy mới (CLAUDE.md §5.1)
- `mrr` trong `app/`: `results.index` → `top_k.index` (lỗi F báo cáo ChatGPT, tự sửa) → **129 passed**.
- BUG CỐ Ý [mrr-bug-1010.py](../drills/mrr-bug-1010.py) (chia số lần TRÚNG): tự nói "chia tổng results", sửa đúng. Bug làm 788 câu phồng 0.562 → 0.685.
- **BM25 Zalo 788: MRR@10 = 0.562** · Hit@10 0.821. MRR còn thiếu: gõ lại đóng sách 11/10 (hẹn với ChatGPT) → qua thì MRR ĐÓNG.
- Vấn đáp 3.5 ⚠️ · Hybrid ✅ (→15/10 cả hai). 1 lỗi đọc (d1↔d2).
- Câu hỏi 1 việc/lượt chạy tốt hơn hẳn sáng nay: 1 lần "không hiểu câu hỏi" (câu ghép, trước khi đổi cách) rồi trơn.
- 21:15 user chọn học tiếp → **NDCG mở**: MRR không phân biệt [A✓ B✗ C✓] với [A✓ B✗ D✗] ✅ · DCG = `1 + 1/log2(4)` = 1.5 ✅ (tự dùng công thức).
  **IDCG trả "2"** (quên giảm giá ở danh sách lý tưởng) → *"lú quá"* — lỗi Claude mở IDCG quá sớm + lỡ dùng "dòng". Giảng IDCG = điểm tối đa,
  NDCG = 1.50/1.63 ≈ 0.92. User nghỉ 22:20. CLAUDE.md §5 viết lại + §6 luật dừng (user yêu cầu).
- **CN 11/10 bắt đầu từ:** (1) *"Kiểm tra lại Hit@k và MRR, không gợi ý trước"*: lời → tính tay dữ liệu MỚI → tự viết 2 hàm → trace (hẹn với ChatGPT) ·
  (2) NDCG: user giảng lại DCG bằng ví dụ A/B/C → IDCG từng bước (hỏi giá trị thứ hạng 2 trong danh sách lý tưởng trước) → NDCG 0.92 · chưa code.

### 2026-10-11 (CN) — chỉ có cửa MRR, không ghi note hôm đó
- CỬA `mrr` đóng sách [mrr-cua-1110.py](../drills/mrr-cua-1110.py) **5/5** (chạy lại 12/10) → **MRR ĐÓNG**. Thêm [Cặp 28](./the-phan-biet.md) (`results` ↔ `top_k`).

### 2026-10-12 (T2) ca tối 20:51-23:25 · LÁT 1 · NDCG khái niệm, chưa code
- Quên công thức DCG (chỉ nhớ "xét cả vị trí sau") → giảng lại → DCG [B,A,C] = 1.13 ✅ (ra phép tính, thiếu số).
- **IDCG: lỗi "= 2" (quên discount) tái phát lần 2** → sửa → chó/mèo/gà tự áp discount ✅. Lẫn DCG↔IDCG 1 lần (chấm list máy thay ideal ranking).
- Câu P/Q (cùng DCG, khác số đáp án) chọn sai P → ẩn dụ Nam 8/10 vs Hoa 8/100 → hiểu.
- Phỏng vấn: câu 1 NDCG vs MRR ⚠️→✅ (ví dụ đầu sai cặp, tự nghĩ cặp chó/mèo đúng) · câu 2 vì sao chia IDCG ⚠️ (ý đúng, thiếu số retrieval) · câu 3 IDCG tính thế nào: user mệt, Claude đưa đáp án.
- CLAUDE.md §5.1 + §5.3: câu hỏi tự đứng được · giữ thuật ngữ tiếng Anh (user yêu cầu). Lỗi Claude: 1 bộ số 2b chọn sai.
- **Sáng 13/10 bắt đầu từ:** gõ `ndcg_at_k` vào `app/` theo 4 mẩu, mỗi mẩu kèm 1 câu định nghĩa: (1) điểm 1 thứ hạng `1/log2(r+1)`, chỉ số→thứ hạng
  (nối MRR `index+1`) · (2) DCG 1 lần tìm = cộng mọi kết quả đúng (vs MRR dừng ở cái đầu) · (3) IDCG = DCG ideal ranking, `min(số đáp án, k)` ô
  · (4) NDCG từng lần → chia **tổng số lần tìm** (giống Hit@k/MRR). ⚠️ `answers` thành list các list (nhiều đáp án/lần tìm) ·
  ôn 3.8 / 10.10 / 3.9 dời sang tối 13/10 · câu 3 phỏng vấn (IDCG 2 đáp án) hỏi lại không gợi ý.

### 2026-10-13 (T3) ca công ty từ 16:41 (~25', vừa làm task cty) · LÁT 1 · ôn Hit@k + MRR tính tay
- ⚠️ User báo CN 11/10 + T2 12/10 **có học**, nhưng `origin/main` vẫn dừng ở 10/10 → **máy nhà chưa push**. Tối nay push rồi bổ sung nhật ký 2 buổi đó.
- Hit@k: *"không nhớ"* → nhắc 1 ví dụ → Hit@2/Hit@3 đúng ngay.
- RR: lần đầu trả **2/5** (lấy độ dài danh sách làm mẫu số) → giảng → 1/3 ✅ → ép chọn tình huống mới 1/4 ✅.
- MRR cả bộ: lần trượt RR=0 ✅ (sau 1 lần sai ghi RR=1) · đổi k=5→3 **quên tính lại RR lần 2** (đề ghi k lẫn trong câu — Claude: từ giờ k đặt trong khung dữ liệu).
- **Lỗi lặp 2 lần: ghi THỨ HẠNG vào chỗ RR** ("lần 2 là 4", "lần 4 RR = 2"). User: gõ nhầm do đang làm task. Kiểm: RR luôn ≤ 1. Hay gọi `mrr@1/2/3` cho từng lần tìm (lẫn `@k` ↔ lần tìm).
- NDCG (`[D,A,C,B,E]`, đúng A+C): chọn log đúng nhưng **cộng log** (1.58+2) → giảng "1 ÷ log" → tính sai 5.58 (đang làm task).
  User tự nói *"nhầm DCG/IDCG/NDCG"* → bảng 3 cột (câu hỏi gì · danh sách nào) → ép chọn **3/3** → IDCG = 1 + 0.63 = 1.63 ✅
  (**hết lỗi 10/10** quên giảm giá thứ hạng 2) → NDCG = 1.13/1.63 ≈ 0.69 ✅.
- **Lỗi gốc của cả buổi (3 lần): đưa SỐ CHIA vào chỗ ĐIỂM** — thứ hạng↔RR (2 lần), log↔điểm (1 lần). Kiểm: điểm 1 văn bản đúng luôn ≤ 1.
- +10' cuối: MRR tình huống mới (k=3, 1 lần trượt) **4 RR đúng sạch** → MRR tính tay QUA (nhưng 3 lần dừng ở RR, không chia ra số MRR cuối).
- NDCG mới không gợi ý (`[P,Q,R]`, đúng Q) ❌: DCG = **1.58** (số chia, lần 4) · IDCG = 1.58 (**không đưa Q lên đầu** danh sách lý tưởng) · NDCG = 1.
- **Lần sau:** NDCG dữ liệu mới không gợi ý lần nữa — kiểm riêng 2 chỗ: điểm = 1 ÷ log · danh sách lý tưởng **xếp lại** đúng lên đầu. Sạch → gõ `ndcg_at_k` vào `app/`.

### 2026-10-14 (T4) ca công ty từ 08:54 (đứt quãng) · LÁT 1
- Máy cty: test đã đổi sang **danh sách văn bản đúng / lần tìm** (`[["a"], ...]`), `hit_at_k`/`mrr` chưa theo → 10 đỏ. `origin` vẫn chưa có buổi 11-12/10.
- Mẩu 1 NDCG không gợi ý (`[M,N,P,Q]`, đúng N+Q, k=4) ✅: điểm = 1 ÷ log ✅ · lý tưởng `[N,Q,M,P]` ✅ · NDCG = 1.06/1.63 ✅ + nghĩa "so với danh sách hoàn hảo" ✅.
  **Hết cả 2 lỗi 13/10.** Còn: 3/3 ô dừng ở công thức, không ra số cuối (≈0.65).
- Mẩu 2 vấn đáp 10.11 ❌ (+2 → 16/10). User yêu cầu: ôn phỏng vấn giảng câu mẫu nghiêm túc, không đố (a)/(b)/(c).
  Hỏi cách nhớ lâu → rút **khung 3 dòng** + chuỗi neo `VectorStore.search → QdrantStore → query_points → SearchHit`. Nói lại 3 dòng ✅ sạch (thiếu tên ví dụ). 16/10 kiểm đóng sách bằng khung này.
- Vấn đáp 3.8 ❌ (+2 → 16/10): IDF sai chiều lần 3. Ép chọn `"ma túy"` 40/61K → cao ✅. Nói lại khung 3 dòng ✅, **tự lấy ví dụ mới** `ma túy đá`↔`methamphetamine` (gọi nhầm "ketamin").

### 2026-10-14 (T4) ca tối ~21:00-22:20 · LÁT 1 · `hit_at_k` + `mrr` theo answers list-các-list · `ndcg_at_k` vào `app/` · **139 passed**
- Merge máy nhà (11-12/10) + máy cty (14/10). `hit_at_k`: đảo vòng ✅ · `answers` ↔ `answers[i]` (lần 1) · `break` ngang `if` → sửa ✅.
- `mrr`: đoán duyệt theo `answers[i]` ra **1/2** (thật 1/3) → hiểu phải duyệt `top_k` ✅ · lại `doc in answers` (**lần 2** lẫn list-các-list) · `index(answers[i])` → `doc` ✅ · thiếu `break` → sửa ✅.
- `ndcg_at_k` 3 mẩu, **Claude dẫn từng bước — CHƯA phải tự viết**: `for i in results` (lặp list thay chỉ số) · quên `+1` thứ hạng, rồi sửa
  sai cả công thức thành `log2(rank)` (bù trừ, chia 0) · `dcg = 0` ngoài vòng ✅ tự chọn đúng · IDCG nói miệng "1 + 1/2" (**lẫn RR của MRR, lần 2 sau 13/10**)
  → ca k=3 tự đọc công thức đúng ✅ · cú pháp: `for x in số` / `range(len(số)` / `math.log` ↔ `log2` / `lo2` / `answer` thiếu s (**2 lần**).
- Nyxara Care: tạo repo **`nyxara-care`** (private) + AGENTS.md 11 task cho Codex · **T1 xong** (khung + Docker + `/health`). Trước lát 1 đóng → chỉ Codex dựng, không ăn giờ XÂY.
- **Sáng 15/10 bắt đầu từ:** CỬA đóng sách `ndcg_at_k` file trắng (mã giả tiếng Việt 4 bước trước) → giảng lại 3 metric bằng khung 3 dòng
  → Claude cài BUG CỐ Ý vào `metrics.py` (bước 2/6). Cặp mới cho [the-phan-biet](./the-phan-biet.md): `answers` ↔ `answers[i]` · RR `1/rank` ↔ điểm NDCG `1/log2(rank+1)`.

### 2026-10-15 (T5) ca tối 21:37-22:40 (mệt, trễ) · LÁT 1 · trace tay 3 metric trên iPad · ⚠️ sáng 15/10 không có CỬA đóng sách
- Bộ dữ liệu: `results=[[A,B,C],[D,E,F]]` · `answers=[[B,C],[X]]` · k=3 → Hit 0.5 · MRR 0.25 · NDCG 0.35.
- Trạm 1 `hit_at_k`: 2 hàng ✅ · `answer` ghi A (lấy từ `top_k`, đúng là B từ `answers[i]`) · **`hits` về 0 khi lần tìm trượt** → in thật
  từng bước → 3 lần tìm ✅ (sau 1 lần trả `1/3` = lẫn `hits` ↔ `return`).
- Trạm 2 `mrr`: return 0.25 ✅ · rank 2 / rr 0.5 ✅ · "có break" ở hàng False (`break` nằm trong `if`) · `total_rr` ghi 0.25 (**lẫn tổng dồn ↔ return, lần 2**)
  → ép chọn RR 1 + 0.5: `total_rr` 1.5 · return 0.75 ✅.
- Trạm 3 NDCG: **quên định nghĩa DCG** (Hit/MRR nói được, An/Bình nói được) → giảng lại 3 câu DCG/IDCG/NDCG trên `[A,B,C]`.
  Câu `[B,A,C]` đúng B+C → trả **2.1** (đúng 1.5) — cộng cả điểm ô sai A. Hết giờ, chưa sửa.
- Cặp mới cho the-phan-biet: **tổng dồn (`hits`/`total_rr`) ↔ giá trị `return`** · `dcg = 0` trong vòng ↔ `hits = 0` ngoài vòng.
- **Sáng 16/10 bắt đầu từ:** (1) 5' làm lại `[B,A,C]` đúng B+C → DCG (chỉ cộng ô đúng) · (2) nói khung 3 câu DCG/IDCG/NDCG đóng sách
  · (3) CỬA: gõ `ndcg_at_k` file trắng (mã giả 4 bước trước) · rồi vấn đáp tới hạn 16/10 (3.8 · 10.11). Phần mới chỉ mở khi CỬA qua.

### 2026-10-16 (T6) ca công ty từ 09:18 (đứt quãng) · LÁT 1 · vấn đáp 3 câu
- Không thấy note 15/10 (chỉ có điểm 3.5 + 3.9 trong bảng); cửa NDCG sáng 15/10 coi như **chưa làm**.
- 3.8 ⚠️ · 10.11 ⚠️ · 10.10 ⚠️ — cả ba lên/giữ, hẹn **21/10** (chi tiết ở bảng trên). **IDF chữ hiếm đúng chiều lần đầu đóng sách.**
- Lẫn mới: rỗng "vì IDF = 0" ↔ **0 ứng viên** (chạy thật kho 3 điều, `ma túy đá` → điều "khai thác đá" đứng đầu).
- Câu kiểm nhánh Elastic: đặt bộ dịch ở `metadata_filter.py` / core → [Cặp 22](./the-phan-biet.md) tái phát theo thư mục; sửa đúng **sau gợi ý**.
- Cửa NDCG từng bước: DCG ✅ sau 2 lần sửa (`for answer in answers` — **lẫn `answers`↔`answers[i]` lần 3**, gọi `['a','b']` là "chuỗi" · `index(answers[i])`/`index(answers)` → `index(answer)`).
  IDCG: tính tay ✅ (không ra số cuối, lần 3) · **mở `metrics.py` → cửa KHÔNG tính**, làm lại đóng sách sau ≥ vài giờ · hỏi vì sao `min`, `range(1, n+1)` → giảng.
  Lẫn mới: **"máy trượt → IDCG = 1"** (đúng: IDCG chỉ theo số văn bản đúng; `["a","b"]` → 1.63) — 2 lượt.
- **User tự phát hiện:** `answers[i] = []` / `results = []` → `ZeroDivisionError` ở cả 3 metric. Claude giảng A/B/C, chốt **A (raise ValueError)** — user nhờ dạy, không tự chốt.
  Giảng lại: ý 1 ✅ · cái giá (cả lượt đo dừng) ❌ · lẫn "bỏ qua" (chỉ cho bộ cố ý không đáp án) với Zalo. **Việc treo: thêm kiểm đầu vào vào `metrics.py` + test.**
- **Cửa `ndcg_at_k` đóng sách** — file [ndcg-cua-1610.py](../drills/ndcg-cua-1610.py): làm lại từ trắng (user hứa trong 16/10).
- Còn treo: Hybrid 2 nhánh (quá hạn 15/10, hỏi không ví dụ dựng sẵn).

### 2026-10-16 (T6) ca tối 20:29-21:40 · LÁT 1 · mệt cuối buổi, user xin dừng
- **CỬA `ndcg_at_k` đóng sách** ([ndcg-cua-1610-toi.py](../drills/ndcg-cua-1610-toi.py)) **7/7 ⚠️ trong 19'** · bỏ bước mã giả.
  `answers[i]` · `min(len(answers[i]), k)` · `range(1, n+1)` ✅ (3 chỗ lẫn sáng nay). Lỗi: `results.index` → `top_k` (tự sửa) ·
  `log2` → `math.log2` (tự) · **`dcg =` ↔ `dcg +=`** (sau gợi ý — lẫn tổng dồn ↔ gán đè **lần 3**).
- Ép chọn IDCG khi máy trượt **2/3**: câu 1 vẫn "1.0" (đúng 1.63, **lần 3**) → in vòng IDCG của chính user (không đọc `results`) →
  2 câu sau ✅. Gốc lẫn: 1 văn bản đúng thì IDCG = 1 thật.
- Vấn đáp Hybrid 2 nhánh ⚠️ → 21/10 (chi tiết ở bảng trên).
- Việc treo kiểm đầu vào: Claude viết `_check_inputs` + 9 test, **cài bug** `if not answers:` (đúng: `answers[i]`).
  User đọc output đúng (NDCG chia 0 · Hit/MRR lặng lẽ tính trượt) · chọn sai dòng 1 lần (`if not results`) · chỉ đúng dòng **sau 2 gợi ý**.
  **CHƯA SỬA** — file vẫn `if not answers:`, suite **3 failed, 145 passed**. Cặp `answers` ↔ `answers[i]` **lần 4**.
- **Buổi sau bắt đầu từ:** (1) gõ sửa dòng `if not answers:` → suite xanh → commit · (2) nói lại đóng sách **cái giá** của phương án A
  (sáng nay ❌) · (3) ép chọn IDCG lần nữa (số mới) trước khi mở việc mới.

### 2026-10-17 (T7) ca tối 21:45-~22:15 · LÁT 1 · mệt, giữ luật >21h = 45'
- (1) Sửa `if not answers:` → `answers[i]` **sau khi in giá trị lượt `i=1`** (không tự nhớ ra) · tự xoá kiểm thừa trong `mrr`/`ndcg_at_k`
  nhưng **xoá mất `:` của `for`** → SyntaxError → sửa. **148 passed**, commit `a5d102f`. `hit_at_k` còn 1 bản kiểm thừa (vô hại, dọn sau).
- (2) Cái giá phương án A ⚠️ (lên từ ❌): "chặn luôn, không ra NDCG" ✅ · nói "mấy câu đầu không đo được" — đúng là **mất cả 787 câu tốt** (kiểm chạy trước khi chấm).
- (3) IDCG: "1" **lần 4** → in vòng IDCG thật → ép chọn IDCG↔NDCG ⚠️ (tự sửa) → gốc lộ: **ideal ranking = 1 vị trí** → bảng 2 hàng → 2.13 ·
  câu mới không bảng (2 đúng, máy trúng hạng 1) **1.63 ✅**. → [Cặp 29](./the-phan-biet.md).
- **Buổi sau (CN 18/10 sáng) bắt đầu từ:** 3' ép chọn Cặp 29 (số mới, không bảng) → **mở A/B harness** (giảng 5 mục trước). Nợ nền đã trả đủ.

---

## ⏸️ CHỖ DỪNG — buổi sau làm từ đây

### A0. ⭐ T7 10/10 — 6h (sáng 2h + tối 4h) · user chốt: **ĐÓNG MRR + NDCG@10** (đủ 6 bước mỗi cái)

| Ca | Phút | Việc |
|---|---|---|
| Sáng | 5' | Ép chọn list lồng (`results[i]` ↔ `results[i][j]`) + `:` (`else`/`def`) |
| | 10' | Vấn đáp **3.8 BM25** (hỏi chiều IDF bằng 2 chữ thật) · **3.9 tenant** (hỏi cả câu 3.9) |
| | 15' | **CỬA:** gõ `hit_at_k` đóng sách vào file trắng → 5 test. Trượt → mã giả 4 bước rồi gõ |
| | 80' | **MRR ca 1** — giảng 5 mục · ép chọn **dòng đếm từ 1 ↔ chỉ số đếm từ 0** · chấm tay bảng chữ cái · gõ vào `app/evaluation/metrics.py` (CODE TAY) · Claude viết test → suite xanh |
| | 10' | Note |
| Tối | 10' | Vấn đáp **3.5 RRF** (cosine trần bao nhiêu, BM25 trần bao nhiêu) · **Hybrid 2 nhánh** |
| | ~120' | **MRR ca 2** — BUG CỐ Ý (Claude cài lỗi logic) → user DEBUG + FIX · chạy 788 câu thật, đọc MRR cạnh Hit@k · **gõ lại đóng sách** · DOCUMENT → **MRR ĐÓNG** |
| | ~110' | **NDCG@10** — giảng 5 mục (DCG · `log2` · IDCG · nhiều điều đúng) · chấm tay · gõ vào `app/` · test · chạy 788 câu. Không kịp đóng → **phần còn dở làm nốt CN** (đã mở T7, không tính là "mới") · nghỉ 10' mỗi ~1h |

### A0b. CN 11/10 — 6h · **KHÔNG kỹ thuật mới** (user chốt): ôn + trace + luyện code + việc cho bớt chán
- Tổng kết tuần 10-20' (roadmap §4): giờ thật Hit@k / MRR / NDCG · số vấn đáp · số lần tắc.
- Gõ lại đóng sách `hit_at_k` · `mrr` · `ndcg_at_k` (spaced, cách ≥12h) · vấn đáp các câu ⚠️/❌ còn treo.
- Trace đường đi thật 1 câu: cây lọc → `HybridRetriever` → 2 nhánh → RRF (vá câu Hybrid ❌ 2 lần).
- **Cho bớt chán:** "đố máy" — user tự gõ câu hỏi đời thường (vd phạt vượt đèn đỏ) → BM25 trả top-5 → user tự chấm bằng mắt, so MRR.
- **T2 12/10:** mục mới kế tiếp của lát 1 = **A/B harness** (vẫn lát 1, chưa sang lát 2).


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
| ~~X5~~ ✅ 03/10 (a+b) | `leaf_matches` trước (bản in 1 lá ở cuối nhật ký 02/10; 2 dòng đầu chép từ `to_leaf_clause`) → `matches` · test `-k leaf` rồi cả file · **X5b** sau đó: `BM25Index` lưu metadata + `HybridRetriever` chuyền cây xuống **cả hai** nhánh · `danh_gia` + `post_filter` → `app/`, tên tiếng Anh | gõ lại từ trắng | khung + test + nối vào nhánh BM25 |
| ~~X6~~ ✅ 06/10 | Test đầu-cuối 10/10 · văn bản thiếu trường → lá `False` (phương án B, khớp Qdrant) · suite 119 passed | — | — |

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

- **Tuần 05→11/10:** sáng T2 05/10 đóng X6 → **LÁT 0 ĐÓNG** → mở lát 1 (nạp 61K + Hit@k). Vấn đáp: 05/10 3.5 + 1.4 · 07/10 10.11 · 08/10 Hybrid 2 nhánh · 09/10 3.8 + 10.10. T7 10/10 lấy hội thoại phòng khám.
- **Phần Claude nối dây:** giảng thẳng có cấu trúc + code thật TRƯỚC, việc làm sau — không mở bằng đố/đoán (user 04/10).
- Lát 0 đóng ở **cây 1 tầng** là đủ. Đệ quy = nâng cấp **một chữ**, chỉ mở khi user tự hỏi *"nếu con lại là cây thì sao"*.
- **CN 04/10** vẫn tổng kết tuần + chấm PRIMM 2 số (nếu có tin nhắn tối CN). Hàng đợi này chạy tới khi giờ cố định trở lại.

### A1b. ✅ USER CHỐT 02/10 — bỏ Orchestrator, làm cả A + B + C · **ĐÃ VÀO ROADMAP 02/10** (user yêu cầu sửa ngay)

- **B đổi thành B1 = trợ lý tư vấn phòng khám THẬT** (FB Ads + Zalo) → [side-lanes mục L](../side-lanes.md). Việc của user trước khi lát 1 đóng: **xin phép phòng khám bằng văn bản** + gom hội thoại (ẩn danh).

- **Bỏ Nyxara-Orchestrator** (bị chê *"không nhắm đúng thị trường, chả ai xài"*; user đồng ý: TypeScript · thị trường extension
  code đã bão hoà · agent code nên khó nhận là của mình).
- **A** — `nyxara-core` lấp 4 lỗ tin tuyển: cloud · adapter OpenAI/Anthropic · Docker kéo lên lát 1 · `PgVectorStore`. ~15-20h, lấy từ ~60h trống.
- **C** — MCP server tra luật cho người ngoài dùng (Claude Desktop/Cursor), gắn lát 5. ~10-15h, lấy từ ~60h trống.
- **B = DỰ ÁN SỐ 2 mới** — agent text-to-SQL trên Postgres (hỏi tiếng Việt → SQL → kết quả + câu SQL đã chạy; đo tỉ lệ đúng).
  ~30-40h, **ăn slot 1h/ngày cũ của Orchestrator**, không đụng giờ core. Python/FastAPI, dùng lại khung eval lát 1.
- ✅ **B bắt đầu SAU LÁT 1** (user chốt 02/10). Bộ đo có sẵn: **ViText2SQL** (VinAI, ~10K câu tiếng Việt, chỉ dùng nghiên cứu/học) — vai trò như Zalo Legal ở core.
- ✅ **Chốt CN 04/10:** B = **Nyxara Care** · lõi áp **Cách A** · dữ liệu phòng khám thật (bảng giá + tin nhắn từ Pancake, tuần sau) → [side-lanes L](../side-lanes.md).
  Dòng text-to-SQL ở trên là phương án cũ trước khi đổi sang phòng khám.

### A2. ~~Bài thiết kế chờ — MẢNG DỮ LIỆU~~ → xong 02/10: không thêm lát data, xem A1b (user nêu 02/10, chưa sửa roadmap)

User thấy lộ trình **thiếu kỹ năng xử lý dữ liệu**: ETL/pipeline · làm sạch · **SQL/Postgres** · crawl · queue · **chạy theo lịch**.
Còn ~60h chưa phân (35 mục ≈ 137h / ~200h tới 15/02). **Cách chốt:** ca sáng, user mang **2-3 tin tuyển thật**
→ Claude đối chiếu từng dòng với ~90 mục hiện có → chỉ thêm thứ tin tuyển đòi. Ba phương án Claude soạn sẵn
(giảng kèm giá trước khi hỏi): **P1** gộp vào lát 1 (nạp 61K bằng pipeline thật: Postgres giữ metadata + job theo lịch) ·
**P2** lát data riêng sau lát 1 (crawl vbpl văn bản mới → làm sạch → Postgres → queue embed) · **P3** chỉ 🟢 nói được.
⭐ **Đã rà 10 tin thật 02/10 → [thi-truong-2026-10.md](./thi-truong-2026-10.md): ETL/Airflow 0 tin bắt buộc ⇒ nghiêng bỏ P2.** X5/X6 lát 0 **chạy tiếp bình thường** — mảng này chỉ ảnh hưởng từ lát 1 trở đi.

### B. Giữ nguyên

- **Nợ cũ:** ~~`eq/ne/gt/gte/lt/lte` vào glossary~~ ✅ 03/10 · dọn 2 tên trong `cham_nhat` (`name = {}` · `max`).
- ⚠️ **Nhắc Claude:** user tắc 4 chỗ cùng lúc thì **hạ bậc bài, đừng hạ tốc độ hỏi** (22/09).
- **Theo dõi:** lỗi đọc đề/chép sai **21 lần**. Tên biến lấy từ đề → **copy-paste**, không gõ tay.

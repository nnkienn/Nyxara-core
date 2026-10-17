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

> Nhật ký 18/09 → 06/10: [archive/2026-10-17-review-schedule.md](../archive/2026-10-17-review-schedule.md).

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
- User đòi học tiếp (22:50) → gõ `hit_at_k` ([drill](../drills/archive/hit-at-k.py)): đúng B1 đếm · B4 chia; sai `.len()`
  + **2 vòng `for` lồng, so list `==` chuỗi, không dùng `k`** → in 9 dòng False. User xin đáp án → Claude đưa lời
  giải + trace; user *"vẫn chưa hiểu lắm"*, dừng ~23:10. **Chưa gõ lại.** Nút thật: **list lồng list + chỉ số `i`**.
- Mai sáng: (1) chấm tay 3 câu trên giấy · (2) in `results[i]`, `results[i][:k]`, `answers[i]` cho i=0..2 ·
  (3) gõ lại 5 dòng từ trắng. Nếu `[i][:k]` còn rối → drill riêng list lồng 10' trước.

### 2026-10-08 (T5) ca tối 21:20-22:10 (~50', ca muộn, không OT) · LÁT 1
- Ca sáng + cty 08/10 không có. Vấn đáp Hybrid 2 nhánh **❌** (→10/10) — giảng bằng bảng RRF k=60.
- Hit@k đoán `0 · 1/3 · 0` → lẫn 2 cặp: **"k dòng đầu" ↔ "dòng thứ k"** · **Hit 1 câu (0/1) ↔ điểm cả đề (chia)**.
  Ép chọn 3/4 (còn hở cặp 1) → 4/4 ✅.
- Gõ lại `hit_at_k` (vào file cũ [hit-at-k.py](../drills/archive/hit-at-k.py)): 2 thiếu `:` · `result` thiếu `s` · `==` → `in`;
  **tự sửa `hits = top_k + 1`** → xanh 0.333/0.666.
- Claude nối [hit-real.py](../drills/archive/hit-real.py): BM25 tối giản 61K × 788 câu, cache `data/zalo_legal/bm25_top10_test.json`.
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
- BUG CỐ Ý [mrr-bug-1010.py](../drills/archive/mrr-bug-1010.py) (chia số lần TRÚNG): tự nói "chia tổng results", sửa đúng. Bug làm 788 câu phồng 0.562 → 0.685.
- **BM25 Zalo 788: MRR@10 = 0.562** · Hit@10 0.821. MRR còn thiếu: gõ lại đóng sách 11/10 (hẹn với ChatGPT) → qua thì MRR ĐÓNG.
- Vấn đáp 3.5 ⚠️ · Hybrid ✅ (→15/10 cả hai). 1 lỗi đọc (d1↔d2).
- Câu hỏi 1 việc/lượt chạy tốt hơn hẳn sáng nay: 1 lần "không hiểu câu hỏi" (câu ghép, trước khi đổi cách) rồi trơn.
- 21:15 user chọn học tiếp → **NDCG mở**: MRR không phân biệt [A✓ B✗ C✓] với [A✓ B✗ D✗] ✅ · DCG = `1 + 1/log2(4)` = 1.5 ✅ (tự dùng công thức).
  **IDCG trả "2"** (quên giảm giá ở danh sách lý tưởng) → *"lú quá"* — lỗi Claude mở IDCG quá sớm + lỡ dùng "dòng". Giảng IDCG = điểm tối đa,
  NDCG = 1.50/1.63 ≈ 0.92. User nghỉ 22:20. CLAUDE.md §5 viết lại + §6 luật dừng (user yêu cầu).
- **CN 11/10 bắt đầu từ:** (1) *"Kiểm tra lại Hit@k và MRR, không gợi ý trước"*: lời → tính tay dữ liệu MỚI → tự viết 2 hàm → trace (hẹn với ChatGPT) ·
  (2) NDCG: user giảng lại DCG bằng ví dụ A/B/C → IDCG từng bước (hỏi giá trị thứ hạng 2 trong danh sách lý tưởng trước) → NDCG 0.92 · chưa code.

### 2026-10-11 (CN) — chỉ có cửa MRR, không ghi note hôm đó
- CỬA `mrr` đóng sách [mrr-cua-1110.py](../drills/archive/mrr-cua-1110.py) **5/5** (chạy lại 12/10) → **MRR ĐÓNG**. Thêm [Cặp 28](./the-phan-biet.md) (`results` ↔ `top_k`).

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

> Chỗ dừng mới nhất = dòng **"Buổi sau bắt đầu từ"** ở cuối buổi gần nhất trong Nhật ký phía trên.
> Kế hoạch cũ (A0 · A0b · hàng đợi X/N · A1b · A2): [archive/2026-10-17-review-schedule.md](../archive/2026-10-17-review-schedule.md).

### B. Giữ nguyên

- **Nợ cũ:** ~~`eq/ne/gt/gte/lt/lte` vào glossary~~ ✅ 03/10 · dọn 2 tên trong `cham_nhat` (`name = {}` · `max`).
- ⚠️ **Nhắc Claude:** user tắc 4 chỗ cùng lúc thì **hạ bậc bài, đừng hạ tốc độ hỏi** (22/09).
- **Theo dõi:** lỗi đọc đề/chép sai **21 lần**. Tên biến lấy từ đề → **copy-paste**, không gõ tay.

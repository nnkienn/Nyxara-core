# 🐛 Bug Log — nhật ký bug (cố ý + thật)

> Trái tim của phương pháp học. Mỗi bug (dù **cố ý gài** ở bước 2, hay **gặp thật** khi chạy)
> ghi lại đây. Đọc lại file này = ôn đúng những chỗ mắt người hay trượt.
>
> **Vì sao đáng ghi:** senior không giỏi vì không tạo bug — giỏi vì **nhận ra pattern bug**.
> Ghi 20 bug → lần 21 nhìn phát ra ngay.

**Template:**
```
### #<n> — <tiêu đề ngắn>  ·  Phase <n>  ·  <cố ý | thật>  ·  <ngày>
- **Triệu chứng:** kết quả sai thế nào (số thật: mong đợi X, nhận Y)
- **Nguyên nhân:** dòng nào, sai vì sao
- **Cách tìm ra:** in gì / trace gì để lần ra (đây là phần quý nhất)
- **Fix:** sửa gì
- **Test chặn tái phát:** tên test regression đã thêm
- **Bài học / pattern:** loại bug này còn xuất hiện ở đâu nữa
```

---

## Phân loại pattern hay gặp (điền dần)

| Pattern | Ví dụ kinh điển | Đã dính ở bug # |
|---|---|---|
| Off-by-one | rank bắt đầu từ 0 thay vì 1 (NDCG, RRF); quên +1 phí đường đi (edit distance) | #1, #4 |
| Sai dấu / ngưỡng | `>= 0` lẽ ra `>= 0.5`; đảo dấu λ trong MMR | — |
| Quên normalize | cosine trên vector chưa L2-norm | — |
| Thiếu `await` | async lây cả chuỗi, coroutine không chạy | — |
| Parse lỏng | `"yes" in text` bắt nhầm "no ... yes-like" | — |
| Silent failure | quên filter `tenant_id` → rò data, KHÔNG crash | #7 |
| State/loop guard | thiếu `max_steps`/`attempts` → lặp vô hạn | #6 |

---

## (Ghi các bug bên dưới, mới nhất trên cùng)

### #1 — `start` không trừ `overlap` khi sang chunk kế tiếp  ·  Phase 0  ·  cố ý  ·  2026-07-14
- **Triệu chứng:** `recursive_chunk("ABCDEFGHIJ", size=6, overlap=2)` mong đợi `chunks[1] == "EFGHIJ"`, nhưng nhận về `"GHIJ"` — thiếu mất 2 ký tự đầu (`"EF"`). `chunks[0]` vẫn đúng (`"ABCDEF"`) — bug chỉ lộ ra từ chunk thứ 2 trở đi.
- **Nguyên nhân:** dòng 7 viết `start = end` thay vì `start = end - overlap` — không lùi lại điểm bắt đầu của chunk sau, nên 2 chunk không còn phần chung.
- **Cách tìm ra:** chạy `pytest`, đọc assertion diff (`'GHIJ' == 'EFGHIJ'`) → so với công thức đã ghi ở [algorithms.md](./algorithms.md) (`start[chunk sau] = end[chunk trước] - overlap`) → thấy dòng 7 thiếu đúng phép trừ đó.
- **Fix:** sửa dòng 7 thành `start = end - overlap`.
- **Test chặn tái phát:** `tests/application/chunking/test_recursive_chunker.py::test_overlap_between_consecutive_chunks`.
- **Bài học / pattern:** off-by-one ở điểm nối 2 phần liền kề — **chunk đầu tiên luôn đúng** vì nó không phụ thuộc overlap, chỉ chunk thứ 2 trở đi mới lộ bug. Nếu test chỉ kiểm `chunks[0]` sẽ không bao giờ bắt được lỗi này → cùng họ với off-by-one rank sẽ gặp lại ở RRF/NDCG (Phase 2-3).

### #2 — quên `result.append(chunk)` → trả về list rỗng  ·  Phase 0  ·  cố ý  ·  2026-07-15
- **Triệu chứng:** `dedup_exact(["mèo","chó","mèo","chim"])` mong đợi `["mèo","chó","chim"]`, nhưng nhận về `[]` (rỗng) — KHÔNG crash, chỉ trả sai.
- **Nguyên nhân:** trong vòng lặp chỉ có `seen.add(chunk)` ("ghi tên lên giấy") mà quên `result.append(chunk)` ("cho vào phòng") → `result` không bao giờ được thêm gì.
- **Cách tìm ra:** chạy thử in ra `[]` → so với người gác cửa làm 2 việc, soi thấy code chỉ làm 1.
- **Fix:** thêm dòng `result.append(chunk)` sau `seen.add(chunk)`.
- **Test chặn tái phát:** `tests/application/ingestion/test_deduplicator.py::test_removes_duplicate_chunks`.
- **Bài học / pattern:** loại "phải cập nhật 2 cấu trúc song song nhưng chỉ làm 1" — gặp lại ở
  bất cứ đâu có 2 nơi phải đồng bộ: cache + store, index + data, `seen` + `result`. Quên 1 nửa
  → không crash, chỉ *âm thầm sai* (họ hàng với silent failure).

### #3 — `seen = set` thiếu `()` → TypeError  ·  Phase 0  ·  thật  ·  2026-07-15
- **Triệu chứng:** `TypeError: argument of type 'type' is not a container` ở dòng `if chunk in seen`.
- **Nguyên nhân:** gán `seen = set` (cái *khuôn*) thay vì `set()` (một *tập rỗng thật*) → `x in <type>` không hợp lệ.
- **Cách tìm ra:** đọc dòng cuối traceback "type ... is not a container" → nhìn lại `seen = set`.
- **Fix:** `seen = set()`.
- **Test chặn tái phát:** cùng test file (crash thì test đỏ ngay).
- **Bài học / pattern:** phân biệt *kiểu* vs *instance của kiểu* — cùng họ lỗi với dùng `list` thay `list()`, `dict` thay `dict()`.



### #4 — quên +1 (cộng phí) khi tính ô trong lưới edit distance  ·  Phase 0  ·  thật  ·  2026-07-16
- **Triệu chứng:** ô `(e,b)` tính ra 1 thay vì 2; sanity check lộ liền: "meo"→"b" không thể tốn 1 phép. **Dính 3 lần trong 1 buổi** — 2 lần lúc trace tay, 1 lần khi vẽ lại ma trận vào notes (3 ô sai).
- **Nguyên nhân:** lấy `min(3 hàng xóm)` mà quên cộng phí bước đi — đặc biệt đường chéo khi 2 ký tự **khác nhau** vẫn phải +1 (chéo chỉ miễn phí khi 2 ký tự GIỐNG hệt).
- **Cách tìm ra:** sanity check bằng trực giác — "biến chuỗi 3 chữ thành 1 chữ mà chỉ tốn 1 phép?" vô lý → dò lại từng số trong phép min → thấy thiếu +1.
- **Fix:** khắc luật: `trên+1, trái+1, chéo+cost` — **luôn cộng phí**, miễn phí là ngoại lệ duy nhất (chéo + ký tự khớp).
- **Test chặn tái phát:** (sẽ thêm) `tests/application/ingestion/test_edit_distance.py` — 5 ca: thay/giống hệt/xoá/thêm/khác hết.
- **Bài học / pattern:** cùng họ **off-by-one** (#1) — sai lệch 1 đơn vị ở phép cộng dồn. Loại này "lì": hiểu rồi vẫn tái phạm khi tay làm nhanh → chỉ có test + sanity check bắt được, đừng tin mắt.

### #5 — `grid[n,m]` + lưới đóng cứng kích thước  ·  Phase 0  ·  thật  ·  2026-07-16
- **Triệu chứng:** (1) `return grid[n,m]` → `TypeError` (list không nhận chỉ số kiểu tuple); (2) tạo lưới bằng `range(2)` + `row=[0,0,0]` cứng → input dài hơn là lưới không đủ chỗ, nổ IndexError.
- **Nguyên nhân:** (1) lưới 2 chiều phải truy cập **2 cặp ngoặc riêng** `grid[i][j]`, không phải `grid[i,j]`; ô cuối là `[n-1][m-1]` (chỉ số lớn nhất = kích thước − 1). (2) đã tính `n, m` từ `len(a), len(b)` nhưng không dùng, hardcode số cứng.
- **Cách tìm ra:** đọc traceback dòng cuối + soi "n, m tính ra để làm gì mà không dùng?".
- **Fix:** `grid = [[0]*m for _ in range(n)]` (hoặc vòng for dài) và `return grid[n-1][m-1]`.
- **Test chặn tái phát:** cùng test file #4 — ca chuỗi dài khác nhau sẽ bắt được hardcode.
- **Bài học / pattern:** "magic number" — số cứng viết tay chỉ đúng cho 1 ví dụ, phải thay bằng biến tính từ input. Và cú pháp truy cập lưới `[i][j]` — nhớ luôn thể `[[0]*n]*m` là bẫy trỏ chung hàng.

### #6 — đệ quy dùng sai slice `separators` (không tiến triển)  ·  Phase 0  ·  cố ý  ·  2026-07-17
- **Triệu chứng:** `split_by_separators("Meo thich ngu\n\nCho thich chay", size=10, separators=["\n\n"," "])`
  → `RecursionError: maximum recursion depth exceeded` (Python tự phát hiện: "same locals & position").
- **Nguyên nhân:** lần gọi đệ quy dùng lại **nguyên `separators`** (rồi thử `separators[:1]` —
  vẫn chỉ giữ lại phần tử **đầu**, tức `"\n\n"`) thay vì `separators[1:]` (bỏ phần tử đầu, giữ
  phần **còn lại**). Vì `part` đã tách bởi `"\n\n"` nên không còn `"\n\n"` bên trong nữa —
  split lại bằng đúng separator đó là no-op, `part` y hệt lần trước → gọi lại chính nó mãi mãi.
- **Cách tìm ra:** đọc traceback thấy cùng 1 dòng lặp lại nhiều lần với "same locals" → hiểu là
  state (ở đây là `separators`) không hề thay đổi giữa các lần gọi → soi lại tham số truyền vào
  lời gọi đệ quy.
- **Fix:** `split_by_separators(part, size, separators[1:])`.
- **Test chặn tái phát:** `tests/application/chunking/test_recursive_chunker.py::test_splits_by_paragraph_then_word`.
- **Bài học / pattern:** **State/loop guard** — đệ quy bắt buộc phải tiến **gần base case hơn**
  ở mỗi lần gọi (ở đây là "dùng hết dần danh sách separator"). Nhầm hướng slice (`[:1]` giữ
  *trước* index vs `[1:]` giữ *từ* index trở đi) là lỗi cú pháp rất nhỏ nhưng gây hậu quả nặng
  (crash toàn bộ, không phải chỉ sai số nhẹ).

### #7 — định nghĩa `save_seen` nhưng quên gọi nó  ·  Phase 0  ·  cố ý  ·  2026-07-17
- **Triệu chứng:** `incremental_ingest(["mèo","gà","chó"], path)` rồi gọi lần 2 với
  `["mèo","gà","chó","chim"]` — mong đợi chỉ `["chim"]`, nhưng nhận về **cả 4 chunk**, kể cả
  3 chunk cũ. Không crash, chạy xong bình thường.
- **Nguyên nhân:** `seen.add(h)` chỉ sửa object `seen` **trong RAM**. Hàm `save_seen()` đã được
  định nghĩa sẵn nhưng **không có dòng nào gọi nó** trong `incremental_ingest` → file trên đĩa
  không bao giờ được ghi lại. Lần gọi sau `load_seen()` đọc file vẫn rỗng/cũ.
- **Cách tìm ra:** viết test mô phỏng **2 lần gọi liên tiếp** (đúng ví dụ mèo/gà/chó/chim đã có
  sẵn trong `algorithms.md`) → so quy trình đã tự ghi trong note ("load → check → **save**")
  với code thật → thấy thiếu bước save.
- **Fix:** gọi `save_seen(seen_path, seen)` trong `incremental_ingest`, sau khi cập nhật `seen`.
- **Test chặn tái phát:** `tests/application/ingestion/test_pipeline.py::test_second_run_only_returns_new_chunks`.
- **Bài học / pattern:** **Silent failure** — hàm chạy xong không lỗi, nhưng "quên lưu trạng
  thái" khiến mọi lần chạy sau coi như chưa từng ingest gì. Test chỉ gọi hàm **1 lần** sẽ
  KHÔNG BAO GIỜ bắt được bug này — phải test qua ít nhất 2 lần gọi liên tiếp mới lộ ra.
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
| Sai dấu / ngưỡng | `>= 0` lẽ ra `>= 0.5`; đảo dấu λ trong MMR; `+` thay vì `*` ở mẫu số cosine | #8 |
| Quên normalize | cosine trên vector chưa L2-norm | — |
| Thiếu `await` | async lây cả chuỗi, coroutine không chạy | — |
| Parse lỏng | `"yes" in text` bắt nhầm "no ... yes-like" | — |
| Silent failure | quên filter `tenant_id` → rò data, KHÔNG crash | #7, #13 |
| Breaking change theo version lib | `.search()` bị gỡ → `.query_points()` | #14 |
| State/loop guard | thiếu `max_steps`/`attempts` → lặp vô hạn | #6 |
| Sửa test thay vì sửa code | đổi số mong đợi trong assert cho khớp output sai, thay vì sửa hàm nguồn | #9 |
| Quên cập nhật 1 trong nhiều cấu trúc song song khi xoá (đối xứng thao tác thêm) | `seen`+`result` (#2); `doc_len`/`doc_count`/`index` khi `remove_document` (#20) | #2, #20 |
| Đoán tên method theo cảm tính (suy từ method khác cùng class), không tra thư viện thật | `.search()`→`.query_points()` (#14); `delete_points`→`delete` (#21) | #14, #21 |
| Để khối comment/TODO thay cho thân hàm thật (trông như xong nhưng Python coi là rỗng) | `get_doc_manifest` thân hàm chỉ có comment, chưa có `return` | #22 |
| Giả định thứ tự của `set()` — Python không đảm bảo thứ tự lặp qua set | `to_upsert` từ `diff_manifest` (đi qua `set()` union) | #23 |
| Thụt lề sai phạm vi (không lỗi cú pháp, sai logic) | code lẽ ra trong `if` bị thụt lề ra ngoài → luôn chạy bất kể điều kiện | #10 |
| Chuẩn hoá 1 bên, quên bên kia | `.upper()` giá trị nhưng so sánh với chuỗi chữ thường → luôn `False` | #19 |
| Timeout mặc định thư viện quá ngắn cho LLM | `httpx`/`requests` mặc định ~5s, LLM cần lâu hơn (đặc biệt lần load đầu) | #18 |

---

## (Ghi các bug bên dưới, mới nhất trên cùng)

### #23 — giả định sai thứ tự của `set()` khi viết assert cho `ingest_document`  ·  Phase 0  ·  thật (lộ qua test tự viết)  ·  2026-08-14
- **Triệu chứng:** `test_ingest_document_writes_to_all_three_stores` fail:
  `embedder.calls == [["chó nâu", "chim xanh", "mèo đen"]]` thay vì đúng thứ tự
  `["mèo đen", "chó nâu", "chim xanh"]` đã ingest vào. Không phải bug logic — dữ liệu vẫn đúng,
  chỉ sai **thứ tự** trong batch gửi cho embedder.
- **Nguyên nhân:** `diff_manifest` tính `all_indices = set(old_manifest) | set(new_manifest)` —
  **`set` trong Python không đảm bảo thứ tự lặp** (khác `list`/`dict` giữ thứ tự chèn từ
  Python 3.7+). `to_upsert` vì vậy ra thứ tự tuỳ theo hash nội bộ của `set`, không phải thứ tự
  `chunk_index` 0→1→2 như trực giác mong đợi.
- **Cách tìm ra:** chạy `pytest` toàn bộ suite (không phải chỉ file đang sửa) — lộ ngay vì assert
  so đúng thứ tự.
- **Fix:** không phải sửa `ingest_document` (đúng rồi) — sửa **assert** trong test, so nội dung
  bằng `sorted(...)` thay vì so thứ tự chính xác.
- **Test chặn tái phát:** `tests/application/ingestion/test_pipeline.py::test_ingest_document_writes_to_all_three_stores`
  (đã tự sửa đúng).
- **Bài học / pattern:** khi 1 giá trị đi qua `set()` ở bất kỳ đâu trong pipeline dữ liệu, **mọi
  thứ tự sau đó không còn đáng tin** — test/assert không được giả định thứ tự trừ khi có bước
  sort tường minh. Ở đây may mắn không phải bug thật (id vẫn khớp đúng text vì 2 list comprehension
  lặp cùng 1 `to_upsert` list), nhưng nếu chỗ khác lỡ dựa vào thứ tự của kết quả từ `set` (vd hiển
  thị UI, ghi log theo batch) thì sẽ *thật* sự sai — luôn chạy `pytest` toàn bộ suite trước khi
  coi 1 tính năng là xong, đừng chỉ chạy file đang sửa.

### #22 — 2 lần thụt lề sai liên tiếp khi thêm hàm mới vào `pipeline.py`  ·  Phase 0  ·  thật  ·  2026-08-14
- **Triệu chứng:** lần 1 — `IndentationError: unindent does not match any outer indentation
  level` ngay khi `import` (dòng `def load_manifest` thừa 1 space so với `def load_seen` phía
  trên). Lần 2 (sau khi sửa lần 1) — `IndentationError: expected an indented block` (thân hàm
  `get_doc_manifest` chỉ có comment, chưa có statement thật nào).
- **Nguyên nhân:** lần 1 — gõ thêm hàm mới ngay dưới hàm cũ nhưng lệch mức thụt lề (1 space
  thay vì thẳng cột với `def` phía trên). Lần 2 — để lại khối comment TODO làm thân hàm tạm,
  nhưng Python không coi comment là "thân hàm" hợp lệ — bắt buộc phải có ít nhất 1 statement
  (kể cả `pass` hay `...`) mới hợp lệ cú pháp.
- **Cách tìm ra:** chạy thẳng `python3 -c "import ..."`, đọc số dòng + loại lỗi trong traceback
  — cả 2 lần đều lộ ngay, không cần đoán.
- **Fix:** lần 1 — dedent `def load_manifest` về đúng cột 0 (ngang hàng các `def` khác ở module
  level). Lần 2 — thêm statement thật (`return manifest.get(tenant_id, {}).get(doc_id, {})`)
  thay vì để trống sau comment.
- **Test chặn tái phát:** không cần test riêng — lỗi cú pháp chặn ngay từ `import`, `pytest`
  collect test sẽ tự fail nếu tái phạm.
- **Bài học / pattern:** cùng họ `#10`/`#16` (thụt lề sai phạm vi) — nhưng ca 2 là biến thể mới:
  **để khối comment/TODO thay cho thân hàm thật** trông giống "đã viết xong" (có nội dung, có
  chữ) nhưng Python vẫn coi là rỗng. Khi khung sẵn có TODO comment, luôn phải thay bằng ít
  nhất 1 dòng lệnh thật trước khi coi là "đã điền".

### #21 — `client.delete_points` không tồn tại, đúng phải là `client.delete`  ·  Phase 0  ·  thật  ·  2026-08-14
- **Triệu chứng:** phát hiện **trước khi chạy** — tra `hasattr(QdrantClient, 'delete_points')`
  → `False`. Nếu chạy thật sẽ nổ `AttributeError: 'QdrantClient' object has no attribute
  'delete_points'`.
- **Nguyên nhân:** đoán tên method theo cảm tính, suy từ các method khác cùng class
  (`upsert`, `search`) nên đoán có `delete_points` riêng — thực tế `qdrant-client` chỉ có
  1 method `delete` chung cho mọi kiểu xoá (theo id list hay theo `Filter`), không tách tên.
- **Cách tìm ra:** tra trực tiếp thư viện thật thay vì đoán — `hasattr(...)` rồi
  `inspect.signature(QdrantClient.delete)` để xem `points_selector` nhận kiểu gì (`Filter`
  được chấp nhận trực tiếp, không cần bọc `FilterSelector`).
- **Fix:** đổi `self.client.delete_points(...)` → `self.client.delete(...)`.
- **Test chặn tái phát:** `tests/infrastructure/adapters/vectorstore/test_qdrant_store.py::test_delete_removes_own_tenant_doc`.
- **Bài học / pattern:** cùng họ `#14` (API không đúng như kỳ vọng) nhưng khác nguồn gốc —
  `#14` là breaking change giữa các version thư viện, còn đây là **đoán sai ngay từ đầu**
  không tra thực tế. Luôn `hasattr`/đọc docstring/type hint thật của thư viện ngoài trước khi
  gọi, đừng suy đoán tên method theo "nghe hợp lý".

### #20 — quên trừ `doc_count` trong `remove_document` → `avg_doc_len` sẽ tính sai  ·  Phase 0  ·  cố ý  ·  2026-08-14
- **Triệu chứng:** `_build_index()` có 3 doc, sau `remove_document("t1", "doc1")` mong đợi
  `doc_count["t1"] == 2`, nhận về `3`. Không crash, chạy xong bình thường.
- **Nguyên nhân:** trong `remove_document`, chỉ xoá `doc_len[tenant_id][doc_id]` và dọn
  `doc_id` khỏi từng term trong `index`, nhưng **quên** dòng `self.doc_count[tenant_id] -= 1`
  — `add_document` phải cập nhật đủ 3 cấu trúc (`doc_len`, `doc_count`, `index`) khi thêm,
  nên `remove_document` cũng phải đối xứng cập nhật đủ cả 3 khi xoá, sót 1 không hề báo lỗi.
- **Cách tìm ra:** viết test `test_remove_document_updates_doc_count`, chạy `pytest` →
  `AssertionError: assert 3 == 2` — số liệu sai lộ ngay, không cần đọc code mới thấy.
- **Fix:** thêm lại `self.doc_count[tenant_id] -= 1` trong khối `if` xoá `doc_len`.
- **Test chặn tái phát:** `tests/application/retrieval/test_bm25_index.py::test_remove_document_updates_doc_count`.
- **Bài học / pattern:** cùng họ `#2` — quên cập nhật 1 trong nhiều cấu trúc song song. Ở đây
  hậu quả âm ỉ hơn `#2`: `doc_count` sai không tự crash, nhưng nuôi `avg_doc_len` (dòng 35,
  `_score`) tính sai dần theo mỗi lần xoá — làm lệch điểm BM25 của **mọi** doc còn lại, không
  chỉ doc vừa xoá. Thao tác "xoá" luôn phải soát lại đúng những gì "thêm" đã từng ghi.

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

### #8 — sai dấu `+` thay vì `*` trong `cosine_similarity`  ·  Phase 1  ·  cố ý  ·  2026-07-19
- **Triệu chứng:** `cosine_similarity([1,0], [1,1])` mong đợi `0.707` (tính tay), nhận về `0.414`.
- **Nguyên nhân:** `return dot / (norm_a + norm_b)` — **cộng** 2 độ dài vector lại làm mẫu số,
  thay vì **nhân** (`norm_a * norm_b`) đúng công thức `cos(a,b) = dot / (||a|| × ||b||)`.
- **Cách tìm ra:** test dùng đúng ví dụ đã tính tay trước đó (`a=[1,0]`, `b=[1,1]`) → so công
  thức đã ghi trong note, thấy dấu toán tử sai.
- **Fix:** đổi `+` thành `*`.
- **Test chặn tái phát:** `tests/domain/test_similarity.py::test_45_degree_angle`.
- **Bài học / pattern:** nhầm phép cộng với phép nhân ở công thức toán — dễ xảy ra khi gõ nhanh
  không nhìn kỹ ký hiệu `×` trong công thức đã viết ra.

### #9 — sửa đáp án của test thay vì sửa code nguồn  ·  Phase 1  ·  cố ý (lộ thêm)  ·  2026-07-19
- **Triệu chứng:** sau khi thấy test đỏ (`0.707` mong đợi vs `0.414` thực tế), thay vì sửa
  `similarity.py`, lại đổi thẳng `assert ... == 0.707` trong **test** thành `0.707 == 0.404`
  (mà `0.404` còn không khớp cả con số sai `0.414` — tính nhầm luôn cả số để né).
- **Nguyên nhân:** hiểu lầm mục tiêu là "làm test xanh", quên rằng test đóng vai trò **đáp án
  đúng cố định** (tính tay, độc lập với code) — sửa đáp án theo bài làm sai là ngược chiều.
- **Cách tìm ra:** đọc lại diff thấy số trong `assert` bị đổi, không phải code nguồn.
- **Fix:** trả `assert` về đúng `0.707` (ground truth), sửa bug thật ở `similarity.py` (xem #8).
- **Test chặn tái phát:** `tests/domain/test_similarity.py::test_45_degree_angle`.
- **Bài học / pattern:** đây là lỗi **tư duy về testing** nghiêm trọng hơn cả bug toán #8 —
  test phải giữ nguyên đáp án đúng, code phải đổi để khớp test, không phải ngược lại. Nếu quen
  tay "sửa test cho xanh", mọi lưới an toàn (regression test) sẽ mất tác dụng vĩnh viễn.

### #10 — `_ensure_collection` thiếu thân `if`, luôn tạo mới không "ensure"  ·  Phase 1  ·  thật  ·  2026-07-19
- **Triệu chứng:** gọi `QdrantStore(...)` lần 2 (collection đã có từ lần 1) → Qdrant trả lỗi
  `409 Conflict: Collection 'test_phase1' already exists!`. Lần đầu chạy vẫn ổn, không lỗi.
- **Nguyên nhân:** `if not self.client.collection_exists(...):` đứng riêng 1 dòng, còn
  `self.client.create_collection(...)` thụt lề **ngang hàng với `if`** (nằm NGOÀI khối `if`)
  → luôn chạy bất kể điều kiện đúng/sai, không hề "ensure" (đảm bảo) gì cả.
- **Cách tìm ra:** chạy lần 2 thấy lỗi 409 → soi lại thụt lề, thấy `create_collection` không
  nằm bên trong khối `if`.
- **Fix:** thụt `create_collection(...)` vào thêm 1 cấp, nằm hẳn bên trong `if`.
- **Test chặn tái phát:** xác nhận tay — gọi `QdrantStore` 2 lần liên tiếp cùng tên collection
  không còn lỗi 409.
- **Bài học / pattern:** thụt lề sai **không phải lúc nào cũng crash ngay** — code vẫn chạy
  được (không `SyntaxError`), chỉ sai **phạm vi thực thi** (chạy luôn thay vì có điều kiện).
  Phải đọc thụt lề để biết dòng nào thực sự nằm trong `if`/`for`/`def`, không chỉ nhìn "code
  có chạy được không".

### #11 — đổi tên biến vòng lặp nhưng quên sửa chỗ dùng  ·  Phase 1  ·  thật  ·  2026-07-19
- **Triệu chứng:** `PointStruct(id=id_, ...) for id, text, vector in zip(ids, texts, vectors)`
  — vòng lặp định nghĩa biến tên `id`, nhưng `PointStruct(...)` lại dùng `id_` (có dấu `_`,
  chưa từng được định nghĩa) → sẽ nổ `NameError` nếu chạy.
- **Nguyên nhân:** tên biến vòng lặp bị đổi qua vài lần sửa liên tiếp (`i` → `id_` → `id`),
  nhưng chỗ **dùng** biến đó (trong `PointStruct`) không được cập nhật theo kịp mỗi lần đổi.
- **Cách tìm ra:** đọc đối chiếu tên biến ở chỗ định nghĩa (dòng `for`) với chỗ dùng
  (`PointStruct(...)`) — phát hiện 2 tên không khớp nhau trước khi chạy.
- **Fix:** đổi `id=id_` thành `id=id` cho khớp đúng tên biến vòng lặp đang dùng.
- **Test chặn tái phát:** xác nhận tay qua lần chạy `upsert` thành công sau đó.
- **Bài học / pattern:** đổi tên 1 biến phải rà lại **mọi chỗ dùng nó**, không chỉ chỗ định
  nghĩa — rất dễ sót khi sửa qua nhiều vòng nhỏ liên tiếp (giống cách bug này xuất hiện).

### #12 — Qdrant point id phải là số nguyên hoặc UUID, không nhận string tuỳ ý  ·  Phase 1  ·  thật  ·  2026-07-19
- **Triệu chứng:** `upsert('tenant_a', ['1'], ['xin chào'], [vector])` → lỗi
  `400 Bad Request: value 1 is not a valid point ID, valid values are either an unsigned
  integer or a UUID`.
- **Nguyên nhân:** Qdrant giới hạn định dạng `id` nghiêm ngặt — không chấp nhận string tuỳ ý
  (kể cả chuỗi số như `"1"`), chỉ nhận số nguyên thật hoặc UUID chuẩn.
- **Cách tìm ra:** đọc thẳng nội dung lỗi 400 Qdrant trả về — rất rõ ràng, không cần đoán.
- **Fix:** băm `id` gốc qua `uuid.uuid5(uuid.NAMESPACE_DNS, id_gốc)` trước khi gán vào
  `PointStruct` — vừa hợp lệ định dạng, vừa **idempotent** (cùng id gốc luôn ra cùng UUID →
  ingest lại ghi đè đúng điểm cũ, không tạo bản trùng).
- **Test chặn tái phát:** xác nhận tay — `upsert` 2 lần liên tiếp cùng id gốc `"1"` đều thành
  công, không lỗi, không tạo điểm thứ 2.
- **Bài học / pattern:** hệ thống ngoài (Qdrant) có ràng buộc định dạng riêng — đây không phải
  lỗi logic trong code tự viết, mà là quy tắc của hệ thống bên ngoài. Đọc kỹ thông báo lỗi từ
  chính hệ thống đó trước khi tự đoán mò nguyên nhân.

### #13 — bỏ filter `tenant_id` trong `search` → rò data tenant khác (KHÔNG crash)  ·  Phase 1  ·  cố ý (drill)  ·  2026-07-19
- **Triệu chứng:** `search(tenant_id="A", ...)` trả về **cả** `"mèo của A"` **và** `"chó của B"`.
  Test đỏ: `AssertionError: assert 'chó của B' not in ['chó của B', 'mèo của A']`. **Code KHÔNG
  hề crash** — Qdrant chạy ngon, trả kết quả bình thường, không một dòng lỗi nào.
- **Nguyên nhân:** bỏ dòng `query_filter=filter` trong `query_points` → query chạy trên **toàn
  bộ collection** (mọi tenant) thay vì chỉ tenant A. Single-collection multi-tenancy mà thiếu
  filter = mọi tenant nhìn thấy nhau.
- **Cách tìm ra:** **chỉ có test bắt được.** Mắt nhìn `search` thấy "cú pháp đúng, chạy được" —
  không thể nhận ra bằng đọc code. Assertion `'chó của B' not in texts` là cái lưới duy nhất.
- **Fix:** khôi phục `query_filter=filter` (filter `tenant_id == <tenant truyền vào>`).
- **Test chặn tái phát:** `tests/infrastructure/adapters/vectorstore/test_qdrant_store.py::test_search_only_returns_own_tenant`.
- **Bài học / pattern:** **Silent failure** — bug tệ nhất của multi-tenancy vì nó *không kêu*:
  code chạy, không exception, chỉ lặng lẽ rò dữ liệu tenant này sang tenant khác cho tới khi
  khách hàng phát hiện. Phân biệt rạch ròi: **"code crash" (nổ đỏ, dễ thấy) ≠ "test đỏ"
  (assertion bắt kết quả sai)**. Ở đây không có crash — chỉ test cứu. Mọi truy vấn trong hệ
  multi-tenant PHẢI có `tenant_id` filter; nên có test isolation cho từng đường đọc dữ liệu.

### #14 — `client.search()` bị GỠ ở qdrant-client mới → dùng `query_points`  ·  Phase 1  ·  thật  ·  2026-07-19
- **Triệu chứng:** `AttributeError: 'QdrantClient' object has no attribute 'search'` khi gọi
  `self.client.search(...)`.
- **Nguyên nhân:** API `.search()` cũ đã bị loại bỏ ở bản qdrant-client hiện tại (breaking change
  giữa các version). Thay bằng `.query_points()` với tên tham số khác: `query_vector=` → `query=`,
  và response mới bọc kết quả trong `.points` (không trả thẳng list nữa).
- **Cách tìm ra:** đọc `AttributeError` — method không tồn tại → tra API mới của thư viện.
- **Fix:** `res = self.client.query_points(collection_name=..., query=query_vector, query_filter=filter, limit=top_k).points`.
- **Test chặn tái phát:** cùng test file #13 (gọi `search` thật → nếu sai API sẽ nổ ngay).
- **Bài học / pattern:** **breaking change theo version thư viện** — code đúng hôm qua, nâng
  version là gãy. Lý do roadmap dặn cắm thư viện có **flag + pin version**, và vì sao bản tay
  (không phụ thuộc API ngoài) đáng giá để *hiểu* dù production dùng lib.

### #15 — `int | None` không chạy được trên Python 3.9  ·  Phase 2  ·  thật  ·  2026-08-02
- **Triệu chứng:** `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'` ngay
  khi `import` module `rrf.py`, trước cả khi gọi hàm.
- **Nguyên nhân:** chữ ký hàm dùng `top_k: int | None = None` — cú pháp union kiểu mới
  (PEP 604) chỉ chạy được từ Python 3.10 trở lên, nhưng `.venv` của dự án là Python 3.9.6.
- **Cách tìm ra:** đọc traceback — lỗi nổ ngay ở dòng định nghĩa hàm (dòng chứa `|`), không
  phải ở logic bên trong, nên nghi ngay cú pháp/type hint thay vì thuật toán.
- **Fix:** `from typing import Optional`, đổi thành `top_k: Optional[int] = None`.
- **Test chặn tái phát:** không cần test riêng — đây là lỗi ngay lúc import, CI chạy trên đúng
  Python 3.9 sẽ tự bắt được nếu tái phạm.
- **Bài học / pattern:** kiểm tra version Python của môi trường **trước** khi dùng cú pháp
  type hint mới (`|`, `list[int]` không union thì vẫn ổn ở 3.9, nhưng `X | Y` thì không) —
  khác họ với "breaking change theo version lib" (#14), đây là "cú pháp ngôn ngữ mới hơn
  version runtime đang chạy".

### #16 — thụt lề sai 2 lần liên tiếp khi gõ lại `reciprocal_rank_fusion`  ·  Phase 2  ·  thật  ·  2026-08-02
- **Triệu chứng:** lần 1 — code thật nằm **sau** `raise NotImplementedError` còn sót lại từ
  khung, nên không bao giờ chạy tới. Lần 2 (sau khi xoá `raise`) — `IndentationError:
  unexpected indent` tại dòng `for ranked_list in ranked_lists:`.
- **Nguyên nhân:** lần 1 — quên xoá dòng `raise NotImplementedError` của skeleton trước khi
  thêm code thật phía dưới nó. Lần 2 — dòng `for ranked_list...` thụt lề **nhiều hơn** dòng
  `scores = {}` phía trên nó dù dòng đó không kết thúc bằng `:` (không mở khối gì), Python
  không chấp nhận thụt lề tăng vô cớ.
- **Cách tìm ra:** chạy thử, đọc thẳng traceback — lần 1 im lặng raise đúng như code viết
  (không phải bug logic, chỉ là quên dọn code cũ); lần 2 Python chỉ đúng số dòng bị lỗi.
- **Fix:** xoá dòng `raise NotImplementedError`; dedent toàn bộ khối về đúng 1 cấp thống nhất
  với `scores = {}` (4 space), chỉ vòng `for` lồng bên trong mới được thụt thêm.
- **Test chặn tái phát:** `tests/application/retrieval/test_rrf.py` (chạy được không lỗi
  cú pháp là điều kiện cần đầu tiên trước khi so kết quả).
- **Bài học / pattern:** cùng họ với `#10` (thụt lề sai phạm vi) — nhưng lần 1 là dạng mới:
  **quên xoá code cũ (dead code) đứng chặn trước code thật**, không phải thụt lề sai. Khi sửa
  file có sẵn khung/TODO, luôn xoá `raise NotImplementedError`/placeholder **trước tiên**,
  đừng viết chèn code thật vào phía sau nó.

### #17 — `QdrantStore.search` trả UUID nội bộ thay vì `doc_id` gốc  ·  Phase 2  ·  thật  ·  2026-08-03
- **Triệu chứng:** không crash, không test nào đỏ (test Phase 1 cũ chỉ check `text`, không
  check `id`). Chỉ lộ ra khi **ghép** `HybridRetriever`: `dense_ranked` sẽ toàn chuỗi UUID
  (`"3f29b7d2-..."`), còn `bm25_ranked` toàn `doc_id` gốc (`"doc1"`) — 2 danh sách không khớp
  id nào, RRF coi mọi doc là khác nhau hoàn toàn, mất hết lợi ích "tìm được ở cả 2 nguồn".
- **Nguyên nhân:** `upsert` băm `doc_id` gốc qua `uuid5` để làm point id (đúng, Qdrant chỉ
  nhận UUID/số nguyên — bug #12), nhưng **không lưu lại `doc_id` gốc vào payload**. `search`
  trả `hit.id` (UUID nội bộ Qdrant) thay vì `doc_id` gốc, vì payload không có gì khác để trả.
- **Cách tìm ra:** **đọc code trước khi ghép**, không phải chạy ra lỗi — so `upsert` (băm id)
  với `search` (trả gì) thấy 2 bên dùng 2 "không gian id" khác nhau trước khi build
  `HybridRetriever`, chứ chưa hề chạy thử.
- **Fix:** thêm `"doc_id": id` vào `payload` lúc `upsert`; `search` trả
  `hit.payload["doc_id"]` thay vì `hit.id`.
- **Test chặn tái phát:** `tests/infrastructure/adapters/vectorstore/test_qdrant_store.py::test_search_returns_original_doc_id_not_internal_uuid`.
- **Bài học / pattern:** silent failure kiểu mới — không phải thiếu filter (#13) mà là
  **2 module dùng 2 "không gian định danh" (id space) khác nhau cho cùng 1 thực thể**, chỉ lộ
  ra khi ghép chúng lại, không lộ khi test từng module riêng lẻ. Trước khi ghép 2 component đã
  test riêng "xanh", phải soát lại: chúng có đang nói cùng 1 ngôn ngữ id không?

### #18 — `httpx.post` timeout mặc định 5s quá ngắn cho LLM  ·  Phase 2  ·  thật  ·  2026-08-12
- **Triệu chứng:** `httpx.ReadTimeout: timed out` khi gọi `OllamaGrader._grade_one(...)` lần
  đầu — dù server Ollama phản hồi bình thường (verify lại bằng `curl` không giới hạn timeout).
- **Nguyên nhân:** `httpx.post(...)` không truyền `timeout=` sẽ dùng mặc định **5 giây** — quá
  ngắn cho LLM, nhất là lần đầu model phải load vào RAM (~8.5s riêng bước load, đo được lúc
  test `curl` trước đó).
- **Cách tìm ra:** so lại với kết quả `curl` thủ công đã chạy được (không timeout) → nghi ngay
  cấu hình timeout phía Python, không phải server/mạng có vấn đề.
- **Fix:** thêm `timeout=60.0` vào `httpx.post(...)`.
- **Test chặn tái phát:** `tests/infrastructure/adapters/grader/test_ollama_grader.py::test_grade_one_passes_timeout`
  (assert `kwargs["timeout"] == 60.0`, dùng mock nên không cần chờ thật 60s).
- **Bài học / pattern:** mọi HTTP client (`httpx`, `requests`...) đều có timeout mặc định
  **rất ngắn** (tối ưu cho API thường, không phải LLM) — gọi LLM qua HTTP phải luôn set
  timeout dài tay, không dùng giá trị mặc định của thư viện.

### #19 — `.upper()` xong so sánh với chuỗi chữ thường → luôn `False`  ·  Phase 2  ·  thật  ·  2026-08-12
- **Triệu chứng:** `_grade_one("mèo đen", "con mèo đen dễ thương")` mong đợi `True` (rõ ràng
  liên quan), nhận về `False` — cả 2 test case (liên quan lẫn không liên quan) đều `False`.
- **Nguyên nhân:** dòng `answer = data["response"].strip().upper()` chuyển `answer` thành CHỮ
  HOA, nhưng dòng so sánh lại viết `answer == "yes" or answer == "có"` — toàn chữ **thường**.
  Chữ hoa không bao giờ khớp chữ thường bằng `==`, nên luôn rơi vào `False`.
- **Cách tìm ra:** in thẳng `repr(answer)` ra xem model trả lời gì thật — thấy `'CÓ'` (đúng),
  nhưng code so sánh sai chỗ khác, không phải model trả lời sai.
- **Fix:** đổi so sánh thành `answer.startswith("YES")` — khớp đúng chữ hoa với `.upper()` ở
  trên, và dùng `startswith` thay vì `==` để không vỡ nếu model trả thêm chữ phía sau.
- **Test chặn tái phát:** `test_grade_one_true_when_model_answers_yes`,
  `test_grade_one_handles_lowercase_and_whitespace`.
- **Bài học / pattern:** cùng họ với bug `#8` (nhầm phép toán ở công thức) nhưng ở tầng chuỗi —
  chuẩn hoá 1 bên (`.upper()`) mà quên chuẩn hoá bên kia (chuỗi so sánh) là lỗi rất dễ mắc,
  không hề crash, chỉ âm thầm luôn sai — đọc `repr()` giá trị thật trước khi đoán nguyên nhân.
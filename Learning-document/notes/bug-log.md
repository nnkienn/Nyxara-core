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
| Off-by-one | rank bắt đầu từ 0 thay vì 1 (NDCG, RRF) | #1 |
| Sai dấu / ngưỡng | `>= 0` lẽ ra `>= 0.5`; đảo dấu λ trong MMR | — |
| Quên normalize | cosine trên vector chưa L2-norm | — |
| Thiếu `await` | async lây cả chuỗi, coroutine không chạy | — |
| Parse lỏng | `"yes" in text` bắt nhầm "no ... yes-like" | — |
| Silent failure | quên filter `tenant_id` → rò data, KHÔNG crash | — |
| State/loop guard | thiếu `max_steps`/`attempts` → lặp vô hạn | — |

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
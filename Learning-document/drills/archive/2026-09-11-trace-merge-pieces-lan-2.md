# Trace `merge_pieces` lần 2 — tranh thủ ở công ty (2026-09-11)

> **Trace bằng tay, KHÔNG chạy.** Ghi **giờ bắt đầu / kết thúc** để tối cộng vào sổ giờ.
> Tối gõ lại kết quả (hoặc chụp ảnh giấy) cho Claude chấm. Sai cứ ghi, ô tắc để trống.
> Mục đích: hiểu **vì sao từng dòng tồn tại** — tối nay vẫn có bài viết lại đóng sách để kiểm.

## Code bản thật (chép nguyên văn từ `app/application/chunking/recursive_chunker.py`)

```python
def merge_pieces(pieces: list[str], size:int) -> list[str]:
    merges = []
    current_merge = ""
    for piece in pieces:
        if (len(current_merge) + len(piece) <= size):
            current_merge += piece
        else:
            if current_merge:
                merges.append(current_merge)
            current_merge = piece
    if current_merge:
        merges.append(current_merge)
    return merges
```

Nhắc hai vai: `current_merge` = **thùng đang cầm** · `merges` = **xe chở thùng đã đóng**.

---

## Bài A — `merge_pieces(["Toi", "an", "com"], 5)`

Mỗi hàng = **một dòng code vừa chạy**. Dòng `if`/`else` thì ghi thêm điều kiện ra True hay False.

| # | dòng vừa chạy (nguyên văn) | `piece` | điều kiện → True/False | `current_merge` sau dòng | `merges` sau dòng |
|---|---|---|---|---|---|
| 1 | `merges = []` | — | — | *(chưa có)* | `[]` |
| 2 | `current_merge = ""` | — | — | `""` | `[]` |
| 3 | `if (len(current_merge) + len(piece) <= size):` | `"Toi"` | 0 + 3 <= 5 → True | `""` | `[]` |
| 4 | `current_merge += piece` | `"Toi"` | — | `"Toi"` | `[]` |
| 5 | | `"an"` | | | |
| 6 | | | | | |
| 7 | | `"com"` | | | |
| 8 | | | | | |
| 9 | | | | | |
| 10 | | | | | |
| 11 | *(hết vòng for)* | — | | | |
| 12 | | — | — | | |

**Kết quả `return`:**

⚠️ Hàng 5: để ý dấu `<=` — `3 + 2` bằng đúng `5` thì sao?

---

## Bài B — `merge_pieces(["abcdefghijkl", "xy"], 5)`

Đây là ca làm sáng nay lòi bug. Trace **bản thật** để thấy nó xử lý đúng thế nào.

| # | dòng vừa chạy (nguyên văn) | `piece` | điều kiện → True/False | `current_merge` sau dòng | `merges` sau dòng |
|---|---|---|---|---|---|
| 1 | `merges = []` | — | — | *(chưa có)* | `[]` |
| 2 | `current_merge = ""` | — | — | `""` | `[]` |
| 3 | | `"abcdefghijkl"` | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | `"xy"` | | | |
| 7 | | | | | |
| 8 | *(hết vòng for)* | — | | | |
| 9 | | — | — | | |

**Kết quả `return`:**

---

## Ba câu so sánh — hai con bug sáng nay (trả lời sau khi xong bài B)

1. Nếu **xoá** dòng `if current_merge:` nằm trong `else` (giữ nguyên hai dòng còn lại, lùi `merges.append(current_merge)` ra một nấc) → bài B `return` ra gì? Chuỗi thừa sinh ra ở hàng mấy của bảng?
2. Nếu thụt `current_merge = piece` **vào trong** `if current_merge:` → bài B `return` ra gì? Mẩu nào mất, và mất ở hàng mấy?
3. Một câu cho mỗi dòng:
   - `if current_merge:` trong `else` **chặn** chuyện gì?
   - `current_merge = piece` **vì sao phải luôn chạy**, kể cả khi thùng rỗng?

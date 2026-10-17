# 01 · Recursive chunking

> Phase 0 · code: [`recursive_chunker.py`](../../app/application/chunking/recursive_chunker.py) · phỏng vấn **1.4** (+ 1.1–1.3) ·
> chi tiết + overlap: [algorithms.md § Recursive chunking](../notes/algorithms.md) · ⚠️ `pipeline/05-chunking.md` là bài **cài lỗi cố ý**, đừng học từ đó

## 1. Bài toán

Một văn bản luật dài không nhét vừa một embedding, và một vector cho cả văn bản thì mờ nghĩa.
Phải cắt thành **chunk** ≤ `size` ký tự, nhưng cắt ở **chỗ tự nhiên** (giữa hai đoạn, cuối dòng) thay vì chặt ngang câu.

## 2. Kiến thức — hai bước, không phải một

1. **CẮT** (`split_by_separators`, đệ quy): thử dấu tách **mạnh nhất** trước — `"\n\n"` (giữa hai đoạn) → `"\n"` (xuống dòng) → `" "` (giữa hai từ).
   Mẩu nào **vẫn dài hơn `size`** mới bị cắt tiếp bằng dấu tách **yếu hơn kế tiếp**; mẩu đã đủ ngắn thì giữ nguyên.
2. **GỘP** (`merge_pieces`): sau bước cắt có rất nhiều mẩu vụn. Dồn các mẩu **liền nhau** vào một chunk cho tới khi thêm mẩu kế tiếp sẽ vượt `size`.

- **Đầu vào:** một chuỗi văn bản · `size` · danh sách dấu tách.
- **Đầu ra:** danh sách chunk (danh sách chuỗi), mỗi chunk ≤ `size` (trừ khi một từ đơn đã dài hơn `size`).

## 3. Ví dụ (chạy code thật, `size = 30`)

```
"Điều 1. Phạm vi.\nLuật này quy định về giao thông.\n\nĐiều 2. Đối tượng.\nÁp dụng cho mọi người."
 └──────────── đoạn 1: 49 ký tự ─────────────┘    └──────── đoạn 2: 41 ký tự ────────┘
```

**CẮT** — cả hai đoạn > 30 nên cắt tiếp; đoạn 1 có một dòng vẫn > 30 nên cắt tới mức từng từ → **10 mẩu**:
```
'Điều 1. Phạm vi.\n' | 'Luật ' | 'này ' | 'quy ' | 'định ' | 'về ' | 'giao ' | 'thông.\n\n' | 'Điều 2. Đối tượng.\n' | 'Áp dụng cho mọi người.'
```

**GỘP** → **4 chunk** (độ dài 30 · 21 · 19 · 22):
```
'Điều 1. Phạm vi.\nLuật này quy ' | 'định về giao thông.\n\n' | 'Điều 2. Đối tượng.\n' | 'Áp dụng cho mọi người.'
```

Để ý chunk 1 cắt giữa `quy | định` — gộp chỉ nhìn độ dài, không hiểu cụm từ. Đây là lý do lát 2 có mục **chunk theo Điều/Khoản**.

## 4. Code trong repo

```python
def recursive_chunk(text, size, separators=None):
    if separators is None:
        separators = ["\n\n", "\n", " "]
    pieces = split_by_separators(text, size, separators)   # bước 1: CẮT
    return merge_pieces(pieces, size)                     # bước 2: GỘP

# trong split_by_separators — chỉ mẩu còn quá dài mới đệ quy với dấu tách yếu hơn:
if len(part) > size:
    result.extend(split_by_separators(part, size, separators[1:]))
```

## 5. Hay lẫn

| Đúng | Sai đã gặp |
|---|---|
| kết quả là **danh sách mẩu / chunk** | gọi là "cây" (07/10) — đệ quy nhưng đầu ra phẳng |
| recursive = CẮT **rồi** GỘP | chỉ kể bước cắt |
| `overlap >= size` → không tiến lên được | (bẫy của `fixed_size_chunk`, xem algorithms.md) |

## 6. Tự kiểm — đóng sách

**Phỏng vấn (1.4):** recursive splitter thật gồm **2 bước** — kể ra. Vì sao thiếu bước gộp thì kết quả vô dụng?

<details><summary>▶ Câu mẫu</summary>

"Bước 1 cắt đệ quy: thử cắt ở chỗ cách đoạn trước, mẩu nào còn dài quá size mới cắt tiếp ở xuống dòng, rồi tới khoảng trắng.
Bước 2 gộp: dồn các mẩu liền nhau lại tới gần size.
Thiếu gộp thì ra hàng loạt mẩu vụn như `'về '`, `'quy '` — ví dụ một văn bản 92 ký tự ra 10 mẩu thay vì 4 chunk. Mỗi mẩu thành một vector, kho phình ra, và mẩu tìm được không đủ ngữ cảnh để trả lời."
</details>

**Việc tay:** gõ lại `merge_pieces` đóng sách → `.venv/bin/python -m pytest -q tests/application/chunking`.

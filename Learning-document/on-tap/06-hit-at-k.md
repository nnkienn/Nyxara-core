# 06 · Hit@k

> Lát 1 · code: [`hit_at_k`](../../app/evaluation/metrics.py) · phỏng vấn **12.1** · hay lẫn: [Cặp 24](../notes/the-phan-biet.md), [Cặp 28](../notes/the-phan-biet.md)

## 1. Bài toán

Máy tìm luật trả về một danh sách điều luật. Cần **một con số** cho cả bộ 788 câu hỏi Zalo để biết máy tốt hay tệ,
và để so 2 cấu hình (BM25 vs hybrid). Hit@k trả lời câu đơn giản nhất: **có lọt được điều đúng vào k kết quả đầu không?**

## 2. Kiến thức

- **Đầu vào:** `results` = list các list (mỗi lần tìm một danh sách id) · `answers` = list các list (mỗi lần tìm một danh sách id đúng) · `k`.
- **Một lần tìm** → **0 hoặc 1**: có ít nhất một id đúng nằm trong `results[i][:k]` (k kết quả **đầu**) thì 1.
- **Cả đề** → số lần trúng / **tổng số lần tìm**.
- Ý nghĩa: **đậu / rớt**. Đúng ở vị trí 1 hay vị trí k đều được 1 — Hit@k **không** quan tâm thứ hạng.

## 3. Ví dụ tính tay (bộ số dùng chung cho thẻ 06 · 07 · 08)

```python
results = [["d3", "d1", "d7"],    # lần tìm 0
           ["d2", "d9", "d4"],    # lần tìm 1
           ["d5", "d6", "d8"]]    # lần tìm 2
answers = [["d1"], ["d4", "d2"], ["d0"]]
k = 3
```

| lần tìm | id đúng | có trong top 3? | điểm |
|---|---|---|---|
| 0 | d1 | có (thứ hạng 2) | 1 |
| 1 | d4, d2 | có | 1 |
| 2 | d0 | không | 0 |

**Hit@3 = 2 / 3 = 0.667** (chạy thật: `0.6666…`)

## 4. Code trong repo

```python
for i in range(len(results)):
    top_k = results[i][:k]            # danh sách của RIÊNG lần tìm i, cắt k cái đầu
    for answer in answers[i]:         # từng id đúng của lần tìm i
        if answer in top_k:
            hits = hits + 1
            break                     # trúng một cái là đủ, không đếm 2 lần
return hits / len(results)            # chia TỔNG số lần tìm
```

**Kiểm đầu vào (dùng chung cả 3 metric — phương án A, chốt 16/10):** `_check_inputs` chạy **trước khi chấm câu nào**.
`results` rỗng · `len(results) != len(answers)` · có `answers[i] == []` → `raise ValueError`.
Cái giá: một câu gán nhãn thiếu là **cả lượt đo dừng**, 787 câu tốt cũng không có điểm → sửa dữ liệu, chạy lại.
Đổi lại: **không bao giờ nhận một con số sai mà không hay biết** (không kiểm thì NDCG chia 0, Hit/MRR lặng lẽ tính câu đó là trượt).

## 5. Hay lẫn

| Đúng | Sai đã gặp |
|---|---|
| 1 lần tìm ra **0 hoặc 1** | ra `1/3`, `1/42` (lấy `i` hay `k` làm mẫu số) — Cặp 24 |
| `[:k]` = **k cái đầu** | `[k-1]` = chỉ **cái thứ k** — Cặp 24 |
| tìm chuỗi trong `top_k` (list chuỗi) | `results.index(...)` — `results` chứa **list**, không chứa chuỗi — Cặp 28 |
| `answers[i]` = id đúng của **lần tìm i** | `answers` = cả bộ (lẫn **lần 4** ngày 16/10, bug `if not answers:`) |

## 6. Tự kiểm — đóng sách

**Bài tính:** `results = [["a","b","c"], ["x","y","z"]]`, `answers = [["c"], ["q"]]`. Tính Hit@2 và Hit@3.

<details><summary>▶ Đáp án</summary>

Hit@2: lần 0 top 2 = `["a","b"]` không có `c` → 0 · lần 1 → 0 ⇒ **0/2 = 0**.
Hit@3: lần 0 có `c` → 1 · lần 1 → 0 ⇒ **1/2 = 0.5**.
</details>

**Phỏng vấn (12.1, phần Hit@k):** Hit@k đo gì, và nó **không** thấy được điều gì?

<details><summary>▶ Câu mẫu</summary>

"Hit@k đo tỉ lệ câu hỏi mà ít nhất một văn bản đúng lọt vào k kết quả đầu — mỗi câu là đậu hoặc rớt.
Ví dụ 788 câu Zalo, 600 câu có điều đúng trong top 10 thì Hit@10 = 0.76.
Giới hạn: không phân biệt đúng ở vị trí 1 với vị trí 10, nên cần thêm MRR hoặc NDCG."
</details>

**Việc tay:** mở file trắng, gõ lại `hit_at_k` đóng sách → `.venv/bin/python -m pytest -q tests/evaluation`.

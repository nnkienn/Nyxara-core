# 07 · MRR — Mean Reciprocal Rank

> Lát 1 · code: [`mrr`](../../app/evaluation/metrics.py) · phỏng vấn **12.1** · hay lẫn: [Cặp 26](../notes/the-phan-biet.md)

## 1. Bài toán

Hit@k cho điểm như nhau dù điều đúng đứng **thứ hạng 1** hay **thứ hạng 10**. Người dùng thì chỉ đọc vài kết quả đầu.
MRR thưởng cho việc **đưa văn bản đúng đầu tiên lên càng cao càng tốt**.

## 2. Kiến thức

- **Một lần tìm:** tìm **vị trí của văn bản đúng đầu tiên** trong `top_k`, đổi ra **thứ hạng** (đếm từ 1) → điểm `RR = 1 / thứ hạng`.
  Không có văn bản đúng nào trong top k → `RR = 0`.
- **Cả đề:** cộng mọi `RR` rồi chia **tổng số lần tìm** (kể cả lần trượt).
- Thang điểm 1 lần tìm: thứ hạng 1 → 1 · thứ hạng 2 → 0.5 · thứ hạng 3 → 0.33 · trượt → 0.
- Neo: **Hit@k = đậu/rớt · MRR = đậu được bao nhiêu điểm.**

## 3. Ví dụ tính tay (cùng bộ số thẻ 06)

```python
results = [["d3", "d1", "d7"], ["d2", "d9", "d4"], ["d5", "d6", "d8"]]
answers = [["d1"], ["d4", "d2"], ["d0"]]
k = 3
```

| lần tìm | văn bản đúng đầu tiên trong top 3 | thứ hạng | RR |
|---|---|---|---|
| 0 | d1 | 2 | 1/2 = 0.5 |
| 1 | d2 (đứng trước d4) | 1 | 1/1 = 1.0 |
| 2 | — | — | 0 |

**MRR = (0.5 + 1.0 + 0) / 3 = 0.5** (chạy thật: `0.5`)

## 4. Code trong repo

```python
for i in range(len(results)):
    top_k = results[i][:k]
    for doc in top_k:                       # đi theo THỨ TỰ máy xếp
        if doc in answers[i]:
            rank = top_k.index(doc) + 1     # chỉ số (từ 0) → thứ hạng (từ 1)
            total_rr += 1 / rank
            break                           # chỉ tính văn bản đúng ĐẦU TIÊN
return total_rr / len(results)
```

Vì sao vòng ngoài đi theo `top_k` chứ không theo `answers[i]`: phải gặp văn bản đúng **theo thứ tự máy xếp**
thì cái gặp trước mới là cái đứng cao nhất.

## 5. Hay lẫn

| Đúng | Sai đã gặp |
|---|---|
| `1 / thứ hạng của văn bản đúng` | `1 / k` — mọi câu trúng cùng điểm → MRR thành Hit@k × hằng số — Cặp 26 |
| thứ hạng = chỉ số **+ 1** | dùng chỉ số luôn → hạng 1 thành `1/0` |
| chia **tổng số lần tìm** | chia số lần trúng → 100 câu trượt 99 ra 1.0 thay vì 0.01 |

## 6. Tự kiểm — đóng sách

**Bài tính:** `results = [["a","b","c"], ["x","y","z"]]`, `answers = [["c","a"], ["z"]]`, `k = 3`. MRR = ?

<details><summary>▶ Đáp án</summary>

Lần 0: văn bản đúng đầu tiên theo thứ tự máy là `a` (thứ hạng 1) → 1.0 (không phải `c`).
Lần 1: `z` thứ hạng 3 → 0.333. MRR = (1.0 + 0.333) / 2 = **0.667**.
</details>

**Phỏng vấn:** MRR khác Hit@k chỗ nào? Khi nào MRR vẫn chưa đủ?

<details><summary>▶ Câu mẫu</summary>

"MRR lấy nghịch đảo thứ hạng của văn bản đúng đầu tiên rồi lấy trung bình trên mọi câu hỏi — đúng ở hạng 1 được 1, hạng 2 được 0.5.
Hit@k chỉ đậu/rớt nên không phân biệt hạng 1 với hạng 10.
Giới hạn: MRR chỉ nhìn văn bản đúng **đầu tiên**; câu hỏi cần nhiều điều luật cùng lúc thì các văn bản đúng sau bị bỏ qua — khi đó dùng NDCG."
</details>

**Việc tay:** gõ lại `mrr` đóng sách vào file trắng → chạy `tests/evaluation`.

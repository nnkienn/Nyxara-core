# 08 · NDCG@k

> Lát 1 · code: [`ndcg_at_k`](../../app/evaluation/metrics.py) · phỏng vấn **12.1** · hay lẫn: [Cặp 29](../notes/the-phan-biet.md) ⭐
> Baseline Zalo Legal SOTA: **NDCG@10 = 0.8488**.

## 1. Bài toán

Một câu hỏi luật có thể cần **nhiều điều đúng** (vd `["d4", "d2"]`). MRR chỉ nhìn văn bản đúng đầu tiên.
NDCG chấm **mọi** văn bản đúng trong top k, văn bản nào đứng càng cao càng được nhiều điểm, rồi đưa về thang **0 → 1**
để các câu hỏi có số văn bản đúng khác nhau so được với nhau.

## 2. Kiến thức — 3 đại lượng

| Đại lượng | Tính trên danh sách nào | Là gì |
|---|---|---|
| **DCG** | `results[i][:k]` — danh sách **máy trả về** | cộng `1/log2(thứ hạng + 1)` cho **mỗi** văn bản đúng máy xếp được |
| **IDCG** | **ideal ranking** — dựng **từ `answers[i]`**, mọi văn bản đúng xếp lên thứ hạng 1, 2, 3… | DCG của danh sách hoàn hảo đó = **một tổng**. **Không đọc `results`** |
| **NDCG** | — | `DCG / IDCG`, từ 0 đến **1**. Bằng 1 khi máy xếp hoàn hảo |

Bảng discount (nhớ 3 số): thứ hạng 1 → **1.00** · thứ hạng 2 → **0.63** · thứ hạng 3 → **0.50**.

IDCG chỉ phụ thuộc **số văn bản đúng** (tối đa k): 1 văn bản → 1.00 · 2 → 1.63 · 3 → 2.13.

## 3. Ví dụ tính tay (cùng bộ số thẻ 06)

```python
results = [["d3", "d1", "d7"], ["d2", "d9", "d4"], ["d5", "d6", "d8"]]
answers = [["d1"], ["d4", "d2"], ["d0"]]
k = 3
```

| lần tìm | DCG (máy) | ideal ranking | IDCG | NDCG |
|---|---|---|---|---|
| 0 | d1 hạng 2 → 0.63 | `[d1]` | 1.00 | **0.631** |
| 1 | d2 hạng 1 → 1.00, d4 hạng 3 → 0.50 ⇒ 1.50 | `[d4, d2]` hạng 1, 2 | 1.63 | **0.920** |
| 2 | 0 | `[d0]` | 1.00 | **0** |

**NDCG@3 = (0.631 + 0.920 + 0) / 3 = 0.517** (chạy thật: `0.5168…`)

So với MRR cùng bộ số (0.5): lần tìm 1 MRR cho 1.0 vì d2 đứng đầu, NDCG chỉ cho 0.92 vì d4 bị đẩy xuống hạng 3.

## 4. Code trong repo

```python
dcg = 0
top_k = results[i][:k]
for doc in top_k:
    if doc in answers[i]:
        rank = top_k.index(doc) + 1
        dcg += 1 / math.log2(rank + 1)          # += cộng dồn, KHÔNG phải = gán đè
idcg = 0
ideal_hits = min(len(answers[i]), k)           # ideal ranking dài bao nhiêu (tối đa k)
for rank in range(1, ideal_hits + 1):          # thứ hạng 1 .. ideal_hits
    idcg += 1 / math.log2(rank + 1)
total_ndcg += dcg / idcg
```

`min(..., k)`: có 15 văn bản đúng nhưng k = 10 thì ideal ranking cũng chỉ có 10 ô.

## 5. Hay lẫn

| Đúng | Sai đã gặp |
|---|---|
| ideal ranking dựng **từ `answers`** (cả văn bản máy bỏ sót) | sắp xếp lại `results` cho đẹp → máy trúng 1 cái thì "IDCG = 1" (**4 lần**, Cặp 29) |
| **NDCG** tối đa = 1 | "IDCG = 1" — IDCG chỉ bằng 1 khi có **đúng 1** văn bản đúng |
| `dcg += …` | `dcg = …` — chỉ giữ văn bản đúng cuối cùng (lẫn tổng dồn ↔ gán đè lần 3) |

Vì sao phải dựng từ `answers`: nếu dựng từ `results`, máy bỏ sót văn bản đúng **không bị phạt** — NDCG chỉ còn chấm thứ tự.

## 6. Tự kiểm — đóng sách

**Bài tính 1:** `answers[i] = ["d1","d2","d3"]`, `k = 5`, máy trả `["x","y","z","w","v"]` (trượt hết). DCG, IDCG, NDCG = ?

<details><summary>▶ Đáp án</summary>DCG = 0 · IDCG = 1 + 0.63 + 0.50 = <b>2.13</b> (không đọc <code>results</code>) · NDCG = 0.</details>

**Bài tính 2:** `answers[i] = ["d1","d2"]`, `k = 5`, máy trả `["d2","x","y","z","w"]`. DCG, IDCG, NDCG = ?

<details><summary>▶ Đáp án</summary>DCG = 1.00 (d2 hạng 1) · IDCG = 1 + 0.63 = <b>1.63</b> · NDCG = 1 / 1.63 = 0.61. Máy trúng hạng 1 nhưng bỏ sót d1 → bị phạt.</details>

**Phỏng vấn (12.1):** Hit@k, MRR, NDCG mỗi cái đo gì? Dự án dùng cái nào làm số chính, vì sao?

<details><summary>▶ Câu mẫu</summary>

"Hit@k: có văn bản đúng trong top k không — đậu/rớt. MRR: văn bản đúng đầu tiên đứng cao cỡ nào — 1/thứ hạng.
NDCG: chấm mọi văn bản đúng, đứng càng cao càng nhiều điểm (chia log2 thứ hạng + 1), rồi chia cho điểm của ideal ranking để về 0–1.
Câu hỏi luật Zalo có thể có nhiều điều đúng, và baseline công bố là NDCG@10 = 0.8488, nên NDCG@10 là số chính; Hit@k và MRR đặt cạnh để dễ đọc."
</details>

**Việc tay:** gõ lại `ndcg_at_k` đóng sách (cửa cũ: [drills/ndcg-cua-1610-toi.py](../drills/ndcg-cua-1610-toi.py)) → chạy `tests/evaluation`.

# 05 · Hybrid + RRF (Reciprocal Rank Fusion)

> Phase 2 · code: [`rrf.py`](../../app/application/retrieval/rrf.py) · [`hybrid_retriever.py`](../../app/application/retrieval/hybrid_retriever.py) ·
> phỏng vấn **3.5** · hay lẫn: [Cặp 5](../notes/the-phan-biet.md) (RRF ↔ cross-encoder) · chi tiết: [algorithms.md § RRF](../notes/algorithms.md)

## 1. Bài toán

BM25 bắt **chữ** (thẻ 02), dense bắt **nghĩa**. Dùng cả hai thì có **hai danh sách** — cần trộn thành **một**.
Không cộng thẳng điểm được: cosine nằm trong khoảng **0 → 1**, còn BM25 **không có trần**, câu hỏi càng nhiều chữ khớp thì điểm BM25 càng lớn.

## 2. Kiến thức

- **Đầu vào:** nhiều danh sách id đã xếp hạng (ở đây 2: `dense_ranked`, `bm25_ranked`) · hằng số `k = 60`.
- **Thao tác:** với **mỗi** danh sách, **mỗi** văn bản ở thứ hạng `r` (đếm từ 1) được cộng `1 / (k + r)`. Văn bản không có trong một danh sách thì danh sách đó **không cộng gì**.
- **Đầu ra:** sắp giảm dần theo tổng, cắt `top_k`.
- Chỉ dùng **thứ hạng**, bỏ hẳn điểm gốc → không cần hai nguồn cùng thang đo. Văn bản đứng cao ở **cả hai** nguồn thắng văn bản xuất sắc một nguồn.

## 3. Ví dụ tính tay (chạy `reciprocal_rank_fusion` thật)

```python
dense_ranked = ["doc2", "doc1", "doc3"]   # doc2 hạng 1, doc1 hạng 2, doc3 hạng 3
bm25_ranked  = ["doc1", "doc3", "doc2"]   # doc1 hạng 1, doc3 hạng 2, doc2 hạng 3
```

| doc | dense | BM25 | RRF |
|---|---|---|---|
| doc1 | hạng 2 → 1/62 | hạng 1 → 1/61 | **0.03252** |
| doc2 | hạng 1 → 1/61 | hạng 3 → 1/63 | 0.03227 |
| doc3 | hạng 3 → 1/63 | hạng 2 → 1/62 | 0.03200 |

doc2 đứng **số 1** ở dense vẫn thua doc1 — vì doc1 cao ở **cả hai** nguồn.

**Nếu cộng thẳng điểm gốc thì hỏng thế nào** → tự làm ca P/Q ở **mục 6** trước khi đọc đáp án.

## 4. Code trong repo

```python
scores = {}
for ranked_list in ranked_lists:
    for rank, doc_id in enumerate(ranked_list, start=1):      # start=1: thứ hạng, không phải chỉ số
        scores[doc_id] = scores.get(doc_id, 0.0) + 1 / (k + rank)
ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
```

`HybridRetriever.search`: mỗi nhánh lấy `candidate_k = top_k * 2` ứng viên (cả hai nhánh cùng nhận cây lọc — thẻ 03) → RRF → `top_k`.

## 5. Hay lẫn

| Đúng | Sai đã gặp |
|---|---|
| BM25 **không có trần** — cộng theo số chữ khớp | "BM25 trần 1" (10/10), "trần 2" (15/10) |
| cosine và BM25 **khác thang đo** | "cùng đại lượng" (05/10) |
| mỗi văn bản có **2 điểm riêng** ở 2 nguồn | lấy một điểm cho cả văn bản → kết luận "cosine quyết định" (ca X/Y, 15/10) |
| RRF = trộn **thứ hạng**, rẻ, không đọc nội dung | lẫn với cross-encoder (đọc cặp câu hỏi + văn bản, chấm lại) — Cặp 5 |

## 6. Tự kiểm — đóng sách

**Bài tính:** `dense = ["A", "B"]`, `bm25 = ["C", "A"]`, `k = 60`. Xếp thứ tự RRF.

<details><summary>▶ Đáp án</summary>

A = 1/61 + 1/62 ≈ 0.0325 · B = 1/62 ≈ 0.0161 · C = 1/61 ≈ 0.0164 ⇒ **A > C > B**.
C chỉ có ở BM25 nhưng đứng hạng 1 nên nhỉnh hơn B (hạng 2, chỉ ở dense).
</details>

**Bài P/Q (cộng thẳng điểm gốc):** câu hỏi 6 chữ. Văn bản P khớp cả 6 chữ, mỗi chữ ~1.5 điểm BM25, cosine 0.40.
Văn bản Q khớp 1 chữ (1.5 điểm BM25), cosine 0.98. Nếu cộng thẳng BM25 + cosine thì ai thắng? Nhánh dense còn tiếng nói không?

<details><summary>▶ Đáp án</summary>

P = 9.0 + 0.40 = **9.40** · Q = 1.5 + 0.98 = **2.48** ⇒ P thắng chỉ nhờ BM25.
Cosine tối đa là 1, nên dù Q giống nghĩa hơn hẳn (0.98 vs 0.40) cũng **không bao giờ lật lại được** khoảng cách 7.5 điểm BM25 → BM25 lấn át, nhánh dense thành vô nghĩa.
</details>

**Phỏng vấn (3.5):** RRF gộp kết quả bằng cách nào? Vì sao dùng **thứ hạng** chứ không dùng **điểm số**?

<details><summary>▶ Câu mẫu</summary>

"RRF cộng 1/(60 + thứ hạng) của văn bản ở mỗi danh sách — ví dụ hạng 1 ở BM25 và hạng 2 ở dense được 1/61 + 1/62.
Dùng thứ hạng vì hai nguồn khác thang đo: cosine nằm trong 0–1, BM25 không có trần và tăng theo số chữ khớp; cộng thẳng thì BM25 lấn át, nhánh dense gần như không có tiếng nói.
Giới hạn: RRF bỏ mất độ chênh điểm — hạng 1 bỏ xa hạng 2 hay sát nút đều như nhau — nên sau RRF còn cross-encoder rerank chấm lại."
</details>

**Việc tay:** gõ lại `reciprocal_rank_fusion` đóng sách → `.venv/bin/python -m pytest -q -k rrf`.

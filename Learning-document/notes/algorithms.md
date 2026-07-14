# 🧮 Algorithms — thuật toán, toán & CTDLGT

> Nơi ghi **kiến thức lõi** của mỗi kỹ thuật: công thức, WHY, độ phức tạp, và bài CTDLGT
> ẩn bên trong. Viết lại bằng lời của mình sau khi code tay — nếu chưa giải thích được
> bằng số thật thì **chưa hiểu**, quay lại bước 1.

**Template cho mỗi kỹ thuật:**
```
### <Tên>  ·  Phase <n>  ·  <ngày>
- **Bài toán nó giải:** …
- **Công thức / thuật toán:** … (viết ra, không link đi nơi khác)
- **Ví dụ bằng SỐ THẬT:** … (tự bịa 2–3 số, chạy công thức tay)
- **CTDLGT bên trong:** … (hash map? heap? graph?) + độ phức tạp O(?)
- **Bẫy dễ sai:** … (thường trùng với bug cố ý ở [[bug-log]])
- **Khi nào đáng bật (flag):** …
```

---

## Bảng CTDLGT ↔ kỹ thuật (bản đồ nhanh)

| Cấu trúc | Kỹ thuật RAG | Phase |
|---|---|---|
| Hash map / inverted index | BM25 (term→postings), dedup | 0, 2 |
| Priority queue / heap | top-k, MMR | 2 |
| Sliding window | chunking, context budgeting | 0, 2 |
| Trie / prefix tree | tokenizer, PII matching | 0, 5 |
| Graph (BFS/DFS) | LangGraph state machine, GraphRAG | 2, 4 |
| Quy hoạch động (DP) | edit distance (near-dup dedup) | 0 |
| Two-pointer / merge | RRF (gộp N ranked list) | 2 |

---

## (Điền kiến thức từng kỹ thuật bên dưới khi học — Phase 0 trở đi)

<!--
Ví dụ khi tới Phase 1:
### Cosine similarity  ·  Phase 1  ·  2026-07-xx
- Bài toán: đo độ giống 2 vector bất kể độ dài.
- Công thức: cos(a,b) = (a·b) / (||a||·||b||). Nếu đã L2-normalize → chỉ còn a·b.
- Số thật: a=[1,0], b=[1,1] → dot=1, ||b||=√2 → cos=0.707 (45°). ✓
- CTDLGT: dot product O(d), d=1024 chiều.
- Bẫy: quên normalize → so magnitude thay vì hướng.
-->

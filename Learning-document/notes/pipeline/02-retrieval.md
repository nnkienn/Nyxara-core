# 2️⃣ Retrieval — query → top-k đoạn liên quan (có text)

> Chặng 2. Input: 1 câu hỏi (`query`) + `tenant_id`. Output: vài đoạn text liên quan nhất,
> đã có sẵn nội dung (không chỉ id). File chính: `hybrid_retriever.py` + `reranking_retriever.py`.

---

## Kể chuyện trước

1. `RerankingRetriever.search(tenant_id, query, candidate_k, top_k)` — đây là hàm **CRAG thật
   sự gọi** (không phải `HybridRetriever` trần, xem cảnh báo bên dưới).
2. Bên trong, nó gọi `HybridRetriever.search(...)` trước — chạy **song song 2 nhánh độc lập**:
   - **Dense** (`Qdrant`): embed query → cosine similarity.
   - **Sparse** (`BM25Index`): đếm từ khoá trùng khớp.
3. Gộp 2 danh sách bằng **RRF** (Reciprocal Rank Fusion) — dùng **thứ hạng**, không dùng điểm số
   gốc (cosine và BM25 khác đơn vị, không cộng thẳng được).
4. `RerankingRetriever` tra `DocStore` lấy text thật cho từng candidate, rồi chạy
   **cross-encoder** (`BGEReranker`) chấm điểm chính xác hơn, sort lại, cắt `top_k` cuối.

---

## Sơ đồ đầy đủ — ví dụ query `"mèo đen"`

```
                          query gốc: "mèo đen"
                                  │
              ┌───────────────────┴───────────────────┐
              ▼ (song song, KHÔNG tuần tự)             ▼ (song song, KHÔNG tuần tự)
     NHÁNH DENSE (bi-encoder)                  NHÁNH SPARSE (BM25 — từ khoá,
     ─────────────────────────                  KHÔNG PHẢI ngữ nghĩa)
     BGEEmbedder.embed(["mèo đen"])             ──────────────────────────
       → vector 1024 chiều                      BM25Index.search(tenant_id,
              ▼                                    "mèo đen", candidate_k)
     QdrantStore.search(...) — cosine                     ▼
       so với vector đã lưu sẵn                  tính điểm theo IDF + TF +
              ▼                                  length norm cho từng doc
     dense_hits (có text, score, id)                      ▼
              ▼ chỉ lấy .id (BỎ score)           bm25_hits (doc_id, score)
     dense_ranked = ["doc2","doc1",...]                    ▼ chỉ lấy doc_id (BỎ score)
                                                  bm25_ranked = ["doc1","doc3",...]
              └───────────────────┬───────────────────┘
                                  ▼
              RRF([dense_ranked, bm25_ranked])  ← bước cuối BÊN TRONG HybridRetriever
                  cộng 1/(60+rank) theo từng doc, qua cả 2 danh sách
                                  ▼
              top_k gộp (vd 30-50 ứng viên, đã sort theo điểm RRF)
                                  ▼ chỉ có (doc_id, score) — CHƯA CÓ TEXT
       ┌──────────────────────────────────────────────────────────┐
       │  RerankingRetriever (bọc NGOÀI HybridRetriever):            │
       │  1. doc_store.get(tenant_id, doc_id) cho từng candidate       │
       │     → mới có text thật (Hybrid không giữ text sau RRF)        │
       │  2. CROSS-ENCODER: model đọc chung (query, doc_text) → 1        │
       │     điểm mới. Điểm RRF cũ bị VỨT BỎ hoàn toàn.                  │
       └──────────────────────────────────────────────────────────┘
                                  ▼
                    sort lại theo điểm cross-encoder
                                  ▼
                  top 3-5 cuối cùng → [(doc_id, score), ...]
                  (CRAG lấy text qua doc_store.get() lần nữa ở node.py)
```

---

## ⚠️ Bẫy khi trace: `HybridRetriever` ≠ retriever CRAG thật sự dùng (bug #24)

`node.py::retrieve_node` gọi `retriever.search(tenant_id, query, candidate_k, top_k)` —
**4 tham số**. Đây đúng chữ ký `RerankingRetriever.search`. `HybridRetriever.search` chỉ có
**3 tham số** (`tenant_id, query, top_k` — tự nhân đôi ra `candidate_k` bên trong).

Nếu wiring ở `main.py` lỡ đưa thẳng `HybridRetriever` vào `build_graph(...)` (thay vì bọc qua
`RerankingRetriever`) → `TypeError: search() takes 4 positional arguments but 5 were given`.
**`pytest` không bắt được lỗi này** vì `test_node.py` dùng `FakeRetriever` tự viết đúng 4 tham
số — chỉ lộ khi ghép với `HybridRetriever` thật qua HTTP.

**Đúng phải là:**
```python
hybrid_retriever = HybridRetriever(embedder, vector_store, bm25_index)
retriever = RerankingRetriever(hybrid_retriever, doc_store, BGEReranker())
build_graph(retriever, doc_store, grader, generator)   # truyền RerankingRetriever, không phải Hybrid trần
```

---

## 5 điểm dễ hiểu nhầm (đã tự vấp phải)

1. **Dense và BM25 chạy song song, không tuần tự.** Cả 2 cùng nhận **query gốc**, độc lập nhau.
2. **BM25 = từ khoá, KHÔNG PHẢI ngữ nghĩa.** Ngữ nghĩa là việc của nhánh dense (bi-encoder).
3. **Bi-encoder ≠ (cosine + BM25).** Bi-encoder chỉ là **1 nhánh** (dense). BM25 không có model.
4. **Cả dense lẫn BM25 đều tự có điểm riêng — nhưng cả 2 điểm đó bị bỏ trước khi vào RRF.** RRF
   chỉ dùng **thứ hạng**, vì cosine (0-1) và BM25 (không giới hạn) khác đơn vị.
5. **Cross-encoder không chạy trên toàn kho**, chỉ chạy trên tập đã lọc (30-50 ứng viên) — chạy
   trên toàn kho không khả thi (phải nhét `(query, 1 doc)` làm 1 input, lặp lại từng doc).

## Vì sao 2 tầng (rẻ → đắt)

| Tầng | Đặc điểm | Vai trò |
|---|---|---|
| Dense + BM25 + RRF | Rẻ, pre-compute được (dense) hoặc tra O(1) (BM25) | Lọc **rộng** từ toàn kho |
| Cross-encoder | Đắt, chạy model cho **từng cặp** (query, doc) | Chấm **hẹp, chính xác** trên tập đã lọc |

---

**Tiếp theo:** [03-crag.md](./03-crag.md) — top-k đoạn này được LLM chấm điểm và dùng để trả lời
như thế nào, kể cả khi kết quả retrieval đầu tiên tệ.

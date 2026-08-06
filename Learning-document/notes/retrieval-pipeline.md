# 🗺️ Retrieval Pipeline — bức tranh toàn cảnh Phase 2

> Sơ đồ tổng hợp sau khi xong Phase 2.1 (BM25 + RRF + HybridRetriever), trước khi vào
> Phase 2.2 (Cross-encoder Rerank). Xem chi tiết công thức/CTDLGT từng kỹ thuật ở
> [algorithms.md](./algorithms.md) — file này chỉ vẽ lại **thứ tự** và **vì sao** mỗi bước
> tồn tại, không lặp lại công thức.

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
              top_k gộp (ví dụ 30-50 ứng viên, đã sort theo điểm RRF)
                                  ▼
       ┌──────────────────────────────────────────────────────────┐
       │  CROSS-ENCODER (Phase 2.2) — với TỪNG doc trong 30-50 đó:  │
       │  model đọc chung (query="mèo đen", doc_text) → 1 điểm mới  │
       │  điểm RRF cũ bị VỨT BỎ hoàn toàn, thay hẳn bằng điểm này    │
       └──────────────────────────────────────────────────────────┘
                                  ▼
                    sort lại theo điểm cross-encoder
                                  ▼
                  top 3-5 cuối cùng → đưa cho LLM/agent trả lời
```

---

## 5 điểm dễ hiểu nhầm (đã tự vấp phải, ghi lại để không lặp)

1. **Dense và BM25 chạy song song, không tuần tự.** Cả 2 cùng nhận **query gốc**, độc lập
   hoàn toàn với nhau — BM25 không "nhận lại" gì từ kết quả của dense.

2. **BM25 = từ khoá, KHÔNG PHẢI ngữ nghĩa.** Ngữ nghĩa là việc của nhánh dense (bi-encoder).
   Đây là chỗ đã nhầm 2 lần trong quá trình học — nhầm vì cả 2 đều "tìm tài liệu liên quan",
   nhưng cơ chế bên trong khác hẳn nhau (đếm chữ trùng vs hiểu nghĩa qua vector).

3. **Bi-encoder ≠ (cosine + BM25).** Bi-encoder chỉ là **1 nhánh** (dense) — `BGEEmbedder` +
   cosine. BM25 không phải "encoder" gì cả vì nó không có model, chỉ có công thức thống kê.

4. **Cả dense lẫn BM25 đều tự có điểm số riêng (cosine, BM25 score) — nhưng cả 2 điểm đó
   đều bị bỏ đi trước khi vào RRF.** RRF chỉ dùng **thứ hạng** (rank/vị trí), không dùng điểm
   gốc — vì cosine (0-1) và BM25 (không giới hạn) khác đơn vị, không cộng thẳng được.

5. **Cross-encoder không chạy trên toàn kho, chỉ chạy trên tập đã lọc từ HybridRetriever**
   (ví dụ 30-50 ứng viên, không phải 10,000 doc gốc) — vì mỗi lần chạy phải nhét
   `(query, 1 doc)` làm 1 input, lặp lại cho từng doc, rất chậm nếu làm trên toàn kho.

---

## Vì sao 2 tầng (rẻ → đắt), không dùng cross-encoder ngay từ đầu

| Tầng | Đặc điểm | Vai trò |
|---|---|---|
| Dense + BM25 + RRF | Rẻ, có thể pre-compute (dense) hoặc tra cứu O(1) (BM25) | Lọc **rộng**, từ toàn kho xuống còn vài chục ứng viên |
| Cross-encoder | Đắt, phải chạy model cho **từng cặp** (query, doc), không pre-compute được | Chấm **hẹp và chính xác** trên tập đã lọc |

Bỏ qua tầng rẻ sẽ buộc cross-encoder chạy trên toàn kho — không khả thi ở quy mô thật.

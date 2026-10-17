# 04 · Port / adapter (kiến trúc hexagonal)

> Nền từ Phase 1, chốt lại ở lát 0 (X3, 02/10) · code: port [`vector_store.py`](../../app/domain/ports/vector_store.py) ·
> adapter [`qdrant_store.py`](../../app/infrastructure/adapters/vectorstore/qdrant_store.py) · người dùng port: [`hybrid_retriever.py`](../../app/application/retrieval/hybrid_retriever.py) ·
> phỏng vấn **10.11** + **10.10** · hay lẫn: [Cặp 23](../notes/the-phan-biet.md) · kiến trúc: [design-system.md](../notes/design-system.md)

## 1. Bài toán

Phần lõi (`HybridRetriever`, RRF, metric…) không được dính chặt vào Qdrant. Mai đổi sang Postgres (`PgVectorStore`, lát 6)
thì chỉ **thêm một file**, không sửa lõi. Viết test cho lõi cũng không cần bật Qdrant thật.

## 2. Kiến thức

- **Port** = bản hợp đồng do **lõi** đặt ra, viết bằng ngôn ngữ của lõi: "tôi cần một thứ có `search(tenant_id, query_vector, top_k, filter_tree)` trả về `list[SearchHit]`".
  Ở đây: `VectorStore` (một `Protocol`) trong `app/domain/ports/`.
- **Adapter** = lớp cắm một công nghệ cụ thể vào port, **dịch hai chiều**:
  - **chiều xuống:** cây trung lập → `Filter` của Qdrant (`to_qdrant_filter`), gọi `client.query_points(...)`.
  - **chiều lên:** kết quả thô của Qdrant (`hit.payload`, `hit.score`) → `SearchHit(id, text, score)` của lõi.
  Ở đây: `QdrantStore` trong `app/infrastructure/adapters/vectorstore/`.
- Chiều phụ thuộc: `domain/ports` ← `application` ← `infrastructure/adapters` ← `presentation`. Lõi **không import** Qdrant.

## 3. Ví dụ — một lần gọi đi qua port

```
HybridRetriever (lõi)
   │  self.vector_store.search("congty_A", vector, 10, {"eq": ["loai", "Nghị định"]})   ← chỉ biết VectorStore
   ▼
QdrantStore (adapter)
   │  to_qdrant_filter(cây) → Filter(must=[tenant, Filter(...)]) → client.query_points(...)
   ▼
Qdrant trả về points (payload, score)
   │  adapter đổi mỗi point → SearchHit(id="ND100_2019_d5", text="...", score=0.83)
   ▼
HybridRetriever nhận list[SearchHit] — không biết Qdrant tồn tại
```

Đổi database = **thêm** `PgVectorStore` cũng có `search(...)` trả `list[SearchHit]`; `HybridRetriever` giữ nguyên.
Test lõi = truyền `FakeVectorStore` (vd [test_hybrid_retriever.py](../../tests/application/retrieval/test_hybrid_retriever.py)) — nhanh, không cần Qdrant.
Cái giá: thêm một tầng file + phải giữ fake khớp hành vi kho thật.

## 4. Code trong repo

```python
class VectorStore(Protocol):                    # domain/ports — PORT
    def search(self, tenant_id: str, query_vector: list[float], top_k: int,
               filter_tree: Optional[dict] = None) -> list[SearchHit]: ...

# infrastructure/adapters — ADAPTER, chiều lên:
return [SearchHit(id=hit.payload["doc_id"], text=hit.payload["text"], score=hit.score) for hit in res]
```

## 5. Hay lẫn

| Đúng | Sai đã gặp |
|---|---|
| port nhận **cây trung lập**, mỗi adapter tự dịch | port nhận dict Qdrant đã dịch sẵn (10.10) |
| câu 10.10 hỏi **dạng dữ liệu chuyền giữa hai nhánh** | trả lời "lọc trước cắt sau" — đó là **thứ tự trong một nhánh** (Cặp 23) |
| trả lời 10.11 **mở đầu bằng ví dụ** `VectorStore` / `QdrantStore` / `query_points` / `SearchHit` | chỉ nói định nghĩa chung, thiếu ví dụ (2 lần) |

## 6. Tự kiểm — đóng sách

**Phỏng vấn (10.11):** port là gì, adapter là gì? Lấy `VectorStore` / `QdrantStore` làm ví dụ.

<details><summary>▶ Câu mẫu</summary>

"Port là hợp đồng do lõi đặt ra, ví dụ `VectorStore.search` nhận tenant, vector, top_k, cây lọc và trả `list[SearchHit]`.
Adapter là lớp cắm công nghệ thật vào hợp đồng đó, ví dụ `QdrantStore`: nó dịch cây lọc sang `Filter` của Qdrant, gọi `query_points`, rồi dịch từng kết quả của Qdrant ngược lên thành `SearchHit`.
Lợi ích: đổi sang Postgres chỉ thêm `PgVectorStore`, lõi không sửa; test lõi bằng fake không cần Qdrant. Cái giá là thêm một tầng và phải giữ fake giống kho thật."
</details>

**Phỏng vấn (10.10):** sao không để `HybridRetriever` dịch luôn sang dict Qdrant rồi truyền xuống `VectorStore.search`? Nêu 2 hậu quả.

<details><summary>▶ Câu mẫu</summary>

"(a) BM25: nhánh BM25 cũng cần cây đó, mà nó không hiểu dict Qdrant — phải viết thêm bộ dịch ngược, hai bộ dịch lệch nhau là lọc sai im lặng.
(b) Đổi database: cú pháp Qdrant nằm trong `HybridRetriever` ở lõi, nên đổi sang Postgres phải **sửa `HybridRetriever`**, và `PgVectorStore` lại phải đọc cú pháp Qdrant. Nhận cây trung lập thì chỉ cần thêm một adapter."
</details>

**Việc tay:** viết một `FakeVectorStore` 5 dòng trả cứng 2 `SearchHit`, truyền vào `HybridRetriever`, in kết quả `search`.

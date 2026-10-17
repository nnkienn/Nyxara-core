# 03 · Metadata filter + tenant

> Lát 0 (đã đóng 06/10) · code: [`metadata_filter.py`](../../app/application/retrieval/metadata_filter.py) (CHẤM) ·
> [`qdrant_filter.py`](../../app/infrastructure/adapters/vectorstore/qdrant_filter.py) (DỊCH) · [`qdrant_store.py`](../../app/infrastructure/adapters/vectorstore/qdrant_store.py) ·
> phỏng vấn **3.9** + "vì sao chuyền cây xuống **cả hai** nhánh" · hay lẫn: [Cặp 22](../notes/the-phan-biet.md), [Cặp 23](../notes/the-phan-biet.md), [Cặp 15](../notes/the-phan-biet.md)

## 1. Bài toán

Người dùng hỏi *"phạt vượt đèn đỏ — chỉ lấy **Nghị định** từ **2015** trở đi"*. Phải loại văn bản sai loại / quá cũ
ở **cả hai** nhánh tìm kiếm, và không bao giờ để văn bản của **công ty khác** (tenant khác) lọt vào.

## 2. Kiến thức

**Cây trung lập** — một dạng chung, không thuộc về Qdrant hay BM25:
```python
{"and": [{"eq": ["loai", "Nghị định"]}, {"gte": ["nam", 2015]}]}    # lá = {phép: [trường, giá trị]}
```

| | `to_qdrant_filter(cây)` — **DỊCH** | `matches(cây, metadata)` — **CHẤM** |
|---|---|---|
| nằm ở | `infrastructure/adapters/` (biết cú pháp Qdrant) | `application/retrieval/` (core) |
| cần metadata văn bản? | **không** — chỉ viết lại câu hỏi | **có** — trả lời trên 1 văn bản |
| trả ra | dict `{"must": [...]}` gửi Qdrant | **một** `True` / `False` |
| dùng ở nhánh | dense (Qdrant) — **pre-filter**: Qdrant lọc trong lúc tìm | BM25 — **post-filter**: chấm điểm xong, lọc, **rồi mới** cắt `top_k` |

**Tenant — hai nhánh, hai cơ chế khác nhau:**
- **Qdrant = lọc thật:** `must = [tenant_id == …, Filter(cây)]` — khoá tenant **luôn ở ngoài cùng**, cây người dùng chỉ được **lồng vào trong** cạnh nó → không cây nào nới được khoá tenant.
- **BM25 = phân vùng:** `self.index[tenant_id]` — văn bản tenant khác không nằm trong vùng được duyệt; `doc_count` và IDF cũng tính **riêng** từng tenant.

## 3. Ví dụ (chạy code thật)

```python
to_qdrant_filter(cây)
# {'must': [{'key': 'loai', 'match': {'value': 'Nghị định'}}, {'key': 'nam', 'range': {'gte': 2015}}]}

matches(cây, {"loai": "Nghị định", "nam": 2020})   # True
matches(cây, {"loai": "Thông tư",  "nam": 2020})   # False — sai loại
matches(cây, {"nam": 2020})                        # False — thiếu trường "loai" → lá False (khớp cách Qdrant làm)
```

**Vì sao phải chuyền cây xuống CẢ HAI nhánh** — giả sử cấm `ND100_2019` nhưng chỉ Qdrant lọc:
nhánh BM25 vẫn trả `ND100_2019` → RRF trộn hai danh sách → văn bản bị cấm **lọt lại vào top** mà không báo lỗi gì.

**Vì sao không lọc một lần SAU RRF:** RRF đã cắt `top_k` rồi mới lọc → nếu top 5 toàn nghị định cũ, lọc `nam >= 2015` ra **0** kết quả,
dù trong kho có văn bản đạt điều kiện ở hạng 6, 7… (cắt trước, lọc sau = **thiếu**). Cùng lý do đó, trong BM25 phải **lọc trước, cắt sau**.

## 4. Code trong repo

```python
# hybrid_retriever.py — cùng một cây đi xuống cả hai nhánh
dense_hits = self.vector_store.search(tenant_id, query_vector, candidate_k, filter_tree)
bm25_hits  = self.bm25_index.search(tenant_id, query, candidate_k, filter_tree)

# qdrant_store.py — tenant ngoài cùng, cây lồng trong
conditions = [FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))]
if filter_tree is not None:
    conditions.append(Filter(**to_qdrant_filter(filter_tree)))
filter = Filter(must=conditions)
```

## 5. Hay lẫn

| Đúng | Sai đã gặp |
|---|---|
| `matches` trả **bool** | chép `to_and_clause` sang → ra `{'must': [True, False]}` (Cặp 22) |
| file có cú pháp Qdrant/Elastic → `infrastructure/adapters/` | đặt bộ dịch Elastic vào `metadata_filter.py` / core (Cặp 22, 16/10) |
| `must_not` = **loại ra** | "ngăn chọn ra" |
| tenant Qdrant = lọc · BM25 = **phân vùng** | "cùng một cơ chế" (3.9 ❌ nhiều lần) |
| chuyền cây để **văn bản bị cấm không lọt vào** | "vì BM25 giỏi khớp chính xác" — lẫn giá trị của nhánh BM25 với việc lọc nhánh BM25 |

## 6. Tự kiểm — đóng sách

**Bài:** cây `{"or": [{"eq": ["co_quan", "Bộ Tài chính"]}, {"lt": ["nam", 2010]}]}`, văn bản `{"co_quan": "Bộ Y tế", "nam": 2005}`. `matches` ra gì? `to_qdrant_filter` ra dict có khoá ngoài cùng nào?

<details><summary>▶ Đáp án</summary>

`matches` → **True** (lá thứ hai `2005 < 2010` đúng, `or` chỉ cần một). `to_qdrant_filter` → `{"should": [...]}`.
</details>

**Phỏng vấn (3.9):** `tenant_id` chặn tài liệu tenant khác — ở nhánh Qdrant và nhánh BM25 có cùng một cơ chế không? Nêu tên file.

<details><summary>▶ Câu mẫu</summary>

"Không. Ở Qdrant là **lọc thật**: `qdrant_store.search` luôn đặt điều kiện `tenant_id` trong `must` ngoài cùng, cây lọc của người dùng lồng vào trong cạnh nó nên không nới được.
Ở BM25 là **phân vùng**: `bm25_index.py` lưu `self.index[tenant_id][term]`, tenant là khoá ngoài cùng nên văn bản tenant khác không bao giờ được duyệt, IDF cũng tính riêng.
Nếu BM25 làm kiểu chấm hết rồi mới lọc tenant thì tốn công, IDF lẫn giữa các tenant, và lọc sau khi cắt `top_k` có thể ra rỗng."
</details>

**Phỏng vấn:** vì sao `HybridRetriever` chuyền cây xuống **cả hai** nhánh, không lọc một lần sau RRF?

<details><summary>▶ Câu mẫu</summary>

"Ý 1: lọc một nhánh thì nhánh kia vẫn trả văn bản bị cấm, RRF trộn lại là nó lọt vào top mà không ai biết.
Ý 2: lọc sau RRF là cắt top_k trước rồi mới lọc — văn bản đạt điều kiện ở hạng thấp đã bị cắt, kết quả thiếu, có khi bằng 0."
</details>

**Việc tay:** gõ lại `matches` (cây 1 tầng) vào file trắng đóng sách → `.venv/bin/python -m pytest -q -k leaf`.

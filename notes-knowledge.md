# RAG Knowledge Notes — Phase 2 & 3

---

## Phase 2 — Vector Embedding & Search

### 1. Vector Embedding

Vector embedding là quá trình ánh xạ text từ không gian token rời rạc sang **không gian vector liên tục** có số chiều cố định — 1024 chiều với `bge-m3`.

Model `bge-m3` được pre-train bằng **contrastive learning** trên hàng tỷ cặp câu đa ngôn ngữ:
- **Objective:** minimize khoảng cách vector của cặp câu cùng nghĩa, maximize khoảng cách của cặp câu khác nghĩa
- **Kết quả:** text có ngữ nghĩa tương đồng → vector nằm gần nhau trong không gian 1024 chiều

> **Không phải hash** — embedding là *learned representation* từ data, không phải tính toán deterministic.

---

### 2. Cosine Similarity

```
cos(θ) = (A · B) / (‖A‖ × ‖B‖)
```

Đo **góc** giữa 2 vector, không đo khoảng cách vật lý.

| Giá trị | Ý nghĩa |
|---------|---------|
| `cos = 1.0` | Cùng hướng = cùng ngữ nghĩa |
| `cos = 0.0` | Vuông góc = không liên quan |
| `cos = -1.0` | Ngược hướng = nghĩa đối lập |

**Tại sao không dùng Euclidean distance?**
Euclidean đo khoảng cách đầu-đến-đầu → doc ngắn và doc dài về cùng chủ đề bị coi là khác nhau vì magnitude khác nhau. Cosine **invariant với magnitude** — chỉ quan tâm hướng.

Vì `bge-m3` trả về **L2-normalized vectors** (`‖A‖ = 1`), cosine rút gọn thành dot product:

```
cos(θ) = A · B = Σ(aᵢ × bᵢ)
```

---

### 3. Tenant Isolation

**Single-collection multi-tenancy:** tất cả tenants lưu chung collection `"chunks"`, phân biệt bằng payload field `tenant_id`.

`tenant_id` filter được **enforce tại tầng infrastructure** tại mọi search operation.

> **Nếu bỏ filter:** query của tenant A trả về documents của tenant B — **silent failure**: không có exception, không có lỗi runtime, chỉ là sai data âm thầm.

---

## Phase 3 — BM25, RRF, Hybrid Search

### 4. TF và IDF

| Khái niệm | Định nghĩa | Phạm vi |
|-----------|-----------|---------|
| **TF** (Term Frequency) | Số lần một term xuất hiện trong **1 document cụ thể** | Per document |
| **IDF** (Inverse Document Frequency) | Độ hiếm của term trên **toàn bộ corpus N docs** | Toàn corpus |

```
IDF(t) = log((N - df + 0.5) / (df + 0.5) + 1)
```

- `N` = tổng số docs trong corpus
- `df` = số docs chứa term đó
- Term càng hiếm → df nhỏ → IDF càng cao → càng quan trọng

**TF-IDF = TF × IDF** — term vừa xuất hiện nhiều trong doc này, vừa hiếm trong corpus → score cao.

---

### 5. Vấn đề của TF-IDF → tại sao cần BM25

**Vấn đề 1 — TF không có saturation:**

Doc A: term xuất hiện 2 lần → score = 2 × IDF
Doc B: term xuất hiện 100 lần → score = 100 × IDF **(cao hơn 50×)**

Nhưng thực tế B không relevant hơn A 50×. TF-IDF không biết điều đó.

**Vấn đề 2 — Không chuẩn hóa theo độ dài doc:**

Doc dài 1000 từ tự nhiên có TF cao hơn doc ngắn 10 từ cho cùng 1 term — không công bằng.

---

### 6. BM25 — Okapi BM25 (Robertson et al. 1994)

```
score(d, t) = IDF(t) × [ TF(t,d) × (k1 + 1) ] / [ TF(t,d) + k1 × (1 - b + b × dl/avgdl) ]
```

#### Tham số k1 = 1.5 — TF saturation

Kiểm soát tốc độ tăng của score khi TF tăng. Khi TF → ∞, score **tiệm cận giới hạn `(k1+1)`** — không tăng mãi như TF-IDF.

| Giá trị | Hành vi |
|---------|---------|
| `k1 = 0` | TF không ảnh hưởng, chỉ IDF quyết định |
| `k1 → ∞` | Trở về TF-IDF thuần, không có saturation |
| `k1 = 1.5` | Tiêu chuẩn — TF có ảnh hưởng nhưng bị cap lại |

#### Tham số b = 0.75 — length normalization

`dl/avgdl` = tỉ lệ độ dài doc so với trung bình corpus.
- Doc ngắn hơn trung bình (`dl/avgdl < 1`) → TF được boost
- Doc dài hơn trung bình (`dl/avgdl > 1`) → TF bị penalize

| Giá trị | Hành vi |
|---------|---------|
| `b = 0` | Bỏ qua độ dài doc hoàn toàn |
| `b = 1` | Chuẩn hóa tối đa |
| `b = 0.75` | Tiêu chuẩn — chuẩn hóa một phần |

---

### 7. RRF — Reciprocal Rank Fusion (Cormack et al. 2009)

```
RRF(d) = Σᵢ  1 / (k + rankᵢ(d))
```

**Tại sao không cộng điểm BM25 và cosine trực tiếp?**

| Metric | Range |
|--------|-------|
| Cosine similarity | `[0, 1]` — bounded |
| BM25 score | `[0, ∞)` — unbounded, phụ thuộc corpus |

Không cùng đơn vị đo → cộng trực tiếp không có ý nghĩa toán học.

**RRF chuyển cả 2 list về rank** (thứ hạng 1, 2, 3...) → **scale-invariant**.
Doc xuất hiện cao trong nhiều list → RRF score cao → được chọn.

**`k = 60`** (từ paper gốc): hằng số damping, làm mờ ưu thế của rank 1 so với rank 2 → kết quả ổn định hơn.

---

### 8. HybridRetriever — Flow

```
query
  ├─→ embedder.embed([query])              → query_vector (1024 floats)
  │       └─→ Qdrant cosine search (2k)   → dense_ranked  [id1, id2, ...]
  │
  ├─→ BM25.search(query, tenant_id) (2k)  → bm25_ranked   [id3, id1, ...]
  │
  └─→ RRF([dense_ranked, bm25_ranked])    → top_k RetrievalHit
```

> `top_k * 2` ở bước search để RRF có đủ candidates để so sánh, sau đó cắt về `top_k` sau fusion.

---

### 9. Hexagonal Architecture

```
domain/ports/           ← định nghĩa WHAT: Protocol + dataclass (không import gì từ infra)
application/services/   ← USE CASE: dùng ports, không biết implementation
infrastructure/         ← triển khai THẬT: Qdrant, bge-m3
```

`RetrieverPort` là `Protocol` (structural typing) — bất kỳ class nào có đúng method signature đều satisfy port **mà không cần kế thừa**. Cho phép swap implementation (HybridRetriever → MockRetriever trong test) mà không thay đổi caller.

---

## Quick Reference — Công thức

```
# Cosine Similarity (L2-normalized vectors)
cos(θ) = A · B = Σ(aᵢ × bᵢ)

# TF-IDF
score(d, t) = TF(t, d) × log(N / df(t))

# IDF (BM25 variant)
IDF(t) = log((N - df + 0.5) / (df + 0.5) + 1)

# BM25
score(d, t) = IDF(t) × TF×(k1+1) / (TF + k1×(1 - b + b×dl/avgdl))

# RRF
RRF(d) = Σᵢ  1 / (k + rankᵢ(d))     # k=60
```

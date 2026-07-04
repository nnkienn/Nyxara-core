# RAG Knowledge Notes — Phase 2 & 3
> Ghi lại WHY (tại sao code như vậy), không chỉ WHAT.
> Mỗi bước code = 1 section. Quiz sai → ghi thêm vào đây.
> Gặp thuật ngữ mới → thêm vào phần Glossary cuối file.

---

## Phase 2 — Vector Embedding & Storage

### Bước 1 — `domain/ports/embedder.py`

```python
class Embedder(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...
```

**WHY batch `list[str]` → `list[list[float]]`:**
GPU xử lý song song. Ingest 1000 chunks mà gọi 1 lần từng text → chậm 10-50×. Gửi cả batch → GPU xử lý cùng lúc.

**WHY `Protocol` không phải `ABC`:**
Structural typing — class nào có đúng method `embed` là satisfy, không cần kế thừa. Swap `BGEEmbedder` → `MockEmbedder` trong test mà không chạm application layer.

**Quiz đã sai:**
- "L2-normalize để stable neuron" → SAI. Để cosine similarity = dot product. Qdrant tính cosine bằng dot product bên trong — chỉ đúng khi vector là unit vector (‖v‖ = 1).

---

### Bước 2 — `domain/ports/vector_store.py`

```python
@dataclass
class VectorSearchResult:
    id: str       # UUID5 — để lookup sau RRF
    score: float  # cosine similarity [0, 1]
    payload: dict # {"text": ..., "source": ..., "tenant_id": ...}

class VectorStore(Protocol):
    def ensure_collection(self, name: str, dim: int) -> None: ...
    def upsert(self, collection: str, vectors: list[list[float]], payloads: list[dict]) -> int: ...
    def search(self, collection: str, vector: list[float], *, tenant_id: str, top_k: int = 5) -> list[VectorSearchResult]: ...
```

**WHY `VectorSearchResult` không phải `RetrievalHit`:**
VectorStore là raw DB result — có `payload: dict` chưa có cấu trúc. `HybridRetriever` mới transform thành `RetrievalHit` sau RRF.

**WHY `payload: dict` không phải field cụ thể:**
VectorStore là domain port — không được biết application layer lưu gì. Hôm nay `{"text", "source"}`, mai thêm `{"language", "sentiment"}`. Hardcode field → phải sửa port mỗi lần (vi phạm Open/Closed).

**WHY `upsert()` trả `int`:**
Caller biết lưu được bao nhiêu chunks. `None` → không debug được khi ingest 0 chunk.

**WHY `*` trước `tenant_id`:**
Keyword-only → bắt buộc gọi rõ tên. `tenant_id` sai = data leak giữa tenants — security bug, không phải logic bug.

**WHY `ensure_collection(dim=1024)` phải đúng:**
Qdrant dùng `dim` để tạo HNSW index. Upsert vector sai dim → **Qdrant throw error ngay**, không phải "mất thông tin".

**WHY `search()` nhận 1 vector, không phải batch:**
User chỉ có 1 query tại 1 thời điểm. `embed()` nhận batch vì ingest nhiều chunk cùng lúc. Khác use case.

**Quiz đã sai:**
- "vectors là chunk băm ra" → SAI. `băm = hash` (deterministic, mất thông tin). Vector là **embedding** — learned representation, giữ ngữ nghĩa.
- "search nhận 1 vector để tránh loãng" → SAI. Vì user chỉ có 1 query tại 1 thời điểm.

---

### Bước 3 — `infrastructure/adapters/embedder/bge_embedder.py`

```python
from FlagEmbedding import FlagModel

class BGEEmbedder:
    def __init__(self, model_name: str = "BAAI/bge-m3") -> None:
        self._model = FlagModel(model_name, use_fp16=True)

    async def embed(self, texts: list[str]) -> list[list[float]]:
        vecs = self._model.encode(texts, normalize_embeddings=True)
        return vecs.tolist()
```

**WHY `use_fp16=True`:**
Float16 thay float32 → nửa RAM, nhanh hơn ~2×. Độ chính xác embedding gần như không đổi.

**WHY `normalize_embeddings=True`:**
L2-normalize → `‖v‖ = 1` → cosine similarity = dot product → Qdrant tính nhanh hơn, kết quả ổn định.

**WHY không kế thừa `Embedder`:**
`Embedder` là `Protocol` — structural typing. Có method `embed()` đúng signature là tự động satisfy. Không cần `class BGEEmbedder(Embedder)`.

---

### Bước 4 — `infrastructure/adapters/vectorstore/qdrant_store.py`

```python
id=str(uuid.uuid5(uuid.NAMESPACE_DNS, p.get("text","") + p.get("tenant_id","")))
```

**WHY ghép `text + tenant_id` không phải chỉ `text`:**
Cùng chunk "kem dưỡng da" có thể tồn tại ở 2 tenant. Chỉ dùng `text` → cùng UUID → tenant B upsert ghi đè data tenant A. Ghép `text + tenant_id` → UUID unique theo (nội dung, tenant).

**WHY `ensure_collection` check trước:**
Qdrant throw error nếu `create_collection()` khi collection đã tồn tại. Check `if name not in existing` để tránh crash.

**WHY filter `tenant_id` trước cosine (pre-filtering):**
Qdrant lọc tenant trước → chỉ tính cosine trên tập đã lọc → nhanh hơn nhiều. Filter sau = tính cosine toàn bộ mọi tenant → tốn tài nguyên vô ích.

**Quiz đã sai:**
- "ghép text+tenant_id vì uuid5 chứa namespace" → SAI. Vì cùng text tồn tại nhiều tenant.
- "bỏ check → duplicate vector" → SAI. Qdrant throw error crash chương trình.
- "filter chạy sau cosine" → SAI. Pre-filtering chạy TRƯỚC.

---

### Bước 5 — `application/ingestion/service.py` (IngestionService)

**Flow:**
```
load JSON → chunk_text() → [texts, payloads] → embed(batch) → ensure_collection → upsert → return count
```

**WHY guard `if not texts: return 0` trước embed:**
Nếu bỏ → `embed([])` trả `[]` → `len(vectors[0])` crash **IndexError** vì list rỗng không có `[0]`. Guard tránh crash, tránh gọi model vô ích.

**WHY `dim=len(vectors[0])` không hardcode `1024`:**
Đổi model từ bge-m3 (1024) sang model khác (768) → không cần sửa IngestionService. Hardcode → phải nhớ sửa mỗi lần đổi model.

**WHY DI (Dependency Injection) — ai quyết định inject gì:**
`main.py` (production) inject `BGEEmbedder + QdrantStore`. Test inject `MockEmbedder + MockStore`. `IngestionService` không biết đang dùng thật hay giả → dễ test, dễ swap.

**WHY `async def ingest_file`:**
Gọi `await embed()` bên trong → function cha phải `async`. async "lây" lên trên.

**Quiz đã sai:**
- "bỏ guard → tạo vector rỗng" → SAI. Crash IndexError tại `vectors[0]` vì list rỗng.
- "dim hardcode không sao" → SAI. Đổi model phải sửa tay, dễ quên.
- "không biết ai inject" → Composition Root: `main.py` hoặc test file quyết định.

---

### Bước 6 — `application/retrieval/bm25_index.py`

**Flow:** `add(doc)` → lưu tokens → `search(query)` → tính BM25 score từng doc → sort → top_k

**WHY `field(default_factory=list)`:**
`_docs: list = []` → mọi instance share cùng 1 list (Python trap). `default_factory` tạo list mới cho mỗi instance.

**WHY tokenize nhất quán `add()` và `search()`:**
`add()` lưu `"kem"` (lowercase). `search()` không `.lower()` → tìm `"KEM"` → `tf=0` → score=0 → không tìm thấy gì dù data đầy đủ.

**WHY `if not tenant_docs: return []`:**
`avgdl = sum(...) / len(tenant_docs)` → nếu rỗng → ZeroDivisionError.

**WHY TF × IDF, không chỉ TF hoặc IDF:**
- Chỉ TF → doc có từ "là" nhiều nhất thắng (từ phổ biến vô nghĩa)
- Chỉ IDF → doc chứa từ hiếm nhất thắng dù chỉ 1 lần
- TF × IDF → doc chứa nhiều lần từ hiếm → thật sự liên quan

**Quiz đã sai:**
- "câu 2 liên quan Qdrant/vector" → SAI. BM25 là text matching thuần, không liên quan Qdrant.
- "IDF cao = từ xuất hiện nhiều" → SAI. IDF cao = từ HIẾM trong corpus.

**🐞 Bug hunt đã làm — tokenize không nhất quán:**
Triệu chứng: search `"KEM"` (hoa) → rỗng, nhưng `"kem"` (thường) → ra bình thường.
Nguyên nhân: `add()` lưu token bằng `text.lower().split()` (toàn chữ thường), nhưng `search()` bị sửa thành `query.split()` (quên `.lower()`). → `tf = tokens.count("KEM")` đếm trong list `["kem",...]` → 0 → score=0 mọi doc → mất kết quả.
Fix: `terms = query.lower().split()`.
LƯU Ý thứ tự: `query.lower().split()` ĐÚNG, `query.split().lower()` CRASH — vì `.split()` trả LIST, list không có `.lower()` (`.lower()` là method của string). → lower() lúc còn là string, split() sau.

---

### Bước 7 — `application/retrieval/rrf.py`

**Flow:** `[dense_ranked, bm25_ranked]` → cộng `1/(k+rank)` cho mỗi doc → sort desc

**WHY `list[list[str]]` không phải 2 param riêng:**
Thêm nguồn thứ 3 (title search) → không sửa signature, chỉ thêm 1 phần tử vào list.

**WHY `scores.get(doc_id, 0.0)` không phải `scores[doc_id]`:**
Lần đầu gặp doc mới → `scores[doc_id]` KeyError. `.get(doc_id, 0.0)` trả default 0.0.

**WHY `enumerate(start=1)`:**
Rank bắt đầu từ 1. `1/(60+0)` là rank không tồn tại — rank trong thực tế là 1, 2, 3...

**WHY không cộng BM25 score + cosine trực tiếp:**
BM25 range `[0,∞)`, cosine range `[0,1]` — khác đơn vị. RRF chuyển về rank → scale-invariant.

**WHY `k=60`:**
Damping — làm mờ ưu thế rank 1 vs rank 2. Doc xuất hiện cao ở nhiều nguồn được thưởng, không phải doc rank 1 ở 1 nguồn độc chiếm.

**Quiz đã sai:**
- "không biết get vs []" → `.get(doc_id, 0.0)` trả 0.0 nếu key chưa tồn tại. `scores[doc_id]` → **KeyError** lần đầu gặp doc mới.
- "không biết list[list[str]]" → Nếu dùng 2 param riêng `(dense, bm25)` → thêm nguồn thứ 3 phải sửa signature hàm. `list[list[str]]` → chỉ thêm 1 phần tử, không sửa gì.

**Mở rộng — ngoài dense + BM25 còn nguồn rank nào cắm vào RRF được?**
RRF source-agnostic — chỉ cần "list doc_id đã xếp hạng", không quan tâm đến từ đâu. Vì `rank_lists: list[list[str]]` nhận N bảng, cắm thêm nguồn KHÔNG sửa code:
- **Title/metadata search** — khớp đúng tên SP, mã SKU, field cụ thể
- **Multi-Query** — 1 query viết lại 3 cách → mỗi cách 1 bảng → gộp
- **HyDE** — bịa câu trả lời giả → embed → search → 1 bảng nữa
- **Temporal / freshness** — doc mới nhất lên cao (tin tức, tài chính)
- **SPLADE / learned sparse** — BM25 "thông minh" bằng neural net
- **Popularity / click** — doc nhiều click lên cao

```python
fused = reciprocal_rank_fusion([dense_ranked, bm25_ranked, title_ranked, temporal_ranked])
#  thêm nguồn = thêm phần tử vào list, hàm RRF chạy y nguyên
```
(Multi-Query, HyDE, Temporal đều nằm trong Phase 3 còn lại — sẽ cắm thẳng vào RRF này.)

---

### Bước 9 — CRAG (Corrective RAG) — `application/generation/`

**CRAG là gì & để làm gì:**
RAG thường chạy thẳng: `tìm top-k → nhét vào model → trả lời`. Vấn đề: retrieval không phải lúc nào cũng trúng → lôi về rác → model không biết cái nào rác, cứ trả lời → **bịa (hallucination)**. "Rác vào → rác ra."
CRAG = RAG **biết tự chấm điểm chunk rồi tự đi tìm lại nếu tệ**. Chữ C = **Corrective**.
```
RAG thường:  tìm → trả lời
CRAG:        tìm → CHẤM từng chunk (yes/no) → đủ tốt? → tốt: trả lời / rác: TÌM LẠI rộng hơn → chấm lại
```
**Mục đích:** giảm bịa/trả lời sai khi retrieval lôi về rác.

**"Sao không kéo model vào luôn?"** — 2 cách hiểu:
- Bỏ retrieval, hỏi thẳng model (như ChatGPT)? → Model KHÔNG học data riêng của shop → bịa sản phẩm không tồn tại. Retrieval để đưa data thật vào.
- Nhét HẾT tài liệu vào model? → (1) giới hạn context (2) tốn tiền theo lượng chữ (3) "lost in the middle" — nhét nhiều model lơ phần giữa. → bắt buộc lọc còn vài chunk → có rủi ro lọc trúng rác.

**Phương án thay thế:** RAG thường (nhanh/rẻ, không kiểm) · Rerank mạnh (rẻ hơn CRAG, không tìm lại) · CRAG (an toàn, chậm+tốn tiền) · Self-RAG · Agentic RAG.
**Đánh đổi CRAG:** chậm + tốn tiền (mỗi lần chấm = 1 lần gọi LLM) ⇄ đổi lấy chất lượng chunk (ít bịa). → là **flag**, eval mới quyết có bật không.

**`state.py` — CRAGState = tờ giấy chuyền qua từng node:**
- INPUT (caller điền lúc `graph.invoke({...})`): `query`, `tenant_id`, `top_k` — đến từ NGOÀI, node không tự nghĩ ra
- TRUNG GIAN (node tính ra, lúc đầu trống): `candidates` (thô), `relevant` (đã grade "yes"), `verdict` ("CORRECT"/"AMBIGUOUS"/"INCORRECT"), `attempts` (đếm số lần tìm lại)
- OUTPUT: `context` (kết quả sạch cuối, finalize điền)
- Dùng `TypedDict` vì chỉ khai báo "tờ giấy có ô gì", không chứa logic. LangGraph merge dict mỗi node trả về vào state chung.

**`attempts` = cái phanh chống lặp vô hạn:**
Có vòng lặp `correct → grade → decide → correct...`. Nếu kho KHÔNG có đồ tốt → verdict luôn INCORRECT → tìm lại mãi → treo máy + đốt tiền LLM. Router check `attempts < max_attempts` → thử tối đa 2 lần, hết lượt thì đi finalize (bỏ cuộc trong danh dự).

**`decision.py` — 2 hàm khác nhau:**
- `decide_verdict(n_relevant, n_candidates)` — chấm cả mẻ. Guard `if n_candidates==0 or n_relevant==0: return INCORRECT` làm 2 việc: (1) chặn chia 0 (`n_relevant/n_candidates`), (2) bắt "0 đồ tốt = INCORRECT" (nếu bỏ, `0/6=0<0.5` ra AMBIGUOUS — sai).
- 3 verdict: **CORRECT** = ≥50% tốt (tin, trả luôn) · **AMBIGUOUS** = có tốt nhưng <50% (lẫn lộn) · **INCORRECT** = 0 đồ tốt/rỗng (tệ nhất). Ngưỡng `_CORRECT_RATIO=0.5`.
- `make_router` — trả về TÊN TRẠM KẾ, `"correct"` chỉ khi verdict INCORRECT **VÀ** còn lượt (`attempts < max_attempts`); ngược lại `"finalize"`.

**🪤 BẪY ĐẶT TÊN (quiz đã sai):** `"CORRECT"` (verdict, chất lượng) ≠ `"correct"` (TÊN trạm correct_node, chỗ tìm lại). Router KHÔNG trả verdict — nó trả "đi đâu tiếp". INCORRECT + hết lượt → router trả `"finalize"` (không phải `"correct"`); verdict INCORRECT vẫn nằm yên trong state. Trùng tên → dễ tưởng router "sửa verdict".

**`node.py` — 2 trạm có logic (3 trạm kia đơn giản):**
- `retrieve_node`: `retriever.retrieve(pool_size=20)` rộng → `reranker.rerank(top_k*2)` lọc. Rerank chạy TRƯỚC grade vì rerank RẺ, grade gọi LLM ĐẮT (mỗi chunk = 1 lần gọi). Pre-filter → LLM chấm ít chunk + tốt hơn → đỡ tốn token.
- `correct_node`: `retriever.retrieve(wide_pool=60)` RỘNG HƠN NỮA (20 đầu đã rác) → **GHI ĐÈ** `candidates` = mẻ mới → `attempts + 1`. Quên `+1` → phanh kẹt 0 → **lặp vô hạn** (khác max_attempts=0 = tắt tính năng).

**🔁 VÒNG LẶP "chấm lại → lọc lại" (chỗ khó nhất — chạy tay mới hiểu):**
`grade` + `decide` chạy NHIỀU LẦN, mỗi lần trên mẻ `candidates` KHÁC (vì `correct` thay ruột candidates = mẻ rộng hơn). Không phải lặp y hệt — mỗi vòng data đã khác (rộng/tốt hơn) → mới có cơ hội thoát.
Ví dụ: V1 grade mẻ 6 (rác) → INCORRECT → correct thay = mẻ 8 → V2 grade mẻ 8 → có đồ tốt → thoát.
**Dừng hay không là do `attempts` chạm `max_attempts`, KHÔNG phải do verdict.** INCORRECT = tín hiệu THỬ LẠI (không phải dừng). Router `attempts < max_attempts`: `1<2`=True→correct, `2<2`=False→finalize, `1<1`=False→finalize. → chỉ finalize khi verdict tốt/AMBIGUOUS, HOẶC INCORRECT + hết lượt.

**`graph.py` — ráp 5 trạm (ẩn dụ ga tàu):**
- `add_node("grade", ...)` = đặt 1 GA (chỗ làm việc). `add_edge("retrieve","grade")` = nối RAY giữa 2 ga.
- `retriever` (đồ vật, = HybridRetriever Bước 8) ≠ `"retrieve"` (tên ga). Đừng lẫn.
- **edge thường** = ray cố định, đi thẳng không rẽ (retrieve→grade→decide). **`add_conditional_edges`** = bẻ ghi, chỗ DUY NHẤT cần rẽ (sau decide: correct hay finalize, tùy verdict).
- ⭐ `add_edge("correct", "grade")` = nối correct QUAY VỀ grade → tạo VÒNG LẶP (chấm lại mẻ mới). `add_edge("finalize", END)` = xong.
- Dict `{"correct":"correct", "finalize":"finalize"}` = bảng phiên dịch "router trả nhãn X → nhảy ga Y". Key=nhãn router trả, Value=tên ga thật (ở đây trùng tên nên nhìn thừa, nhưng nguyên tắc là tách 2 thứ).
- `g.compile()` → đóng gói thành graph chạy được.

**⚠️ TRẠNG THÁI THẬT:** CRAG code có đủ 6 file trong `app/application/generation/` NHƯNG chưa cắm vào app — `grep build_crag_graph app/` chỉ thấy trong generation/, `main.py` chỉ có `/health`, `routes/__init__.py` rỗng. → "Cỗ máy lắp xong chưa cắm điện". Gap roadmap: chưa wire API/pipeline.

**💡 Insight thiết kế:** CRAG này CHỈ tìm lại khi verdict = **INCORRECT** (0 đồ tốt). **AMBIGUOUS** (có ít tốt, <50%) → CHẤP NHẬN luôn, đi finalize, KHÔNG tìm lại. Router: `if verdict == "INCORRECT" and ...`. → CRAG "dễ tính", chỉ sửa khi hỏng hẳn. Có thể đổi cho AMBIGUOUS cũng tìm lại nhưng chậm/tốn hơn (design choice).

**Quiz đã sai:**
- "max_attempts=0 → không trả về gì (câm)" → SAI. Đáp án: **giống RAG thường**. Router `0 < 0 = False` → không bao giờ đi correct → luôn finalize. `finalize_node` LUÔN trả `context` (rỗng thì trả `[]`, không câm). "Không sửa" ≠ "không trả lời". → CRAG với max_attempts=0 thoái hóa về RAG thường (đúng nghĩa "kỹ thuật là flag").
- "router INCORRECT + hết lượt → trả correct (sai, phải incorrect)" → SAI. Nhầm verdict "CORRECT" với TÊN trạm "correct". Router trả TÊN TRẠM KẾ, hết lượt → `"finalize"`, không trả verdict.

---

## Công thức cốt lõi

```
# Cosine Similarity (L2-normalized)
cos(θ) = A · B = Σ(aᵢ × bᵢ)

# IDF (BM25 variant)
IDF(t) = log((N - df + 0.5) / (df + 0.5) + 1)

# BM25
score(d,t) = IDF(t) × TF×(k1+1) / (TF + k1×(1 - b + b×dl/avgdl))
  k1=1.5 → TF saturation (score tiệm cận, không tăng mãi)
  b=0.75 → length normalization (doc dài không lợi thế)

# RRF
RRF(d) = Σᵢ  1/(k + rankᵢ(d))    k=60
```

---

## Glossary — Thuật ngữ nhanh

| Thuật ngữ | Một câu |
|---|---|
| **Embedding** | biến text thành dãy số (vector) để máy so sánh *nghĩa* |
| **Vector** | dãy số (1024 chiều với bge-m3) đại diện nghĩa một đoạn text |
| **Chunk** | một mẩu văn bản nhỏ cắt ra từ tài liệu dài |
| **Cosine similarity** | đo độ giống về nghĩa bằng *góc* giữa 2 vector |
| **Dense retrieval** | tìm theo *nghĩa* bằng vector — giỏi ngữ nghĩa, dễ trượt từ khóa chính xác |
| **Sparse retrieval / BM25** | tìm theo *từ khóa* khớp chữ — bắt "SPF 50+", mã SKU |
| **Hybrid search** | dense + sparse → RRF → lấy điểm mạnh cả hai |
| **RRF** | gộp nhiều bảng xếp hạng bằng *thứ hạng*, không phải điểm tuyệt đối |
| **Rerank** | chấm lại top-k cho chính xác hơn sau retrieve |
| **Cross-encoder** | đọc query + doc *cùng nhau* → chính xác hơn, chậm hơn |
| **Bi-encoder** | encode query và doc *riêng lẻ* → nhanh, kém tinh hơn |
| **Qdrant** | vector database chuyên lưu & tìm vector |
| **Payload** | metadata kèm theo mỗi vector (text gốc, source, tenant_id) |
| **tenant_id** | nhãn ngăn cách dữ liệu từng kênh — mọi search bắt buộc lọc theo nó |
| **UUID5** | ID deterministic từ namespace + content → cùng chunk ingest 2 lần = overwrite, không duplicate |
| **HNSW** | thuật toán index của Qdrant — cần biết `dim` khi tạo collection |
| **Protocol** | "phải có method gì" — không cần kế thừa, có đủ method là hợp lệ |
| **Port / Adapter** | Port = interface (contract); Adapter = implementation thật |
| **DI (Dependency Injection)** | tiêm phụ thuộc từ ngoài vào, không để class tự tạo bên trong |
| **use_fp16** | dùng float16 thay float32 → nửa RAM, nhanh hơn ~2× |
| **normalize_embeddings** | L2-normalize → ‖v‖=1 → cosine = dot product |
| **CRAG** | RAG tự chấm điểm kết quả rồi sửa sai khi gặp rác |
| **LLM-as-judge** | dùng LLM làm giám khảo chấm điểm (yes/no liên quan) |
| **State machine** | chạy theo các trạm có thứ tự, mỗi trạm xử lý rồi chuyển tiếp |
| **Hallucination** | model bịa thông tin không có trong nguồn |
| **Grounding** | câu trả lời bám chặt vào nguồn dữ liệu thật |
| **fp16** | float16 — nửa độ chính xác của float32, đủ dùng cho embedding |
| **Structural typing** | match bằng cấu trúc (có method gì), không phải bằng kế thừa |
| **keyword-only argument** | tham số sau `*` — bắt buộc gọi với tên, không nhầm thứ tự |
| **Open/Closed principle** | mở để mở rộng, đóng để sửa — không sửa port khi thêm field |
| **VectorSearchResult** | raw result từ Qdrant — có id, score, payload dict chưa structured |
| **RetrievalHit** | output đã xử lý sau RRF — có doc_id, text, score, source rõ ràng |
| **temperature** | mức ngẫu nhiên/sáng tạo của LLM. Cao = đa dạng (hợp sáng tác); `0.0` = luôn bốc từ khả năng cao nhất = **deterministic** (hợp chấm điểm/phân loại) |
| **deterministic** | cùng input → luôn cùng output. Cần cho chấm điểm ổn định + debug/eval lặp lại được |
| **max_tokens** | giới hạn độ dài câu trả lời của LLM. Chấm yes/no → đặt nhỏ (~5) để khỏi tốn tiền/chậm |
| **TypedDict** | khai báo "dict có ô gì" (như CRAGState) — chỉ cấu trúc, KHÔNG chứa logic/method |
| **CRAG (Corrective RAG)** | RAG tự chấm điểm chunk (LLM-as-judge yes/no) rồi tự tìm lại nếu tệ. Chữ C = Corrective |
| **verdict** | phán quyết chất lượng retrieval: CORRECT / AMBIGUOUS / INCORRECT (do `decide_verdict` tính từ tỉ lệ relevant/candidates) |
| **attempts** | bộ đếm số lần CRAG tìm lại — cái phanh chống lặp vô hạn khi kho không có đồ tốt |
| **max_attempts** | ngưỡng tìm lại tối đa (flag). =0 → CRAG thoái hóa về RAG thường |

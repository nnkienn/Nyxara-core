# 4️⃣ API — bọc thành HTTP endpoint thật

> Chặng cuối. Nối [01-ingest.md](./01-ingest.md) → [02-retrieval.md](./02-retrieval.md) →
> [03-crag.md](./03-crag.md) thành 2 endpoint gọi được qua `curl`/HTTP thật. File chính:
> `app/main.py` (lifespan) + `app/presentation/api/ask.py` + `app/presentation/api/ingest.py`.
>
> **Đây là nơi cả 2 bug #24 và #25 thật sự lộ ra** — không phải trong logic từng chặng riêng lẻ
> (đã test `pytest` xanh hết), mà ở chỗ **ráp chúng lại với nhau** lúc chạy thật.

---

## Kể chuyện trước

1. `main.py` có 1 `lifespan` — chạy **đúng 1 lần** lúc server khởi động (không phải mỗi request):
   dựng cả 4 adapter thật + ráp `RerankingRetriever` + `build_graph(...)`, lưu vào `app.state`.
2. `POST /ingest` — nhận `{tenant_id, doc_id, text}`, tự chunk, gọi `ingest_document(...)` (dùng
   lại đúng các instance đã dựng ở bước 1 qua `request.app.state.*`).
3. `POST /ask` — nhận `{tenant_id, query}`, gọi `request.app.state.graph.invoke(...)`, trả
   `{answer}`.

---

## Thứ tự dựng trong `lifespan` (đúng thứ tự phụ thuộc)

```
embedder = BGEEmbedder()
client   = QdrantClient(location=":memory:")
vector_store = QdrantStore(client, collection="docs", dim=embedder.dim)
bm25_index   = BM25Index()
doc_store    = InMemoryDocStore()

hybrid_retriever = HybridRetriever(embedder, vector_store, bm25_index)
reranker         = BGEReranker()
retriever        = RerankingRetriever(hybrid_retriever, doc_store, reranker)
#        ▲ PHẢI bọc qua RerankingRetriever — xem bug #24 ở 02-retrieval.md.
#          Đưa thẳng hybrid_retriever vào build_graph() sẽ TypeError khi gọi thật.

grader    = OllamaGrader(base_url=OLLAMA_BASE_URL)
generator = OllamaGenerator(base_url=OLLAMA_BASE_URL)

graph = build_graph(retriever, doc_store, grader, generator)

app.state.embedder, .vector_store, .bm25_index, .doc_store, .manifest_path, .graph = ...
```

---

## ⚠️ Bẫy #1 — sync/async

`graph.invoke(...)` là hàm **đồng bộ** (`OllamaGrader`/`OllamaGenerator` gọi `httpx.post` chặn
luồng). Nếu handler viết `async def ask(...)` rồi gọi thẳng `graph.invoke(...)` bên trong, nó
**chặn cả event loop** — không request nào khác chạy được cùng lúc. Cách né: viết handler là
`def ask(...)` (**không** `async`) — FastAPI tự chạy trong threadpool riêng.

## ⚠️ Bẫy #2 — `uvicorn --reload` xoá sạch state in-memory (liên quan bug #25)

Mỗi lần sửa file `.py` và `--reload` restart process, `BM25Index`/`Qdrant(":memory:")`/
`InMemoryDocStore` **mất sạch** (chỉ sống trong RAM). Nhưng `data/manifest.json` (ghi xuống đĩa)
thì **không mất** — dẫn tới bug #25: `/ingest` lại tưởng thành công nhưng bị `to_skip` oan vì
manifest cũ vẫn nhớ. Chi tiết: [01-ingest.md](./01-ingest.md).

**Khi trace mà gặp lỗi lạ sau khi sửa code + reload:** luôn `rm data/manifest.json` rồi
`/ingest` lại từ đầu trước khi nghi ngờ logic.

---

## Trace bằng tay — checklist từng bước

```bash
# 1. Cài đủ dependency (chỉ cần làm 1 lần)
.venv/bin/python3 -m pip install -r requirements.txt

# 2. Set biến môi trường (Ollama qua Tailscale)
export OLLAMA_BASE_URL="http://100.78.59.56:11434"

# 3. Chạy server
.venv/bin/uvicorn app.main:app --reload --port 8000
# Đợi tới dòng "Application startup complete."

# 4. (Terminal khác) Ingest 1 tài liệu
curl -X POST localhost:8000/ingest -H "Content-Type: application/json" \
  -d '{"tenant_id":"t1","doc_id":"doc1","text":"..."}'
# → {"chunk_count": N}

# 5. Hỏi
curl -X POST localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"tenant_id":"t1","query":"..."}'
# → {"answer": "..."}
```

**Nếu lỗi:** đọc traceback ở **terminal chạy uvicorn** (không phải output của `curl` — curl chỉ
hiện "Internal Server Error" chung chung), đối chiếu dòng lỗi với đúng chặng 1-2-3 ở các file
trước để biết đang vỡ ở đâu.

---

## Files

| File | Vai trò |
|---|---|
| `app/main.py` | `lifespan` (dựng 4 adapter + graph), đăng ký router |
| `app/presentation/api/ingest.py` | `POST /ingest` |
| `app/presentation/api/ask.py` | `POST /ask` |

**Test:** không có unit test riêng cho wiring này — bug #24/#25 đều chỉ lộ khi chạy `uvicorn`
thật, không lộ qua `pytest`. Đây là bài học lớn nhất buổi: **test unit xanh ≠ hệ thống chạy được
thật** — luôn verify qua HTTP thật ít nhất 1 lần trước khi coi tính năng end-to-end là xong.

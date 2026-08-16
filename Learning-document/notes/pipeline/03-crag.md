# 3️⃣ CRAG — chấm điểm, lặp lại nếu tệ, rồi sinh câu trả lời

> Chặng 3. Input: kết quả retrieval từ [02-retrieval.md](./02-retrieval.md). Output: câu trả lời
> cuối (`answer`). Khác biệt lớn nhất so với retrieval thuần: **có rẽ nhánh thật + có thể lặp lại**.
> File chính: `app/application/generation/graph.py` + `node.py`.

---

## Kể chuyện trước

1. Bạn hỏi `"mèo đen"`.
2. **`retrieve`** — gọi `RerankingRetriever` (xem [02-retrieval.md](./02-retrieval.md)), rồi tra
   `doc_store.get(...)` lấy text → ghi vào `state.retrieved_docs`.
3. **`grade`** — 1 "giám khảo" (LLM, `OllamaGrader`) đọc từng đoạn vừa tìm, tự hỏi "đoạn này có
   thật sự liên quan không?" → đếm được bao nhiêu "có"/"không" → kết luận `verdict`:
   `CORRECT` (đủ tốt) / `INCORRECT` (tệ) / `AMBIGUOUS` (nửa nạc nửa mỡ).
4. Tuỳ kết luận:
   - **Đủ tốt** (`CORRECT`/`AMBIGUOUS`) → đi thẳng tới `generate`.
   - **Tệ** (`INCORRECT`) → quay lại `retrieve`, tìm **rộng hơn**, rồi `grade` lại.
5. Vòng lặp ở bước 4 **không được lặp mãi** — có bộ đếm `attempts`, thử tối đa vài lần; quá số
   đó thì **buộc** đi `generate` dù tài liệu chưa hoàn hảo — còn hơn treo mãi.

---

## Sơ đồ

```
              query = "mèo đen", attempts = 0
                          │
                          ▼
            ┌───────────────────────────┐
            │  NODE: retrieve             │
            │  gọi RerankingRetriever      │
            │  → ghi state.retrieved_docs  │
            └───────────────────────────┘
                          │
                          ▼
            ┌───────────────────────────┐
            │  NODE: grade                 │
            │  LLM chấm CÓ/KHÔNG từng doc  │
            │  → ghi state.verdict         │
            └───────────────────────────┘
                          │
                          ▼
                  verdict là gì?
           ┌──────────────┼───────────────┐
           │               │                │
   CORRECT/AMBIGUOUS   INCORRECT        INCORRECT
     (đủ tốt)        attempts<max     attempts≥max
           │               │           (van an toàn)
           │               ▼                │
           │     attempts += 1               │
           │     quay lại NODE: retrieve      │
           │     (tìm RỘNG hơn)               │
           │     (vòng lặp về grade lại)      │
           │                                  │
           └────────────────┬─────────────────┘
                             ▼
            ┌───────────────────────────┐
            │  NODE: generate              │
            │  sinh câu trả lời từ docs     │
            │  → ghi state.answer          │
            └───────────────────────────┘
                             ▼
                           END
```

---

## ⚠️ Hợp đồng (contract) giữa `graph.py`/`node.py` và retriever (liên quan bug #24)

`build_graph(retriever, doc_store, grader, generator, candidate_k=10, top_k=5, max_attempts=3)`
**giả định** `retriever` có `.search(tenant_id, query, candidate_k, top_k)` — 4 tham số. Đây là
hợp đồng ngầm, không được `Port`/type-check nào bảo vệ (xem [02-retrieval.md](./02-retrieval.md)
mục bug #24) — ai wiring `main.py` phải nhớ đúng hợp đồng này, `pytest` (dùng Fake) không tự
nhắc được.

---

## Khác biệt cốt lõi so với retrieval thuần (chặng 2)

| | `HybridRetriever`/`RerankingRetriever` (chặng 2) | CRAG (chặng 3) |
|---|---|---|
| Luồng | Thẳng 1 đường, không rẽ nhánh | Có **ngã ba thật** (`decision`) |
| Lặp lại | Không bao giờ | Có thể quay lại `retrieve` nếu `INCORRECT` |
| Cần gì mới | Chỉ hàm gọi tuần tự | `StateGraph` (LangGraph) — node/edge/conditional-edge |
| Van an toàn | Không cần | `attempts` — chặn lặp vô hạn khi kho thật sự không có dữ liệu |

---

## Files

| File | Vai trò |
|---|---|
| `state.py` | "tờ giấy" — field của `state` (`query`, `retrieved_docs`, `verdict`, `attempts`, `answer`, `tenant_id`, `grades`) |
| `node.py` | `retrieve_node`/`grade_node`/`generate_node` (closure, "nhớ" dependency đã inject) |
| `decision.py` | `decide()` đếm CÓ/KHÔNG → verdict (ngưỡng 0.6/0.0) · `route()` verdict+attempts → node kế tiếp |
| `grader.py`/`ollama_grader.py` | LLM-as-judge chấm YES/NO — Ollama (`qwen2.5:3b`) qua Tailscale |
| `generator.py`/`ollama_generator.py` | sinh câu trả lời cuối từ `retrieved_docs`, cùng Ollama |
| `graph.py` | nối `retrieve→grade→(generate hoặc retrieve lại)` bằng `StateGraph` |

**Test:** `.venv/bin/python3 -m pytest tests/application/generation/ -v` (17 test — decision, node,
graph e2e, grader, generator — grader/generator dùng mock, không cần mạng).

---

**Tiếp theo:** [04-api.md](./04-api.md) — 2 chặng retrieval + CRAG này được bọc thành HTTP endpoint
gọi được thật như thế nào.

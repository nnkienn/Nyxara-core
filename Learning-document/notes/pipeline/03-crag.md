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
   - **Tệ** (`INCORRECT`) → quay lại `retrieve` chạy lại **y hệt lần trước**, rồi `grade` lại.

     > 🐛 **Đây là bug #26, không phải mô tả đúng.** Chữ "tìm **rộng hơn**" từng nằm ở đây là thứ
     > *định làm* chứ code chưa hề làm. `retrieve_node` lấy `candidate_k`/`top_k` từ **closure**
     > (đông cứng lúc `build_graph()` chạy — đúng 1 lần, lúc server boot), không lấy từ `state`.
     > Nên lần retry thứ 2, thứ 3 nhận **y nguyên 4 input như lần 1** → cùng docs → cùng
     > `verdict INCORRECT` → vòng lặp không bao giờ khá lên, chỉ đốt thêm 2 lượt gọi LLM grader.
     > Muốn chữ "rộng hơn" thành thật thì cần đủ **2 nửa**: `retrieve_node` phải *đọc*
     > `candidate_k` từ `state` (closure tụt xuống chỉ còn làm default lần đầu), **và**
     > `grade_node` — nơi sinh ra `verdict`, nơi đã đếm `attempts + 1` — phải *ghi* một
     > `candidate_k` lớn hơn vào state khi verdict là `INCORRECT`. Chi tiết: [bug-log #26](../bug-log.md).
5. Vòng lặp ở bước 4 **không được lặp mãi** — có bộ đếm `attempts`, thử tối đa `max_attempts`
   lần; quá số đó thì **buộc** đi `generate` dù tài liệu chưa hoàn hảo — còn hơn treo mãi.

   > ⚠️ Vì bug #26 ở trên, hiện tại đây **không phải** van dự phòng hiếm khi chạm tới — nó là
   > **đường ra duy nhất** mỗi khi verdict là `INCORRECT`. Đã kiểm chứng bằng cách chạy graph
   > thật với grader giả luôn trả `False` (04/09): `retrieve` chạy đúng 3 lần, cả 3 lần
   > `candidate_k=10`, `verdict` cuối vẫn `INCORRECT`, `attempts=3`, và vẫn có `answer` trả về
   > cho người dùng — **không kèm bất kỳ cảnh báo nào** rằng hệ thống tự biết tài liệu không liên quan.

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

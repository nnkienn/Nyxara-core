# 🔁 CRAG Pipeline — sơ đồ Phase 2.3

> Xem chi tiết từng kỹ thuật Phase 2.1/2.2 ở [retrieval-pipeline.md](./retrieval-pipeline.md).
> File này chỉ vẽ luồng CRAG (Corrective RAG) — điểm khác biệt lớn nhất so với Phase 2.1/2.2:
> **có rẽ nhánh thật + có thể lặp lại**, không còn chạy thẳng 1 đường như trước.

---

## Kể chuyện trước (đọc phần này nếu sơ đồ dưới còn rối)

1. Bạn hỏi `"mèo đen"`.
2. **`retrieve`** — tìm vài đoạn tài liệu có vẻ liên quan (dùng lại `RerankingRetriever` đã xây).
3. **`grade`** — 1 "giám khảo" (LLM) đọc từng đoạn vừa tìm, tự hỏi "đoạn này có thật sự liên
   quan không?" — đếm được bao nhiêu "có", bao nhiêu "không", tổng kết thành 1 kết luận:
   `CORRECT` (đủ tốt) / `INCORRECT` (tệ) / `AMBIGUOUS` (nửa nạc nửa mỡ).
4. Tuỳ kết luận:
   - **Đủ tốt** (`CORRECT`/`AMBIGUOUS`) → đi thẳng tới `generate`, dùng tài liệu đó trả lời.
   - **Tệ** (`INCORRECT`) → quay lại `retrieve`, lần này tìm **rộng hơn**, rồi `grade` lại.
5. Vòng lặp ở bước 4 (nhánh dưới) **không được lặp mãi** — có bộ đếm `attempts`, thử tối đa
   vài lần; quá số đó thì **buộc** đi `generate` dù tài liệu chưa hoàn hảo — còn hơn treo mãi.

---

## Sơ đồ (ASCII — đọc được ở mọi nơi, không cần extension)

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

## Khác biệt cốt lõi so với Phase 2.1/2.2 (đã xây)

| | `HybridRetriever` / `RerankingRetriever` | CRAG |
|---|---|---|
| Luồng | Thẳng 1 đường, không rẽ nhánh | Có **ngã ba thật** (`decision`) |
| Lặp lại | Không bao giờ | Có thể quay lại `retrieve` nếu `INCORRECT` |
| Cần gì mới | Chỉ hàm gọi tuần tự | `StateGraph` (LangGraph) — node/edge/conditional-edge |
| Van an toàn | Không cần | `attempts` — chặn lặp vô hạn khi kho thật sự không có dữ liệu |

---

## File sẽ build (`app/application/generation/`)

| File | Vai trò | Trạng thái |
|---|---|---|
| `state.py` | "tờ giấy" — định nghĩa field của `state` (kể cả `tenant_id`) | ✅ xong |
| `node.py` | `retrieve_node` (closure, gọi lại `RerankingRetriever`+`DocStore`) | ✅ xong — 1 test verify |
| `decision.py` | `decide()` đếm CÓ/KHÔNG → verdict (ngưỡng 0.6/0.0, là tham số) · `route()` verdict+attempts → node kế tiếp | ✅ xong — 6 test pass |
| `grader.py`/`ollama_grader.py` | LLM-as-judge chấm YES/NO mỗi doc — gọi Ollama (`qwen2.5:3b`) qua Tailscale (`100.78.59.56:11434`) | ✅ xong — 5 test (mock, không cần mạng) |
| `generator.py`/`ollama_generator.py` | sinh câu trả lời cuối từ `retrieved_docs`, cùng Ollama | ✅ xong — 3 test (mock) |
| `graph.py` | nối `retrieve→grade→(generate hoặc retrieve lại)` bằng `StateGraph`, `grade_node` tự tăng `attempts` | ✅ xong — 2 test e2e (happy path + van an toàn) |

**CRAG (Phase 2.3) hoàn tất 2026-08-12** — verify bằng graph thật (LangGraph `StateGraph`), 2 kịch bản: luôn CORRECT (đi thẳng) và luôn INCORRECT (lặp đúng `max_attempts` lần rồi cưỡng bức generate). Model thật (`qwen2.5:3b` qua Tailscale) đã dùng để xây `grader.py`/`generator.py`, nhưng test tự động dùng mock để không phụ thuộc mạng.

---

## ⚠️ Việc còn treo — Docker networking cho Ollama (xử lý khi deploy, không cấp bách)

`grader.py` gọi HTTP tới Ollama qua Tailscale (`100.78.59.56:11434`) từ máy host (`.venv` local) —
chạy đúng vì máy host có Tailscale. Nhưng **container Docker mặc định cô lập mạng với host**,
không tự có kết nối Tailscale này. Khi thật sự đóng gói app vào Docker để deploy, cần 1 trong 2:
- Chạy container ở chế độ `--network host`, hoặc
- Cài Tailscale ngay bên trong container (image riêng hoặc sidecar)

Chưa cần xử lý bây giờ (đang code tay/test qua `.venv`) — chỉ xử lý khi thật sự deploy.

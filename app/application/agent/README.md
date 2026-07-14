# application/agent

Phase 4 — Agentic Orchestrator. Từ RAG một phát → agent nhiều bước biết dùng tool, nhớ ngữ cảnh.

| File/thư mục (sẽ build) | Kỹ thuật | Ưu tiên |
|---|---|---|
| `supervisor.py` | Supervisor → Researcher → Creator → Critic → Human gate | 🔴 |
| `tools/` | tool implementations + structured-output retry | 🔴 |
| `memory.py` | multi-turn / thread memory | 🔴 |

**Code tay trước:** tự dựng StateGraph supervisor (tái dùng skill CRAG), retry-loop cho tool call
lỗi JSON trước khi dùng structured-output helper.
**Bug cố ý:** supervisor không có điều kiện dừng → loop vô hạn. Fix bằng `max_steps` guard
(cùng họ với `attempts` ở CRAG).
Cắm LangFuse tracing ngay từ agent đầu tiên.

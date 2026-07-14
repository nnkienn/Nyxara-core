# application/generation

Phase 2.3 — CRAG (Corrective RAG) qua LangGraph state machine.

| File (sẽ build) | Vai trò |
|---|---|
| `state.py` | "tờ giấy" chạy qua các node, điền dần từng ô |
| `node.py` | node = hàm `state → dict` |
| `grader.py` | LLM-as-judge chấm CÓ/KHÔNG mỗi doc |
| `decision.py` | đếm verdict → CORRECT / AMBIGUOUS / INCORRECT → router |
| `graph.py` | nối node/edge/conditional-edge, `attempts` guard chặn lặp vô hạn |

**3 bug cũ từng gặp (né lại):** HybridRetriever thiếu `await` (async lây cả chuỗi) ·
`attempts` KeyError ở đường thành công (phải init `attempts=0`) ·
cần `extra_hosts` cho core-api reach Ollama grader (đã có trong docker-compose.yml).

CTDLGT: graph (node/edge, conditional routing, cycle guard).

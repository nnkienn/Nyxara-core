# safety

Phase 5 — UGC (user-generated content) không tin được. Agent phơi ra internet cần giáp 2 chiều.

| File (sẽ build) | Kỹ thuật | Ưu tiên |
|---|---|---|
| `pii.py` | phát hiện + che SĐT/địa chỉ (PDPD/GDPR) | 🔴 code tay Trie/regex trước Presidio |
| `injection.py` | chặn prompt injection từ input độc | 🔴 |
| `sanitize.py` | output sanitization (XSS/markdown injection) — khác injection input | 🔴 |
| `circuit_breaker.py` | Qdrant/LLM sập → xuống cấp êm, state machine CLOSED→OPEN→HALF_OPEN | 🟡 |

**Bug cố ý injection:** để prompt template nối thẳng UGC → nhét "ignore previous instructions"
thấy agent bị lái. Fix bằng cách tách data/instruction (delimiter, role).

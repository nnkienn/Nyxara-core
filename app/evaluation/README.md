# evaluation

Phase 3 — ⭐ phase quan trọng nhất. "Không có eval = bay mù": mọi kỹ thuật Phase 2 chỉ được
bật khi eval chứng minh nó thật sự cải thiện.

| File (sẽ build) | Kỹ thuật | Ưu tiên |
|---|---|---|
| `retrieval_metrics.py` | Hit@k · MRR · NDCG — deterministic, chạy mỗi commit | 🔴 code tay trước |
| `judge.py` | Custom LLM Judge — prompt chấm + parse structured JSON + retry | 🔴 |
| `metrics.py` | faithfulness, answer-relevancy — tự implement trước khi so với RAGAS | 🔴 |
| `ragas_runner.py` | đối chiếu bản tay với RAGAS chuẩn ngành | 🔴 |
| `ab_harness.py` | A/B + statistical significance (đổi đúng 1 biến/lần) | 🔴 |
| `calibration.py` | human vs LLM judge agreement (κ / Pearson) | 🟡 |
| `cost_metrics.py` | tokens · latency (p50/p95) · cost/query · throughput | 🔴 |
| `golden/v1.jsonl` | golden dataset 50–100 cặp, **versioned** (bump version khi đổi, không sửa lén) | 🔴 |
| `regression/` | mỗi bug production → 1 file test vĩnh viễn ở đây | 🔴 |

**3 bug cố ý kinh điển:** judge parse lỏng (`"yes" in text` chấm sai câu phủ định) ·
NDCG sai log-base/off-by-one rank · A/B đổi 2 biến cùng lúc.

**Nguyên tắc:** debug retrieval eval TRƯỚC generation eval — kho trả sai doc thì LLM giỏi mấy cũng bịa.

# ops/serving

Phase 7 — MLOps & Production. Config hạ tầng serving, không phải Python package.

| File (sẽ build) | Vai trò |
|---|---|
| `vllm.yaml` | serve LLM throughput cao (paged attention) qua vLLM |

Radar 📡: canary/blue-green deploy, DR/backup, scaling/backpressure — phần lớn thuộc về cloud layer.

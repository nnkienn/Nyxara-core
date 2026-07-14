# observability

Phase 3.5 (timing nội bộ pipeline) + Phase 7 (metric hạ tầng). Phân biệt rạch ròi với
**agent tracing (LangFuse, Phase 4)** — cái này đo cả hệ thống, không phải từng bước agent.

| File (sẽ build) | Phase | Ghi chú |
|---|---|---|
| `timing.py` | 3.5 | decorator `@timed` gom latency từng chặng (embed/dense/sparse/rerank) vào dict |
| `metrics.py` | 7 | Prometheus metric — latency p50/p95, error rate, uptime |

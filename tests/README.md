# tests

Mirrors `app/` 1:1 — `tests/application/chunking/` tests `app/application/chunking/`, etc.
No separate `tests/domain/`: ports are pure `Protocol` interfaces with no logic to test directly;
contract tests for a port live alongside the adapter that implements it
(e.g. `tests/infrastructure/adapters/vectorstore/test_qdrant_store.py` asserts it satisfies
`VectorStorePort`).

Every regression case from a fixed bug gets a permanent test here (or in
`app/evaluation/regression/` for eval-layer bugs) — see
[LEARNING_ROADMAP.md](../Learning-document/LEARNING_ROADMAP.md) §vòng 6 bước, bước 5.

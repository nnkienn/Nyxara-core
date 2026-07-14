<div align="center">

# Nyxara 🤖🚀

### An AI Engineering Toolkit you build from scratch — advanced RAG, agents, fine-tuning & evaluation — aimed at one real niche

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-DC244C.svg?logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C.svg)](https://langchain-ai.github.io/langgraph/)
[![Status](https://img.shields.io/badge/status-rebuilding_from_scratch-orange.svg)](./Learning-document/LEARNING_ROADMAP.md)

**Most "learn AI" side projects die as glued-together tutorials — no users, no way to tell if anything works, and a black-box core nobody understands. Nyxara is the opposite bet: you build every layer *by hand* — the embedding math, the RRF formula, the reranker, CRAG, the LoRA update, the eval metrics — and you point it at one real job: a *Comment Assistant* for TikTok Shop / Shopee seller-affiliates. Human-in-the-loop, never auto-post.**

🌐 🇬🇧 **English** · 🇻🇳 [Tiếng Việt](./README.vi.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇨🇳 [中文](./README.zh.md)

</div>

---

> ### 🔁 Status: rebuilding from scratch (reset 2026-07)
> The repo was deliberately reset to a **bootable skeleton** — Docker + an empty hexagonal
> structure + a `/health` endpoint. The old harvester and RAG brain (and their 74 tests) were
> deleted on purpose, so every layer can be **re-built by hand and actually understood**, not
> inherited as a black box. Everything below the "Why" section describes the **target system
> and the learning path to it** — follow the honest status in the [roadmap](#-roadmap--the-learning-path).

---

## 🎯 Why this exists

Two things kill most "I'm learning AI engineering" projects:

1. **They're stitched from tutorials.** You wire up a LangChain retriever, get an answer, and never learn *why* dense retrieval missed, what RRF actually computes, or whether your reranker helped. The understanding never lands.
2. **They have no destination.** No real task, no real user, no way to measure "better." Motivation evaporates.

**Nyxara fixes both.** It is a multilingual **RAG + agentic engine you build from scratch** — owning the embedding math, the RRF formula, the cross-encoder rerank, the LoRA update, the eval metrics — pointed at a **concrete niche with real (if small) users:** content & social automation for **seller-affiliates on TikTok Shop / Shopee in Vietnam.**

> **The 2026 reality:** AI writes the boilerplate now. The skill that still pays is *reading a flow deeply and catching the bug* — because AI ships subtle bugs too (`>= 0` where it meant `>= 0.5`). So Nyxara runs on one non-negotiable rule: **every core technique is implemented by hand first, and only then swapped for a library.** If you can't build it and can't debug it, you can't tell whether the library is lying to you.

It is designed to run **100% local** by default (no byte leaves your box unless you choose a cloud tier), and a `tenant_id` **namespace** lets one install host several niches side by side — *folder per niche*, not *tenant per paying customer*. The MIT core has no billing, auth, or dashboard; any of that lives in a **separate cloud layer** (see [Phase 9](#-roadmap--the-learning-path)).

---

## 🧭 How you learn here — the discipline

This repo is a **learning vehicle first**, a niche tool second. The method is not "read code and nod." Every core technique goes through a **6-step loop** before a library is allowed anywhere near it:

```
1. BUILD BY HAND   ← write the core from zero (naive is fine); no library doing it for you
2. PLANT A BUG     ← break one thing on purpose (off-by-one, wrong sign, missing normalize / await)
3. DEBUG BY HAND   ← read the trace, print real numbers, find it yourself — don't ask the AI first
4. FIX             ← fix it, and explain exactly what wrong output the bug produced
5. TEST            ← write the test that catches that bug (regression) + the happy path
6. DOCUMENT        ← the WHY into notes/, new terms into the glossary, the bug into the bug-log
```

Only after those six do you swap in the standard library (FlagEmbedding, rank-bm25…) **and diff your result against the hand-built one.** Libraries are for production; the hand-built version is for understanding.

**Data structures are not separate homework** — each RAG technique *is* a data-structure problem in disguise:

| Structure / algorithm | Where it shows up |
|---|---|
| Hash map / inverted index | BM25 (term → posting list), dedup |
| Priority queue / heap | top-k retrieval, MMR |
| Sliding window | chunking, context-window budgeting |
| Trie / prefix tree | tokenizer, PII pattern matching |
| Graph (BFS/DFS) | LangGraph state machines, GraphRAG multi-hop |
| Dynamic programming | edit distance for near-duplicate dedup |
| Two-pointer / merge | RRF (merge N ranked lists) |

> **Learning docs live in [`Learning-document/`](./Learning-document/):**
> [LEARNING_ROADMAP.md](./Learning-document/LEARNING_ROADMAP.md) (the full path + hand-code drills) and
> [`notes/`](./Learning-document/notes/) — **design-system**, **algorithms**, **glossary**, **bug-log**.

---

## 🛍️ Flagship use case — the Comment Assistant

This is the niche destination that gives every technique a reason to exist.

A seller-affiliate posts a product video on TikTok Shop / Shopee. Underneath, dozens of comments pile up: *"giá bao nhiêu?"*, *"da dầu dùng được không?"*, *"ship mấy ngày?"*. The Comment Assistant turns that firehose into reviewed, on-brand replies:

1. **Read** the public comments under the video.
2. **Retrieve** the right product facts — price, ingredients, usage, official link — **filtered to *that specific product*** (metadata filter first, *then* semantic search — not "closest vector wins").
3. **Draft** a reply in the seller's voice and locale.
4. **Critique** it: a dedicated **Critic agent blocks fabricated facts and unverified efficacy claims** — non-negotiable for cosmetics/health, where a wrong claim is a trust and legal problem.
5. **Human approves** before anything is sent. **Nyxara never auto-posts.** When a reply *is* sent, it goes through the platform's **official API** — never a stealth browser.

Every RAG/agent/eval technique in the roadmap earns its place by answering a real question here: *did retrieval pull the right product? did rerank actually lift the answer? did the Critic catch the false claim?* — and Phase 3 evaluation is how you **prove** the answer instead of guessing.

---

## 🧱 The system you'll build (target architecture)

> These are the pieces the roadmap constructs, phase by phase. **Current code = skeleton;** each
> item below is a build target, not a shipped feature. Statuses are in the [roadmap table](#-roadmap--the-learning-path).

- **Ingestion pipeline (Phase 0):** a pluggable data connector (drop one file per source) + chunking → dedup → incremental upsert. Data acquisition is decoupled from inference — *the ingest layer never calls an LLM*.
- **Vector memory (Phase 1):** `BAAI/bge-m3` (1024-dim, 100+ languages) into [Qdrant](https://qdrant.tech/), one shared cross-lingual index. Every `upsert`/`search` carries a mandatory `tenant_id` filter — **zero cross-niche bleed** as an architectural guarantee. (Drop the filter and it *silently* leaks another niche's data — no crash. That's a Phase-1 debug drill.)
- **Advanced retrieval (Phase 2):** Hybrid (dense + BM25) → RRF → cross-encoder rerank → CRAG, then metadata filtering, MMR, query transformation, temporal, Adaptive/Self-RAG, GraphRAG — each **built by hand** and toggled per query.
- **Evaluation (Phase 3):** hand-built Hit@k/MRR/NDCG + RAGAS + custom LLM judge + golden/regression sets + A/B — the loop that decides which techniques actually stay on.
- **Dual-engine LLM router:** one `LLMClientBase` (OpenAI-compatible) so every agent runs on Ollama/MLX (local dev) or vLLM/cloud (scale) with no code change — routing is a runtime config decision.
- **Supervisor–Worker agents (Phase 4):** Supervisor → Researcher → Creator → **Critic** → Human gate. The **Critic verifies grounding before a draft reaches the human**, and the human is the final gate. There is no auto-publish agent.
- **Safety (Phase 5), Fine-tuning (Phase 6), MLOps (Phase 7), Extensibility (Phase 8)** — see the roadmap.

---

## 🏗️ Hexagonal Architecture — and the Core ↔ Cloud line

The domain core depends on nothing; the outside world plugs in through ports. You can replace Qdrant, the LLM engine, or the web framework without touching business logic.

> **Core (this repo) vs. a Cloud layer.** This repo is the **pure, MIT, niche-agnostic AI brain** — deliberately *no* billing, auth, or customer accounts (`tenant_id` is a **namespace**, not a customer). Any productization (auth, billing, dashboard, API gateway, per-customer metering, wallet/credit) belongs in a **separate cloud layer that calls this engine's HTTP API** and maps each *customer → tenant_id namespace*. The core exposes **ports** (e.g. `MeteringPort`, `EntitlementPort`); the cloud plugs in **adapters**. CI rejects `import stripe` / auth / billing inside the core. The brain stays forkable and learnable; the commercial shell never leaks in. That bridge is [Phase 9](#-roadmap--the-learning-path).

Full tree scaffolded for every phase up front (2026-07-14) — every folder has its own
`README.md` naming the phase, the files it expects, and the priority; files themselves are
still empty until that phase is hand-built:

```
nyxara-core/
├── app/
│   ├── domain/ports/                        # P0-9  interfaces (Protocol), zero framework deps
│   ├── application/
│   │   ├── chunking/                        # P0    recursive/semantic/proposition chunkers
│   │   ├── ingestion/                       # P0    dedup + incremental + versioning pipeline
│   │   ├── retrieval/                       # P2.1  BM25 · RRF · hybrid retriever
│   │   ├── services/                        # P2.4  MMR · query transform · context compressor
│   │   ├── generation/                      # P2.3  CRAG state machine (LangGraph)
│   │   ├── graphrag/                        # P2.4  📡 radar — multi-hop, off by default
│   │   └── agent/tools/                     # P4    supervisor · tools · memory
│   ├── infrastructure/
│   │   ├── adapters/embedder|vectorstore|reranker/  # P1/2.2  BGE · Qdrant · cross-encoder
│   │   └── cache/                           # P3.5  semantic cache
│   ├── observability/                       # P3.5/7  @timed profiling · Prometheus metrics
│   ├── evaluation/golden|regression/        # P3    ⭐ Hit@k/MRR/NDCG · judge · RAGAS · A/B
│   ├── safety/                              # P5    PII · injection · sanitize · circuit breaker
│   ├── plugins/                             # P8    registry + Port enforcement
│   ├── lifecycle/                           # P7    embedding re-embed / migration
│   ├── presentation/api/                    # FastAPI routers & schemas
│   └── main.py                              # Composition root — currently just /health
├── tests/                                    # mirrors app/ 1:1 — see tests/README.md
├── experiments/lora/                         # P6    manual LoRA layer + Qwen2.5 training
├── ops/serving/                              # P7    vLLM serving config
├── examples/                                 # P8    one runnable example per technique
├── docs/                                     # P8    architecture docs for contributors
├── Learning-document/
│   ├── LEARNING_ROADMAP.md                  # ★ the full learning path
│   └── notes/                               # design-system · algorithms · glossary · bug-log
├── CONTRIBUTING.md                           # Core↔Cloud line + 6-step-loop rule for PRs
├── docker-compose.yml                        # redis + qdrant + core-api
├── Dockerfile                                # slim core-API image
├── requirements.txt                          # slim; each phase adds its own deps
└── LICENSE                                   # MIT
```

---

## ⚡ Tech Stack (target)

| Layer | Technology |
|---|---|
| API | FastAPI (Python 3.11) · Pydantic v2 |
| Vector / RAG | **Qdrant** · `BAAI/bge-m3` embeddings (1024-dim, multilingual) · Hybrid + RRF + cross-encoder rerank (`bge-reranker-v2-m3`) + CRAG · metadata filtering · semantic chunking |
| Inference | `LLMClientBase` → Ollama / Apple MLX (dev) · vLLM / Cloud API (scale) |
| Agent framework | LangGraph (Supervisor–Worker, multi-agent, human-in-the-loop, tracing, MCP) |
| Evaluation | **RAGAS** + hand-built retrieval metrics (Hit@k/MRR/NDCG) + custom LLM judge + A/B |
| Fine-tuning | LoRA/QLoRA on `Qwen2.5-7B` · GGUF quantization · embedding/domain fine-tuning |
| Safety | prompt-injection defense · PII redaction · toxicity moderation · output sanitization · circuit breaker |
| Async jobs | Celery 5 + Redis 7 broker |
| MLOps | vLLM/TGI serving · LangFuse · Prometheus + Grafana · CI/CD retrain |
| Visual / Video — *OPTIONAL* | ComfyUI · Flux / SDXL · ControlNet · XTTS / CosyVoice · ffmpeg *(needs GPU)* |
| Containers | Docker Compose |
| License | MIT |

---

## 🗺️ Roadmap — the Learning Path

Phases are ordered so each teaches a layer of the stack from scratch. **Status is honest, not aspirational — after the 2026-07 reset, everything is being rebuilt by hand.** Numbering matches the detailed **[LEARNING_ROADMAP.md](./Learning-document/LEARNING_ROADMAP.md)**. **CORE** phases are the main path; **CLOUD** (Phase 9) is a separate commercial layer; the **OPTIONAL** Visual track sits off to the side.

| Phase | Track | Theme | What you build & learn | Status |
|---|---|---|---|---|
| **0. Foundation & Ingestion** | CORE | Data connector → clean → **chunk · dedup · incremental ingest** | Plugin architecture, recursive/semantic chunking, dedup (hash + edit-distance) | ⏳ **Start here** |
| **1. Vector Memory** | CORE | `bge-m3` + Qdrant + multi-namespace | Embedding math, cosine similarity **by hand**, mandatory-`tenant_id` isolation | ⏳ Rebuild |
| **2. Advanced Retrieval** | CORE | Hybrid + RRF + rerank + CRAG, then metadata filter · MMR · query transform · temporal · Adaptive/Self-RAG · GraphRAG | RRF & rerank math, bi- vs cross-encoder, graph workflows — each retriever **built by hand** | ⏳ Rebuild |
| **3. Evaluation Framework** ⭐ | CORE | RAGAS + custom LLM judge + hand-built Hit@k/MRR/NDCG + golden/regression + A/B + cost/latency | **Whether each Phase-2 technique truly helps** — the central loop | ⏳ Planned |
| **3.5 Query Performance** | CORE | Latency profiling · HNSW tuning · quantization · payload indexing · semantic caching | Measure-then-optimize; recall ↔ latency trade-offs | ⏳ Planned |
| **4. Agentic Orchestrator** | CORE | LangGraph Supervisor–Worker (Researcher → Creator → **Critic**) · **Comment Assistant** e2e · HITL · intent triage · memory · abstention · tracing (LangFuse) · MCP | Multi-agent design, grounding & anti-hallucination, HITL | ⏳ Planned |
| **5. Safety & Guardrails** | CORE | Prompt-injection defense · PII redaction · toxicity moderation · output sanitization · red-teaming · circuit breaker | Hardening an LLM that ingests untrusted user comments | ⏳ Planned |
| **6. Fine-tuning** | CORE | **LoRA/QLoRA** on `Qwen2.5-7B` · synthetic data · GGUF merge · embedding/domain tuning | Low-rank update math (a LoRA layer in raw PyTorch), quantization | ⏳ Planned |
| **7. Production & MLOps** | CORE | vLLM/TGI serving · Prometheus + Grafana · data lifecycle · drift detection · CI/CD · canary | Observability, reproducible ML, keeping a KB correct over time | ⏳ Planned |
| **8. Extensibility & Community** | CORE | Plugin system · niche templates · benchmark suite · docs · runnable examples | Open-source extensibility, port/adapter registry design | ⏳ Planned |
| **9. SaaS Bridge** | **CLOUD** | Usage metering · feature/entitlement ports · multi-tenancy enforcement · wallet (2-phase hold/settle) | The commercial shell — **a separate layer, never inside the core brain** | ⏳ Future · separate repo |
| **★ Visual & Character Engine** | **OPTIONAL** | ComfyUI + IP-Adapter/FaceID + character LoRA · Flux/SDXL + ControlNet · image/text→video · TTS clone · ffmpeg | Consistency techniques, diffusion control, video pipeline | 🧩 Add-on · needs GPU |

### Phase 2 in depth — Advanced RAG, every technique togglable per query

The whole point is to build each technique **by hand** (pure Python over `LLMClientBase` + `qdrant-client`, LangGraph for flow only) and then **measure whether it actually helps** in Phase 3 — *learning RAG without measuring is learning blind.*

| Technique | What it does | What you learn |
|---|---|---|
| **Hybrid Search** (dense + sparse/BM25) | run semantic + keyword retrieval together | when dense beats sparse and vice-versa |
| **RRF** (Reciprocal Rank Fusion) | merge several ranked lists into one | the RRF formula by hand; fusing rankings |
| **Cross-encoder reranking** (`bge-reranker-v2-m3`) | re-score top-k by reading query+doc *together* | why reranking lifts top-k most; **bi- vs cross-encoder** |
| **CRAG** (Corrective RAG) via LangGraph | grade retrieved context, then retry / widen | self-scoring context; self-correcting loops; state machines |
| **Metadata filtering** (vector + filter) | filter to the right product *before* semantic search | structured filter + vector search — **used live in the Comment Assistant** |
| **MMR** (retrieval diversity) | avoid a top-k of near-duplicate chunks | maximal marginal relevance (a priority-queue drill) |
| **Query Transformation** (Multi-Query · HyDE · Step-back) | expand / rewrite the query before search | the query↔document space mismatch |
| **Temporal / freshness-aware** | weight recency, not just relevance | time-decay scoring; a per-niche flag |
| **Context Compression** + lost-in-the-middle | trim to answering sentences; order for the window | cutting noise; token budgeting |
| **Adaptive-RAG / Self-RAG** | decide *whether to retrieve at all* up front | CRAG's sibling; routing before retrieval |
| **GraphRAG** (knowledge graph + multi-hop) | answer questions that join several facts | where pure vector search is weak; graph traversal |

Every technique is a **per-query flag, default off**, so you can A/B *with* vs *without* and read the metrics. The **evaluation framework** comes up early (Phase 3) because you can't choose flags wisely without it.

---

## 🚀 Quick Start

Right now this boots the **skeleton** — a health endpoint plus Redis + Qdrant, ready for the phases to build on.

```bash
git clone https://github.com/nnkienn/nyxara-core.git
cd nyxara-core
cp .env.example .env
docker compose up -d --build      # spins up redis + qdrant + core-api

curl http://localhost:8100/health
# {"status":"ok","service":"nyxara-core"}
```

| Service | URL |
|---|---|
| Core API | http://localhost:8100 |
| Qdrant (vector DB) | http://localhost:6353 |
| Redis (broker) | localhost:6399 |

> **Next:** open [LEARNING_ROADMAP.md](./Learning-document/LEARNING_ROADMAP.md) and start at **Phase 0** —
> hand-build the chunker, plant a bug, debug it, test it, document it. Features light up as you build them.

---

## 🔐 Non-Negotiable Engineering Rules

These are **constitutional**. PRs that violate them are auto-rejected.

- ✋ **Hand-build before you import.** Every core technique ships with a from-scratch implementation and its tests *before* a library replaces it. A black-box core kills an open-source project.
- 📏 **Measure before you enable.** Every RAG technique is a per-query flag, default **off**; it turns on only when Phase-3 eval shows it helps on the golden set. No "I heard it's good."
- 🛡️ **Namespace everywhere.** Every Vector DB op, cache key, and audit log MUST carry a `tenant_id` namespace so niches never bleed into each other.
- 🧠 **Single embedding model.** `BAAI/bge-m3` is the only embedding allowed — no per-language model, no OpenAI ada.
- 🔌 **`LLMClientBase` abstraction.** Agents call `client.complete(...)` — never `openai.ChatCompletion.*` or `transformers` directly.
- ✅ **TDD mandatory.** Red → Green → Refactor. RAG/Agent logic needs **cross-language tests** (VN, EN, DE, CN); every fixed bug becomes a permanent regression test.
- 🏛️ **Core stays pure.** No `import stripe`, auth, or billing in the core — the commercial layer is separate (Phase 9).
- 🙋 **Human-in-the-loop, no auto-publish.** Drafts go to a person to approve, edit, or reject. Nothing is sent autonomously; when content *is* sent, it uses the platform's **official API** — never browser automation / stealth posting.
- 🌾 **Zero-hardcode data sources.** Scraping/ingest targets live in config, public pages only, robots.txt respected.

---

<div align="center">

**License:** [MIT](LICENSE) · Free to use, fork, modify, and self-host. Built for the open-source AI community. 🌍

📞 **nnkienn@gmail.com**

</div>

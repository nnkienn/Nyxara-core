# ⚖️ TECH STACK RULE — n-assistant-core (OPEN-SOURCE · SINGLE REPO)

> **Status:** Constitutional for this repo. A PR that violates any rule below is auto-rejected.
> **License of this repo:** MIT (public, open-source).
> **Companion docs:** [`../docs/product-requirements.md`](../docs/product-requirements.md) · [`../docs/ai-agent-design.md`](../docs/ai-agent-design.md).

---

## §0. THE GOLDEN RULE — A LOCAL-FIRST, OPEN-SOURCE LEARNING ENGINE

`n-assistant-core` is an **OPEN-SOURCE (MIT)**, modular **Virtual Content
Factory** built as a learning vehicle — fork it for your niche, run it 100%
local. It MUST run standalone in Docker / on a self-hosted box with **zero**
dependency on any external SaaS layer.

It is **not** a commercial product: there is no billing, no user accounts, no
admin dashboard, no second repo. Keep the stack lean and focused:

| Concern | Approved technology |
|---|---|
| Language | **Python 3.11** |
| Web framework | **FastAPI** + Uvicorn |
| ORM / local DB | **SQLAlchemy** (+ Alembic migrations), PostgreSQL — for local config, source registry, run history |
| Vector DB | **Qdrant** (`qdrant-client`) |
| Async jobs | **Celery** + **Redis** broker |
| Inference | `LLMClientBase` → Ollama / Apple MLX (dev) · vLLM / Cloud API (scale) |
| Fine-tuning | LoRA on `Qwen2.5-7B` · GGUF quantization merge (Phase 4) |
| Visual / Video | ComfyUI · SDXL / Flux · ControlNet · XTTS / CosyVoice · ffmpeg (Phase 5) |
| Eval / MLOps | RAGAS + custom metrics · LangFuse / Prometheus + Grafana · DVC / W&B / MLflow (Phase 7, light) |

Adding anything outside this list requires a note in the architecture spec.

---

## §1. OUT OF SCOPE BY DESIGN

This is a learning engine, not a SaaS. The following are **not built here** — not
because they belong in another repo, but because they are simply not the goal:

| # | Out of scope |
|---|---|
| 1.1 | Billing / invoicing / metered-charge / credit-wallet logic (`import stripe`, `TenantCredits`, etc.). Token counting emits **usage metadata for observability only** — there is nothing to debit. |
| 1.2 | User authentication, login/signup, password/passkey handling, OAuth flows, session issuance for end users. |
| 1.3 | A multi-user SaaS dashboard / RBAC admin panel / subscription-plan UI. |

A user-facing UI, if ever added, is a **thin optional** Streamlit/Gradio panel
that calls the same local API — it never becomes a tenancy/billing system.

> **`tenant_id` is a NAMESPACE, not a customer.** It lets one install host
> several niches/users side by side in Qdrant. The engine trusts and enforces it
> on every DB/Vector path; it does **not** manage identity, auth, or money.

---

## §2. WHAT THE ENGINE OWNS

- FastAPI orchestrator (`app/api`), domain/services logic (`app/services`),
  shared config & infra wiring (`app/core`).
- Harvester subsystem (`app/infrastructure/harvester/`) — see §4.
- RAG pipeline: chunking → embedding → Qdrant upsert/search (always with a
  `tenant_id` namespace payload filter); Hybrid + RRF + CRAG as it matures.
- LangGraph Supervisor–Worker agent graph (see `ai-agent-design.md`), growing a
  Visual Director + Video Producer in Phase 5–6.
- Celery workers for ingest / embedding / fine-tuning / video / long-running tasks.
- All LLM access goes through a single `LLMClientBase` abstraction — never call
  `openai.*` / `anthropic.*` / `transformers.pipeline(...)` directly.

---

## §3. ENFORCEMENT

| # | Rule |
|---|---|
| 3.1 | A CI job greps for forbidden patterns (`import stripe`, end-user auth/login flows, raw `openai.*`/`transformers.pipeline` in agent code) and **fails the build** on a match. |
| 3.2 | Approved dependencies only. Adding anything outside §0 requires a note in the architecture spec. |
| 3.3 | The engine MUST start and pass `GET /health` fully standalone, with no external SaaS secrets present. |
| 3.4 | When `INFERENCE_MODE=self_hosted`, no outbound HTTPS to OpenAI/Anthropic/Gemini (privacy-by-default for a local fork). CI greps to verify. |

---

## §4. Harvester (Phase 0 — Data Ingestion, binding)

| # | Rule |
|---|---|
| 4.1 | **Data Ingestion ≠ Inference.** The Harvester MUST NOT call an LLM, import agent code, or share a process with the agent graph. It only acquires and lands data. |
| 4.2 | **Zero-hardcode sources.** Every scraping target lives in `scraper_config.yaml` (URL, selectors, cadence, locale, `tenant_id`). A hardcoded URL literal in Python is an instant reject. |
| 4.3 | **Public data only.** Never scrape login-walled or private content. Respect `robots.txt` / platform ToS; rate-limit per source. |
| 4.4 | **`tenant_id` at the source.** Every harvested raw artifact is stamped with its `tenant_id` namespace at the Harvester layer (first landing). An artifact missing `tenant_id` is discarded, never ingested. |
| 4.5 | Pipeline order is fixed: **Crawl → Raw Data Lake → Filter (Clean) → Qdrant upsert** (with `tenant_id` namespace filter). No skipping the clean stage. |

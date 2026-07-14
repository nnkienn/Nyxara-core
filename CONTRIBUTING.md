# Contributing to nyxara-core

This repo doubles as a learning project and an open-source AI toolkit. Two rules matter more
than usual here.

## 1. Core vs. Cloud line

`nyxara-core` (this repo, MIT) is the niche-agnostic AI brain: RAG, retrieval, agents, eval,
fine-tuning, MLOps. It contains **no billing, no auth, no customer accounts** — `tenant_id` is
a namespace, not a customer. Any commercial layer (Stripe, accounts, dashboards) belongs in a
separate cloud repo that calls this engine's HTTP API. Core exposes **ports**
(`app/domain/ports/`); a cloud layer plugs in **adapters**. PRs that add `import stripe` or
similar billing/auth logic to core will be rejected.

## 2. Every core technique must be hand-implemented before a library replaces it

See [Learning-document/LEARNING_ROADMAP.md](Learning-document/LEARNING_ROADMAP.md) — the
"vòng 6 bước" (6-step loop: hand-code → inject a bug → debug by hand → fix → test → document).
A PR that swaps in a library for a technique that has no hand-built reference implementation
and no test covering its known failure mode will be asked to add both first. This is what
keeps the core forkable and understandable instead of a black box.

## Where things go

Each `app/<layer>/<folder>/README.md` documents which roadmap phase it belongs to and which
files are expected there. Check the folder's README before adding a new file to make sure it
lands in the right layer (`domain` → pure entities/ports, `application` → use cases,
`infrastructure` → adapters to external systems, `presentation` → FastAPI routers).

## Tests

Every bug fixed anywhere becomes a permanent regression test — see
`app/evaluation/regression/` for eval-layer bugs, `tests/` for everything else, mirroring the
`app/` tree.

<div align="center">

# N-Assistant Core 🤖🚀

### Die Open-Source Virtual Content Factory — forke sie für deine Nische, betreibe sie 100% lokal

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-DC244C.svg?logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![Celery](https://img.shields.io/badge/Celery-37814A.svg?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33.svg?logo=playwright&logoColor=white)](https://playwright.dev/)

**Eine modulare, MIT-lizenzierte Engine zum Bauen einer autonomen KI-Content-Pipeline — ernten → erinnern → schlussfolgern → fine-tunen → Visuals erzeugen → veröffentlichen. Läuft vollständig lokal, kein Vendor-Lock-in.**

🌐 🇬🇧 [English](./README.md) · 🇻🇳 [Tiếng Việt](./README.vi.md) · 🇩🇪 **Deutsch** · 🇨🇳 [中文](./README.zh.md)

</div>

---

## 🎯 Projektvision

**N-Assistant Core** ist eine Open-Source **Virtual Content Factory**: eine modulare KI-Engine, die du **für deine eigene Nische forkst und anpasst** — MMO/Affiliate, Game AI, Beauty, Crypto, Bildung, was auch immer — und **100% lokal** betreibst.

Sie verkettet ein **mehrsprachiges Retrieval-Augmented-Generation (RAG)**-Gehirn mit einem **LangGraph**-Agentengraphen und einem **Playwright**-Automatisierungsarm, sodass eine autonome Pipeline **recherchieren → schreiben → Visuals erzeugen → prüfen → veröffentlichen** kann — auf YouTube, Facebook & Instagram, ohne Mensch in der Schleife und ohne ein einziges Byte an eine Drittanbieter-Cloud zu senden, es sei denn, *du* willst es.

Sie ist als **Vehikel zum tiefen Lernen gebaut, nicht als Produkt zum Verkaufen.** Das Ziel ist, jede Schicht zu *verstehen* — die Embedding-Mathematik, RRF, die Low-Rank-Updates von LoRA, Quantisierung, Agentengraphen, ComfyUI-Konsistenz — indem man sie von Grund auf baut und jede laufende Zeile besitzt.

> **Multi-Nische, kein Multi-Tenant-SaaS.** Eine Installation kann mehrere Nischen nebeneinander beherbergen. Eine `tenant_id` (Namespace) hält das Wissen jeder Nische im Vektorspeicher getrennt — dein MMO-Index läuft nie in deinen Game-AI-Index über. Es gibt **kein Billing, keine Auth, keine kommerzielle Cloud** — nur einen sauberen Namespace, damit du (oder ein Fork) viele Domains aus einer Engine betreiben kannst.

---

## 🔥 Kernfähigkeiten

### 1. 🌾 Pluggable Harvester — Jede Plattform, Community-getrieben
**Das ist Phase 0 — das Fundament, von dem alles andere lebt.** Ein geplanter (Cron) Crawler erfasst **öffentliche** Daten, stempelt sie mit einem `tenant_id`-Namespace, legt sie in einem nischenweisen **Raw Data Lake** ab und reinigt sie dann durch einen 3-Schichten-Anti-Spam-Filter — vollständig von den Agenten entkoppelt (*Datenerfassung ≠ Inferenz*; diese Schicht ruft **nie** ein LLM auf).

**Binde jede Plattform ein — lege eine Datei ab.** Die Engine erkennt zur Laufzeit automatisch jedes Plugin unter [`extractors/plugins/`](./app/infrastructure/harvester/extractors/plugins/). Eine neue Quelle ist eine Klasse — keine Core-Änderungen, keine hartkodierten Imports:

```python
class MyPlatformExtractor(BaseExtractor):
    PLUGIN_TYPE = "my_platform"          # ← referenziert über `type:` in scraper_config.yaml
    async def extract(self) -> list[HarvestedItem]:
        url = self.options["url"]        # alles aus YAML — zero-hardcode
        ...
```

Ein abstürzendes Plugin wird geloggt und übersprungen — eine schlechte Quelle reißt nie den ganzen Lauf nieder.

**Heute ausgeliefert:** `x_twscrape` (X / Twitter via twscrape) · `youtube_shorts` (YouTube Shorts via yt-dlp).
**Wir brauchen deine Hilfe** 🤝 — Plattformen entwickeln ihre Anti-Bot-Abwehr ständig weiter. Trage ein neues Plattform-Plugin bei (TikTok, Instagram, Reddit, LinkedIn…) oder eine frische **Bypass-/Stealth-Technik** für ein bestehendes. Der ganze Vertrag ist eine Datei: [`base.py`](./app/infrastructure/harvester/extractors/base.py).

**3-Schichten-Anti-Spam-Filter** — fail-fast und kostenbewusst; jedes Item muss sich die nächste Schicht verdienen, sodass der bezahlte LLM-Aufruf nur sieht, was bereits zwei kostenlose CPU-Gates überlebt hat:

| Schicht | Stufe | Kosten | Verwirft |
|---|---|---|---|
| **L1** | Heuristik (Hashtag- / Wortzahl- / Mention-Gates) | O(1) CPU | Engagement-Bait, Einzeiler, Mass-Mention-Spam |
| **L2** | Text-Clean (URLs, Emojis, Boilerplate entfernen) | O(n) CPU | nach Reinigung leere Items |
| **L3** | LLM-Judge (gebündelt, OpenAI-kompatibel) | ~1 API-Call / 10 Items | Witze, Replies, Geschwätz mit geringem Wert |

Freigegebene Items landen in `raw_data_lake/filtered/approved.json`, Qdrant-bereit. Quellen und Schwellen leben in [`scraper_config.yaml`](./scraper_config.yaml) → `filter_config`, **nie hartkodiert**.

### 2. 🔀 Dual-Engine-LLM-Router (Lokal + Cloud)
Eine einzige `LLMClientBase` (OpenAI-kompatible) Schnittstelle lässt jeden Agenten auf beiden Engines laufen — **ohne Code-Änderung**:
- **Lokal- / Dev-Stufe:** Ollama oder Apple MLX mit `Qwen2.5` / `Llama-3.1-8B-Instruct` → kostenfreies R&D, vollständig offline.
- **Scale-Stufe:** vLLM auf gemieteter GPU (RunPod, AWS) oder Fallback auf eine Cloud-API für schwere Batches.

Das Routing ist eine **Laufzeit-Konfigurationsentscheidung**, nie ein Rewrite. Derselbe Agenten-Code läuft in beiden Stufen.

### 3. 🧠 Multi-Nische & mehrsprachiges RAG
- **Vektorspeicher:** [Qdrant](https://qdrant.tech/) mit namespace-gebundenen Collections.
- **Embeddings:** `BAAI/bge-m3` (1024-dim, 100+ Sprachen) → ein gemeinsamer sprachübergreifender Index, **keine Collection pro Sprache**.
- **Namespace-Isolation:** jedes `upsert` / `search` trägt einen verpflichtenden `tenant_id`-Payload-Filter, sodass mehrere Nischen/Nutzer in einem Speicher koexistieren — mit **null nischenübergreifendem Durchsickern**, eine Architekturgarantie, keine Laufzeitprüfung.
- **Sprachübergreifendes Retrieval:** eine vietnamesische Nische kann ihre deutschsprachige Wissensbasis in einem Raum abfragen.
- **Was du hier lernst:** Chunking-Strategie, die Embedding-Mathematik, Cosinus-Ähnlichkeit von Hand, dann **Hybrid Search + RRF + Corrective RAG (CRAG)**, wenn das Gehirn reift (Phase 3).

### 4. 🕹️ Supervisor–Worker-Agenten-Topologie
Wir stopfen **nicht** alles in einen riesigen Prompt. Jede Anfrage wird in spezialisierte Rollen zerlegt:

| Rolle | Verantwortung | Werkzeuge |
|---|---|---|
| **Supervisor (Planner)** | Intent zerlegen → geordneter Task-Graph; an Worker routen | Task-Router |
| **Researcher** | Trend-Mining + namespace-gebundene RAG-Abfrage | `search_vector_db(tenant_id, …)` |
| **Creator** | Skript / Copy / Storyboard entwerfen | `generate_text`, `generate_image`, `generate_audio` |
| **Critic** | Stimmen-Review + Claim-vs-Context-Anti-Halluzination | RAG-Verifier (≤ 3 Retry-Schleifen) |
| **Publisher** | Playwright-Auto-Upload auslösen | `publish_to_platform(tenant_id, …)` |

Der Critic prüft die Verankerung, bevor etwas ausgeliefert wird. Wenn die **Visual Engine** landet (Phase 5–6), wächst dieser Graph um einen **Visual Director** und einen **Video Producer**.

### 5. 📡 Omnichannel-Auto-Distribution
**Redis + Celery** leiten asynchrone Jobs an **Playwright**-Headless-Browser, die veröffentlichen und dabei menschliches Verhalten imitieren, um in Plattformlimits zu bleiben:
- YouTube Shorts · Facebook · Instagram Reels.
- Sitzungs-Cookies **AES-256-verschlüsselt** gespeichert (nie im Klartext).
- `playwright-stealth` zur Umgehung von Bot-Erkennung.
- Planung nach Namespace-Zeitzone + Peak-Hour-Heuristik.

---

## 🏗️ Hexagonale Architektur

Der Domain-Kern hängt von nichts ab; die Außenwelt steckt sich über Ports ein. Du kannst Qdrant, die LLM-Engine oder das Web-Framework ersetzen, ohne die Geschäftslogik anzufassen.

```
n-assistant-core/
├── app/
│   ├── domain/                  # Reine Geschäftsentitäten & Ports — null Framework-Deps
│   ├── application/             # Use Cases + Filter-Pipelines (3-Schichten-Anti-Spam)
│   ├── infrastructure/
│   │   └── harvester/           # engine.py · extractors/plugins/ (X, YouTube…) · filters/
│   └── api/                     # Driving Adapter: FastAPI-Router, Schemas, DI-Verdrahtung
├── cli.py                       # ★ Einheitliche CLI — einziger Einstiegspunkt für alle Harvest-Ops
├── scraper_config.yaml          # Harvester-Quellen + Filter-Schwellen — zero-hardcode
├── raw_data_lake/               # Landezone pro Namespace: texts/ (roh) + filtered/ (sauber)
├── docker-compose.yml           # redis + qdrant + core-api (+ Harvester-Profil)
├── Dockerfile · Dockerfile.harvester   # core-API-Image · Chromium-Image für Plugins
├── requirements.txt
└── LICENSE                      # MIT
```

---

## ⚡ Tech-Stack

| Schicht | Technologie |
|---|---|
| API | FastAPI (Python 3.11) · Pydantic v2 · SQLAlchemy 2.x |
| Vector / RAG | **Qdrant** · `BAAI/bge-m3`-Embeddings (1024-dim, mehrsprachig) · Hybrid + RRF + CRAG |
| Inferenz | `LLMClientBase` → Ollama / Apple MLX (dev) · vLLM / Cloud-API (scale) |
| Fine-tuning | LoRA auf `Qwen2.5-7B` · GGUF-Quantisierungs-Merge (Q4/Q5/Q8) |
| Visual / Video | ComfyUI · Flux / SDXL · ControlNet · IP-Adapter / FaceID · XTTS / CosyVoice · ffmpeg |
| Agenten-Framework | LangGraph (Supervisor–Worker, Multi-Agent) |
| Async-Jobs | Celery 5 + Redis-7-Broker |
| Automatisierung | Playwright + `playwright-stealth` |
| Eval / MLOps | RAGAS + Custom-Metriken · LangFuse / Prometheus + Grafana · DVC / W&B / MLflow (leicht) |
| ML-Runtime | PyTorch (MPS auf Mac, CUDA auf Linux-GPU) |
| Container | Docker Compose (Profile: default, harvester) |
| Lizenz | MIT |

---

## 🗺️ Roadmap — Ein Lernpfad, Phasen 0→8

Die Phasen sind so geordnet, dass jede eine Schicht des Stacks von Grund auf lehrt. Der Status ist ehrlich, nicht aspirational.

| Phase | Thema | Was du baust & lernst | Status |
|---|---|---|---|
| **0. Fundament** | Daten-Crawling-Pipeline (rohes JSON aus X, YouTube, Web) · sauberes MIT-Repo · Beispiele pro Nische | Plugin-Architektur, Zero-Hardcode-Config, 3-Schichten-Filter | 🟢 Fertig |
| **1. Skelett** | FastAPI-Core, `/health`, Docker, einheitliche CLI | Hexagonale Architektur, Container-Workflow | ✅ Fertig |
| **2. Vektor-Gedächtnis** | Chunking + `bge-m3` + Qdrant + Multi-Namespace | Embedding-Mathematik, Cosinus-Ähnlichkeit **von Hand**, Namespace-Isolation | 🚧 In Arbeit |
| **3. Advanced RAG** | Hybrid Search + **RRF** + **Corrective RAG (CRAG)** via LangGraph · Domain-Adapter pro Nische | RRF-Mathematik, Graph-Workflows, Retrieval-Korrektur | ⏳ Als Nächstes |
| **4. Fine-tuning** | **LoRA** auf `Qwen2.5-7B` · Multi-Domain-Dataset (Basis + pro Nische) · GGUF-Merge | Low-Rank-Update-Mathematik, Quantisierung, Dataset-Design | ⏳ Geplant |
| **5. Visual & Character Engine** | ComfyUI + IP-Adapter / FaceID + Character-LoRA · Flux/SDXL + ControlNet · Image/Text→Video · Lip-Sync + TTS-Clone (XTTS/CosyVoice) · ffmpeg-Auto-Edit | Konsistenztechniken, Diffusionssteuerung, Video-Pipeline | ⏳ Geplant |
| **6. Agentic Orchestrator** | LangGraph-Multi-Agent (Researcher → Script Writer → Visual Director → Video Producer → Critic) · **Domain-Router** · Tool-Calling | Multi-Agent-Design, Nischen-Routing | ⏳ Geplant |
| **7. Production, MLOps & Eval** | Voller Docker-Stack (Qdrant + Ollama + ComfyUI + FastAPI + Redis) · **RAGAS** + Custom-Metriken · Monitoring/Logging (LangFuse, Prometheus + Grafana) · `config.yaml` · CI/CD-Retrain · Experiment-Tracking (W&B / MLflow) · Dataset-/Adapter-/Prompt-Versionierung (DVC / HF Hub) | Eval-Frameworks, Observability, leichtes MLOps | ⏳ Geplant |
| **8. Community & Erweiterbarkeit** | Nischen-Templates (MMO, Game AI, Tech, Bildung…) · Plugin-Architektur (Scraper / Visual / TTS) · Beispielprojekte | OSS-Erweiterbarkeit, Plugin-Design | ⏳ Geplant |

### Was du tief lernst
- **Mathematik:** Embeddings, Cosinus-Ähnlichkeit, RRF, Low-Rank-Adaptation (LoRA), Quantisierung.
- **Architektur:** Advanced RAG, Agentic Workflows (LangGraph), Vektor-DB, Multi-Namespace.
- **Production:** Fine-tuning, Quantisierung, Pipeline-Orchestrierung, Evaluation, leichtes MLOps.
- **Visual AI:** ComfyUI-Workflows, ControlNet, Charakter-/Identitätskonsistenz.
- **Engineering:** modularer Code, Docker, API-Design, Open-Source-Best-Practices.

---

## 🚀 Schnellstart

```bash
git clone https://github.com/nnkienn/n-assistant-core.git
cd n-assistant-core
docker compose up -d          # startet redis + qdrant + core-api

curl http://localhost:8000/health
# {"status":"ok","service":"core-api-opensource"}
```

Das war's — eine vollständige lokale KI-Engine auf `http://localhost:8000`.

| Dienst | URL |
|---|---|
| Core API (RAG / LLM) | http://localhost:8000 |
| Qdrant (Vektor-DB) | http://localhost:6333 |
| Redis (Broker) | localhost:6379 |

📖 **[docs/HARVESTER_GUIDE.md](./docs/HARVESTER_GUIDE.md)** — Phase-0-Deep-Dive: Plugin-Architektur, CLI-Referenz, wie man in 30 Minuten einen neuen Scraper hinzufügt.

**Die Daten-Pipeline ausführen** — ernten, dann filtern, **vollständig über Docker** (kein lokales Python, kein venv). Ein dünner Wrapper führt die einheitliche `cli.py` *innerhalb* des Harvester-Containers aus:

```bash
# Linux / macOS: ./nassistant.sh <befehl>      Windows: .\nassistant.ps1 <befehl>

# Alle registrierten Plugins + ihren An/Aus-Status in config/scraper_config.yaml zeigen
./nassistant.sh list-plugins

# Ernten: jede aktivierte Quelle scrapen → Raw Data Lake
./nassistant.sh harvest

# Eine einzelne benannte Quelle ernten (erst dry-run zur Vorschau)
./nassistant.sh harvest --source yt-long-matt-wolfe --dry-run
./nassistant.sh harvest --source yt-long-matt-wolfe

# Alle Quellen eines Plugin-Typs ernten, je 5 Items begrenzt
./nassistant.sh harvest --type youtube_long --limit 5

# Filtern: die 3-Schichten-Anti-Spam-Pipeline über alle geernteten Daten laufen lassen
./nassistant.sh filter

# Nur YouTube-Long-Video-Segmente filtern
./nassistant.sh filter --type youtube_long
```

Führe `./nassistant.sh --help` oder `./nassistant.sh <befehl> --help` aus, um alle Optionen zu sehen.

> **Schicht 3 ruft ein LLM auf**, also setze zuerst `INFERENCE_PROVIDER` / `INFERENCE_BASE_URL` / `INFERENCE_MODEL` / `INFERENCE_API_KEY` in `.env` — Gemini, OpenAI oder lokales Ollama (jeder OpenAI-kompatible Endpunkt). Schichten 1–2 sind reine CPU und laufen ohne Key.

<details>
<summary>Lieber rohes <code>docker compose</code>? (kein Wrapper)</summary>

Der Wrapper ist nur ein Einzeiler um `docker compose run`. Das Harvester-Image liefert `cli.py` mit, sodass jeder Unterbefehl funktioniert:

```bash
docker compose --profile harvester run --rm harvester python cli.py list-plugins
docker compose --profile harvester run --rm harvester python cli.py harvest
docker compose --profile harvester run --rm harvester python cli.py filter
```

</details>

---

## 🔐 Nicht verhandelbare Engineering-Regeln

Diese sind **konstitutionell**. PRs, die sie verletzen, werden automatisch abgelehnt.

- 🛡️ **Namespace überall.** Jede Vector-DB-Op, jeder Cache-Key und jeder Audit-Log MUSS einen `tenant_id`-Namespace tragen, damit Nischen/Nutzer nie ineinander durchsickern.
- 🧠 **Ein einziges Embedding-Modell.** `BAAI/bge-m3` ist das einzig erlaubte Embedding — kein Modell pro Sprache, kein OpenAI ada.
- 🔌 **`LLMClientBase`-Abstraktion.** Agenten rufen `client.complete(...)` — nie `openai.ChatCompletion.*` oder `transformers` direkt.
- ✅ **TDD verpflichtend.** Red → Green → Refactor. RAG/Agent-Logik braucht **sprachübergreifende Tests** (VN, EN, DE, CN).
- 🔒 **Verschlüsselter Sitzungs-Tresor.** Playwright-Cookies → AES-256 → Speicher. Nie im Klartext.
- 🌾 **Zero-Hardcode-Harvesting.** Scraping-Ziele leben in `scraper_config.yaml`, nur öffentliche Seiten, robots.txt respektiert.

---

<div align="center">

**Lizenz:** [MIT](LICENSE) · Frei zu nutzen, zu forken, zu ändern und selbst zu hosten. Gebaut für die Open-Source-KI-Community. 🌍

📞 **nnkienn@gmail.com**

</div>

<div align="center">

# N-Assistant Core 🤖🚀

### 开源虚拟内容工厂 — 为你的细分领域 fork，100% 本地运行

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-DC244C.svg?logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![Celery](https://img.shields.io/badge/Celery-37814A.svg?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33.svg?logo=playwright&logoColor=white)](https://playwright.dev/)

**一个模块化、MIT 许可的引擎，用于构建自治 AI 内容流水线 — 采集 → 记忆 → 推理 → 微调 → 生成视觉 → 发布。完全本地运行，无厂商锁定。**

🌐 🇬🇧 [English](./README.md) · 🇻🇳 [Tiếng Việt](./README.vi.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇨🇳 **中文**

</div>

---

## 🎯 项目愿景

**N-Assistant Core** 是一个开源的**虚拟内容工厂**：一个模块化 AI 引擎，你可以**为自己的细分领域 fork 并定制** — MMO/联盟营销、游戏 AI、美妆、加密货币、教育，任何领域 — 并**100% 本地运行**。

它将**多语言检索增强生成（RAG）**大脑、**LangGraph** 智能体图与 **Playwright** 自动化臂串联起来，让一条自治流水线能够在 YouTube、Facebook 与 Instagram 上**研究 → 撰写 → 生成视觉 → 审查 → 发布**内容 — 无需人工介入，除非*你*愿意，否则不向任何第三方云发送一个字节。

它被构建为一台**深度学习的载体，而非待售的产品。** 目标是*理解*每一层 — 嵌入数学、RRF、LoRA 的低秩更新、量化、智能体图、ComfyUI 一致性 — 通过从零搭建并掌控运行中的每一行代码。

> **多细分领域，而非多租户 SaaS。** 一次安装可并排承载多个细分领域。一个 `tenant_id`（命名空间）在向量库中保持每个领域知识的隔离 — 你的 MMO 索引绝不会渗入游戏 AI 索引。**没有计费、没有认证、没有商业云** — 只有一个干净的命名空间，让你（或某个 fork）从一个引擎运行多个领域。

---

## 🔥 核心能力

### 1. 🌾 可插拔采集器 — 任意平台，社区驱动
**这是第 0 阶段 — 一切其它东西赖以为生的基础。** 一个定时（cron）爬虫采集**公开**数据，盖上 `tenant_id` 命名空间，落地到按领域划分的**原始数据湖**，再经过 3 层反垃圾过滤器清洗 — 与智能体完全解耦（*数据采集 ≠ 推理*；该层**绝不**调用 LLM）。

**接入任意平台 — 放入一个文件即可。** 引擎在运行时自动发现 [`extractors/plugins/`](./app/infrastructure/harvester/extractors/plugins/) 下的每个插件。新增数据源 = 写一个类 — 无需改动核心，无硬编码导入：

```python
class MyPlatformExtractor(BaseExtractor):
    PLUGIN_TYPE = "my_platform"          # ← 由 scraper_config.yaml 中的 `type:` 引用
    async def extract(self) -> list[HarvestedItem]:
        url = self.options["url"]        # 一切来自 YAML — 零硬编码
        ...
```

崩溃的插件会被记录并跳过 — 一个坏数据源绝不会拖垮整次运行。

**目前已交付：** `x_twscrape`（X / Twitter，经 twscrape）· `youtube_shorts`（YouTube Shorts，经 yt-dlp）。
**我们需要你的帮助** 🤝 — 平台不断升级其反爬防御。请贡献一个新平台插件（TikTok、Instagram、Reddit、LinkedIn…）或为现有插件贡献一项新的**绕过 / 隐身技术**。整个契约就在一个文件里：[`base.py`](./app/infrastructure/harvester/extractors/base.py)。

**3 层反垃圾过滤器** — 快速失败、成本敏感；每个条目必须挣得下一层，因此付费的 LLM 调用只会看到已经通过两道免费 CPU 关卡的内容：

| 层 | 阶段 | 成本 | 丢弃 |
|---|---|---|---|
| **L1** | 启发式（话题标签 / 词数 / @提及 阈值） | O(1) CPU | 互动诱饵、单行句、批量@提及垃圾 |
| **L2** | 文本清洗（去除 URL、表情、模板文字） | O(n) CPU | 清洗后为空的条目 |
| **L3** | LLM 评判（批量，OpenAI 兼容） | 约每 10 条 1 次 API 调用 | 笑话、回复、低价值闲聊 |

通过的条目落地到 `raw_data_lake/filtered/approved.json`，可直接入 Qdrant。数据源与阈值位于 [`scraper_config.yaml`](./scraper_config.yaml) → `filter_config`，**绝不硬编码**。

### 2. 🔀 双引擎 LLM 路由（本地 + 云）
单一的 `LLMClientBase`（OpenAI 兼容）接口让每个智能体在任一引擎上运行而**无需改代码**：
- **本地 / 开发档：** Ollama 或 Apple MLX 运行 `Qwen2.5` / `Llama-3.1-8B-Instruct` → 零成本研发，完全离线。
- **扩展档：** 租用 GPU（RunPod、AWS）上的 vLLM，或在重批量时回退到云 API。

路由是**运行时配置决策**，绝非重写。同一份智能体代码在两档上都能运行。

### 3. 🧠 多细分领域 & 多语言 RAG
- **向量库：** [Qdrant](https://qdrant.tech/)，集合按命名空间隔离。
- **嵌入：** `BAAI/bge-m3`（1024 维，100+ 语言）→ 一个共享的跨语言索引，**无需每种语言一个集合**。
- **命名空间隔离：** 每次 `upsert` / `search` 都携带强制的 `tenant_id` 载荷过滤，因此多个领域/用户在一个库中共存，**零跨领域渗漏** — 是架构保证，而非运行时检查。
- **跨语言检索：** 一个越南语领域可在同一空间中查询其德语知识库。
- **你在这里学到：** 分块策略、嵌入数学、手写余弦相似度，随后随着大脑成熟而进入 **混合检索 + RRF + 纠错式 RAG（CRAG）**（第 3 阶段）。

### 4. 🕹️ 主管–工作者 智能体拓扑
我们**不**把一切塞进一个巨型 prompt。每个请求被分解为专门角色：

| 角色 | 职责 | 工具 |
|---|---|---|
| **主管（规划者）** | 分解意图 → 有序任务图；路由到工作者 | 任务路由器 |
| **研究员** | 趋势挖掘 + 按命名空间的 RAG 查询 | `search_vector_db(tenant_id, …)` |
| **创作者** | 起草脚本 / 文案 / 分镜 | `generate_text`、`generate_image`、`generate_audio` |
| **评论者** | 语气审查 + 主张对上下文的反幻觉 | RAG 校验器（≤ 3 次重试循环） |
| **发布者** | 触发 Playwright 自动上传 | `publish_to_platform(tenant_id, …)` |

评论者在任何内容发出之前校验其依据。当**视觉引擎**落地（第 5–6 阶段），该图会长出 **视觉总监** 与 **视频制片**。

### 5. 📡 全渠道自动分发
**Redis + Celery** 将异步任务排空到 **Playwright** 无头浏览器，在发布时模仿人类行为以保持在平台限额内：
- YouTube Shorts · Facebook · Instagram Reels。
- 会话 cookie 以 **AES-256 加密**存储（绝不明文）。
- `playwright-stealth` 以规避机器人检测。
- 按命名空间时区 + 高峰时段启发式排程。

---

## 🏗️ 六边形架构

领域核心不依赖任何东西；外部世界通过端口插入。你可以替换 Qdrant、LLM 引擎或 Web 框架而不触碰业务逻辑。

```
n-assistant-core/
├── app/
│   ├── domain/                  # 纯业务实体与端口 — 零框架依赖
│   ├── application/             # 用例 + 过滤流水线（3 层反垃圾）
│   ├── infrastructure/
│   │   └── harvester/           # engine.py · extractors/plugins/ (X, YouTube…) · filters/
│   └── api/                     # 驱动适配器：FastAPI 路由、schema、DI 装配
├── cli.py                       # ★ 统一 CLI — 所有采集操作的唯一入口
├── scraper_config.yaml          # 采集器数据源 + 过滤阈值 — 零硬编码
├── raw_data_lake/               # 按命名空间的落地区：texts/（原始）+ filtered/（清洗）
├── docker-compose.yml           # redis + qdrant + core-api（+ harvester profile）
├── Dockerfile · Dockerfile.harvester   # core-API 镜像 · 供插件用的 Chromium 镜像
├── requirements.txt
└── LICENSE                      # MIT
```

---

## ⚡ 技术栈

| 层 | 技术 |
|---|---|
| API | FastAPI (Python 3.11) · Pydantic v2 · SQLAlchemy 2.x |
| Vector / RAG | **Qdrant** · `BAAI/bge-m3` 嵌入（1024 维，多语言）· Hybrid + RRF + CRAG |
| 推理 | `LLMClientBase` → Ollama / Apple MLX（dev）· vLLM / Cloud API（scale） |
| 微调 | 在 `Qwen2.5-7B` 上做 LoRA · GGUF 量化合并（Q4/Q5/Q8） |
| 视觉 / 视频 | ComfyUI · Flux / SDXL · ControlNet · IP-Adapter / FaceID · XTTS / CosyVoice · ffmpeg |
| 智能体框架 | LangGraph（主管–工作者，多智能体） |
| 异步任务 | Celery 5 + Redis 7 broker |
| 自动化 | Playwright + `playwright-stealth` |
| 评估 / MLOps | RAGAS + 自定义指标 · LangFuse / Prometheus + Grafana · DVC / W&B / MLflow（轻量） |
| ML 运行时 | PyTorch（Mac 上 MPS，Linux GPU 上 CUDA） |
| 容器 | Docker Compose（profiles: default, harvester） |
| 许可 | MIT |

---

## 🗺️ 路线图 — 一条学习路径，阶段 0→8

各阶段经过排序，每个阶段从零教授栈的一层。状态是诚实的，而非愿景。

| 阶段 | 主题 | 你构建 & 学到什么 | 状态 |
|---|---|---|---|
| **0. 基础** | 数据爬取流水线（来自 X、YouTube、web 的原始 JSON）· 干净的 MIT 仓库 · 按领域的示例 | 插件架构、零硬编码配置、3 层过滤器 | 🟢 完成 |
| **1. 骨架** | FastAPI 核心、`/health`、Docker、统一 CLI | 六边形架构、容器工作流 | ✅ 完成 |
| **2. 向量记忆** | 分块 + `bge-m3` + Qdrant + 多命名空间 | 嵌入数学、**手写**余弦相似度、命名空间隔离 | 🚧 进行中 |
| **3. 高级 RAG** | 混合检索 + **RRF** + **纠错式 RAG（CRAG）**经 LangGraph · 按领域的 domain adapter | RRF 数学、图工作流、检索纠错 | ⏳ 下一步 |
| **4. 微调** | 在 `Qwen2.5-7B` 上做 **LoRA** · 多领域数据集（基础 + 按领域）· GGUF 合并 | 低秩更新数学、量化、数据集设计 | ⏳ 计划中 |
| **5. 视觉与角色引擎** | ComfyUI + IP-Adapter / FaceID + 角色 LoRA · Flux/SDXL + ControlNet · 图/文→视频 · 唇形同步 + TTS 克隆（XTTS/CosyVoice）· ffmpeg 自动剪辑 | 一致性技术、扩散控制、视频流水线 | ⏳ 计划中 |
| **6. 智能体编排器** | LangGraph 多智能体（研究员 → 脚本作者 → 视觉总监 → 视频制片 → 评论者）· **领域路由器** · 工具调用 | 多智能体设计、领域路由 | ⏳ 计划中 |
| **7. 生产、MLOps & 评估** | 完整 Docker 栈（Qdrant + Ollama + ComfyUI + FastAPI + Redis）· **RAGAS** + 自定义指标 · 监控/日志（LangFuse、Prometheus + Grafana）· `config.yaml` · CI/CD 再训练 · 实验跟踪（W&B / MLflow）· 数据集/适配器/prompt 版本管理（DVC / HF Hub） | 评估框架、可观测性、轻量 MLOps | ⏳ 计划中 |
| **8. 社区与可扩展性** | 领域模板（MMO、游戏 AI、Tech、教育…）· 插件架构（采集器 / 视觉 / TTS）· 示例项目 | 开源可扩展性、插件设计 | ⏳ 计划中 |

### 你将深入学习的内容
- **数学：** 嵌入、余弦相似度、RRF、低秩适配（LoRA）、量化。
- **架构：** 高级 RAG、智能体工作流（LangGraph）、向量数据库、多命名空间。
- **生产：** 微调、量化、流水线编排、评估、轻量 MLOps。
- **视觉 AI：** ComfyUI 工作流、ControlNet、角色/身份一致性。
- **工程：** 模块化代码、Docker、API 设计、开源最佳实践。

---

## 🚀 快速开始

```bash
git clone https://github.com/nnkienn/n-assistant-core.git
cd n-assistant-core
docker compose up -d          # 启动 redis + qdrant + core-api

curl http://localhost:8000/health
# {"status":"ok","service":"core-api-opensource"}
```

就是这样 — 一个完整的本地 AI 引擎运行在 `http://localhost:8000`。

| 服务 | URL |
|---|---|
| Core API (RAG / LLM) | http://localhost:8000 |
| Qdrant (向量库) | http://localhost:6333 |
| Redis (broker) | localhost:6379 |

📖 **[docs/HARVESTER_GUIDE.md](./docs/HARVESTER_GUIDE.md)** — 第 0 阶段深入：插件架构、CLI 参考、如何在 30 分钟内添加一个新爬虫。

**运行数据流水线** — 先采集再过滤，**完全通过 Docker**（无需本地 Python，无需 venv）。一个轻量包装脚本在 harvester 容器*内部*运行统一的 `cli.py`：

```bash
# Linux / macOS: ./nassistant.sh <命令>      Windows: .\nassistant.ps1 <命令>

# 显示所有已注册插件及其在 config/scraper_config.yaml 中的开/关状态
./nassistant.sh list-plugins

# 采集：抓取每个启用的数据源 → 原始数据湖
./nassistant.sh harvest

# 采集单个命名数据源（先 dry-run 预览）
./nassistant.sh harvest --source yt-long-matt-wolfe --dry-run
./nassistant.sh harvest --source yt-long-matt-wolfe

# 采集某一插件类型的全部数据源，每个限 5 条
./nassistant.sh harvest --type youtube_long --limit 5

# 过滤：对全部已采集数据运行 3 层反垃圾流水线
./nassistant.sh filter

# 仅过滤 YouTube Long Video 片段
./nassistant.sh filter --type youtube_long
```

运行 `./nassistant.sh --help` 或 `./nassistant.sh <命令> --help` 查看所有选项。

> **第 3 层调用 LLM**，因此先在 `.env` 中设置 `INFERENCE_PROVIDER` / `INFERENCE_BASE_URL` / `INFERENCE_MODEL` / `INFERENCE_API_KEY` — Gemini、OpenAI 或本地 Ollama（任何 OpenAI 兼容端点）。第 1–2 层仅用 CPU，无需密钥即可运行。

<details>
<summary>更喜欢原生 <code>docker compose</code>？（不用包装脚本）</summary>

包装脚本只是 `docker compose run` 的一行封装。harvester 镜像自带 `cli.py`，因此任何子命令都能用：

```bash
docker compose --profile harvester run --rm harvester python cli.py list-plugins
docker compose --profile harvester run --rm harvester python cli.py harvest
docker compose --profile harvester run --rm harvester python cli.py filter
```

</details>

---

## 🔐 不可妥协的工程规则

这些是**宪法级**的。违反它们的 PR 会被自动拒绝。

- 🛡️ **命名空间无处不在。** 每个向量库操作、缓存键和审计日志都必须携带 `tenant_id` 命名空间，使领域/用户绝不互相渗漏。
- 🧠 **单一嵌入模型。** `BAAI/bge-m3` 是唯一允许的嵌入 — 无按语言的模型，无 OpenAI ada。
- 🔌 **`LLMClientBase` 抽象。** 智能体调用 `client.complete(...)` — 绝不直接调用 `openai.ChatCompletion.*` 或 `transformers`。
- ✅ **TDD 强制。** Red → Green → Refactor。RAG/智能体逻辑需要**跨语言测试**（VN、EN、DE、CN）。
- 🔒 **加密的会话保险库。** Playwright cookie → AES-256 → 存储。绝不明文。
- 🌾 **零硬编码采集。** 采集目标位于 `scraper_config.yaml`，仅公开页面，尊重 robots.txt。

---

<div align="center">

**许可：** [MIT](LICENSE) · 自由使用、fork、修改与自托管。为开源 AI 社区而建。🌍

📞 **nnkienn@gmail.com**

</div>

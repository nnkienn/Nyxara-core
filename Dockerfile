# nyxara-core (MIT, open-source) — FastAPI service
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/root/.cache/huggingface

WORKDIR /app

COPY requirements.txt ./

# Slim skeleton after the 2026-07 reset — no torch/FlagEmbedding yet, so the image is small.
# When a phase adds a heavy dep (e.g. FlagEmbedding → torch), re-add any needed apt build
# packages (build-essential, zlib1g-dev) above this line.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Application code
COPY app ./app

# Tests baked in — CI chạy `pytest` không cần volume mount.
# Local dev: `-v ./tests:/app/tests` để override.
COPY tests ./tests

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

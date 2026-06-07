#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# N-Assistant CLI — Docker wrapper (Linux / macOS)
#
# Runs cli.py *inside* the harvester container, so you never need a local
# Python install or a venv. Everything (deps, Chromium-free scrapers, the
# 3-layer filter) ships in the Dockerfile.harvester image.
#
#   ./nassistant.sh list-plugins
#   ./nassistant.sh harvest --source yt-long-matt-wolfe --dry-run
#   ./nassistant.sh filter --type youtube_long
#
# It's just a one-liner around `docker compose run` — see the raw form below.
# ═══════════════════════════════════════════════════════════════════════════
set -euo pipefail

exec docker compose --profile harvester run --rm harvester python cli.py "$@"

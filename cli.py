"""N-Assistant Core — Unified Harvester CLI (Phase 1).

Single entry point for all data pipeline operations.

Usage
-----
    python cli.py harvest                              # all enabled sources
    python cli.py harvest --source yt-long-matt-wolfe # one source by name
    python cli.py harvest --type youtube_long          # all sources of a type
    python cli.py harvest --type youtube_long --limit 3
    python cli.py harvest --dry-run                    # preview without fetching

    python cli.py filter                               # filter all raw data
    python cli.py filter --type youtube_long           # one pipeline only

    python cli.py list-plugins                         # registry + config status
    python cli.py list-plugins --verbose               # include option details

    python cli.py ingest                               # embed all approved JSON → Qdrant
    python cli.py ingest --file raw_data_lake/filtered/approved.json
    python cli.py search "AI coding assistant"         # query the vector memory
    python cli.py search "..." --tenant tenant_demo --top-k 5
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(
    name="nassistant",
    help="N-Assistant Core CLI — Phase 1: Harvester",
    add_completion=False,
    no_args_is_help=True,
)

# Output path per source type — single source of truth.
_FILTER_OUTPUTS: dict[str, Path] = {
    "x_twscrape":     Path("raw_data_lake/filtered/approved.json"),
    "youtube_shorts": Path("raw_data_lake/filtered/yt_approved.json"),
    "youtube_long":   Path("raw_data_lake/filtered/yt_long_approved.json"),
}


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  harvest                                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════╝

@app.command("harvest")
def cmd_harvest(
    source: Optional[str] = typer.Option(
        None, "--source", "-s",
        help="Run a specific source by name (from config/scraper_config.yaml).",
        show_default=False,
    ),
    plugin_type: Optional[str] = typer.Option(
        None, "--type", "-t",
        help="Filter sources by plugin type (e.g. youtube_long, x_twscrape).",
        show_default=False,
    ),
    limit: Optional[int] = typer.Option(
        None, "--limit", "-l",
        help="Override the items limit for all matched sources.",
        show_default=False,
    ),
    no_cleanup: bool = typer.Option(
        False, "--no-cleanup",
        help="Skip the TTL-based Raw Data Lake cleanup step.",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Resolve config + print matched sources, but do not fetch.",
    ),
) -> None:
    """Fetch raw data from configured sources into the Raw Data Lake."""
    asyncio.run(_harvest(source, plugin_type, limit, no_cleanup, dry_run))


async def _harvest(
    source_name: str | None,
    plugin_type: str | None,
    limit: int | None,
    no_cleanup: bool,
    dry_run: bool,
) -> None:
    from app.core.config import settings
    from app.infrastructure.harvester.engine import HarvesterEngine

    engine = HarvesterEngine()

    # ── Step 1: TTL cleanup ─────────────────────────────────────────────
    if not no_cleanup:
        typer.echo(f"→ Cleaning Raw Data Lake (TTL={settings.RAW_DATA_LAKE_TTL_HOURS}h) ...")
        c = engine.cleanup()
        typer.echo(
            f"   deleted {c['deleted_files']} file(s), "
            f"{c['deleted_dirs']} dir(s)  [{c['skipped']} kept]"
        )

    # ── Step 2: Plugin discovery ────────────────────────────────────────
    typer.echo("\n→ Discovering plugins ...")
    registry = engine.discover_plugins()
    for pt, cls in sorted(registry.items()):
        typer.echo(f"   • {pt:<22} → {cls.__name__}")

    # ── Step 3: Load + filter sources ──────────────────────────────────
    sources = engine.load_sources()

    if source_name:
        sources = [s for s in sources if s.name == source_name]
        if not sources:
            typer.echo(typer.style(
                f"\n[error] No source named '{source_name}' in config/scraper_config.yaml.",
                fg=typer.colors.RED,
            ))
            raise typer.Exit(1)

    if plugin_type:
        sources = [s for s in sources if s.type == plugin_type]
        if not sources:
            typer.echo(typer.style(
                f"\n[error] No sources of type '{plugin_type}' found.",
                fg=typer.colors.RED,
            ))
            raise typer.Exit(1)

    # ── Step 4: Override limit ──────────────────────────────────────────
    if limit is not None:
        for s in sources:
            s.options["limit"] = limit

    enabled  = [s for s in sources if s.enabled]
    disabled = [s for s in sources if not s.enabled]

    typer.echo(f"\n→ Matched sources: {len(enabled)} enabled, {len(disabled)} disabled")
    for s in enabled:
        lim_hint = f"  (limit={s.options.get('limit', '?')})" if limit else ""
        typer.echo(f"   {typer.style('▸', fg=typer.colors.GREEN)} [{s.type}] {s.name}{lim_hint}")
    for s in disabled:
        typer.echo(typer.style(f"   – [{s.type}] {s.name} (disabled)", fg=typer.colors.BRIGHT_BLACK))

    if dry_run:
        typer.echo(typer.style("\n[dry-run] No fetch performed.", fg=typer.colors.YELLOW))
        return

    if not enabled:
        typer.echo("[warn] No enabled sources matched. Nothing to harvest.")
        return

    # ── Step 5: Run ─────────────────────────────────────────────────────
    typer.echo("\n→ Running sources ...\n")
    report: dict = {"sources": [], "total_items": 0, "total_failures": 0}

    for src in enabled:
        # _run_source is called directly to support per-source filtering
        # that engine.run() (which runs ALL sources) doesn't expose.
        result = await engine._run_source(src)
        report["sources"].append(result)
        report["total_items"]    += result["items"]
        report["total_failures"] += 0 if result["status"] == "ok" else 1

    _print_harvest_report(report)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  filter                                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════╝

@app.command("filter")
def cmd_filter(
    plugin_type: str = typer.Option(
        "all", "--type", "-t",
        help=f"Pipeline to run. Choices: all, {', '.join(_FILTER_OUTPUTS)}",
    ),
) -> None:
    """Run the 3-layer anti-spam filter pipeline over harvested raw data."""
    valid = {"all", *_FILTER_OUTPUTS}
    if plugin_type not in valid:
        typer.echo(typer.style(
            f"[error] Unknown type '{plugin_type}'. Valid: {', '.join(sorted(valid))}",
            fg=typer.colors.RED,
        ))
        raise typer.Exit(1)

    asyncio.run(_filter(plugin_type))


async def _filter(plugin_type: str) -> None:
    from app.application.services.filter_pipeline import run_filter_pipeline

    raw_lake = Path("raw_data_lake/texts")
    targets  = list(_FILTER_OUTPUTS.keys()) if plugin_type == "all" else [plugin_type]

    for pt in targets:
        items = _load_raw_items(raw_lake, source_type=pt)
        out   = _FILTER_OUTPUTS[pt]
        typer.echo(f"\n→ Filter [{pt}]: {len(items)} raw item(s) ...")
        approved = await run_filter_pipeline(items, pt, output_path=out)
        _print_filter_summary(len(approved), len(items), out)


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  list-plugins                                                            ║
# ╚══════════════════════════════════════════════════════════════════════════╝

@app.command("list-plugins")
def cmd_list_plugins(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show per-source option details."),
) -> None:
    """List all registered Harvester plugins and their configuration status."""
    from app.infrastructure.harvester.engine import HarvesterEngine

    engine   = HarvesterEngine()
    registry = engine.discover_plugins()
    sources  = engine.load_sources()

    typer.echo(f"\n{'─'*62}")
    typer.echo(f"  Registered plugins  ({len(registry)} discovered)")
    typer.echo(f"{'─'*62}")
    for pt, cls in sorted(registry.items()):
        count = sum(1 for s in sources if s.type == pt)
        typer.echo(f"  {typer.style('✓', fg=typer.colors.GREEN)}  {pt:<24}  {cls.__name__:<30}  ({count} configured)")

    typer.echo(f"\n{'─'*62}")
    typer.echo(f"  Sources in config/scraper_config.yaml  ({len(sources)} total)")
    typer.echo(f"{'─'*62}")

    for s in sources:
        badge = (typer.style(" ON  ", fg=typer.colors.GREEN, bold=True)
                 if s.enabled else typer.style(" OFF ", fg=typer.colors.BRIGHT_BLACK))
        known        = s.type in registry
        type_display = s.type if known else typer.style(s.type + " [unknown!]", fg=typer.colors.RED)
        typer.echo(f"  [{badge}]  {type_display:<24}  {s.name}")

        if verbose:
            for k, v in s.options.items():
                is_secret = any(w in k.lower() for w in ("token", "cookie", "key", "secret", "password", "auth"))
                display   = "***" if is_secret else str(v)
                typer.echo(f"           {typer.style(k, fg=typer.colors.BRIGHT_BLACK)}: {display}")

    typer.echo("")


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  ingest   (Phase 2 — Vector Memory)                                      ║
# ╚══════════════════════════════════════════════════════════════════════════╝

@app.command("ingest")
def cmd_ingest(
    file: Optional[str] = typer.Option(
        None, "--file", "-f",
        help="One approved JSON file. Default: every file in raw_data_lake/filtered/.",
        show_default=False,
    ),
    collection: str = typer.Option(
        "memory", "--collection", "-c", help="Qdrant collection name.",
    ),
    tenant: str = typer.Option(
        "tenant_demo", "--tenant", "-t",
        help="Namespace fallback for items missing tenant_id. MUST match `search --tenant`.",
    ),
) -> None:
    """Chunk → embed (bge-m3) → upsert approved JSON into Qdrant."""
    # Lazy imports: BGEEmbedder pulls torch (~GB) and loads the model. Pay that
    # cost ONLY when this command runs — never on `python cli.py --help`.
    from app.application.services.ingestion import IngestionService
    from app.infrastructure.adapters.bge_embedder import BGEEmbedder
    from app.infrastructure.adapters.qdrant_store import QdrantStore

    files = [Path(file)] if file else list(_FILTER_OUTPUTS.values())
    files = [f for f in files if f.exists()]
    if not files:
        typer.echo(typer.style("[error] No approved JSON found to ingest.", fg=typer.colors.RED))
        raise typer.Exit(1)

    typer.echo("→ Loading bge-m3 (first run downloads ~4.5GB) ...")
    # ── THE EDGE (composition root): concrete adapters are built HERE and
    #    injected into the service. The service itself stays backend-agnostic.
    service = IngestionService(BGEEmbedder(), QdrantStore())

    total = 0
    for f in files:
        n = service.ingest_file(f, collection=collection, tenant_id=tenant)
        typer.echo(f"   {f.name:<30} → {n} chunk(s)")
        total += n
    typer.echo(typer.style(
        f"\n✅ Ingested {total} chunk(s) into '{collection}' (tenant={tenant})",
        fg=typer.colors.GREEN,
    ))


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  search   (Phase 2 — Vector Memory)                                      ║
# ╚══════════════════════════════════════════════════════════════════════════╝

@app.command("search")
def cmd_search(
    query: str = typer.Argument(..., help="The question to search the memory for."),
    collection: str = typer.Option("memory", "--collection", "-c"),
    tenant: str = typer.Option("tenant_demo", "--tenant", "-t", help="Namespace to search within."),
    top_k: int = typer.Option(5, "--top-k", "-k", help="How many results to return."),
) -> None:
    """Search the vector memory: embed the query → nearest chunks in the namespace."""
    from app.infrastructure.adapters.bge_embedder import BGEEmbedder
    from app.infrastructure.adapters.qdrant_store import QdrantStore

    embedder = BGEEmbedder()
    store = QdrantStore()

    # Embed ONLY the query (1 text) — never re-embed the corpus. That's the
    # payoff of storing the vectors: ingest once, search cheaply many times.
    vector = embedder.embed([query])[0]
    hits = store.search(collection, vector, tenant_id=tenant, top_k=top_k)

    if not hits:
        typer.echo(typer.style(
            "No results — empty collection, or --tenant doesn't match the ingested namespace?",
            fg=typer.colors.YELLOW,
        ))
        return

    typer.echo(f"\n→ Top {len(hits)} for {query!r}\n")
    for h in hits:
        text = (h.payload.get("text") or "").replace("\n", " ")[:80]
        typer.echo(f"  {typer.style(f'{h.score:.4f}', fg=typer.colors.GREEN)}  {text}...")


# ── Helpers ──────────────────────────────────────────────────────────────────

def _load_raw_items(lake: Path, source_type: str) -> list[dict]:
    """Load RawEnvelope JSON files for a given plugin type from the Raw Data Lake."""
    import structlog
    log   = structlog.get_logger()
    items = []

    if not lake.exists():
        return items

    for tenant_dir in lake.iterdir():
        if not tenant_dir.is_dir():
            continue
        target = tenant_dir / source_type
        if not target.exists():
            continue
        for f in target.rglob("*.json"):
            try:
                envelope            = json.loads(f.read_text(encoding="utf-8"))
                item                = envelope.get("item", {})
                item["tenant_id"]   = envelope.get("tenant_id")
                item["source_name"] = envelope.get("source_name")
                item["harvest_id"]  = envelope.get("harvest_id")
                items.append(item)
            except Exception as exc:  # noqa: BLE001
                log.warning("load_failed", file=str(f), error=str(exc))
    return items


def _print_harvest_report(report: dict) -> None:
    marks = {"ok": "✅", "failed": "💥", "discarded": "🚫", "skipped": "⏭ ", "unknown_plugin": "❓"}
    typer.echo("\n──────────── HARVEST REPORT ────────────")
    for entry in report["sources"]:
        mark = marks.get(entry["status"], "⚠️ ")
        line = f"{mark} {entry['source']:<42} {entry['status']:<16} items={entry['items']}"
        if entry.get("error"):
            line += f"  ({entry['error'][:80]})"
        typer.echo(line)
    typer.echo("─────────────────────────────────────────")
    typer.echo(
        f"sources={len(report['sources'])}  "
        f"total_items={report['total_items']}  "
        f"failures={report['total_failures']}"
    )


def _print_filter_summary(approved: int, total: int, out: Path) -> None:
    colour = typer.colors.GREEN if approved else typer.colors.YELLOW
    typer.echo(f"  {typer.style(f'{approved}/{total}', fg=colour)} items approved  →  {out}")


if __name__ == "__main__":
    app()

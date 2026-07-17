from app.application.ingestion.pipeline import incremental_ingest


def test_second_run_only_returns_new_chunks(tmp_path):
    seen_path = str(tmp_path / "seen.json")

    incremental_ingest(["mèo", "gà", "chó"], seen_path)
    new_chunks = incremental_ingest(["mèo", "gà", "chó", "chim"], seen_path)

    assert new_chunks == ["chim"]

from app.application.ingestion.deduplicator import dedup_exact


def test_removes_duplicate_chunks():
    # ca hiển nhiên: "mèo" xuất hiện 2 lần -> chỉ còn 1
    result = dedup_exact(["mèo", "chó", "mèo", "chim"])

    assert result == ["mèo", "chó", "chim"]


def test_preserves_first_seen_order():
    result = dedup_exact(["mèo", "chó", "chim", "mèo"])          # ← BẠN ĐIỀN: 1 list có trùng, thứ tự "lộn xộn"

    assert result == ["mèo", "chó", "chim"]               # ← BẠN ĐIỀN: kết quả đúng theo thứ tự lần đầu xuất hiện

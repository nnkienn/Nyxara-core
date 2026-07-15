from app.application.chunking.recursive_chunker import recursive_chunk, split_by_separators


def test_overlap_between_consecutive_chunks():
    chunks = recursive_chunk("ABCDEFGHIJ", size=6, overlap=2)

    assert chunks[0] == "ABCDEF"
    assert chunks[1] == "EFGHIJ"


def test_splits_by_paragraph_then_word():
    text = "Meo thich ngu\n\nCho thich chay"

    result = split_by_separators(text, size=10, separators=["\n\n", " "])

    assert result == ["Meo", "thich", "ngu", "Cho", "thich", "chay"]

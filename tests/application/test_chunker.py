"""Tests for the chunker — pure logic, no model, no I/O → fast & deterministic."""

from app.application.services.chunker import chunk_text


def test_empty_text_returns_no_chunks():
    assert chunk_text("") == []
    assert chunk_text("   ") == []


def test_short_text_is_a_single_chunk():
    text = "This is one short sentence, well under the word limit."
    assert chunk_text(text) == [text]  # nhánh 1: ≤ max_words → để nguyên


def test_long_text_splits_into_multiple_chunks():
    text = ". ".join(f"sentence{i} aaa bbb ccc ddd" for i in range(40)) + "."
    chunks = chunk_text(text, max_words=20, overlap_words=8)
    assert len(chunks) > 1  # nhánh 2: dài → cắt


def test_overlap_duplicates_some_content():
    text = ". ".join(f"sentence{i} aaa bbb ccc ddd" for i in range(40)) + "."
    chunks = chunk_text(text, max_words=20, overlap_words=8)
    original_words = len(text.split())
    total_chunk_words = sum(len(c.split()) for c in chunks)
    # overlap repeats the tail of each chunk → total words across chunks > original
    assert total_chunk_words > original_words

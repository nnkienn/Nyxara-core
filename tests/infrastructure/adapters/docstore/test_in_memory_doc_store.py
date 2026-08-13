import pytest

from app.infrastructure.adapters.docstore.in_memory_doc_store import InMemoryDocStore


def test_save_and_get_returns_text():
    store = InMemoryDocStore()
    store.save("t1", "d1", "xin chào")
    assert store.get("t1", "d1") == "xin chào"


def test_delete_then_get_raises():
    store = InMemoryDocStore()
    store.save("t1", "d1", "xin chào")
    store.delete("t1", "d1")
    with pytest.raises(KeyError):
        store.get("t1", "d1")


def test_delete_nonexistent_does_not_crash():
    store = InMemoryDocStore()
    store.delete("t1", "d1")  # chưa từng save gì -> guard của bạn phải chặn được, không crash

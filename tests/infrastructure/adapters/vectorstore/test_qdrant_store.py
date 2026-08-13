import pytest
from qdrant_client import QdrantClient

from app.infrastructure.adapters.vectorstore.qdrant_store import QdrantStore


@pytest.fixture
def store():
    # client IN-MEMORY -> không cần Docker, mỗi test 1 kho sạch riêng
    client = QdrantClient(location=":memory:")
    s = QdrantStore(client=client, collection="test", dim=3)

    # nạp 2 điểm CÙNG vector [1,0,0] nhưng KHÁC tenant:
    s.upsert(tenant_id="A", ids=["a1"], texts=["mèo của A"], vectors=[[1.0, 0.0, 0.0]])
    s.upsert(tenant_id="B", ids=["b1"], texts=["chó của B"], vectors=[[1.0, 0.0, 0.0]])
    return s


def test_search_only_returns_own_tenant(store):
    hits = store.search(tenant_id="A", query_vector=[1.0, 0.0, 0.0], top_k=5)

    texts = [h.text for h in hits]

    # TODO (bạn điền 2 assert):
    assert "mèo của A" in texts
    assert "chó của B" not in texts
    #   1. text của A PHẢI có mặt trong kết quả
    #   2. text của B KHÔNG được lộ ra (đây là điểm mấu chốt của tenant isolation)


def test_search_returns_original_doc_id_not_internal_uuid(store):
    # HybridRetriever cần ghép doc_id giữa QdrantStore (dense) và BM25Index (sparse) —
    # nếu search() trả UUID nội bộ (uuid5) thay vì doc_id gốc, 2 danh sách sẽ không bao giờ
    # khớp id với nhau, RRF coi mọi doc là khác nhau hoàn toàn (silent failure, không crash).
    hits = store.search(tenant_id="A", query_vector=[1.0, 0.0, 0.0], top_k=5)

    assert hits[0].id == "a1"
def test_delete_removes_own_tenant_doc(store):
    store.delete("A", "a1")
    hits = store.search(tenant_id="A", query_vector=[1.0, 0.0, 0.0], top_k=5)
    assert hits == []

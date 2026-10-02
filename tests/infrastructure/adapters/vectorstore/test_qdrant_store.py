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


# ---- Lọc metadata (lát 0, X4) -------------------------------------------------
# Kho nhỏ đã biết đáp án: MỌI điểm cùng vector [1,0,0] -> điểm dense bằng nhau hết,
# nên vb nào lọt ra hay không là do BỘ LỌC quyết, không phải do độ giống.

@pytest.fixture
def legal_store():
    client = QdrantClient(location=":memory:")
    s = QdrantStore(client=client, collection="legal", dim=3)
    v = [1.0, 0.0, 0.0]
    s.upsert(
        tenant_id="A",
        ids=["vb1", "vb2", "vb5"],
        texts=["Nghị định về thuế 2020", "Nghị định về đất 2010", "Thông tư về thuế 2021"],
        vectors=[v, v, v],
        metadatas=[
            {"loai": "Nghị định", "nam": 2020},
            {"loai": "Nghị định", "nam": 2010},
            {"loai": "Thông tư", "nam": 2021},
        ],
    )
    # tenant B có 1 Nghị định -> dùng để kiểm bộ lọc KHÔNG làm lộ tenant khác
    s.upsert(
        tenant_id="B",
        ids=["b_vb"],
        texts=["Nghị định của B"],
        vectors=[v],
        metadatas=[{"loai": "Nghị định", "nam": 2020}],
    )
    return s


def _ids(store, tree):
    hits = store.search(tenant_id="A", query_vector=[1.0, 0.0, 0.0], top_k=10, filter_tree=tree)
    return sorted(h.id for h in hits)


def test_eq_filter_cuts_thong_tu(legal_store):
    # vb5 đúng chủ đề "thuế" vẫn bị cắt vì loai != Nghị định
    assert _ids(legal_store, {"eq": ["loai", "Nghị định"]}) == ["vb1", "vb2"]


def test_and_filter_combines_type_and_year(legal_store):
    tree = {"and": [{"eq": ["loai", "Nghị định"]}, {"gte": ["nam", 2015]}]}
    assert _ids(legal_store, tree) == ["vb1"]


def test_filter_never_leaks_other_tenant(legal_store):
    # b_vb cũng là Nghị định, nhưng khoá tenant ở ngoài cùng nên không lọt
    assert "b_vb" not in _ids(legal_store, {"eq": ["loai", "Nghị định"]})


def test_no_filter_keeps_old_behaviour(legal_store):
    assert _ids(legal_store, None) == ["vb1", "vb2", "vb5"]

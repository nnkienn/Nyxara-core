import pytest
from qdrant_client import QdrantClient

from app.application.retrieval.bm25_index import BM25Index
from app.application.retrieval.hybrid_retriever import HybridRetriever
from app.infrastructure.adapters.vectorstore.qdrant_store import QdrantStore

# ---- X6: đầu-cuối lát 0 ---------------------------------------------------------------
# Qdrant THẬT (bộ nhớ) + BM25 THẬT + HybridRetriever, cùng một cây trung lập.
# Mọi vector giống nhau -> nhánh dense không phân biệt được ai; vb nào sống là do BỘ LỌC quyết.

V = [1.0, 0.0, 0.0]

CORPUS_A = [
    ("vb1", "Nghị định về thuế thu nhập", {"loai": "Nghị định", "nam": 2020}),
    ("vb2", "Nghị định về đất đai", {"loai": "Nghị định", "nam": 2010}),
    ("vb3", "Luật về thuế giá trị gia tăng", {"loai": "Luật", "nam": 2016}),
    ("vb4", "Luật doanh nghiệp", {"loai": "Luật", "nam": 2020}),
    ("vb5", "Thông tư hướng dẫn về thuế", {"loai": "Thông tư", "nam": 2021}),
]
# tenant B: cũng Nghị định, cũng "thuế" -> lọt ra ở bất kỳ ca nào là lộ dữ liệu
CORPUS_B = [("b_vb", "Nghị định về thuế của B", {"loai": "Nghị định", "nam": 2022})]


class FakeEmbedder:
    dim = 3

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [V for _ in texts]


@pytest.fixture
def retriever():
    store = QdrantStore(client=QdrantClient(location=":memory:"), collection="legal", dim=3)
    bm25 = BM25Index()
    for tenant_id, corpus in (("A", CORPUS_A), ("B", CORPUS_B)):
        store.upsert(
            tenant_id=tenant_id,
            ids=[doc_id for doc_id, _, _ in corpus],
            texts=[text for _, text, _ in corpus],
            vectors=[V for _ in corpus],
            metadatas=[meta for _, _, meta in corpus],
        )
        for doc_id, text, meta in corpus:
            bm25.add_document(tenant_id, doc_id, text, meta)
    return HybridRetriever(FakeEmbedder(), store, bm25)


def _ids(retriever, tree):
    result = retriever.search("A", "thuế", top_k=10, filter_tree=tree)
    return sorted(doc_id for doc_id, _ in result)


def test_no_filter_returns_whole_tenant(retriever):
    assert _ids(retriever, None) == ["vb1", "vb2", "vb3", "vb4", "vb5"]


def test_eq_cuts_thong_tu_even_on_topic(retriever):
    # vb5 nói đúng "thuế" nhưng loai = Thông tư -> bị cắt ở CẢ HAI nhánh
    assert _ids(retriever, {"eq": ["loai", "Nghị định"]}) == ["vb1", "vb2"]


def test_and_type_and_year(retriever):
    tree = {"and": [{"eq": ["loai", "Nghị định"]}, {"gte": ["nam", 2015]}]}
    assert _ids(retriever, tree) == ["vb1"]


def test_or_two_types(retriever):
    tree = {"or": [{"eq": ["loai", "Luật"]}, {"eq": ["loai", "Thông tư"]}]}
    assert _ids(retriever, tree) == ["vb3", "vb4", "vb5"]


def test_not_type(retriever):
    assert _ids(retriever, {"not": [{"eq": ["loai", "Nghị định"]}]}) == ["vb3", "vb4", "vb5"]


def test_bare_range_leaf(retriever):
    assert _ids(retriever, {"lt": ["nam", 2015]}) == ["vb2"]


def test_filter_matching_nothing_returns_empty_not_error(retriever):
    assert _ids(retriever, {"eq": ["loai", "Quyết định"]}) == []


@pytest.mark.parametrize(
    "tree",
    [None, {"eq": ["loai", "Nghị định"]}, {"or": [{"eq": ["tenant_id", "B"]}, {"gte": ["nam", 2020]}]}],
)
def test_never_leaks_other_tenant(retriever, tree):
    assert "b_vb" not in _ids(retriever, tree)

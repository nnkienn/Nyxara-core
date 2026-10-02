import pytest

from app.application.retrieval.metadata_filter import leaf_matches, matches

VB1 = {"loai": "Nghị định", "nam": 2020}
VB2 = {"loai": "Nghị định", "nam": 2010}
VB5 = {"loai": "Thông tư", "nam": 2021}


@pytest.mark.parametrize(
    "pred, metadata, expected",
    [
        ({"eq": ["loai", "Nghị định"]}, VB1, True),
        ({"eq": ["loai", "Nghị định"]}, VB5, False),
        ({"gt": ["nam", 2020]}, VB1, False),
        ({"gte": ["nam", 2020]}, VB1, True),
        ({"lt": ["nam", 2015]}, VB2, True),
        ({"lte": ["nam", 2009]}, VB2, False),
    ],
)
def test_leaf(pred, metadata, expected):
    assert leaf_matches(pred, metadata) is expected


def test_leaf_unknown_operator_raises():
    with pytest.raises(ValueError):
        leaf_matches({"like": ["loai", "Luật"]}, VB1)


AND_TREE = {"and": [{"eq": ["loai", "Nghị định"]}, {"gte": ["nam", 2015]}]}
OR_TREE = {"or": [{"eq": ["loai", "Thông tư"]}, {"lt": ["nam", 2015]}]}
NOT_TREE = {"not": [{"eq": ["loai", "Thông tư"]}]}


@pytest.mark.parametrize(
    "pred, metadata, expected",
    [
        # and: phải đúng CẢ HAI
        (AND_TREE, VB1, True),
        (AND_TREE, VB2, False),   # đúng loại, sai năm
        (AND_TREE, VB5, False),   # sai loại
        # or: đúng MỘT là đủ
        (OR_TREE, VB1, False),    # không con nào đúng
        (OR_TREE, VB2, True),     # đúng con thứ hai
        (OR_TREE, VB5, True),     # đúng con thứ nhất
        # not: lật kết quả của con duy nhất
        (NOT_TREE, VB1, True),
        (NOT_TREE, VB5, False),
        # lá trần
        ({"eq": ["loai", "Thông tư"]}, VB5, True),
    ],
)
def test_matches(pred, metadata, expected):
    assert matches(pred, metadata) is expected


def test_same_answer_as_qdrant_on_5_docs():
    # Cùng cây, cùng kho với bản in N8 tối 02/10 -> Qdrant trả ['vb1'] (tenant A).
    # Nhánh BM25 phải ra ĐÚNG như vậy, lệch là hai nhánh lọc khác nhau (lỗi im lặng).
    store = {"vb1": VB1, "vb2": VB2, "vb3": {"loai": "Luật", "nam": 2019}, "vb5": VB5}
    kept = sorted(doc_id for doc_id, meta in store.items() if matches(AND_TREE, meta))
    assert kept == ["vb1"]

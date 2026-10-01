import pytest

from app.infrastructure.adapters.vectorstore.qdrant_filter import to_qdrant_filter


def test_and_of_leaves_goes_to_must():
    pred = {"and": [{"eq": ["loai", "Luật"]}, {"gte": ["nam", 2020]}]}

    assert to_qdrant_filter(pred) == {
        "must": [
            {"key": "loai", "match": {"value": "Luật"}},
            {"key": "nam", "range": {"gte": 2020}},
        ]
    }


def test_or_of_leaves_goes_to_should():
    pred = {"or": [{"eq": ["co_quan", "Quốc hội"]}, {"eq": ["co_quan", "Chính phủ"]}]}

    assert to_qdrant_filter(pred) == {
        "should": [
            {"key": "co_quan", "match": {"value": "Quốc hội"}},
            {"key": "co_quan", "match": {"value": "Chính phủ"}},
        ]
    }


def test_not_of_leaf_goes_to_must_not():
    pred = {"not": [{"eq": ["co_quan", "Bộ Tài chính"]}]}

    assert to_qdrant_filter(pred) == {
        "must_not": [{"key": "co_quan", "match": {"value": "Bộ Tài chính"}}]
    }


def test_bare_match_leaf_is_wrapped_in_must():
    # Qdrant chỉ nhận điều kiện nằm trong must / should / must_not -> lá trần phải được bọc.
    assert to_qdrant_filter({"eq": ["loai", "Luật"]}) == {
        "must": [{"key": "loai", "match": {"value": "Luật"}}]
    }


def test_bare_range_leaf_is_wrapped_in_must():
    assert to_qdrant_filter({"lt": ["nam", 2015]}) == {
        "must": [{"key": "nam", "range": {"lt": 2015}}]
    }


def test_unknown_operator_raises():
    with pytest.raises(ValueError):
        to_qdrant_filter({"like": ["loai", "Luật"]})

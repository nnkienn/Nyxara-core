import pytest

from app.application.retrieval.rrf import reciprocal_rank_fusion


def test_doc_strong_in_both_lists_ranks_first():
    dense_ranked = ["doc2", "doc1", "doc3"]
    bm25_ranked = ["doc1", "doc3", "doc2"]

    result = reciprocal_rank_fusion([dense_ranked, bm25_ranked])
    doc_ids = [doc_id for doc_id, _ in result]

    # doc1: hạng 2 + hạng 1 (đều tay) > doc2: hạng 1 + hạng 3 (mạnh 1 bên, yếu bên kia)
    assert doc_ids == ["doc1", "doc2", "doc3"]


def test_score_matches_hand_calculation():
    dense_ranked = ["doc2", "doc1", "doc3"]
    bm25_ranked = ["doc1", "doc3", "doc2"]

    result = dict(reciprocal_rank_fusion([dense_ranked, bm25_ranked]))

    assert result["doc1"] == pytest.approx(0.032522, abs=1e-5)
    assert result["doc2"] == pytest.approx(0.032266, abs=1e-5)
    assert result["doc3"] == pytest.approx(0.032002, abs=1e-5)


def test_doc_only_in_one_list_still_included():
    dense_ranked = ["doc1", "doc4"]  # doc4 chỉ dense tìm ra
    bm25_ranked = ["doc1"]

    result = dict(reciprocal_rank_fusion([dense_ranked, bm25_ranked]))

    assert "doc4" in result
    # doc4 chỉ được cộng từ 1 nguồn (dense, hạng 2) -> điểm thấp hơn doc1 (cả 2 nguồn, hạng 1+1)
    assert result["doc4"] < result["doc1"]


def test_top_k_truncates_result():
    dense_ranked = ["doc2", "doc1", "doc3"]
    bm25_ranked = ["doc1", "doc3", "doc2"]

    result = reciprocal_rank_fusion([dense_ranked, bm25_ranked], top_k=1)

    assert len(result) == 1
    assert result[0][0] == "doc1"


def test_rank_starts_at_one_not_zero():
    # 1 danh sách, 1 doc duy nhất ở hạng 1 -> RRF = 1/(60+1), không phải 1/(60+0)
    result = dict(reciprocal_rank_fusion([["doc1"]]))
    assert result["doc1"] == pytest.approx(1 / 61, abs=1e-9)

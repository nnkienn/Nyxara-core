import pytest

from app.application.retrieval.bm25_index import BM25Index


def _build_index() -> BM25Index:
    idx = BM25Index()
    idx.add_document("t1", "doc1", "con mèo đen")
    idx.add_document("t1", "doc2", "con chó nâu")
    idx.add_document("t1", "doc3", "mèo và chó")
    return idx


def test_add_document_builds_inverted_index():
    idx = _build_index()
    assert idx.index["t1"]["mèo"] == {"doc1": 1, "doc3": 1}
    assert idx.doc_len["t1"] == {"doc1": 3, "doc2": 3, "doc3": 3}
    assert idx.doc_count["t1"] == 3


def test_idf_higher_for_rarer_term():
    idx = _build_index()
    # "mèo" ở 2/3 doc, "đen" chỉ ở 1/3 doc -> "đen" hiếm hơn -> idf phải cao hơn.
    assert idx._idf("t1", "đen") > idx._idf("t1", "mèo")


def test_idf_zero_for_unknown_term():
    idx = _build_index()
    assert idx._idf("t1", "không_tồn_tại") == 0.0


def test_score_zero_when_term_not_in_doc():
    idx = _build_index()
    assert idx._score("t1", "chó", "doc1") == 0.0


def test_score_matches_hand_calculation():
    idx = _build_index()
    # Tính tay: N=3, df("mèo")=2 -> idf=log(1.6)≈0.470; tf=1, dl=avgdl=3 -> mẫu=2.5
    # score = 0.470 * (1*2.5)/2.5 ≈ 0.470
    assert idx._score("t1", "mèo", "doc1") == pytest.approx(0.470, abs=1e-3)


def test_search_ranks_by_score_descending():
    idx = _build_index()
    results = idx.search("t1", "mèo đen", top_k=5)
    doc_ids = [doc_id for doc_id, _ in results]
    assert doc_ids == ["doc1", "doc3"]  # doc2 không chứa từ nào trong query -> bị loại


def test_search_respects_top_k():
    idx = _build_index()
    results = idx.search("t1", "mèo đen", top_k=1)
    assert len(results) == 1
    assert results[0][0] == "doc1"


def test_tenant_isolation():
    idx = BM25Index()
    idx.add_document("tenant_a", "doc1", "bí mật công ty A")
    idx.add_document("tenant_b", "doc1", "bí mật công ty B")

    # cùng doc_id "doc1" nhưng 2 tenant khác nhau -> index/doc_count phải tách riêng
    assert idx.doc_count == {"tenant_a": 1, "tenant_b": 1}
    assert idx.index["tenant_a"]["bí"] == {"doc1": 1}
    assert idx.index["tenant_b"]["bí"] == {"doc1": 1}

    results = idx.search("tenant_a", "công ty", top_k=5)
    assert len(results) == 1
    assert results[0][0] == "doc1"


def test_remove_document_updates_doc_count():
    idx = _build_index()
    idx.remove_document("t1", "doc1")
    assert idx.doc_count["t1"] == 2

import pytest

from app.infrastructure.adapters.reranker.bge_reranker import BGEReranker


@pytest.fixture(scope="module")
def reranker():
    # scope="module" -> chỉ load model 1 LẦN cho cả file test này.
    return BGEReranker()


def test_score_returns_one_float_per_doc(reranker):
    scores = reranker.score("mèo đen", ["con mèo màu đen dễ thương", "con chó màu nâu"])
    assert len(scores) == 2


def test_relevant_doc_scores_higher_than_irrelevant(reranker):
    scores = reranker.score("mèo đen", ["con mèo màu đen dễ thương", "con chó màu nâu"])
    assert scores[0] > scores[1]

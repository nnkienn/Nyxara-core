from app.application.generation.node import (
    make_generate_node,
    make_grade_node,
    make_retrieve_node,
)


class FakeRetriever:
    def search(self, tenant_id, query, candidate_k, top_k):
        return [("doc1", 4.75), ("doc3", 1.20)]


class FakeDocStore:
    def get(self, tenant_id, doc_id):
        return {"doc1": "con mèo đen", "doc3": "mèo và chó"}[doc_id]


class FakeGrader:
    def __init__(self, grades):
        self._grades = grades

    def grade(self, query, docs):
        return self._grades


class FakeGenerator:
    def generate(self, query, docs):
        return f"trả lời dựa trên {len(docs)} đoạn"


def test_retrieve_node_fills_retrieved_docs_from_ids():
    node = make_retrieve_node(FakeRetriever(), FakeDocStore(), candidate_k=10, top_k=2)

    result = node({"tenant_id": "t1", "query": "mèo đen"})

    assert result == {"retrieved_docs": ["con mèo đen", "mèo và chó"], "candidate_k": 10}


def test_grade_node_computes_verdict_from_grades():
    node = make_grade_node(FakeGrader([True, True, False]))

    result = node({"query": "mèo đen", "retrieved_docs": ["a", "b", "c"]})

    assert result == {
        "verdict": "CORRECT",  # 2/3 ≈ 0.667 >= 0.6
        "grades": [True, True, False],
        "attempts": 1,
    }


def test_grade_node_increments_existing_attempts():
    node = make_grade_node(FakeGrader([False, False, False]))

    result = node(
        {"query": "mèo đen", "retrieved_docs": ["a", "b", "c"], "attempts": 1}
    )

    assert result["attempts"] == 2


def test_generate_node_fills_answer():
    node = make_generate_node(FakeGenerator())

    result = node({"query": "mèo đen", "retrieved_docs": ["a", "b"]})

    assert result == {"answer": "trả lời dựa trên 2 đoạn"}

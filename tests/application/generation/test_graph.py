from app.application.generation.graph import build_graph


class FakeRetriever:
    def search(self, tenant_id, query, candidate_k, top_k):
        return [("doc1", 4.75)]


class FakeDocStore:
    def get(self, tenant_id, doc_id):
        return "con mèo đen"


class AlwaysRelevantGrader:
    def grade(self, query, docs):
        return [True] * len(docs)


class AlwaysIrrelevantGrader:
    def grade(self, query, docs):
        return [False] * len(docs)


class FakeGenerator:
    def generate(self, query, docs):
        return f"trả lời từ {len(docs)} đoạn"


def test_graph_goes_straight_to_generate_when_correct():
    graph = build_graph(
        FakeRetriever(), FakeDocStore(), AlwaysRelevantGrader(), FakeGenerator(), max_attempts=3
    )

    result = graph.invoke({"tenant_id": "t1", "query": "mèo đen", "attempts": 0})

    assert result["verdict"] == "CORRECT"
    assert result["attempts"] == 1
    assert result["answer"] == "trả lời từ 1 đoạn"


def test_graph_retries_then_forces_generate_at_max_attempts():
    graph = build_graph(
        FakeRetriever(), FakeDocStore(), AlwaysIrrelevantGrader(), FakeGenerator(), max_attempts=3
    )

    result = graph.invoke({"tenant_id": "t1", "query": "mèo đen", "attempts": 0})

    # van an toàn: dù verdict vẫn INCORRECT, đạt max_attempts thì vẫn phải ra answer,
    # không được lặp vô hạn.
    assert result["verdict"] == "INCORRECT"
    assert result["attempts"] == 3
    assert result["answer"] == "trả lời từ 1 đoạn"

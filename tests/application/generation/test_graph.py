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

class RecordingRetriever:
    def __init__(self):
        self.candidate_ks = []          # (1) nơi cất nhật ký — cần một thứ chứa được nhiều giá trị theo thứ tự

    def search(self, tenant_id, query, candidate_k, top_k):
        self.candidate_ks.append(candidate_k)                      # (2) ghi candidate_k lần này vào nhật ký
        return [("doc1", 33333)]   # trả gì cũng được, test này không quan tâm nội dung tài liệu


def test_retry_noi_rong_candidate_k():
    retriever = RecordingRetriever()

    graph = build_graph(
        retriever, FakeDocStore(), AlwaysIrrelevantGrader(), FakeGenerator(),
        candidate_k=10, max_attempts=3,
    )

    graph.invoke({"tenant_id": "t1", "query": "mèo đen", "attempts": 0})

    assert retriever.candidate_ks == [10, 20, 40]   # (3) đọc lại nhật ký từ đâu?

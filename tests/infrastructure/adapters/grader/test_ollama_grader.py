from unittest.mock import MagicMock, patch

from app.infrastructure.adapters.grader.ollama_grader import OllamaGrader


def _fake_response(text: str) -> MagicMock:
    mock = MagicMock()
    mock.json.return_value = {"response": text}
    return mock


@patch("app.infrastructure.adapters.grader.ollama_grader.httpx.post")
def test_grade_one_true_when_model_answers_yes(mock_post):
    mock_post.return_value = _fake_response("YES")
    grader = OllamaGrader("http://fake-host:11434")

    assert grader._grade_one("mèo đen", "con mèo đen dễ thương") is True


@patch("app.infrastructure.adapters.grader.ollama_grader.httpx.post")
def test_grade_one_false_when_model_answers_no(mock_post):
    mock_post.return_value = _fake_response("NO")
    grader = OllamaGrader("http://fake-host:11434")

    assert grader._grade_one("mèo đen", "con chó màu nâu") is False


@patch("app.infrastructure.adapters.grader.ollama_grader.httpx.post")
def test_grade_one_handles_lowercase_and_whitespace(mock_post):
    mock_post.return_value = _fake_response("  yes\n")
    grader = OllamaGrader("http://fake-host:11434")

    assert grader._grade_one("mèo đen", "con mèo đen dễ thương") is True


@patch("app.infrastructure.adapters.grader.ollama_grader.httpx.post")
def test_grade_returns_one_bool_per_doc_in_order(mock_post):
    mock_post.side_effect = [_fake_response("YES"), _fake_response("NO")]
    grader = OllamaGrader("http://fake-host:11434")

    result = grader.grade("mèo đen", ["con mèo đen dễ thương", "con chó màu nâu"])

    assert result == [True, False]


@patch("app.infrastructure.adapters.grader.ollama_grader.httpx.post")
def test_grade_one_passes_timeout(mock_post):
    mock_post.return_value = _fake_response("YES")
    grader = OllamaGrader("http://fake-host:11434")

    grader._grade_one("mèo đen", "con mèo đen dễ thương")

    _, kwargs = mock_post.call_args
    assert kwargs["timeout"] == 60.0

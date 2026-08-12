from unittest.mock import MagicMock, patch

from app.infrastructure.adapters.generator.ollama_generator import OllamaGenerator


def _fake_response(text: str) -> MagicMock:
    mock = MagicMock()
    mock.json.return_value = {"response": text}
    return mock


@patch("app.infrastructure.adapters.generator.ollama_generator.httpx.post")
def test_generate_returns_stripped_answer(mock_post):
    mock_post.return_value = _fake_response("  Con mèo của Lan màu đen.  \n")
    generator = OllamaGenerator("http://fake-host:11434")

    answer = generator.generate("Con mèo màu gì?", ["Con mèo của Lan có màu đen."])

    assert answer == "Con mèo của Lan màu đen."


@patch("app.infrastructure.adapters.generator.ollama_generator.httpx.post")
def test_generate_includes_all_docs_in_prompt(mock_post):
    mock_post.return_value = _fake_response("...")
    generator = OllamaGenerator("http://fake-host:11434")

    generator.generate("query", ["doc một", "doc hai"])

    _, kwargs = mock_post.call_args
    prompt = kwargs["json"]["prompt"]
    assert "doc một" in prompt
    assert "doc hai" in prompt


@patch("app.infrastructure.adapters.generator.ollama_generator.httpx.post")
def test_generate_passes_timeout(mock_post):
    mock_post.return_value = _fake_response("...")
    generator = OllamaGenerator("http://fake-host:11434")

    generator.generate("query", ["doc"])

    _, kwargs = mock_post.call_args
    assert kwargs["timeout"] == 60.0

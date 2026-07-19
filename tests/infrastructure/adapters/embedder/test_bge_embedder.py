import pytest

from app.infrastructure.adapters.embedder.bge_embedder import BGEEmbedder


@pytest.fixture(scope="module")
def embedder():
    # scope="module" -> chỉ load model 1 LẦN cho cả file test này, không phải mỗi hàm test.
    return BGEEmbedder()


def test_dim_is_1024(embedder):
    assert embedder.dim == 1024  # ← điền số (đã thấy khi chạy demo lúc nãy)


def test_batch_returns_one_vector_per_text(embedder):
    vectors = embedder.embed(["xin chào", "hello", "con mèo"])

    assert len(vectors) == 3  # ← đưa vào bao nhiêu câu thì phải ra bấy nhiêu vector?


def test_each_vector_has_correct_dimension(embedder):
    vectors = embedder.embed(["xin chào"])

    assert len(vectors[0]) == 1024  # ← mỗi vector phải dài bao nhiêu?

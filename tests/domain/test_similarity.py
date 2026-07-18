from app.domain.similarity import cosine_similarity


def test_45_degree_angle():
    # a=[1,0], b=[1,1] -> đúng ví dụ đã tính tay: cos ~= 0.707 (45 do)
    result = cosine_similarity([1, 0], [1, 1])

    assert round(result, 3) == 0.707

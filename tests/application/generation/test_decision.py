from app.application.generation.decision import decide, route


def test_decide_correct_when_ratio_at_or_above_threshold():
    assert decide([True, True, False]) == "CORRECT"   # 2/3 ≈ 0.667 >= 0.6
    assert decide([True, True, True]) == "CORRECT"


def test_decide_incorrect_when_all_false():
    assert decide([False, False, False]) == "INCORRECT"


def test_decide_ambiguous_when_between_thresholds():
    assert decide([True, False, False]) == "AMBIGUOUS"   # 1/3 ≈ 0.333


def test_route_generate_when_correct_or_ambiguous():
    assert route("CORRECT", attempts=0) == "generate"
    assert route("AMBIGUOUS", attempts=1) == "generate"


def test_route_retrieve_when_incorrect_and_attempts_remain():
    assert route("INCORRECT", attempts=1, max_attempts=3) == "retrieve"


def test_route_generate_when_incorrect_but_max_attempts_reached():
    # van an toàn — không lặp vô hạn khi kho thật sự không có dữ liệu liên quan
    assert route("INCORRECT", attempts=3, max_attempts=3) == "generate"

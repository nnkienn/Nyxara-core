import pytest

from app.evaluation.metrics import hit_at_k, mrr

# Đề nhỏ 3 lần tìm, mỗi lần tìm có MỘT DANH SÁCH văn bản đúng (Zalo: 1 câu có thể nhiều điều đúng).
# Văn bản đúng ở thứ hạng 1 · ở thứ hạng 3 · không có.
RESULTS = [
    ["son_tung", "cover", "remix"],
    ["cover", "remix", "son_tung"],
    ["cover", "remix", "karaoke"],
]
ANSWERS = [["son_tung"], ["son_tung"], ["son_tung"]]


def test_hit_at_1_counts_only_first_rank():
    assert hit_at_k(RESULTS, ANSWERS, 1) == pytest.approx(1 / 3)


def test_hit_at_3_looks_at_all_first_three_ranks():
    assert hit_at_k(RESULTS, ANSWERS, 3) == pytest.approx(2 / 3)


def test_k_larger_than_list_is_fine():
    assert hit_at_k(RESULTS, ANSWERS, 10) == pytest.approx(2 / 3)


def test_all_missed_gives_zero():
    assert hit_at_k(RESULTS, [["x"], ["y"], ["z"]], 3) == 0.0


def test_one_question_is_zero_or_one_not_a_fraction():
    # câu 42 thật: văn bản đúng ở thứ hạng 1 -> cả đề 1 lần tìm được 1/1, không phải 1/42
    assert hit_at_k([["44/2011/tt-bca+2", "44/2005/qh11+50"]], [["44/2011/tt-bca+2"]], 1) == 1.0


def test_hit_counts_once_even_if_two_answers_in_top_k():
    # 2 văn bản đúng cùng lọt top-3 -> lần tìm này vẫn chỉ là 1 lần trúng, không phải 2
    assert hit_at_k([["a", "b", "c"]], [["a", "c"]], 3) == 1.0


def test_hit_with_second_answer_only():
    # văn bản đúng thứ nhất ("z") không có, văn bản đúng thứ hai ("c") có trong top-3 -> trúng
    assert hit_at_k([["a", "b", "c"]], [["z", "c"]], 3) == 1.0


# ---- MRR: mỗi lần tìm cộng 1/thứ hạng của văn bản đúng ĐẦU TIÊN (đếm từ 1), trượt cộng 0, chia số lần tìm ----


def test_mrr_rewards_higher_ranks_more():
    # thứ hạng 1 -> 1 · thứ hạng 3 -> 1/3 · trượt -> 0
    assert mrr(RESULTS, ANSWERS, 3) == pytest.approx((1 + 1 / 3 + 0) / 3)


def test_mrr_single_question_at_rank_two_is_half():
    assert mrr([["cover", "son_tung", "remix"]], [["son_tung"]], 3) == pytest.approx(0.5)


def test_mrr_respects_k_cutoff():
    # văn bản đúng ở thứ hạng 3 nhưng k=2 -> coi như trượt
    assert mrr([["cover", "remix", "son_tung"]], [["son_tung"]], 2) == 0.0


def test_mrr_all_missed_gives_zero():
    assert mrr(RESULTS, [["x"], ["y"], ["z"]], 3) == 0.0


def test_mrr_separates_same_hit_different_rank():
    # Lan: luôn thứ hạng 1 · Minh: luôn thứ hạng 3 -> Hit@3 bằng nhau, MRR khác nhau
    lan = [["ok", "x", "y"], ["ok", "x", "y"]]
    minh = [["x", "y", "ok"], ["x", "y", "ok"]]
    answers = [["ok"], ["ok"]]
    assert hit_at_k(lan, answers, 3) == hit_at_k(minh, answers, 3) == 1.0
    assert mrr(lan, answers, 3) == pytest.approx(1.0)
    assert mrr(minh, answers, 3) == pytest.approx(1 / 3)


def test_mrr_uses_first_correct_rank_not_answer_order():
    # văn bản đúng ghi theo thứ tự ["c", "b"], nhưng trong danh sách máy trả "b" đứng trước (thứ hạng 2)
    assert mrr([["a", "b", "c"]], [["c", "b"]], 3) == pytest.approx(1 / 2)

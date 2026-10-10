import pytest

from app.evaluation.metrics import hit_at_k, mrr

# Đề nhỏ 3 câu: đáp án ở dòng 1 · ở dòng 3 · không có.
RESULTS = [
    ["son_tung", "cover", "remix"],
    ["cover", "remix", "son_tung"],
    ["cover", "remix", "karaoke"],
]
ANSWERS = ["son_tung", "son_tung", "son_tung"]


def test_hit_at_1_counts_only_first_row():
    assert hit_at_k(RESULTS, ANSWERS, 1) == pytest.approx(1 / 3)


def test_hit_at_3_looks_at_all_first_three_rows():
    assert hit_at_k(RESULTS, ANSWERS, 3) == pytest.approx(2 / 3)


def test_k_larger_than_list_is_fine():
    assert hit_at_k(RESULTS, ANSWERS, 10) == pytest.approx(2 / 3)


def test_all_missed_gives_zero():
    assert hit_at_k(RESULTS, ["x", "y", "z"], 3) == 0.0


def test_one_question_is_zero_or_one_not_a_fraction():
    # câu 42 thật: đáp án ở dòng 1 -> cả đề 1 câu được 1/1, không phải 1/42
    assert hit_at_k([["44/2011/tt-bca+2", "44/2005/qh11+50"]], ["44/2011/tt-bca+2"], 1) == 1.0


# ---- MRR: mỗi câu cộng 1/dòng của đáp án (dòng đếm từ 1), trượt cộng 0, chia số câu ----


def test_mrr_rewards_higher_rows_more():
    # dòng 1 -> 1 · dòng 3 -> 1/3 · trượt -> 0
    assert mrr(RESULTS, ANSWERS, 3) == pytest.approx((1 + 1 / 3 + 0) / 3)


def test_mrr_single_question_at_row_two_is_half():
    assert mrr([["cover", "son_tung", "remix"]], ["son_tung"], 3) == pytest.approx(0.5)


def test_mrr_respects_k_cutoff():
    # đáp án ở dòng 3 nhưng k=2 -> coi như trượt
    assert mrr([["cover", "remix", "son_tung"]], ["son_tung"], 2) == 0.0


def test_mrr_all_missed_gives_zero():
    assert mrr(RESULTS, ["x", "y", "z"], 3) == 0.0


def test_mrr_separates_same_hit_different_rank():
    # Lan: luôn dòng 1 · Minh: luôn dòng 3 -> Hit@3 bằng nhau, MRR khác nhau
    lan = [["ok", "x", "y"], ["ok", "x", "y"]]
    minh = [["x", "y", "ok"], ["x", "y", "ok"]]
    answers = ["ok", "ok"]
    assert hit_at_k(lan, answers, 3) == hit_at_k(minh, answers, 3) == 1.0
    assert mrr(lan, answers, 3) == pytest.approx(1.0)
    assert mrr(minh, answers, 3) == pytest.approx(1 / 3)

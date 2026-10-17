"""CỬA 11/10 — gõ mrr ĐÓNG SÁCH. Chạy: .venv/bin/python Learning-document/drills/mrr-cua-1110.py"""


def mrr(results: list[list[str]], answers: list[str], k: int) -> float:
    total_rr = 0
    for i in range(len(results)):
        top_k = results[i][:k]
        if answers[i] in top_k:
            rank = top_k.index(answers[i]) + 1
            rr = 1/rank
            total_rr+= rr
    return total_rr / len(results)



# ---- Claude viết phần dưới, đừng sửa ----
RESULTS = [
    ["dieu_5", "dieu_9", "dieu_2"],
    ["dieu_9", "dieu_2", "dieu_5"],
    ["dieu_9", "dieu_2", "dieu_7"],
]
ANSWERS = ["dieu_5", "dieu_5", "dieu_5"]

checks = [
    ("k=3", mrr(RESULTS, ANSWERS, 3), (1 + 1 / 3 + 0) / 3),
    ("k=2 cắt", mrr(RESULTS, ANSWERS, 2), (1 + 0 + 0) / 3),
    ("hạng 2", mrr([["a", "b", "c"]], ["b"], 3), 0.5),
    ("trượt hết", mrr(RESULTS, ["x", "y", "z"], 3), 0.0),
    ("2 câu", mrr([["a", "b"], ["c", "d"]], ["b", "c"], 2), (1 / 2 + 1) / 2),
]
for name, got, want in checks:
    ok = got is not None and abs(got - want) < 1e-9
    print(f"{'✅' if ok else '❌'} {name:10} ra {got!r:22} cần {want:.4f}")

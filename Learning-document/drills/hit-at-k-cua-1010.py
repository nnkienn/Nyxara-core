"""CỬA 10/10 — gõ hit_at_k ĐÓNG SÁCH. Chạy: .venv/bin/python Learning-document/drills/hit-at-k-cua-1010.py"""


def hit_at_k(results: list[list[str]], answers: list[str], k: int) -> float:
    hits = 0
    for i in range(len(results)):
        top_k=results[i][:k]
        if answers[i] in top_k:
            hits=hits+1
    return hits / len(results)



# ---- Claude viết phần dưới, đừng sửa ----
RESULTS = [
    ["son_tung", "cover", "remix"],
    ["cover", "remix", "son_tung"],
    ["cover", "remix", "karaoke"],
]
ANSWERS = ["son_tung", "son_tung", "son_tung"]

checks = [
    ("k=1", hit_at_k(RESULTS, ANSWERS, 1), 1 / 3),
    ("k=3", hit_at_k(RESULTS, ANSWERS, 3), 2 / 3),
    ("k=10", hit_at_k(RESULTS, ANSWERS, 10), 2 / 3),
    ("trượt hết", hit_at_k(RESULTS, ["x", "y", "z"], 3), 0.0),
    ("1 câu", hit_at_k([["a", "b"]], ["a"], 1), 1.0),
]
for name, got, want in checks:
    ok = got is not None and abs(got - want) < 1e-9
    print(f"{'✅' if ok else '❌'} {name:10} ra {got!r:22} cần {want:.4f}")

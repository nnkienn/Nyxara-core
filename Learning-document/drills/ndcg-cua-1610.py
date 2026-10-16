2 """CỬA 16/10 — gõ ndcg_at_k ĐÓNG SÁCH. Chạy: .venv/bin/python Learning-document/drills/ndcg-cua-1610.py

Bước 1: viết mã giả tiếng Việt 4 bước vào chỗ "# Mã giả" bên dưới (không mở app/evaluation/metrics.py).
Bước 2: gõ ruột hàm ngay dưới mã giả, tên biến tiếng Anh.
"""

import math


def ndcg_at_k(results: list[list[str]], answers: list[list[str]], k: int) -> float:
    for i in range(len(results)):
        dcg = 0
        top_k = results[i][:k]
        for answer in answers[i]:
            if answer in top_k:
                rank = top_k.index(answer)+1
                dcg += 1/math.log2(rank+1)
        idcg = 0
        idel_hits= min(len(answers[i],k))
        for


# ---- Claude viết phần dưới, đừng sửa ----
def _score(rank):
    return 1 / math.log2(rank + 1)


checks = [
    ("hoàn hảo", ndcg_at_k([["dieu_5", "dieu_9"]], [["dieu_5", "dieu_9"]], 2), 1.0),
    ("trượt hết", ndcg_at_k([["dieu_1", "dieu_2"]], [["dieu_5"]], 2), 0.0),
    ("đúng ở hạng 3", ndcg_at_k([["x", "y", "dieu_5"]], [["dieu_5"]], 3), _score(3) / _score(1)),
    ("k=2 cắt", ndcg_at_k([["x", "y", "dieu_5"]], [["dieu_5"]], 2), 0.0),
    ("2 đúng, hạng 1+3", ndcg_at_k([["a", "x", "b"]], [["a", "b"]], 3),
     (_score(1) + _score(3)) / (_score(1) + _score(2))),
    ("3 đúng, k=2", ndcg_at_k([["a", "b", "x"]], [["a", "b", "c"]], 2), 1.0),
    ("2 lần tìm", ndcg_at_k([["a", "x"], ["x", "b"]], [["a"], ["b"]], 2), (1 + _score(2)) / 2),
]
for name, got, want in checks:
    ok = got is not None and abs(got - want) < 1e-9
    print(f"{'✅' if ok else '❌'} {name:18} ra {got!r:22} cần {want:.4f}")

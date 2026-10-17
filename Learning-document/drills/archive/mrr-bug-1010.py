"""BUG CỐ Ý 10/10 tối — mrr dưới đây CHẠY ĐƯỢC, không nổ, nhưng ra số SAI. Tìm dòng sai, sửa.
Chạy: .venv/bin/python Learning-document/drills/mrr-bug-1010.py"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from app.evaluation.metrics import hit_at_k


def mrr(results: list[list[str]], answers: list[str], k: int) -> float:
    total_rr = 0
    for i in range(len(results)):
        top_k = results[i][:k]
        if answers[i] in top_k:
            rank = top_k.index(answers[i]) + 1
            total_rr += 1 / rank
    return total_rr / len(results)


# ---- Claude viết phần dưới, đừng sửa ----
RESULTS = [
    ["son_tung", "cover", "remix"],
    ["cover", "remix", "son_tung"],
    ["cover", "remix", "karaoke"],
]
ANSWERS = ["son_tung", "son_tung", "son_tung"]
print(f"Bộ nhỏ 3 lần tìm, k=3:  MRR ra {mrr(RESULTS, ANSWERS, 3):.4f}   (tính tay cần 0.4444)")

saved = json.loads((ROOT / "data/zalo_legal/bm25_top10_test.json").read_text())
R, A = saved["results"], saved["answers"]
print(f"Zalo 788 lần tìm, k=10: Hit@10 {hit_at_k(R, A, 10):.4f} · MRR@10 {mrr(R, A, 10):.4f}")

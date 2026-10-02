# Ôn +15 tiếng: gõ lại to_qdrant_filter TỪ TRẮNG.
# ĐÓNG file app/infrastructure/adapters/vectorstore/qdrant_filter.py trước khi gõ.
# 4 hàm phụ đã có sẵn (import từ app/), bạn chỉ gõ ruột hàm chia đường ở dưới.
#
# Chạy:  cd ~/Developer/nyxara-core && .venv/bin/python Learning-document/drills/2026-10-02-toi-go-lai-to-qdrant-filter.py

import sys
sys.path.insert(0, ".")

from app.infrastructure.adapters.vectorstore.qdrant_filter import (
    to_and_clause,
    to_leaf_clause,
    to_not_clause,
    to_or_clause,
)


def to_qdrant_filter(pred: dict) -> dict:
    op = list(pred.keys())[0]
    if op == "and":
        return to_and_clause(pred)
    elif op == "or":
        return to_or_clause(pred)
    elif op == "not":
        return to_not_clause(pred)
    else:
        value  = []
        key = to_leaf_clause(pred)
        value.append(key)
        return {"must": value}
# ---------------- ca thử — KHÔNG sửa phần dưới ----------------
CASES = [
    ("and", {"and": [{"eq": ["loai", "Luật"]}, {"gte": ["nam", 2020]}]},
     {"must": [{"key": "loai", "match": {"value": "Luật"}}, {"key": "nam", "range": {"gte": 2020}}]}),
    ("or", {"or": [{"eq": ["loai", "Luật"]}, {"eq": ["loai", "Nghị định"]}]},
     {"should": [{"key": "loai", "match": {"value": "Luật"}}, {"key": "loai", "match": {"value": "Nghị định"}}]}),
    ("not", {"not": [{"eq": ["loai", "Thông tư"]}]},
     {"must_not": [{"key": "loai", "match": {"value": "Thông tư"}}]}),
    ("lá eq trần", {"eq": ["loai", "Luật"]},
     {"must": [{"key": "loai", "match": {"value": "Luật"}}]}),
    ("lá lt trần", {"lt": ["nam", 2015]},
     {"must": [{"key": "nam", "range": {"lt": 2015}}]}),
]

passed = 0
for name, pred, expected in CASES:
    try:
        got = to_qdrant_filter(pred)
    except Exception as e:
        got = f"NỔ {type(e).__name__}: {e}"
    ok = got == expected
    passed += ok
    print(("✅" if ok else "❌"), name)
    if not ok:
        print("     mong:", expected)
        print("     ra  :", got)

try:
    to_qdrant_filter({"like": ["loai", "Luật"]})
    print("❌ like  — lẽ ra phải nổ ValueError")
except ValueError:
    print("✅ like  — nổ ValueError đúng")
    passed += 1
except Exception as e:
    print(f"❌ like  — nổ sai loại: {type(e).__name__}")

print(f"\n{passed}/6")

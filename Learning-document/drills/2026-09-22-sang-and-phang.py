# SANG 22/09 — DICH "and" BANG VONG FOR. KHONG DE QUY.
# Chay: .venv/bin/python Learning-document/drills/2026-09-22-sang-and-phang.py

NUMERIC_OPS = ("gt", "gte", "lt", "lte")


# ─── CLAUDE VIET SAN: dich MOT la. Dung sua. ────────────────────
def to_leaf_clause(pred: dict) -> dict:
    """{"eq": ["loai", "Luat"]}  -> {"key": "loai", "match": {"value": "Luat"}}
       {"gte": ["nam", 2015]}    -> {"key": "nam",  "range": {"gte": 2015}}"""
    op = list(pred.keys())[0]
    field = pred[op][0]
    value = pred[op][1]
    if op == "eq":
        return {"key": field, "match": {"value": value}}
    if op in NUMERIC_OPS:
        return {"key": field, "range": {op: value}}
    raise ValueError(f"khong phai la: {op}")


# ─── CUA BAN: dich mot cay "and" chi gom cac LA ─────────────────
# Vao : {"and": [la1, la2, ...]}
# Ra  : {"must": [<to don cua la1>, <to don cua la2>, ...]}
#
# Bon buoc, moi buoc mot dong:
#   1. tao mot list rong de gom
#   2. di qua tung con trong pred["and"]
#   3.   dich con do bang to_leaf_clause, bo vao list
#   4. tra ve mot dict co khoa "must", gia tri la list vua gom
def to_and_clause(pred: dict) -> dict:
    list_out=[]
    for child in pred["and"]:
        child = to_leaf_clause(child)
        list_out.append(child)
    return {"must": list_out}
# ═══════ TU DAY XUONG LA CUA CLAUDE — DUNG SUA ══════════════════
CASES = [
    ({"and": [{"eq": ["loai", "Nghi dinh"]}, {"gte": ["nam", 2015]}]},
     {"must": [{"key": "loai", "match": {"value": "Nghi dinh"}},
               {"key": "nam", "range": {"gte": 2015}}]}),

    ({"and": [{"eq": ["co_quan", "Quoc hoi"]}]},
     {"must": [{"key": "co_quan", "match": {"value": "Quoc hoi"}}]}),

    ({"and": [{"eq": ["loai", "Luat"]}, {"gte": ["nam", 2010]}, {"lt": ["nam", 2020]}]},
     {"must": [{"key": "loai", "match": {"value": "Luat"}},
               {"key": "nam", "range": {"gte": 2010}},
               {"key": "nam", "range": {"lt": 2020}}]}),
]


def main() -> None:
    ok = 0
    for src, want in CASES:
        try:
            got = to_and_clause(src)
        except Exception as e:
            print(f"NO    vao : {src}\n      {type(e).__name__}: {e}\n")
            continue
        if got == want:
            ok += 1
            print(f"DUNG  {src}")
        else:
            print(f"SAI   vao : {src}\n      ra  : {got}\n      mong: {want}")
    print(f"\n{ok}/{len(CASES)} ca dung")


if __name__ == "__main__":
    main()

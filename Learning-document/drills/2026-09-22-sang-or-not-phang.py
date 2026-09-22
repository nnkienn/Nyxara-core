# SANG 22/09 (30' them) — "or" va "not", VAN PHANG, KHONG DE QUY
# Chay: .venv/bin/python Learning-document/drills/2026-09-22-sang-or-not-phang.py

NUMERIC_OPS = ("gt", "gte", "lt", "lte")


# ─── CLAUDE VIET SAN: dich MOT la. Dung sua. ────────────────────
def to_leaf_clause(pred: dict) -> dict:
    op = list(pred.keys())[0]
    field, value = pred[op][0], pred[op][1]
    if op == "eq":
        return {"key": field, "match": {"value": value}}
    if op in NUMERIC_OPS:
        return {"key": field, "range": {op: value}}
    raise ValueError(f"khong phai la: {op}")


# ─── CUA BAN 1 — "or" ───────────────────────────────────────────
# Vao : {"or": [la1, la2, ...]}   Ra: {"should": [<to don la1>, <to don la2>, ...]}
# Y HET to_and_clause ban vua go sang nay, doi dung mot chu.
def to_or_clause(pred: dict) -> dict:
    list_out = []
    for child in pred["or"]:
        child = to_leaf_clause(child)
        list_out.append(child)
    return {"should" : list_out }


# ─── CUA BAN 2 — "not" ──────────────────────────────────────────
# Vao : {"not": [la]}   ->   Ra: {"must_not": [<to don cua la>]}
# pred["not"] la mot LIST co DUNG 1 phan tu. Khong can vong for.
# Gia tri cua "must_not" VAN LA MOT LIST, du chi chua 1 to don.
def to_not_clause(pred: dict) -> dict:
    list_out =[]
    child = to_leaf_clause(pred["not"][0])
    list_out.append(child)
    return {"must_not" : list_out}


# ═══════ TU DAY XUONG LA CUA CLAUDE — DUNG SUA ══════════════════
CASES = [
    ("or 2 la", to_or_clause,
     {"or": [{"eq": ["co_quan", "Quoc hoi"]}, {"eq": ["co_quan", "Chinh phu"]}]},
     {"should": [{"key": "co_quan", "match": {"value": "Quoc hoi"}},
                 {"key": "co_quan", "match": {"value": "Chinh phu"}}]}),

    ("or 3 la", to_or_clause,
     {"or": [{"eq": ["loai", "Luat"]}, {"eq": ["loai", "Nghi dinh"]}, {"gte": ["nam", 2020]}]},
     {"should": [{"key": "loai", "match": {"value": "Luat"}},
                 {"key": "loai", "match": {"value": "Nghi dinh"}},
                 {"key": "nam", "range": {"gte": 2020}}]}),

    ("not 1 la (chuoi)", to_not_clause,
     {"not": [{"eq": ["co_quan", "Bo Tai chinh"]}]},
     {"must_not": [{"key": "co_quan", "match": {"value": "Bo Tai chinh"}}]}),

    ("not 1 la (so)", to_not_clause,
     {"not": [{"gte": ["nam", 2020]}]},
     {"must_not": [{"key": "nam", "range": {"gte": 2020}}]}),
]


def main() -> None:
    ok = 0
    for ten, ham, src, want in CASES:
        try:
            got = ham(src)
        except Exception as e:
            print(f"NO    [{ten}]  {type(e).__name__}: {e}\n")
            continue
        if got == want:
            ok += 1
            print(f"DUNG  [{ten}]")
        else:
            print(f"SAI   [{ten}]\n      ra  : {got}\n      mong: {want}")
    print(f"\n{ok}/{len(CASES)} ca dung")


if __name__ == "__main__":
    main()

# CHIỀU 20/09 — GÕ RUỘT: đúng một nhánh so sánh số
# Bạn gõ 4 dòng trong  # ✍️ ... # ✍️ hết.  Phần còn lại Claude đã nối dây.
# Chạy: .venv/bin/python Learning-document/drills/2026-09-20-chieu-go-ruot-range.py

NUMERIC_OPS = ("gt", "gte", "lt", "lte")


def to_range_clause(pred: dict) -> dict:
    """pred = {"gte": ["nam", 2015]}  ->  {"key": "nam", "range": {"gte": 2015}}"""
    op = list(pred.keys())[0]
    field = pred[op][0]
    value = pred[op][1]
    return {"key": field, "range": {  op : value}}

CASES = [ 
    ({"gte": ["nam", 2015]}, {"key": "nam", "range": {"gte": 2015}}),
    ({"lt": ["nam", 2020]}, {"key": "nam", "range": {"lt": 2020}}),
    ({"gt": ["so_dieu", 10]}, {"key": "so_dieu", "range": {"gt": 10}}),
    ({"lte": ["nam", 2018]}, {"key": "nam", "range": {"lte": 2018}}),
]


def main() -> None:
    ok = 0
    for src, want in CASES:
        got = to_range_clause(src)
        if got == want:
            ok += 1
            print(f"ĐÚNG  {src}")
        else:
            print(f"SAI   vào : {src}\n      ra  : {got}\n      mong: {want}")
    print(f"\n{ok}/{len(CASES)} ca đúng")


if __name__ == "__main__":
    main()

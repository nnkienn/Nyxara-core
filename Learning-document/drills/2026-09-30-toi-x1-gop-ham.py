# TỐI 30/09 — X1: GỘP 3 hàm phẳng thành MỘT cửa vào  to_qdrant_filter(pred)
# Chạy: .venv/bin/python Learning-document/drills/2026-09-30-toi-x1-gop-ham.py
# Cây 1 TẦNG (con toàn là lá). KHÔNG đệ quy.

NUMERIC_OPS = ("gt", "gte", "lt", "lte")


# ─── CÓ SẴN (bạn đã gõ 20-22/09). Đừng sửa. ─────────────────────
def to_leaf_clause(pred: dict) -> dict:
    op = list(pred.keys())[0]
    field, value = pred[op][0], pred[op][1]
    if op == "eq":
        return {"key": field, "match": {"value": value}}
    if op in NUMERIC_OPS:
        return {"key": field, "range": {op: value}}
    raise ValueError(f"không phải lá: {op}")


def to_and_clause(pred: dict) -> dict:
    out = []
    for child in pred["and"]:
        out.append(to_leaf_clause(child))
    return {"must": out}


def to_or_clause(pred: dict) -> dict:
    out = []
    for child in pred["or"]:
        out.append(to_leaf_clause(child))
    return {"should": out}


def to_not_clause(pred: dict) -> dict:
    return {"must_not": [to_leaf_clause(pred["not"][0])]}


# ─── CỦA BẠN — cửa vào duy nhất ─────────────────────────────────
# Vào : MỘT pred bất kỳ trong 4 dạng ở bảng ĐƯỜNG ĐI (chạy file để xem bảng).
# Ra  : dict filter của Qdrant.
# Dòng đầu đã có sẵn: lấy ra chữ khoá ngoài cùng của pred, cất vào  op.
# Bạn gõ phần còn lại: if / elif / elif / else, mỗi nhánh MỘT dòng return.
def to_qdrant_filter(pred: dict) -> dict:
    op = list(pred.keys())[0]
    if(op == "and"):
        return to_and_clause(pred)
    elif(op == "or"):
        return to_or_clause(pred)
    elif(op == "not"):
        return to_not_clause(pred)
    else:
        value = []
        key = to_leaf_clause(pred)
        value.append(key)
        return {"must" : value}   


# ═══════ TỪ ĐÂY XUỐNG LÀ CỦA CLAUDE — ĐỪNG SỬA ══════════════════
LEAF = {"eq": ["loai", "Luật"]}
CASES = [
    ("and 2 lá", {"and": [{"eq": ["loai", "Luật"]}, {"gte": ["nam", 2020]}]},
     {"must": [{"key": "loai", "match": {"value": "Luật"}},
               {"key": "nam", "range": {"gte": 2020}}]}),
    ("or 2 lá", {"or": [{"eq": ["co_quan", "Quốc hội"]}, {"eq": ["co_quan", "Chính phủ"]}]},
     {"should": [{"key": "co_quan", "match": {"value": "Quốc hội"}},
                 {"key": "co_quan", "match": {"value": "Chính phủ"}}]}),
    ("not 1 lá", {"not": [{"eq": ["co_quan", "Bộ Tài chính"]}]},
     {"must_not": [{"key": "co_quan", "match": {"value": "Bộ Tài chính"}}]}),
    ("lá trần (eq)", LEAF,
     {"must": [{"key": "loai", "match": {"value": "Luật"}}]}),
    ("lá trần (lt)", {"lt": ["nam", 2015]},
     {"must": [{"key": "nam", "range": {"lt": 2015}}]}),
]


def show_path() -> None:
    print("ĐƯỜNG ĐI — pred vào, op là chữ gì, Qdrant cần nhận cái gì")
    for ten, src, want in CASES:
        print(f"\n  [{ten}]")
        print(f"    vào : {src}")
        print(f"    op  : {list(src.keys())[0]!r}")
        print(f"    ra  : {want}")
    print("\n  Hậu quả nếu đưa LÁ TRẦN thẳng cho Qdrant, không bọc:")
    print(f"    to_leaf_clause(LEAF) = {to_leaf_clause(LEAF)}")
    print("    -> Qdrant chỉ hiểu 3 ngăn must / should / must_not. Tờ đơn nằm ngoài ngăn = bị từ chối.")
    print("    -> vì vậy lá trần phải ra:  {\"must\": [<tờ đơn>]}\n")


def main() -> None:
    show_path()
    ok = 0
    for ten, src, want in CASES:
        try:
            got = to_qdrant_filter(src)
        except Exception as e:
            print(f"NỔ    [{ten}]  {type(e).__name__}: {e}")
            continue
        if got == want:
            ok += 1
            print(f"ĐÚNG  [{ten}]")
        else:
            print(f"SAI   [{ten}]\n      ra  : {got}\n      mong: {want}")
    print(f"\n{ok}/{len(CASES)} ca đúng")


if __name__ == "__main__":
    main()

# ĐỀ TỐI 19/09 — DỊCH CÂY BỘ LỌC SANG TỜ ĐƠN QDRANT
# Bạn chỉ gõ vào chỗ  ✍️ GÕ Ở ĐÂY.  Khung, dữ liệu, ca thử: Claude lo.
# Chạy:  .venv/bin/python Learning-document/drills/2026-09-19-to-qdrant-filter.py
# Máy tự chấm từng mẩu, in ĐÚNG / SAI + cái nó mong đợi. Không cần hỏi Claude mới biết đúng sai.
#
# ─── BẢNG TRA (copy-paste giá trị, đừng gõ tay) ──────────────────
#   phép eq                  -> {"key": <ten_truong>, "match": {"value": <gia_tri>}}
#   phép gt/gte/lt/lte       -> {"key": <ten_truong>, "range": {<phep>: <gia_tri>}}
#   {"and": [...]}           -> {"must":     [<dịch từng con>]}
#   {"or":  [...]}           -> {"should":   [<dịch từng con>]}
#   {"not": [con]}           -> {"must_not": [<dịch con>]}
#
# Một nút lá luôn có đúng 3 mẩu tin:
#   pred = {"gte": ["nam", 2015]}
#   phep       = list(pred.keys())[0]   -> "gte"
#   ten_truong = pred[phep][0]          -> "nam"
#   gia_tri    = pred[phep][1]          -> 2015


def to_qdrant_filter(pred: dict) -> dict:
    phep = list(pred.keys())[0]

    # MẨU A — lá phép "eq". Trả ra dict có "key" và "match".
    # ✍️ GÕ Ở ĐÂY
    if phep == "eq":
        

    # MẨU B — lá phép so số: gt / gte / lt / lte. Trả ra dict có "key" và "range".
    #          (4 phép này gộp một nhánh được, tên phép đem dùng thẳng làm khoá trong range)
    # ✍️ GÕ Ở ĐÂY
    if phep == "gt" or phep == "gte" or phep == "lt" or phep == "lte":
        pass

    # MẨU C — "and": pred["and"] là list các con.
    #          Dịch TỪNG con (gọi lại to_qdrant_filter), gom vào một list, bỏ vào "must".
    # ✍️ GÕ Ở ĐÂY
    if phep == "and":
        pass

    # MẨU D — "or"  -> "should"   (giống hệt mẩu C, đổi tên hộp)
    # ✍️ GÕ Ở ĐÂY
    if phep == "or":
        pass

    # MẨU E — "not": pred["not"] là list có ĐÚNG 1 con -> "must_not"
    # ✍️ GÕ Ở ĐÂY
    if phep == "not":
        pass

    raise ValueError(f"phép không hợp lệ: {phep}")


# ═══════ TỪ ĐÂY XUỐNG LÀ CỦA CLAUDE — ĐỪNG SỬA ═══════════════════

CA_THU = [
    ("A", {"eq": ["loai_van_ban", "Luật"]},
          {"key": "loai_van_ban", "match": {"value": "Luật"}}),
    ("A", {"eq": ["co_quan", "Chính phủ"]},
          {"key": "co_quan", "match": {"value": "Chính phủ"}}),
    ("B", {"gte": ["nam", 2015]},
          {"key": "nam", "range": {"gte": 2015}}),
    ("B", {"lt": ["nam", 2020]},
          {"key": "nam", "range": {"lt": 2020}}),
    ("C", {"and": [{"eq": ["loai_van_ban", "Nghị định"]}, {"gte": ["nam", 2015]}]},
          {"must": [{"key": "loai_van_ban", "match": {"value": "Nghị định"}},
                    {"key": "nam", "range": {"gte": 2015}}]}),
    ("D", {"or": [{"eq": ["co_quan", "Quốc hội"]}, {"eq": ["co_quan", "Chính phủ"]}]},
          {"should": [{"key": "co_quan", "match": {"value": "Quốc hội"}},
                      {"key": "co_quan", "match": {"value": "Chính phủ"}}]}),
    ("E", {"not": [{"eq": ["co_quan", "Bộ Tài chính"]}]},
          {"must_not": [{"key": "co_quan", "match": {"value": "Bộ Tài chính"}}]}),
    ("E", {"and": [{"eq": ["loai_van_ban", "Nghị định"]},
                   {"not": [{"gte": ["nam", 2020]}]}]},
          {"must": [{"key": "loai_van_ban", "match": {"value": "Nghị định"}},
                    {"must_not": [{"key": "nam", "range": {"gte": 2020}}]}]}),
]


def main() -> None:
    dem_dung = 0
    for ten_mau, vao, mong_doi in CA_THU:
        try:
            ra = to_qdrant_filter(vao)
        except Exception as e:
            print(f"[{ten_mau}] NỔ  {type(e).__name__}: {e}")
            continue
        if ra == mong_doi:
            dem_dung += 1
            print(f"[{ten_mau}] ĐÚNG  {vao}")
        else:
            print(f"[{ten_mau}] SAI   vào     : {vao}")
            print(f"        bạn trả ra  : {ra}")
            print(f"        mong đợi    : {mong_doi}")
    print(f"\n{dem_dung}/{len(CA_THU)} ca đúng")


if __name__ == "__main__":
    main()

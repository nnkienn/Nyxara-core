# TỐI 20/09 — GÕ RUỘT CÁI GỐC (and / or / not)
#
# Vì sao có bài này: tối nay trượt 3 lượt liên tiếp, cả 3 cùng một lỗ —
#   (1) đoán cây "and" -> trả ra 2 dict rời, QUÊN cái bọc ngoài {"must": [...]}
#   (2) đếm số lần gọi -> nói 2, thiếu đúng lần gọi trên cả cây
#   (3) (lượt này bản in của Claude căn lề sai, không tính)
# Lá (eq, so số) bạn đã nắm -> Claude để sẵn, chạy được.
# BA NHÁNH GỐC là chỗ bạn gõ. Đó là chỗ tối nay hỏng.
#
# Chạy:  .venv/bin/python Learning-document/drills/2026-09-20-toi-go-ruot-goc.py
#
# ─── BẢNG TRA (copy-paste, ĐỪNG GÕ TAY — lỗi chép đã 10 lần) ──────
#   {"and": [...]}  -> {"must":     [<dịch từng con>]}
#   {"or":  [...]}  -> {"should":   [<dịch từng con>]}
#   {"not": [con]}  -> {"must_not": [<dịch con>]}     not luôn đúng 1 con
#
# Nhớ bản in tối nay: cây {"and": [la1, la2]} gọi hàm 3 lần, không phải 2.
# Lần gọi ngoài cùng nhận vào SỚM NHẤT, trả ra MUỘN NHẤT.


SO_SANH_SO = ("gt", "gte", "lt", "lte")


def to_qdrant_filter(pred: dict) -> dict:
    phep = list(pred.keys())[0]

    # ── Claude để sẵn: hai nhánh LÁ, đã chạy được, đừng sửa ──────
    if phep == "eq":
        return {"key": pred[phep][0], "match": {"value": pred[phep][1]}}

    if phep in SO_SANH_SO:
        return {"key": pred[phep][0], "range": {phep: pred[phep][1]}}

    # ── TỪ ĐÂY LÀ CỦA BẠN ────────────────────────────────────────

    # RUỘT 1 — "and".  pred["and"] là list các con.
    #   Dịch TỪNG con bằng cách gọi lại to_qdrant_filter(con),
    #   gom vào một list, rồi trả ra một dict có khoá "must".
    if phep == "and":
        danh_sach_con =[]
        for con in pred[phep]:
            danh_sach_con.append(to_qdrant_filter(con))
        return {"must": danh_sach_con}


    # RUỘT 2 — "or".  Giống hệt ruột 1, chỉ đổi tên hộp thành "should".
    if phep == "or":
        danh_sach_con = []
        for con in pred[phep]:
            danh_sach_con.append(to_qdrant_filter(con))
        return {"should": danh_sach_con}
        

    # RUỘT 3 — "not".  pred["not"] là list có ĐÚNG 1 con.
    #   Không cần vòng for. Trả ra dict có khoá "must_not".
    #   Giá trị của "must_not" vẫn là một LIST, dù chỉ có 1 con.
    if phep == "not":
        return {"must_not": [to_qdrant_filter(pred["not"][0])]}

    raise ValueError(f"phép không hợp lệ: {phep}")


# ═══════ TỪ ĐÂY XUỐNG LÀ CỦA CLAUDE — ĐỪNG SỬA ═══════════════════

CA_THU = [
    ("gốc and, 2 lá",
     {"and": [{"eq": ["loai_van_ban", "Nghị định"]}, {"gte": ["nam", 2015]}]},
     {"must": [{"key": "loai_van_ban", "match": {"value": "Nghị định"}},
               {"key": "nam", "range": {"gte": 2015}}]}),

    ("gốc or, 2 lá",
     {"or": [{"eq": ["co_quan", "Quốc hội"]}, {"eq": ["co_quan", "Chính phủ"]}]},
     {"should": [{"key": "co_quan", "match": {"value": "Quốc hội"}},
                 {"key": "co_quan", "match": {"value": "Chính phủ"}}]}),

    ("gốc not, 1 lá",
     {"not": [{"eq": ["co_quan", "Bộ Tài chính"]}]},
     {"must_not": [{"key": "co_quan", "match": {"value": "Bộ Tài chính"}}]}),

    ("gốc and, 3 lá",
     {"and": [{"eq": ["loai_van_ban", "Luật"]},
              {"gte": ["nam", 2010]},
              {"lt": ["nam", 2020]}]},
     {"must": [{"key": "loai_van_ban", "match": {"value": "Luật"}},
               {"key": "nam", "range": {"gte": 2010}},
               {"key": "nam", "range": {"lt": 2020}}]}),

    ("gốc and, trong có not — ca hỏng tối nay",
     {"and": [{"eq": ["loai_van_ban", "Nghị định"]}, {"not": [{"gte": ["nam", 2020]}]}]},
     {"must": [{"key": "loai_van_ban", "match": {"value": "Nghị định"}},
               {"must_not": [{"key": "nam", "range": {"gte": 2020}}]}]}),

    ("gốc not, trong có or — hai tầng",
     {"not": [{"or": [{"eq": ["co_quan", "Quốc hội"]}, {"eq": ["co_quan", "Chính phủ"]}]}]},
     {"must_not": [{"should": [{"key": "co_quan", "match": {"value": "Quốc hội"}},
                               {"key": "co_quan", "match": {"value": "Chính phủ"}}]}]}),
]


def main() -> None:
    dung = 0
    for ten, vao, mong_doi in CA_THU:
        try:
            ra = to_qdrant_filter(vao)
        except Exception as e:
            print(f"[{ten}]\n    NỔ    {type(e).__name__}: {e}\n")
            continue
        if ra == mong_doi:
            dung += 1
            print(f"[{ten}]\n    ĐÚNG\n")
        else:
            print(f"[{ten}]")
            print(f"    vào   : {vao}")
            print(f"    ra    : {ra}")
            print(f"    mong  : {mong_doi}\n")
    print(f"{dung}/{len(CA_THU)} ca đúng")


if __name__ == "__main__":
    main()

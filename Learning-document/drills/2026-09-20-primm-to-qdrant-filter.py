# SÁNG 20/09 — PRIMM · BỘ DỊCH CÂY BỘ LỌC -> TỜ ĐƠN QDRANT
#
# Đổi cách (chốt 19/09): kỹ thuật MỚI thì ĐỌC TRƯỚC, VIẾT SAU.
# Thứ tự bắt buộc, làm đúng từng bước, KHÔNG nhảy cóc:
#
#   1. ĐOÁN   — đọc hàm dưới, tự nói mỗi ca thử ra gì. Ghi ra giấy/comment. CHƯA CHẠY.
#   2. CHẠY   — .venv/bin/python Learning-document/drills/2026-09-20-primm-to-qdrant-filter.py
#               so với cái mình đoán. Chỗ lệch chính là chỗ chưa hiểu.
#   3. SOI    — trả lời 5 câu ở mục SOI. Có code trước mặt, được nhìn thoải mái.
#   4. SỬA VẶT— mục SỬA VẶT: 3 việc nhỏ trên code đã chạy được.
#   5. GÕ LẠI — mục CUỐI: đóng file này, mở file trắng, gõ lại từ đầu.
#
# ─── BẢNG TRA ────────────────────────────────────────────────────
#   eq                  -> {"key": <truong>, "match": {"value": <gia_tri>}}
#   gt/gte/lt/lte       -> {"key": <truong>, "range": {<phep>: <gia_tri>}}
#   {"and": [...]}      -> {"must":     [...]}     ngăn BẮT BUỘC
#   {"or":  [...]}      -> {"should":   [...]}     ngăn CÓ CÁI NÀO CŨNG ĐƯỢC
#   {"not": [con]}      -> {"must_not": [...]}     ngăn LOẠI RA  (không phải chọn ra!)


SO_SANH_SO = ("gt", "gte", "lt", "lte")


def to_qdrant_filter(pred: dict) -> dict:
    """Dịch một cây bộ lọc sang tờ đơn Qdrant. KHÔNG chấm điểm văn bản nào cả -
    lúc hàm này chạy, trong tay chưa có văn bản nào. Nó chỉ viết đơn."""
    phep = list(pred.keys())[0]

    if phep == "eq":
        ten_truong = pred[phep][0]
        gia_tri = pred[phep][1]
        return {"key": ten_truong, "match": {"value": gia_tri}}

    if phep in SO_SANH_SO:
        ten_truong = pred[phep][0]
        gia_tri = pred[phep][1]
        return {"key": ten_truong, "range": {phep: gia_tri}}

    if phep == "and":
        danh_sach_con = []
        for con in pred["and"]:
            danh_sach_con.append(to_qdrant_filter(con))
        return {"must": danh_sach_con}

    if phep == "or":
        danh_sach_con = []
        for con in pred["or"]:
            danh_sach_con.append(to_qdrant_filter(con))
        return {"should": danh_sach_con}

    if phep == "not":
        return {"must_not": [to_qdrant_filter(pred["not"][0])]}

    raise ValueError(f"phép không hợp lệ: {phep}")


# ═══════ MỤC SOI — trả lời sau khi CHẠY (viết vào đây, dạng comment) ═══════
#
# S1. Nhánh "and" gọi lại chính hàm này. Với cây {"and": [la1, la2]} thì
#     to_qdrant_filter được gọi tất cả mấy lần?                        -> ...
# S2. Xoá dòng  return {"must": danh_sach_con}  thì hàm trả ra cái gì,
#     và Python có báo lỗi không?                                      -> ...
# S3. Nhánh "eq" và nhánh so số khác nhau đúng mấy chỗ? Kể ra.         -> ...
# S4. Vì sao nhánh "not" không cần vòng for như "and"/"or"?            -> ...
# S5. Hàm này KHÔNG nhận metadata. Nếu muốn biết "văn bản tt-08-2010 có
#     đạt bộ lọc không" thì phải dùng hàm nào?                         -> ...


# ═══════ MỤC SỬA VẶT — làm trên code đã chạy được, chạy lại sau mỗi việc ═══
#
# V1. Thêm phép "in": {"in": ["co_quan", ["Quốc hội", "Chính phủ"]]}
#     -> {"key": "co_quan", "match": {"any": [...]}}.  Thêm 1 nhánh.
# V2. Đổi nhánh "or" cho dùng chung thân với "and" (cùng một vòng for,
#     chỉ khác tên hộp "must"/"should"). Chạy lại phải vẫn đúng hết.
# V3. Cây {"not": [con1, con2]} là sai luật (not phải đúng 1 con) nhưng
#     hàm hiện tại nuốt im, bỏ quên con2. Bắt nó nổ.


# ═══════ CA THỬ — Claude viết, đừng sửa ═══════════════════════════
CA_THU = [
    ({"eq": ["loai_van_ban", "Luật"]},
     {"key": "loai_van_ban", "match": {"value": "Luật"}}),
    ({"gte": ["nam", 2015]},
     {"key": "nam", "range": {"gte": 2015}}),
    ({"and": [{"eq": ["loai_van_ban", "Nghị định"]}, {"gte": ["nam", 2015]}]},
     {"must": [{"key": "loai_van_ban", "match": {"value": "Nghị định"}},
               {"key": "nam", "range": {"gte": 2015}}]}),
    ({"or": [{"eq": ["co_quan", "Quốc hội"]}, {"eq": ["co_quan", "Chính phủ"]}]},
     {"should": [{"key": "co_quan", "match": {"value": "Quốc hội"}},
                 {"key": "co_quan", "match": {"value": "Chính phủ"}}]}),
    ({"not": [{"eq": ["co_quan", "Bộ Tài chính"]}]},
     {"must_not": [{"key": "co_quan", "match": {"value": "Bộ Tài chính"}}]}),
    ({"and": [{"eq": ["loai_van_ban", "Nghị định"]}, {"not": [{"gte": ["nam", 2020]}]}]},
     {"must": [{"key": "loai_van_ban", "match": {"value": "Nghị định"}},
               {"must_not": [{"key": "nam", "range": {"gte": 2020}}]}]}),
]


def main() -> None:
    dung = 0
    for vao, mong_doi in CA_THU:
        try:
            ra = to_qdrant_filter(vao)
        except Exception as e:
            print(f"NỔ  {type(e).__name__}: {e}\n    vào: {vao}")
            continue
        if ra == mong_doi:
            dung += 1
            print(f"ĐÚNG  {vao}")
        else:
            print(f"SAI   vào   : {vao}\n      ra    : {ra}\n      mong  : {mong_doi}")
    print(f"\n{dung}/{len(CA_THU)} ca đúng")


if __name__ == "__main__":
    main()

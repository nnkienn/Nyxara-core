# ĐỀ SÁNG 18/09 — VÒNG ĐOÁN mẩu "not" (nợ từ sáng 17/09)
# ĐỔI DỮ LIỆU: thẻ giờ là metadata THẬT của một văn bản pháp luật VN (theo thiết kế lại 17/09),
# không còn lang/year/lang_count. Logic y hệt — chỉ đổi cái thẻ mà bảo vệ đang cầm.
#
# Cách làm: ĐÓNG mọi file khác. KHÔNG chạy. Không sửa code.
# Viết dự đoán vào 3 dòng ✍️ ở cuối file, kèm 1 câu vì sao. Xong báo Claude chạy.

the = {
    "loai_van_ban": "Luật",
    "co_quan": "Quốc hội",
    "nam": 2021,
    "con_hieu_luc": True,
}


def xet_mot_luat(dieu_kien: dict, the: dict) -> bool:
    phep = list(dieu_kien.keys())[0]
    gia_tri = dieu_kien[phep][1]
    ten_truong = dieu_kien[phep][0]
    gia_tri_the = the[ten_truong]

    if phep == "lt":
        ket_qua = gia_tri_the < gia_tri
    elif phep == "gt":
        ket_qua = gia_tri_the > gia_tri
    elif phep == "eq":
        ket_qua = gia_tri_the == gia_tri
    return ket_qua


def danh_gia(pred: dict, the: dict) -> bool:
    phep = list(pred.keys())[0]

    if phep == "eq" or phep == "gt" or phep == "lt":
        return xet_mot_luat(pred, the)

    if phep == "and":
        for con in pred["and"]:
            if danh_gia(con, the) == False:
                return False
        return True

    if phep == "or":
        for con in pred["or"]:
            if danh_gia(con, the) == True:
                return True
        return False

    if phep == "not":
        # chốt 18/09 (user chọn b): KHÔNG chỉ được có ĐÚNG 1 con, sai hình dạng thì nổ tại chỗ
        if len(pred["not"]) != 1:
            raise ValueError(f"KHÔNG phải có đúng 1 con, đang có {len(pred['not'])}: {pred}")
        return not danh_gia(pred["not"][0], the)

    raise ValueError(f"phép không hợp lệ: {phep}")


# ─── BA DÒNG PHẢI ĐOÁN ────────────────────────────────────────────
# dòng 1  — "không phải Nghị định"
#   danh_gia({"not": [{"eq": ["loai_van_ban", "Nghị định"]}]}, the)
#
# dòng 2  — "do Chính phủ ban hành, HOẶC không cũ hơn 2020"
#   danh_gia({"or": [{"eq": ["co_quan", "Chính phủ"]},
#                    {"not": [{"lt": ["nam", 2020]}]}]}, the)
#
# dòng 3  — "KHÔNG (mới hơn 2020 HOẶC là Nghị định)"
#   danh_gia({"not": [{"or": [{"gt": ["nam", 2020]},
#                             {"eq": ["loai_van_ban", "Nghị định"]}]}]}, the)


# ─── ✍️ VIẾT DỰ ĐOÁN Ở ĐÂY (True/False + vì sao, 1 câu) ───────────
# dòng 1 =            vì sao:
# dòng 2 =            vì sao:
# dòng 3 =            vì sao:

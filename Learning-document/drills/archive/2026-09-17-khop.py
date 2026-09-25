# ĐỀ SÁNG 17/09 — HÀM khop: MỘT THẺ, CẢ TỜ LUẬT
# Chỉ làm file này. Tắt Copilot. Mỗi lần làm MỘT mẩu → báo Claude chạy → mới sang mẩu sau.
#
# ─── Ẩn dụ bảo vệ cửa ───────────────────────────────────────────
#   thẻ tên   = metadata   → của NGƯỜI MUỐN VÀO (một bài báo)
#   tờ luật   = bo_loc     → bảo vệ CẦM TRÊN TAY, gồm NHIỀU luật
#   một luật  = dieu_kien  → một dòng trên tờ luật, ví dụ {"gt": ["year", 2020]}
#                              ô [0] = "year"  (nhìn dòng nào trên thẻ)
#                              ô [1] = 2020    (so với số nào)
#   Thẻ luôn đứng TRƯỚC dấu:  gt → >   ·   lt → <   ·   eq → ==
#
# Bảo vệ đọc từng luật trên tờ, luật nào cũng so với CÙNG một thẻ.


# ─── DỮ LIỆU (đừng sửa) ──────────────────────────────────────────
metadata = {"lang": "vi", "year": 2021, "lang_count": 5}

bo_loc = [
    {"eq": ["lang", "vi"]},        # luật 1: phải tiếng Việt
    {"gt": ["year", 2020]},        # luật 2: phải mới hơn 2020
    {"lt": ["lang_count", 3]},     # luật 3: phải ít hơn 3 ngôn ngữ
]


# ─── MẨU 1 ── vòng for, chỉ IN ra từng luật ──────────────────────
# Viết 2 dòng: một dòng for qua tờ luật, một dòng print luật đang cầm.
# Đặt tên biến vòng là  dieu_kien.
#
# Phải in ra:
#   {'eq': ['lang', 'vi']}
#   {'gt': ['year', 2020]}
#   {'lt': ['lang_count', 3]}

# ─── MẨU 2 ── trong vòng, tính ket_qua cho TỪNG luật ─────────────
# Làm xong mẩu 1 mới làm. Sửa lại chính vòng for ở mẩu 1:
# thay dòng print luật bằng:  lấy phep · ten_truong · gia_tri · gia_tri_the  →  so  →  print(ket_qua)
#
# Được chép khối bạn tự viết hôm qua (nhớ thụt lề vào TRONG vòng for):
#     phep = list(dieu_kien.keys())[0]
#     ten_truong = dieu_kien[phep][0]
#     ten_truong = dieu_kien[phep][0]
#     gia_tri_the = metadata[ten_truong]
#     if phep == "lt":
#         ket_qua = gia_tri_the < gia_tri
#     elif phep == "gt":
#         ket_qua = gia_tri_the > gia_tri
#     elif phep == "eq":
#         ket_qua = gia_tri_the == gia_tri
#
# Phải in ra:
#   True     ← "vi" == "vi"
#   True     ← 2021 > 2020
#   False    ← 5 < 3 ?




# ─── MẨU 3 ── gói vào hàm, trả MỘT câu trả lời: cho vào hay không ─
# Làm xong mẩu 2 mới làm.
#   def khop(bo_loc: list, metadata: dict) -> bool:
# Cho vào (True) khi TẤT CẢ luật đều đạt. Chỉ cần MỘT luật trượt là False.
# Tự nghĩ: gặp luật trượt thì làm gì? Dòng return True đặt ở đâu?
#
# Ca thử có sẵn (bỏ dấu # đi khi hàm đã viết xong):
                                # False — trượt luật 3
#
# Tự thêm 1 ca của bạn:



# ─── MẨU 4 ── bảo vệ kiểu HOẶC: khop_hoac ─────────────────────────
# Chỉ cần MỘT luật đạt là cho vào. Đọc hết tờ mà không luật nào đạt → False.
#
#              | gặp luật nào thì DỪNG NGAY      | đọc hết tờ không dừng thì nói
#   VÀ   khop  | luật TRƯỢT → return False       | True
#   HOẶC       | luật ĐẠT   → return True        | False
#
# Viết hàm MỚI bên dưới (đừng sửa khop ở trên):
#   def khop_hoac(bo_loc: list, metadata: dict) -> bool:
#
# Ca thử (bỏ dấu # khi viết xong):

def khop_hoac(bo_loc: list, metadata: dict) -> bool:
    for dieu_kien in bo_loc:
        phep = list(dieu_kien.keys())[0]
        gia_tri = dieu_kien[phep][1]
        ten_truong = dieu_kien[phep][0]
        gia_tri_the = metadata[ten_truong]

        if phep == "lt":
            ket_qua = gia_tri_the < gia_tri
        elif phep == "gt":
            ket_qua = gia_tri_the > gia_tri
        elif phep == "eq":
            ket_qua = gia_tri_the == gia_tri
        if ket_qua == True:
            return True
    return False
print(khop_hoac([{"eq": ["lang", "en"]}, {"gt": ["year", 2020]}], metadata))   # True  — trượt luật 1, ĐẠT luật 2
print(khop_hoac([{"eq": ["lang", "vi"]}, {"gt": ["year", 2025]}], metadata))   # True  — ĐẠT luật 1
print(khop_hoac([{"eq": ["lang", "en"]}, {"gt": ["year", 2025]}], metadata))   # False — trượt cả 2
print(khop_hoac([], metadata))                                                 # False — tờ trống, không ai đạt

# ─── MẨU 5 ── tách khúc giống nhau ra hàm riêng: xet_mot_luat ─────
# Nhận MỘT luật + thẻ → trả True/False: luật này đạt hay trượt.
# KHÔNG có vòng for bên trong (vòng for là việc của khop / khop_hoac, không phải của hàm này).
#
#   def xet_mot_luat(dieu_kien: dict, metadata: dict) -> bool:
#
# Ca thử (bỏ dấu # khi viết xong):
# print(xet_mot_luat({"gt": ["year", 2020]}, metadata))       # True  — 2021 > 2020
# print(xet_mot_luat({"lt": ["lang_count", 3]}, metadata))    # False — 5 < 3 ?
# print(xet_mot_luat({"eq": ["lang", "en"]}, metadata))       # False — "vi" == "en" ?

def xet_mot_luat(dieu_kien: dict, metadata: dict) -> bool:
    phep = list(dieu_kien.keys())[0]
    gia_tri = dieu_kien[phep][1]
    ten_truong = dieu_kien[phep][0]
    gia_tri_the = metadata[ten_truong]

    if phep == "lt":
        ket_qua = gia_tri_the < gia_tri
    elif phep == "gt":
        ket_qua = gia_tri_the > gia_tri
    elif phep == "eq":
        ket_qua = gia_tri_the == gia_tri
    return ket_qua


def khop(bo_loc: list, metadata: dict) -> bool:
    for dieu_kien in bo_loc:
        ket_qua = xet_mot_luat(dieu_kien, metadata)
        if ket_qua == False:
            return False
    return True
print(khop([{"eq": ["lang", "vi"]}, {"gt": ["year", 2020]}], metadata))   # True  — đạt cả 2
print(khop([{"eq": ["lang", "vi"]}, {"gt": ["year", 2025]}], metadata))   # False — trượt luật 2
print(khop([{"eq": ["lang", "en"]}, {"gt": ["year", 2020]}], metadata))   # False — trượt luật 1, đạt luật 2
print(khop(bo_loc, metadata))             
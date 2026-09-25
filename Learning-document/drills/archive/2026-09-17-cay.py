# ĐỀ SÁNG 17/09 (phần 2) — BỘ LỌC LỒNG: danh_gia
# Chỉ gõ vào chỗ có chữ  ✍️ GÕ Ở ĐÂY. Thứ tự hàm, dấu #, dòng thử: Claude lo, bạn không đụng.
# Tắt Copilot. Mỗi lần một mẩu → báo Claude chạy.
#
# ─── Tờ luật giờ có thể LỒNG ─────────────────────────────────────
#   lá     {"gt": ["year", 2020]}                       → so với thẻ (xet_mot_luat làm được)
#   VÀ     {"and": [con, con, ...]}                     → giống khop
#   HOẶC   {"or":  [con, con, ...]}                     → giống khop_hoac
#   KHÔNG  {"not": [con]}                               → lật kết quả của đúng 1 con
#   Mỗi "con" lại có thể là lá, HOẶC là một and/or/not khác.


# ─── DỮ LIỆU (đừng sửa) ──────────────────────────────────────────
metadata = {"lang": "vi", "year": 2021, "lang_count": 5}


# ─── Hàm bạn tự viết sáng nay (đừng sửa) ─────────────────────────
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


# ─── HÀM MỚI ─────────────────────────────────────────────────────
def danh_gia(pred: dict, metadata: dict) -> bool:
    phep = list(pred.keys())[0]

    # MẨU A — nút LÁ: phep là "eq" hoặc "gt" hoặc "lt" → trả kết quả so với thẻ
    # ✍️ GÕ Ở ĐÂY
    if phep == "eq" or phep == "gt" or phep == "lt":
        return xet_mot_luat(pred, metadata)


    # MẨU B — "and": pred["and"] là list các con. Tất cả con đạt mới True.
    # ✍️ GÕ Ở ĐÂY
    if phep == "and":
        for con in pred["and"]:
            if danh_gia(con, metadata) == False:
                return False
        return True



    # MẨU C — "or": một con đạt là True.   (logic của bạn; Claude sửa 2 chỗ chép từ and + thụt lề)
    if phep == "or":
        for con in pred["or"]:
            if danh_gia(con, metadata) == True:
                return True
        return False

    # MẨU D — "not": pred["not"] là list có ĐÚNG 1 con. Lật kết quả con đó.
    # ⚠️ Claude viết — CÓ CÀI LỖI. Đừng sửa, đọc thôi.
    if phep == "not":
        return not danh_gia(pred["not"][0], metadata)

    # Không lọt nhánh nào → gõ sai tên phép. Nổ to, đừng lặng lẽ trả None (None != False → and cho qua).
    raise ValueError(f"phép không hợp lệ: {phep}")


# ─── CA THỬ (Claude bật từng nhóm khi tới mẩu đó) ────────────────
print("--- mẩu A ---")
print(danh_gia({"gt": ["year", 2020]}, metadata))    # True
print(danh_gia({"eq": ["lang", "en"]}, metadata))    # False

print("--- mẩu B ---")
print(danh_gia({"and": [{"eq": ["lang", "vi"]}, {"gt": ["year", 2020]}]}, metadata))   # True  — đạt cả 2
print(danh_gia({"and": [{"eq": ["lang", "vi"]}, {"gt": ["year", 2025]}]}, metadata))   # False — trượt con 2

print("--- mẩu B2: con lại là một 'and' ---")
print(danh_gia({"and": [{"eq": ["lang", "vi"]}, {"and": [{"gt": ["year", 2020]}, {"lt": ["lang_count", 9]}]}]}, metadata))   # True — vi · 2021>2020 · 5<9

print("--- mẩu C ---")
print(danh_gia({"or": [{"eq": ["lang", "en"]}, {"gt": ["year", 2020]}]}, metadata))   # True  — con 2 đạt
print(danh_gia({"or": [{"eq": ["lang", "en"]}, {"gt": ["year", 2025]}]}, metadata))   # False — trượt cả 2
print(danh_gia({"and": [{"eq": ["lang", "vi"]}, {"or": [{"gt": ["year", 2025]}, {"lt": ["lang_count", 9]}]}]}, metadata))   # True — lồng: vi VÀ (2021>2025 HOẶC 5<9)

print("--- VÒNG ĐOÁN (mẩu D) ---")
print(danh_gia({"not": [{"eq": ["lang", "en"]}]}, metadata))                                        # dòng 1
print(danh_gia({"or": [{"eq": ["lang", "en"]}, {"not": [{"lt": ["year", 2020]}]}]}, metadata))      # dòng 2
print(danh_gia({"not": [{"or": [{"gt": ["year", 2020]}, {"eq": ["lang", "en"]}]}]}, metadata))      # dòng 3

print("--- LỖI THẬT: gõ sai tên phép ---")
try:
    danh_gia({"and": [{"eg": ["lang", "en"]}, {"gt": ["year", 2020]}]}, metadata)
    print("KHÔNG NỔ — lọt cửa (SAI)")
except ValueError as e:
    print("NỔ đúng:", e)

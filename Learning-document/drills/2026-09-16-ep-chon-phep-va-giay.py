# ĐỀ SÁNG 16/09 — ÉP CHỌN. Hộp 12 phút, làm hết rồi báo Claude chấm MỘT lần.
# Không chạy code. Không mở file khác. Trả lời cụt lủn 1-2 chữ là được, gõ ngay sau dấu >
#
# ─── VÁN 1: phép → dấu (8 câu, mỗi câu 1 dấu) ────────────────────────────
# Chỉ ghi dấu: <  hoặc  >  hoặc  ==

# 1. {"gt": ["year", 2020]}        > >
# 2. {"lt": ["year", 2020]}        > <
# 3. {"eq": ["lang", "vi"]}        > ==
# 4. {"gt": ["lang_count", 9]}     > >
# 5. {"lt": ["score", 0.5]}        > <
# 6. {"gt": ["score", 0.5]}        > >


# ─── VÁN 2: cùng luật, ra True hay False (6 câu) ─────────────────────────
# the = {"lang": "vi", "year": 2019, "lang_count": 5}
# Chỉ ghi True hoặc False.

# 7.  {"gt": ["year", 2020]}        > FALSE
# 8.  {"lt": ["year", 2020]}        > TRUE
# 9.  {"gt": ["lang_count", 3]}     > TRUE
# 10. {"lt": ["lang_count", 3]}     > FALSE
# 11. {"eq": ["lang", "vi"]}        > true
# 12. {"eq": ["lang", "en"]}        > false


# ─── VÁN 3: mảnh này nằm trên giấy nào (7 câu) ───────────────────────────
# Chỉ ghi LUAT hoặc THE.
# luật: {"gt": ["lang_count", 3]}      thẻ: {"lang": "vi", "lang_count": 5, "year": 2019}

# 13. chữ "gt"            nằm trên   > LUAT
# 14. chữ "lang_count"    nằm trên   > THE
# 15. số 3                nằm trên   > LUAT
# 16. số 5                nằm trên   > THE
# 17. chữ "vi"            nằm trên   > THE
# 18. số 2019             nằm trên   > THE
# 19. Trong một luật, có đúng mấy mảnh phải đi lấy từ THẺ?   > 1


# ─── VÁN 4: có nháy hay không nháy (4 câu) ───────────────────────────────
# ten_truong = "lang_count"     (biến, đã gán sẵn)
# the = {"lang": "vi", "lang_count": 5, "year": 2019}
# Ghi: ra số mấy, hoặc chữ NỔ.

# 20. the[ten_truong]        >  nổ
# 21. the["ten_truong"]      > 5
# 22. the["lang_count"]      > 5
# 23. the[lang_count]        > nổ

# Bài CÂY PREDICATE — 2026-09-15 ở công ty  ·  cầu nối từ drill dict lồng sang `danh_gia`
#
# Cách làm:
#   - Điền vào chỗ ___ . Chỉ ghi trong comment, KHÔNG sửa dòng code `p2 = ...` và `metadata = ...`.
#   - Làm HẾT 4 câu rồi mới báo Claude. Sai cũng cứ ghi.
#   - Tắt Copilot.

p2 = {"or": [{"eq": ["lang", "en"]}, {"not": [{"lt": ["year", 2020]}]}]}
metadata = {"lang": "vi", "year": 2021}


# ─── CÂU 1: điền cây ─────────────────────────────────────────────
# Mỗi ô ___ : ghi KIỂU (dict / list) hoặc GIÁ TRỊ (chuỗi / số).
# Mẫu tham chiếu (cây của p, KHÔNG phải p2):
#
#   p                          dict
#   └─ "and" →                 list
#        ├─ [0] →              dict
#        │    └─ "eq" →        list
#        │         ├─ [0] → "lang"
#        │         └─ [1] → "vi"
#        └─ [1] →              dict
#             └─ "gt" →        list
#                  ├─ [0] → "year"
#                  └─ [1] → 2020
#
# Cây của p2 — điền:
#
#   p2                         dict
#   └─ "or" →                  list
#        ├─ [0] →              list
#        │    └─ "[{"eq": ["lang", "en"]}, {"not": [{"lt": ["year", 2020]}]}]" →       ___
#        │         ├─ [0] → "eq": ["lang", "en"]}
#        │         └─ [1] → {"not": [{"lt": ["year", 2020]}]}
#        └─ [1] →              ___
#             └─ "___" →       ___
#                  └─ [0] →    ___
#                       └─ "___" →   ___
#                            ├─ [0] → ___
#                            └─ [1] → ___


# ─── CÂU 2 ───────────────────────────────────────────────────────
# list(p2.keys())[0]  ra:  ___
# p2["or"][1]  là nút LÁ hay nút NHÁNH:  ___   (vì sao:  ___ )


# ─── CÂU 3 ───────────────────────────────────────────────────────
# Biểu thức lấy ra chuỗi "year" (đếm đủ nấc):
#   p2___


# ─── CÂU 4: tự tay đi từ LÁ lên GỐC, với metadata ở trên ───────────
# Nút lá thì nhìn metadata. Nút nhánh thì chỉ nhìn kết quả các con.
#
#   nút                         | nhìn vào cái gì            | ra True/False
#   ----------------------------|----------------------------|--------------
#   {"eq": ["lang", "en"]}      | ___                        | ___
#   {"lt": ["year", 2020]}      | ___                        | ___
#   {"not": [...]}              | ___                        | ___
#   {"or": [...]}  (cả p2)      | ___                        | ___

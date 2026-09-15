# ĐỀ CA TỐI 15/09 (20:40-21:40) — BỘ LỌC PHẲNG
# Chỉ làm file này. Bỏ qua mọi đề khác trong chat. Tắt Copilot.
#
# ─── Ẩn dụ bảo vệ cửa ───────────────────────────────────────────
#   tờ luật     = bo_loc      (một list các luật)
#   một luật    = dieu_kien   ví dụ {"lt": ["year", 2010]}
#                              "lt"   = PHÉP     (lt: nhỏ hơn · gt: lớn hơn · eq: bằng)
#                              "year" = NHÌN dòng nào trên thẻ     ← nằm trên LUẬT
#                              2010   = SO VỚI cái gì              ← nằm trên LUẬT
#   thẻ tên     = metadata    ví dụ {"lang": "vi", "year": 2021}
#   cho vào?    = True / False
#
# Chỉ MỘT thứ lấy từ metadata: giá trị thật trên thẻ (2021). Mọi thứ khác lấy từ dieu_kien.

dieu_kien = {"lt": ["year", 2010]}
metadata = {"lang": "vi", "year": 2021}


# ─── BƯỚC 1 ── đã xong (bạn tự gõ chiều nay) ──────────────────────
phep = list(dieu_kien.keys())[0]
ten_truong = dieu_kien[phep][0]    
gia_tri = dieu_kien[phep][1]       
gia_tri_the = metadata[ten_truong]   



# ─── BƯỚC 2 ── ĐANG LÀM ───────────────────────────────────────────
# Cất số 2010 vào biến gia_tri. Chỉ dùng dieu_kien, KHÔNG có chữ metadata.
# Gợi ý: dieu_kien["lt"] là ["year", 2010]  →  ô [0] là "year", ô [1] là ...



# Rồi một dòng so sánh "nhỏ hơn" giữa gia_tri_the và gia_tri (bạn đã gõ đúng chiều nay):
if (phep == "lt"):
    ket_qua = gia_tri_the < gia_tri
elif( phep == "gt"):
    ket_qua = gia_tri_the > gia_tri
elif ( phep == "eq"):
    ket_qua = gia_tri_the == gia_tri
  



print(ket_qua)   # phải ra False   (2021 < 2010 ?)




# ─── BƯỚC 3 ── chưa làm ───────────────────────────────────────────
# Ở trên đang gõ cứng "lt" trong dieu_kien["lt"]. Phép cũng phải lấy từ luật.
# Luật chỉ có ĐÚNG 1 key → dùng món list(....keys())[0] đã luyện sáng nay.
# Rồi: phép là "lt" thì so <, "gt" thì so >, "eq" thì so ==.
# (làm sau khi bước 2 chạy đúng)


# ─── BƯỚC 4 ── chưa làm ───────────────────────────────────────────
# def khop(bo_loc: list, metadata: dict) -> bool:
#     ...
# bo_loc có hình dạng giống `qua`: list các dict, mỗi dict 1 key.
# Cho vào khi TẤT CẢ luật đều đạt.
# (làm sau khi bước 3 chạy đúng)

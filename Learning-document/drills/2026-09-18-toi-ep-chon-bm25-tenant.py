# DRILL ÉP CHỌN — BM25 MẶT CHỮ ↔ DENSE NGHĨA  +  TENANT PHÂN VÙNG ↔ LỌC
# Soạn tối 18/09, nhắm 2 câu hỏng nặng nhất slot công ty sáng cùng ngày (Cặp 15 · câu 3.9).
# Cách làm: KHÔNG chạy file, KHÔNG mở note. Trả lời LIÊN TỤC hết 12 câu rồi mới báo Claude chấm 1 lượt.
# Ghi câu trả lời ngay sau dấu "=". Mỗi câu một chữ/một cụm.
#
# ─── KHO ĐANG XÉT (dùng chung cả 3 ván) ──────────────────────────
#   tenant "congty_A" có 2 doc:
#     d1 = "gia xe hoi tang manh trong nam nay"
#     d2 = "thu tuc dang ky kinh doanh theo Luat Doanh nghiep 2020"
#   tenant "congty_B" có 1 doc:
#     d3 = "gia xe hoi tang manh trong nam nay"      <- chữ y hệt d1
#
#   Hệ thống có 2 nhánh: BM25Index (tự viết)  và  dense (BGE + Qdrant).


# ═══ VÁN 1 — CHỈ nhánh BM25, tenant congty_A. Trả về CÓ hay RỖNG? ═══
# Trả lời bằng CÓ hoặc RỖNG.

# 1.  hỏi "xe hoi"                                              =
# 2.  hỏi "o to"                                                =
# 3.  hỏi "oto"                                                 =
# 4.  hỏi "dang ky kinh doanh"                                  =
# 5.  hỏi "thanh lap cong ty"                                   =


# ═══ VÁN 2 — ÉP CHỌN NHÁNH. Nhánh nào bắt được truy vấn này? ═══
# Trả lời bằng BM25 hoặc DENSE. (Chỉ chọn MỘT — nhánh khoẻ hơn hẳn ở ca đó.)

# 6.  "o to"                       (doc viết "xe hoi")          =
# 7.  "Luat Doanh nghiep 2020"     (doc viết đúng nguyên văn)    =
# 8.  "Nghi dinh 15/2022/ND-CP"    (số hiệu văn bản)            =
# 9.  "thu tuc mo doanh nghiep"    (doc viết "dang ky kinh doanh") =


# ═══ VÁN 3 — TENANT: cơ chế chặn là gì ═══

# 10. congty_A hỏi "xe hoi" — có bao giờ thấy d3 không?
#     Trả lời CÓ hoặc KHÔNG.                                    =

# 11. Bên BM25Index, cái chặn d3 là: một bước LỌC sau khi chấm điểm,
#     hay là do d3 KHÔNG NẰM TRONG vòng lặp chấm điểm ngay từ đầu?
#     Trả lời LỌC SAU hoặc KHÔNG VÀO ĐƯỢC.                      =

# 12. Bên Qdrant, cái chặn doc tenant khác là gì?
#     Trả lời LỌC THẬT hoặc KHÔNG VÀO ĐƯỢC.                     =

"""
Drill closure — 2026-09-05
==========================
Vì sao có file này: tối 05/09, khi tự sửa bug #26, vấp `UnboundLocalError` do gán đè lên
chính tên biến closure. Hiểu thì hiểu rồi, nhưng chưa gõ ra được từ màn hình trắng.
Drill này để chuyển từ "nhận ra" sang "tự dựng".

LUẬT:
- ĐÓNG app/application/generation/node.py lại. Không nhìn.
- Tự gõ phần thân hàm. Phần kiểm tra bên dưới mỗi bài đã viết sẵn, đừng sửa nó.
- Chạy:  .venv/bin/python3 Learning-document/drills/2026-09-05-closure.py
- Sai thì đọc thông báo lỗi (tên lỗi + dòng nó chỉ vào) trước khi sửa bất cứ thứ gì.
"""

# =====================================================================
# BÀI 1 — dựng nhà máy đẻ hàm
# Yêu cầu: make_adder(n) trả về MỘT HÀM; hàm đó nhận x và trả về x + n.
# =====================================================================


def make_adder(n):
    def adder(x):
        return x + n
    return adder
print("=== BÀI 1 ===")
add5 = make_adder(5)
add10 = make_adder(10)
print("add5(1), add10(1) =", add5(1), add10(1))          # kỳ vọng: 6 11
print("add5 is add10     =", add5 is add10)              # tôi đoán là False, vì mỗi lần gọi make_adder là tạo ra một hàm mới
print("add5 nhớ n =", add5.__closure__[0].cell_contents)  # kỳ vọng 5
print("add10 nhớ n =", add10.__closure__[0].cell_contents)


# =====================================================================
# BÀI 2 — chính là hình dạng bản fix bug #26, nhưng đổi bối cảnh, viết từ số 0
# Yêu cầu: make_bao_cao(so_dong_mac_dinh) trả về hàm bao_cao(tuy_chon).
#   - tuy_chon là một dict.
#   - Nếu dict CÓ key "so_dong"      -> dùng giá trị trong dict.
#   - Nếu dict KHÔNG có key đó       -> dùng so_dong_mac_dinh.
#   - Trả về số dòng thực dùng (return, không phải print).
# =====================================================================


def make_bao_cao(so_dong_mac_dinh):
    def bao_cao(tuy_chon):
        so_dong = tuy_chon.get("so_dong", so_dong_mac_dinh)
        return so_dong
    return bao_cao


print("\n=== BÀI 2 ===")
f = make_bao_cao(10)
print("f({})                  =", f({}))                   # kỳ vọng 10
print("f({'so_dong': 50})     =", f({"so_dong": 50}))      # kỳ vọng 50
print("f({}) lần nữa          =", f({}))                   # kỳ vọng LẠI 10  <-- quan trọng nhất
assert f({}) == 10 and f({"so_dong": 50}) == 50 and f({}) == 10, "Bài 2 chưa đúng"
print("Bài 2 OK — lượt gọi trước không làm nhiễm lượt sau")


# =====================================================================
# BÀI 3 — tự gây lại đúng lỗi đã vấp tối nay, rồi tự sửa
# Yêu cầu: chép make_bao_cao ở bài 2 xuống đây, đổi tên thành make_bao_cao_loi,
#          nhưng ĐẶT TÊN BIẾN TRONG HÀM TRONG TRÙNG với so_dong_mac_dinh.
#          Chạy -> phải nổ. Đọc kỹ tên lỗi. Ghi lại nó vào biến TEN_LOI bên dưới.
#          Sau đó sửa lại cho chạy được (giữ nguyên tên hàm make_bao_cao_loi).
# =====================================================================

TEN_LOI = "UnboundLocalError"   # điền đúng tên lỗi bạn thấy


def make_bao_cao_loi(so_dong_mac_dinh):
    def bao_cao(tuy_chon):
        so_dong = tuy_chon.get("so_dong", so_dong_mac_dinh)
        return so_dong
    return bao_cao


print("\n=== BÀI 3 ===")
print("Tên lỗi đã gặp:", TEN_LOI)
g = make_bao_cao_loi(7)
print("g({}) =", g({}))


# =====================================================================
# BÀI 4 — nonlocal
# Yêu cầu: make_dem() trả về một hàm; mỗi lần gọi hàm đó thì trả về số lần
#          nó đã được gọi (lần 1 -> 1, lần 2 -> 2, lần 3 -> 3).
#          Gợi ý tra cứu: từ khoá `nonlocal` (khác `global`).
# =====================================================================


def make_dem():
    def dem():
        nonlocal count
        count += 1
        return count
    count = 0
    return dem

print("\n=== BÀI 4 ===")
dem = make_dem()
print(dem(), dem(), dem())          # kỳ vọng 1 2 3
dem2 = make_dem()
print("bộ đếm mới:", dem2())        # kỳ vọng 1 — đếm riêng, không dính bộ đếm cũ

# --- CÂU HỎI VIẾT (trả lời bằng lời, gõ thẳng vào chuỗi bên dưới) ---
TRA_LOI = "nonlocal sai ở đây tại vì ghi đè vào cía closuse và sẽ ảnh hởng tới người khác ví dụ người a tìm không ra candidate = 10 khi nâng lên 40 tại vì là biến toàn cụ nên người bên B cũng bị ảnh hưởng
  "
Nếu trong retrieve_node dùng `nonlocal candidate_k` để nới rộng, thay vì tạo biến mới:
- Request TIẾP THEO của một người dùng khác sẽ nhận candidate_k bằng bao nhiêu? nếu theo bài 4 sẽ tăng 1 vì đã nới rộng ra 1 rồi Vì sao?
- Điều đó gây vấn đề gì? không biết

(viết câu trả lời của bạn ở đây)
"""
print("\n=== CÂU HỎI VIẾT ===")
print(TRA_LOI)

# PHÒNG TẬP CÚ PHÁP — VÁN 2  (soạn 29/09)
# Mục tiêu: VỎ cú pháp, nhắm Cặp 18 (tên biến vs tên hàm trước dấu "(") + "= []" + ":" + nháy.
# Luật: gõ hết 10 ô RỒI mới chạy. Chạy xong sửa một lượt. Tên biến: COPY-PASTE từ đề, không gõ tay.
# Chạy: .venv/bin/python Learning-document/drills/gym-cu-phap-van-2.py

BOX = [4, 9, 2, 7]
PRICES = {"cam": 30, "xoai": 50}


# 1. Khai một dict RỖNG, đặt tên là  stock
# ✍️
stock = {}

# 2. Gán vào  stock  khoá "tao" với giá trị 12  (một dòng, dùng ngoặc vuông và dấu =)
# ✍️
stock["tao"] = 12

# 3. Đếm  BOX  có bao nhiêu phần tử, cất vào biến  size   -> ra 4
# ✍️
size = len(BOX)

# 4. Tổng các số trong  BOX  bằng hàm có sẵn  sum , cất vào biến  total   -> ra 22
# ✍️
total = sum(BOX)

# 5. Lấy danh sách các KHOÁ của  PRICES  thành một list, cất vào biến  fruits   -> ra ["cam", "xoai"]
# ✍️
fruits = list(PRICES.keys())

# 6. Lấy GIÁ của "xoai" trong  PRICES , cất vào biến  mango_price   -> ra 50
# ✍️
mango_price = PRICES["xoai"]

# 7. Nối chuỗi "gia: " với chữ "re" thành MỘT chuỗi, cất vào biến  label   -> ra "gia: re"
# ✍️
label = "gia: " + "re"


# 8. Viết hàm  grade : score >= 8 trả "gioi", score >= 5 trả "kha", còn lại trả "yeu"
#    (def + if + elif + else, mỗi dòng mở khối phải có dấu ":")
# ✍️  xoá dòng "pass" rồi gõ ruột
def grade(score: int) -> str:
    if(score >= 8):
        return "gioi"
    elif (score >= 5 ):
        return "kha"
    else:
        return "yeu"

# 9. Gọi hàm  grade  với số 6, cất vào biến  result   -> ra "kha"
# 
result = grade(6)

# 10. Viết hàm  only_big : trả về list mới chỉ gồm các số LỚN HƠN 5 trong  xs
#     (list rỗng + for + if + append + return)
# ✍️  xoá dòng "pass" rồi gõ ruột
def only_big(xs: list) -> list:
    new_list = []
    for value in xs :
        if(value > 5):
            new_list.append(value)
    return new_list


# ═══════ TỪ ĐÂY XUỐNG LÀ CỦA CLAUDE — ĐỪNG SỬA ══════════════════
def _safe(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return f"NO: {type(e).__name__}"


CHECKS = [
    ("1. stock dung kieu dict", type(stock).__name__ if stock is not None else None, "dict"),
    ("2. stock sau khi gan", stock if stock else None, {"tao": 12}),
    ("3. size", size, 4),
    ("4. total", total, 22),
    ("5. fruits", fruits, ["cam", "xoai"]),
    ("6. mango_price", mango_price, 50),
    ("7. label", label, "gia: re"),
    ("8. grade(9) / grade(5) / grade(2)",
     None if grade(9) is None else (_safe(grade, 9), _safe(grade, 5), _safe(grade, 2)),
     ("gioi", "kha", "yeu")),
    ("9. result", result, "kha"),
    ("10. only_big([4, 9, 2, 7])", _safe(only_big, [4, 9, 2, 7]), [9, 7]),
]


def main() -> None:
    ok = 0
    for ten, got, want in CHECKS:
        if got == want:
            ok += 1
            print(f"DUNG  {ten}")
        elif got is None:
            print(f"chua go  {ten}")
        else:
            print(f"SAI   {ten}  ->  {got!r}   (mong: {want!r})")
    print(f"\n{ok}/{len(CHECKS)} o dung")
    if ok < len(CHECKS):
        print("Sai o nao thi sua o do roi chay lai. Khong xem dap an o dau khac.")


if __name__ == "__main__":
    main()

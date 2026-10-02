# PHÒNG TẬP CÚ PHÁP — VÁN 3  (soạn 02/10 tối)
# Mục tiêu: gán khoá vào dict · list(...) ngoặc tròn · Cặp 21 (.append trả None, sửa list gốc) · Cặp 19 (dict↔list).
# Luật: gõ hết 10 ô RỒI mới chạy. Chạy xong sửa một lượt. Tên biến: COPY-PASTE từ đề, không gõ tay.
# Mỗi ô: XOÁ chữ None sau dấu = rồi gõ vào chỗ đó (ô 9, 10: xoá dòng "return None").
# Chạy: .venv/bin/python Learning-document/drills/gym-cu-phap-van-3.py

PRED = {"or": [{"eq": ["loai", "Luật"]}, {"gte": ["nam", 2020]}]}
SCORES = {"an": 7, "binh": 9}
NAMES = ["an", "binh"]


# 1. Thêm vào dict  SCORES  khoá "chi" với giá trị 5  (một dòng, ngoặc vuông + dấu =; KHÔNG gán cho biến khác)
# ✍️
SCORES_STEP_1 = None   # ← xoá cả dòng này, gõ dòng của bạn thay vào

# 2. Đổi điểm của "an" trong  SCORES  thành 8  (một dòng)
# ✍️
SCORES_STEP_2 = None   # ← xoá cả dòng này, gõ dòng của bạn thay vào

# 3. Lấy các KHOÁ của  SCORES  thành một list, cất vào biến  people   -> ra ["an", "binh", "chi"]
# ✍️
people = None

# 4. Lấy list nằm dưới khoá "or" của  PRED , cất vào biến  children   -> ra list 2 dict con
# ✍️
children = None

# 5. Lấy dict con THỨ HAI trong  children , cất vào biến  second   -> ra {"gte": ["nam", 2020]}
# ✍️
second = None

# 6. Lấy số 2020 từ  second , cất vào biến  year   (bóc 2 lớp: khoá "gte" rồi vị trí)
# ✍️
year = None

# 7. Tạo list MỚI  bigger  = NAMES nối thêm "chi" bằng DẤU +  (NAMES phải giữ nguyên 2 tên)
# ✍️
bigger = None

# 8. Dùng .append nhét "dung" vào  bigger  (một dòng, KHÔNG có dấu =)
#    rồi ở dòng dưới: cất  len(bigger)  vào biến  count   -> ra 4
# ✍️
count = None


# 9. Viết hàm  collect_ops : nhận list các dict con, trả LIST các khoá ngoài cùng của từng con
#    vd collect_ops(children) -> ["eq", "gte"]
#    (list rỗng + for + list(...keys())[0] + append trên DÒNG RIÊNG + return tên list)
# ✍️
def collect_ops(items: list) -> list:
    return None


# 10. Viết hàm  count_letters : nhận một chuỗi, trả DICT đếm mỗi chữ xuất hiện mấy lần
#     vd count_letters("aba") -> {"a": 2, "b": 1}
#     (dict rỗng + for + if chữ đã có trong dict thì +1, không thì gán 1 + return)
# ✍️
def count_letters(text: str) -> dict:
    return None


# ═══════ TỪ ĐÂY XUỐNG LÀ CỦA CLAUDE — ĐỪNG SỬA ══════════════════
def _safe(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return f"NỔ: {type(e).__name__}"


CHECKS = [
    ("1+2. SCORES sau ô 1 và ô 2", SCORES if SCORES != {"an": 7, "binh": 9} else None,
     {"an": 8, "binh": 9, "chi": 5}),
    ("3. people", people, ["an", "binh", "chi"]),
    ("4. children", children, [{"eq": ["loai", "Luật"]}, {"gte": ["nam", 2020]}]),
    ("5. second", second, {"gte": ["nam", 2020]}),
    ("6. year", year, 2020),
    ("7a. bigger", bigger if bigger is None else bigger[:3], ["an", "binh", "chi"]),
    ("7b. NAMES giữ nguyên", NAMES if bigger is not None else None, ["an", "binh"]),
    ("8. count", count, 4),
    ("9. collect_ops", _safe(collect_ops, PRED["or"]), ["eq", "gte"]),
    ("10. count_letters('aba')", _safe(count_letters, "aba"), {"a": 2, "b": 1}),
]


def main() -> None:
    ok = 0
    for name, got, want in CHECKS:
        if got == want:
            ok += 1
            print(f"ĐÚNG  {name}")
        elif got is None:
            print(f"chưa gõ  {name}")
        else:
            print(f"SAI   {name}  ->  {got!r}   (mong: {want!r})")
    print(f"\n{ok}/{len(CHECKS)} ô đúng")
    if ok < len(CHECKS):
        print("Sai ô nào thì sửa ô đó rồi chạy lại. Không xem đáp án ở đâu khác.")


if __name__ == "__main__":
    main()

"""Khởi động cú pháp Python — 6 bài, không dính RAG.

Chạy:  .venv/bin/python Learning-document/drills/2026-09-07-cu-phap.py

Điền thân từng hàm (thay chỗ `pass`). Chạy lại sau mỗi bài để xem ĐÚNG/SAI ngay.
Không cần làm hết một lượt — làm 1 bài, chạy, rồi sang bài sau.
"""


# BÀI 1 — for + append
# Trả về danh sách MỚI, mỗi số nhân đôi.
def bai1(nums):
    result = []
    for n in nums:
        result.append(n * 2)
    return result


# BÀI 2 — for + cộng dồn vào một biến
# Trả về tổng của tất cả các số.
def bai2(nums):
    result = 0
    for n in nums:
        result += n
    return result


# BÀI 3 — for + if + append
# Trả về danh sách MỚI chỉ gồm các số chẵn.  (chẵn: n % 2 == 0)
def bai3(nums):
    result = []
    for n in nums:
        if(n% 2==0):
            result.append(n)
    return result


# BÀI 4 — for + cộng dồn vào một CHUỖI
# Nối tất cả các chuỗi lại thành một chuỗi duy nhất.
def bai4(words):
    result = ""
    for w in words:
        result += w
    return result


# BÀI 5 — for + if/else + hai danh sách
# Trả về (ngan, dai): chuỗi <= 3 ký tự vào `ngan`, còn lại vào `dai`.
def bai5(words):
    ngan = []
    dai = []
    for w in words:
        if(len(w) <= 3):
            ngan.append(w)
        else:
            dai.append(w)
    return (ngan, dai)


# BÀI 6 — len() + đếm
# Trả về SỐ LƯỢNG chuỗi dài hơn 3 ký tự.
def bai6(words):
    count = 0
    for w in words:
        if len(w) > 3:
            count += 1
    return count


# ----------------------------------------------------------------- chấm bài
TESTS = [
    ("bài 1", lambda: bai1([1, 2, 3]),            [2, 4, 6]),
    ("bài 2", lambda: bai2([1, 2, 3, 4]),         10),
    ("bài 3", lambda: bai3([1, 2, 3, 4, 5, 6]),   [2, 4, 6]),
    ("bài 4", lambda: bai4(["a", "b", "c"]),      "abc"),
    ("bài 5", lambda: bai5(["meo", "cho", "ca vang"]), (["meo", "cho"], ["ca vang"])),
    ("bài 6", lambda: bai6(["meo", "cho", "ca vang", "chim canh cut"]), 2),
]

for ten, chay, mong_doi in TESTS:
    try:
        thuc_te = chay()
    except Exception as e:
        print("{}  LỖI: {}".format(ten, e))
        continue
    if thuc_te == mong_doi:
        print("{}  ĐÚNG".format(ten))
    elif thuc_te is None:
        print("{}  chưa làm".format(ten))
    else:
        print("{}  SAI  — ra {!r}, cần {!r}".format(ten, thuc_te, mong_doi))

# Drill CÚ PHÁP vòng 2 — 2026-09-15 ~06:30  ·  nhắm thẳng 5 lỗi gốc của vòng 1
#
# Vòng 1 (2026-09-15-cu-phap-dict-long.py): ~3/13. Năm lỗi gốc lặp đi lặp lại:
#   L1. quên bước index vào list  ->  don["combo"] KHÁC don["combo"][0]
#   L2. `in` trên dict hỏi KEY, không hỏi value
#   L3. đếm index từ 1 (lấy [1] tưởng là phần tử đầu)
#   L4. ["pho", 2] là LIST, không phải dict
#   L5. print trong vòng for in ra NHIỀU DÒNG, không gộp thành 1 list
#
# Dữ liệu ĐỔI HÌNH so với vòng 1 — để không trả lời bằng trí nhớ.
# Luật cũ: KHÔNG chạy file. Ghi vào "# DỰ ĐOÁN". Làm hết rồi báo. Tắt Copilot.
# Ghi chú thì ghi ở DÒNG # DỰ ĐOÁN, đừng ghi chèn vào dòng code (vòng 1 file hỏng vì vậy).

kho = {"sach": [{"ten": ["python", 120]}, {"tac_gia": ["nam", 7]}, {"nam": [2021]}]}


def bai_1():
    print(list(kho.keys()))
    print(len(kho))
# DỰ ĐOÁN 1:
["sach"]
1


def bai_2():
    print("sach" in kho)
    print("ten" in kho)
    print("python" in kho)
# DỰ ĐOÁN 2:
True
False
false

def bai_3():
    print(len(kho["sach"]))
    print(type(kho["sach"]).__name__)
    print(type(kho["sach"][0]).__name__)
# DỰ ĐOÁN 3:
3 
list
dict


def bai_4():
    print(kho["sach"][0])
    print(kho["sach"][1])
    print(kho["sach"][2])
# DỰ ĐOÁN 4:
{"ten": ["python", 120]}
{"tac_gia": ["nam", 7]}
{"nam": [2021]}


def bai_5():
    con = kho["sach"][1]
    print(list(con.keys())[0])
# DỰ ĐOÁN 5:
con = {"tac_gia": ["nam", 7]} => key = "tac_gia"

def bai_6():
    con = kho["sach"][0]
    ten = list(con.keys())[0]
    print(ten)
    print(con[ten])
    print(con[ten][0])
    print(con[ten][1])
# DỰ ĐOÁN 6:


con = {"ten": ["python", 120]}
ten = "python"
con[ten][0] = "python"
con[ten][1] = 120
con[ten] = ["python", 120]

def bai_7():
    print(isinstance(kho["sach"], list))
    print(isinstance(kho["sach"][2], dict))
    print(isinstance(kho["sach"][2]["nam"], dict))
    print(isinstance(kho["sach"][2]["nam"], list))
# DỰ ĐOÁN 7:

True
True
false => list
true
def bai_8():
    for con in kho["sach"]:
        print(list(con.keys())[0])
# DỰ ĐOÁN 8:
kho = {"sach": [{"ten": ["python", 120]}, {"tac_gia": ["nam", 7]}, {"nam": [2021]}]}
"ten"
def bai_9():
    ket_qua = []
    for con in kho["sach"]:
        ket_qua.append(list(con.keys())[0])
    print(ket_qua)
# DỰ ĐOÁN 9:
# (bài 8 và bài 9 in ra KHÁC nhau chỗ nào? ghi rõ.)
["ten"]


def bai_10():
    con = kho["sach"][2] = {"nam": [2021]}
    ten = list(con.keys())[0] 2021
    print(len(con[ten])) 1
# DỰ ĐOÁN 10:

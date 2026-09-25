# Drill CÚ PHÁP — đi lại trong dict LỒNG  ·  2026-09-15 sáng (ca 5:25-7:30)
#
# Vì sao có bài này: sáng 15/09 bí bước 1 mốc 2, user báo bí "kiểu A và B luôn"
# (vừa bí logic vừa bí cú pháp). Luật §3.5: bí cú pháp thì DỪNG bài chính,
# drill riêng 10' rồi quay lại. Ép tiếp khi bí cú pháp là phí giờ vàng.
#
# Bài này CHỈ tập đi lại trong dict lồng. KHÔNG có đệ quy, KHÔNG có lời giải
# của `danh_gia` ở đây — phần đó vẫn là của bạn.
#
# Cách làm:
#   1. KHÔNG chạy file. Đọc từng bài, ghi output bạn đoán vào dòng "# DỰ ĐOÁN".
#   2. Làm HẾT rồi mới báo Claude. Sai cũng cứ ghi — cần thấy sai ở đâu.
#   3. Claude chạy thật rồi so từng dòng.
#   4. Tắt Copilot.


don = {"combo": [{"mon": ["pho", 2]}, {"nuoc": ["tra_da", 3]}]}


def bai_1():
    print(list(don.keys()))
# DỰ ĐOÁN 1:
[{"mon": ["pho", 2]}, {"nuoc": ["tra_da", 3]}]

def bai_2():
    print(len(don))
# DỰ ĐOÁN 2:
1

def bai_3():
    print("combo" in don)
    print("mon" in don)
# DỰ ĐOÁN 3:
[{"mon": ["pho", 2]}, {"nuoc": ["tra_da", 3]}]

["pho", 2]

def bai_4():
    print(type(don["combo"]).__name__)
    print(len(don["combo"]))
# DỰ ĐOÁN 4:

str
2
def bai_5():
    print(don["combo"][0])
# DỰ ĐOÁN 5:
[{"mon": ["pho", 2]}, {"nuoc": ["tra_da", 3]}]

def bai_6():
    print(type(don["combo"][0]).__name__)
# DỰ ĐOÁN 6:
list

def bai_7():
    print(don["combo"][0]["mon"])
# DỰ ĐOÁN 7:


def bai_8():
    print(don["combo"][0]["mon"][0])
    print(don["combo"][0]["mon"][1])
# DỰ ĐOÁN 8:
["pho", 2]

def bai_9():
    con = don["combo"][1]
    print(list(con.keys())[0])
# DỰ ĐOÁN 9:
"mon"

def bai_10():
    con = don["combo"][1] {"nuoc": ["tra_da", 3]}
    ten = list(con.keys())[0] = mon
    print(con[ten])
# DỰ ĐOÁN 10:

[]


def bai_11():
    print(isinstance(don["combo"], list))
    print(isinstance(don["combo"][0], dict))
    print(isinstance(don["combo"][0]["mon"], dict))
# DỰ ĐOÁN 11:

don = {"combo": [{"mon": ["pho", 2]}, {"nuoc": ["tra_da", 3]}]}
true
true
true 

def bai_12():
    # Cẩn thận: hai dòng này KHÁC nhau khi key không tồn tại.
    print(don.get("khuyen_mai"))
    print(don.get("khuyen_mai", []))
# DỰ ĐOÁN 12:
NONE
[]

def bai_13():
    for con in don["combo"]:
        print(list(con.keys())[0])
# DỰ ĐOÁN 13:

["mon","nuoc"]


if __name__ == "__main__":
    for ten, ham in sorted(globals().items()):
        if ten.startswith("bai_"):
            print(f"--- {ten} ---")
            ham()

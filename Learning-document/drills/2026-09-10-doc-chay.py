# Drill ĐỌC-CHẠY từng dòng — 2026-09-10 tối (ngày B, khối 2)
#
# Cách làm:
#   1. KHÔNG chạy file. Đọc từng bài, ghi output bạn đoán vào dòng "# DỰ ĐOÁN" ngay dưới bài
#      (bài nào in nhiều dòng thì ghi nhiều dòng).
#   2. Làm HẾT các bài rồi mới báo Claude. Sai cũng cứ ghi — cần thấy sai ở đâu.
#   3. Claude chạy thật rồi so từng dòng.
#   4. Tắt Copilot.


def bai_1a():
    tong = 0
    for x in [1, 2, 3]:
        tong += x
    print(tong)

# DỰ ĐOÁN 1a:


def bai_1b():
    for x in [1, 2, 3]:
        tong = 0
        tong += x
    print(tong)

# DỰ ĐOÁN 1b:


def bai_2():
    for chu in ["a", "b", "c"]:
        print("trong", chu)
    print("ngoai", chu)

# DỰ ĐOÁN 2:


def bai_3():
    s = ""
    xe = []
    for w in ["Toi", "an", "com"]:
        s += w
        xe.append(w)
    print(s)
    print(xe, len(xe))

# DỰ ĐOÁN 3:


def bai_4a():
    xe = ["A", "B"]
    thung = "CD"
    mon = "E"
    xe.append(thung)
    thung = mon
    print(xe, thung)

# DỰ ĐOÁN 4a:


def bai_4b():
    xe = ["A", "B"]
    thung = "CD"
    mon = "E"
    thung = mon
    xe.append(thung)
    print(xe, thung)

# DỰ ĐOÁN 4b:


def bai_5():
    for n in [5, 12, 3]:
        if n <= 10:
            print("nho", n)
        else:
            print("lon", n)
        print("het vong", n)
    print("xong")

# DỰ ĐOÁN 5:


def bai_6():
    a = ["x", "y", "x"]
    b = {"x", "y", "x"}
    print(len(a), len(b))

# DỰ ĐOÁN 6:


def bai_7():
    vi = 0
    tui = []
    for tien in [4, 3, 5, 1]:
        if vi + tien <= 7:
            vi += tien
        else:
            tui.append(vi)
            vi = tien
    tui.append(vi)
    print(tui, vi)

# DỰ ĐOÁN 7:


if __name__ == "__main__":
    for ten, ham in list(globals().items()):
        if ten.startswith("bai_"):
            print(f"--- {ten} ---")
            ham()

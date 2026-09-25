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
    6
# DỰ ĐOÁN 1a:


def bai_1b():
    for x in [1, 2, 3]:
        tong = 0
        tong += x
    print(tong)
    3
# DỰ ĐOÁN 1b:


def bai_2():
    for chu in ["a", "b", "c"]:
        print("trong", chu)
    print("ngoai", chu)
    tronga trongb trongc
    ngoai c

    # DỰ ĐOÁN 2:


def bai_3():
    s = ""
    xe = []
    for w in ["Toi", "an", "com"]:
        s += w
        xe.append(w)
    print(s)
    print(xe, len(xe))

    Toiancom
    ['Toi', 'an', 'com'] 3   

# DỰ ĐOÁN 3:


def bai_4a():
    xe = ["A", "B"]
    thung = "CD"
    mon = "E"
    xe.append(thung)
    thung = mon
    print(xe, thung)

    ['A', 'B', 'CD'] E
# DỰ ĐOÁN 4a:


def bai_4b():
    xe = ["A", "B"]
    thung = "CD"
    mon = "E"
    thung = mon = "E"
    xe.append(thung) "CÓ SẴN A B"
    print(xe, thung)
    
    ['A', 'B', 'E']        E
# DỰ ĐOÁN 4b:


def bai_5():
    for n in [5, 12, 3]:
        if n <= 10:
            print("nho", n)
        else:
            print("lon", n)
        print("het vong", n)
    print("xong")

    nho 5 
    het vong 5
    lon 12
    het vong 12
    nho 3
    het vong 3
    xong

# DỰ ĐOÁN 5:


def bai_6():
    a = ["x", "y", "x"]
    b = {"x", "y", "x"}
    print(len(a), len(b))
    CÂU NÀY TÔI HIỂU ĐỌC LƯỚT K THẤY NHƯNG MÀ CÓ VẺ TÔI SAI SET LÀ NÓ GỘP GIÁ TRỊ GIỐNG NHAU THEO DẠNG KEY VALUE NÊN B CHỈ CÓ 2

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

    
    
    v1: vi = 0 + 4 = 4 rơi nhánh if vi = 4
    v2: vi = 4 + 3 = 7 rơi nhánh if vi = 7
    v3: vi = 7 + 5 = 12 rơi nhánh else
        tui.append(vi) => tui = [7]
        vi = tien => vi = 5
    v4: vi = 5 + 1 = 6 rơi nhánh if
        vi = 6
    tui.append(vi) => tui = [7, 6] vi - 6 

    

# DỰ ĐOÁN 7:


if __name__ == "__main__":
    for ten, ham in list(globals().items()):
        if ten.startswith("bai_"):
            print(f"--- {ten} ---")
            ham()

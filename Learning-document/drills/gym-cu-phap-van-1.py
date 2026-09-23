# PHONG TAP CU PHAP — VAN 1  (soan 22/09)
# Muc tieu: go nhanh, khong nghi thuat toan. Chi VO cu phap.
# Luat: go het 10 mau ROI moi chay. Chay xong sua mot luot. Khong go mot mau chay mot lan.
# Chay: .venv/bin/python Learning-document/drills/gym-cu-phap-van-1.py

D = {"gte": ["nam", 2015]}
CAY = {"and": [{"eq": ["loai", "Luat"]}, {"lt": ["nam", 2020]}]}
XS = [10, 20, 30]


# 1. Khai mot list RONG, dat ten la  bag
# ✍️
bag = None
bag = []

# 2. Them so 7 vao cuoi  bag  (mot dong, dung .append)
# ✍️
bag.append(7)

# 3. Lay CHU dau tien trong cac khoa cua  D  -> phai ra "gte"
# ✍️
key1 = list(D.keys())[0]

# 4. Dung bien  key_1  de lay gia tri tuong ung trong  D  -> ra ["nam", 2015]
# ✍️
val_1 = D[key1]

# 5. Lay phan tu DAU TIEN cua  XS  -> ra 10
# ✍️
first = XS[0]

# 6. Lay phan tu CUOI cua  XS  bang so am -> ra 30
# ✍️
last = XS[2]

# 7. Dem  XS  co bao nhieu phan tu -> ra 3   (dung ham co san len)
# ✍️
n = XS.len()

# 8. Tu  CAY  lay ra con THU HAI -> ra {"lt": ["nam", 2020]}
# ✍️
child_2 = CAY["and"][list(bag.key[0])[1]]

# 9. Viet ham tra ve mot dict co khoa "must", gia tri la  items  (dung 2 dong: def + return)
# ✍️
def wrap_must(items: list) -> dict:
    return {"must" : items}

# 10. Viet ham dem so phan tu LON HON 15 trong mot list (4 dong: def, count=0, for+if, return)
# ✍️
def count_big(xs: list) -> int:
    count = 0
    for child in xs :
        if(child > 15):
            count = count + 1
    return count
            


# ═══════ TU DAY XUONG LA CUA CLAUDE — DUNG SUA ══════════════════
def _safe(f, *a):
    try:
        return f(*a)
    except Exception as e:
        return f"NO: {type(e).__name__}"


CHECKS = [
    ("1. bag dung kieu list", type(bag).__name__ if bag is not None else None, "list"),
    ("2. bag sau append", bag, [7]),
    ("3. key_1", key_1, "gte"),
    ("4. val_1", val_1, ["nam", 2015]),
    ("5. first", first, 10),
    ("6. last", last, 30),
    ("7. n", n, 3),
    ("8. child_2", child_2, {"lt": ["nam", 2020]}),
    ("9. wrap_must([1,2])", _safe(wrap_must, [1, 2]), {"must": [1, 2]}),
    ("10. count_big([10,20,30])", _safe(count_big, [10, 20, 30]), 2),
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

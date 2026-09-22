# SANG 22/09 — BOC LOP: dict long list long dict
# Khong Qdrant. Khong de quy. Chi mot bien duy nhat, boc tung lop.
# Chay: .venv/bin/python Learning-document/drills/2026-09-22-sang-boc-lop.py

CAY = {"and": [{"eq": ["loai", "Nghi dinh"]}, {"gte": ["nam", 2015]}]}

# ─── PHAN A — CLAUDE IN SAN, ban chi doc ────────────────────────
print("LOP 0 :", type(CAY).__name__, "=", CAY)
print("LOP 1 :", type(CAY["and"]).__name__, "=", CAY["and"])
print("LOP 2 :", type(CAY["and"][0]).__name__, "=", CAY["and"][0])
print("LOP 3 :", type(CAY["and"][0]["eq"]).__name__, "=", CAY["and"][0]["eq"])
print("LOP 4 :", type(CAY["and"][0]["eq"][0]).__name__, "=", CAY["and"][0]["eq"][0])
print()
print("Moi lop boc them DUNG MOT dau ngoac. dict thi boc bang [\"ten khoa\"],")
print("list thi boc bang [so thu tu]. Nhin cot type de biet lop sau dung dau nao.")
print()

# ─── PHAN B — CUA BAN. Thay None bang bieu thuc boc tu CAY ──────
# Khong duoc gan gia tri tay (vi du = 2015). Phai boc ra tu bien CAY.

ten_hop_ngoai = list(CAY.keys())[0]   
con_thu_hai = CAY[ten_hop_ngoai][1]
nam_2015 = con_thu_hai[list(con_thu_hai.keys())[0]][1]          # ✍️ ra: 2015
ten_truong_con_dau =  CAY[ten_hop_ngoai][0][list(CAY[ten_hop_ngoai][0].keys())[0]][0]
# ═══════ TU DAY XUONG LA CUA CLAUDE — DUNG SUA ══════════════════
BAI = [
    ("ten_hop_ngoai", ten_hop_ngoai, "and"),
    ("con_thu_hai", con_thu_hai, {"gte": ["nam", 2015]}),
    ("nam_2015", nam_2015, 2015),
    ("ten_truong_con_dau", ten_truong_con_dau, "loai"),
]
dung = 0
for ten, ra, mong in BAI:
    if ra == mong:
        dung += 1
        print(f"DUNG  {ten} = {ra!r}")
    elif ra is None:
        print(f"chua go  {ten}")
    else:
        print(f"SAI   {ten} = {ra!r}   (mong: {mong!r})")
print(f"\n{dung}/{len(BAI)} o dung")

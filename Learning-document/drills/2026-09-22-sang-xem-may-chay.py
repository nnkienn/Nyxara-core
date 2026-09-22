# SANG 22/09 — XEM MAY CHAY to_qdrant_filter, KHONG HOI GI
# Ban chi chay va doc. Moi lan ham duoc goi, no in ra 2 dong:
#   VAO  <do sau>  <cay nhan duoc>
#   RA   <do sau>  <to don tra ve>
# Chay: .venv/bin/python Learning-document/drills/2026-09-22-sang-xem-may-chay.py

SO_SANH_SO = ("gt", "gte", "lt", "lte")
do_sau = 0


def to_qdrant_filter(pred: dict) -> dict:
    global do_sau
    thut = "    " * do_sau
    print(f"{thut}VAO  [{do_sau}]  {pred}")
    do_sau += 1

    phep = list(pred.keys())[0]

    if phep == "eq":
        ket_qua = {"key": pred[phep][0], "match": {"value": pred[phep][1]}}
    elif phep in SO_SANH_SO:
        ket_qua = {"key": pred[phep][0], "range": {phep: pred[phep][1]}}
    elif phep == "and":
        danh_sach_con = []
        for con in pred[phep]:
            danh_sach_con.append(to_qdrant_filter(con))
        ket_qua = {"must": danh_sach_con}
    elif phep == "or":
        danh_sach_con = []
        for con in pred[phep]:
            danh_sach_con.append(to_qdrant_filter(con))
        ket_qua = {"should": danh_sach_con}
    elif phep == "not":
        ket_qua = {"must_not": [to_qdrant_filter(pred["not"][0])]}
    else:
        raise ValueError(phep)

    do_sau -= 1
    print(f"{thut}RA   [{do_sau}]  {ket_qua}")
    return ket_qua


CAY = {
    "not": [
        {"or": [
            {"eq": ["co_quan", "Quoc hoi"]},
            {"eq": ["co_quan", "Chinh phu"]},
        ]}
    ]
}

print("Cay dau vao:", CAY)
print("Nghia: LOAI BO van ban cua Quoc hoi HOAC Chinh phu\n")
to_qdrant_filter(CAY)

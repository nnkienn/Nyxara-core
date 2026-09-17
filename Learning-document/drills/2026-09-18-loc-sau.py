# MÃ GIẢ CỦA USER (18/09) — Claude dịch nguyên văn, KHÔNG thêm bước nào
#   với mỗi tờ giấy trong danh sách vào:
#       đọc cái năm vào, đem đi so
#       đạt thì nhét vào
#       trượt thì loại

from importlib.machinery import SourceFileLoader
_m = SourceFileLoader("x", "Learning-document/drills/2026-09-18-not-doan.py").load_module()
danh_gia = _m.danh_gia

kho_metadata = {
    "luat-dn-2020": {"loai_van_ban": "Luật",      "co_quan": "Quốc hội",     "nam": 2021},
    "nd-15-2015":   {"loai_van_ban": "Nghị định", "co_quan": "Chính phủ",    "nam": 2015},
    "tt-08-2010":   {"loai_van_ban": "Thông tư",  "co_quan": "Bộ Tài chính", "nam": 2010},
}


def loc_sau(danh_sach_doc_id: list, bo_loc: dict, kho_metadata: dict) -> list:
    danh_sach_ra = []                                   # (user chốt A) đặt TRƯỚC vòng for
    for doc_id in danh_sach_doc_id:                     # với mỗi tờ giấy trong danh sách vào
        the = kho_metadata[doc_id]                      # đọc cái năm vào
        ket_qua = danh_gia(bo_loc, the)                 # đem đi so
        if ket_qua == True:
            danh_sach_ra.append(doc_id)                 # đạt thì nhét vào
        # trượt thì loại
    return danh_sach_ra                                 # (user) cần cái return


print(loc_sau(["luat-dn-2020", "nd-15-2015", "tt-08-2010"], {"gt": ["nam", 2020]}, kho_metadata))

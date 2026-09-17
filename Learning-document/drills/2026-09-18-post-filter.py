# GÕ THẬT — 18/09. Tên hàm/biến: TIẾNG ANH (luật mới CLAUDE.md §2).
# Khung + dữ liệu: Claude gõ. RUỘT: bạn gõ, ở chỗ ✍️. Tắt Copilot.
# Logic bạn đã tự nghĩ ra sáng nay rồi — đây là gõ lại bằng tay, không phải nghĩ lại.

from importlib.machinery import SourceFileLoader

_m = SourceFileLoader("x", "Learning-document/drills/2026-09-18-not-doan.py").load_module()
evaluate = _m.danh_gia          # hàm cây and/or/not bạn viết hôm qua (sẽ đổi tên sau khi dọn sang app/)

metadata_store = {
    "luat-dn-2020": {"doc_type": "Luật",      "issuer": "Quốc hội",     "year": 2021},
    "nd-15-2015":   {"doc_type": "Nghị định", "issuer": "Chính phủ",    "year": 2015},
    "tt-08-2010":   {"doc_type": "Thông tư",  "issuer": "Bộ Tài chính", "year": 2010},
}

ranked_ids = ["luat-dn-2020", "nd-15-2015", "tt-08-2010"]
predicate = {"gt": ["year", 2020]}


def post_filter(ranked_ids: list, predicate: dict, metadata_store: dict) -> list:
    # ✍️ GÕ Ở ĐÂY — 5 dòng: chồng chứa · vòng lặp · lấy thẻ · so · giữ lại · trả ra
    pass


print(post_filter(ranked_ids, predicate, metadata_store))   # phải ra: ['luat-dn-2020']

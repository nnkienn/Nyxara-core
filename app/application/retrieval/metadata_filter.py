# Chấm một văn bản theo cây điều kiện TRUNG LẬP (cùng cây mà to_qdrant_filter dịch cho Qdrant).
# Dùng cho nhánh BM25: BM25 không có bộ lọc riêng, nên lọc SAU khi chấm (post-filter).
# Hiện hỗ trợ cây 1 TẦNG: and / or / not mà con toàn là lá, hoặc một lá trần.
#
# metadata của một văn bản, ví dụ:  {"loai": "Nghị định", "nam": 2020}
#
# leaf_matches({"eq":  ["loai", "Nghị định"]}, metadata) -> True
# leaf_matches({"gte": ["nam", 2015]},         metadata) -> True
# leaf_matches({"lt":  ["nam", 2015]},         metadata) -> False
# leaf_matches({"like": [...]},                metadata) -> nổ ValueError
#
# matches({"and": [lá, lá]}, metadata)  -> True khi ...  (bạn biết rồi)
# matches({"or":  [lá, lá]}, metadata)  -> ...
# matches({"not": [lá]},     metadata)  -> ...
# matches(lá trần,           metadata)  -> ...


def leaf_matches(pred: dict, metadata: dict) -> bool:
    # ✍️ gõ ruột
    raise NotImplementedError


def matches(pred: dict, metadata: dict) -> bool:
    # ✍️ gõ ruột
    raise NotImplementedError

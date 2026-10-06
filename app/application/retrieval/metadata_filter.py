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
    op = list(pred.keys())[0]
    field , value = pred[op][0] , pred[op][1]
    if field not in metadata: 
        return False
    actual = metadata[field]
    if op == "gte":
        return actual >= value
    if op == "gt":
        return actual > value
    if op == "eq":
        return actual == value
    if op == "lt":
        return actual < value
    if op == "lte":
        return actual <= value
    raise ValueError(f"unsupported leaf operator: {op}")


def matches(pred: dict, metadata: dict) -> bool:
    op = list(pred.keys())[0]
    if op == "and":
        for child in pred["and"]:
            matched = leaf_matches(child,metadata)
            if not matched:
                return False
        return True
    elif op == "or":
        for child in pred["or"]:
            matched = leaf_matches(child,metadata)
            if matched == True:
                return True
        return False
    elif op == "not":
        return not leaf_matches(pred["not"][0],metadata)
    else:
        return leaf_matches(pred,metadata)
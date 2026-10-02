# Dịch cây điều kiện trung lập ({"and": [...]}, {"eq": [field, value]}, ...) sang dict filter của Qdrant.
# Hiện hỗ trợ cây 1 TẦNG: and / or / not mà con toàn là lá, hoặc một lá trần.

NUMERIC_OPS = ("gt", "gte", "lt", "lte")


def to_leaf_clause(pred: dict) -> dict:
    op = list(pred.keys())[0]
    field, value = pred[op][0], pred[op][1]
    if op == "eq":
        return {"key": field, "match": {"value": value}}
    if op in NUMERIC_OPS:
        return {"key": field, "range": {op: value}}
    raise ValueError(f"unsupported leaf operator: {op}")


def to_and_clause(pred: dict) -> dict:
    clauses = []
    for child in pred["and"]:
        clauses.append(to_leaf_clause(child))
    return {"must": clauses}


def to_or_clause(pred: dict) -> dict:
    clauses = []
    for child in pred["or"]:
        clauses.append(to_leaf_clause(child))
    return {"should": clauses}


def to_not_clause(pred: dict) -> dict:
    return {"must_not": [to_leaf_clause(pred["not"][0])]}


# Cửa vào duy nhất: nhận MỘT pred, trả dict filter của Qdrant.
def to_qdrant_filter(pred: dict) -> dict:
    op = list(pred.keys())[0]
    if op == "and":
        return to_and_clause(pred)
    elif op == "or":
        return to_or_clause(pred)
    elif op == "not":
        return to_not_clause(pred)
    else:
        value = []
        value.append(to_leaf_clause(pred))
        return {"must" : value}
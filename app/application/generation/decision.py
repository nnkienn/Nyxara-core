def decide(grades: list[bool], correct_threshold: float = 0.6, incorrect_threshold: float = 0.0) -> str:
    count_yes =  grades.count(True)
    ratio = count_yes / len(grades)

    if ratio >= correct_threshold:
        return "CORRECT"
    elif ratio <= incorrect_threshold:
        return "INCORRECT"
    else:
        return "AMBIGUOUS"

def route(verdict: str, attempts: int, max_attempts: int = 3) -> str:
    # TODO:
    # verdict "CORRECT" hoặc "AMBIGUOUS" -> return "generate"
    # verdict "INCORRECT" và attempts < max_attempts -> return "retrieve"
    # verdict "INCORRECT" nhưng attempts >= max_attempts -> return "generate" (van an toàn)
    if verdict in ["CORRECT", "AMBIGUOUS"]:
        return "generate"
    elif verdict == "INCORRECT" and attempts < max_attempts:
        return "retrieve"
    else:
        return "generate"

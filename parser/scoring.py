def score_document(data: dict, w_scope, w_cost, w_deductible, w_other) -> float:
    total = 0
    if "omfattning" in data:
        total += len(data["omfattning"]) * w_scope
    if "premie" in data:
        total += (10000 - float(data["premie"])) * w_cost
    if "självrisk" in data:
        total += (5000 - float(data["självrisk"])) * w_deductible
    return total / (w_scope + w_cost + w_deductible + w_other)

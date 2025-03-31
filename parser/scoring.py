def score_document(data, w_scope, w_cost, w_deduct, w_other):
    scope_score = 1 if data["omfattning"] != "Ej hittad" else 0
    cost_score = 1 if data["premie"] != "Ej angiven" else 0
    deduct_score = 1 if data["självrisk"] != "Ej angiven" else 0
    other_score = 1 if data["belopp"] != "Ej angivet" else 0
    return round((w_scope * scope_score + w_cost * cost_score + w_deduct * deduct_score + w_other * other_score) / 100, 2)

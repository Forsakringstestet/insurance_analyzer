def safe_float(val):
    try:
        return float(val.replace(" ", "").replace(",", "."))
    except:
        return 0.0

def score_document(data, w_scope, w_cost, w_deductible, w_other):
    total = 0
    total += float(data.get("belopp", 0)) * w_scope
    total += (100000 - float(data.get("premie", 0))) * w_cost
    total += (5000 - safe_float(data.get("självrisk", 0))) * w_deductible
    total += 42 * w_other
    return total

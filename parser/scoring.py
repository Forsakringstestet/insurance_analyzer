def score_document(data, weight_scope, weight_cost, weight_deductible, weight_other):
    # Normalize vikt-summa
    total_weight = weight_scope + weight_cost + weight_deductible + weight_other
    if total_weight == 0:
        return 0

    # === Scope (omfattning) ===
    scope_fields = [
        data.get("maskiner", 0),
        data.get("varor", 0),
        data.get("byggnad", 0),
        data.get("produktansvar", 0),
        data.get("ansvar", 0),
        data.get("rättsskydd", 0),
        data.get("gdpr_ansvar", 0),
        data.get("transport", 0),
    ]
    scope_score = sum(scope_fields)

    # === Premie (ju lägre desto bättre) ===
    premie = data.get("premie", 0)
    cost_score = -premie  # negativ påverkan

    # === Självrisk (ju lägre desto bättre) ===
    sjalvrisk = data.get("självrisk", 0)
    deductible_score = -sjalvrisk  # negativ påverkan

    # === Övrigt (t.ex. AI-betyg, ansvarstid, karens) ===
    ansvarstid = data.get("ansvarstid", "0").split()[0]
    ansvarstid = int(ansvarstid) if ansvarstid.isdigit() else 0

    karens = data.get("karens", "0").split()[0]
    karens_val = int(karens) if karens.isdigit() else 0
    other_score = ansvarstid - karens_val  # längre ansvarstid & kortare karens = bättre

    # === Total viktad poäng ===
    total_score = (
        (scope_score * weight_scope) +
        (cost_score * weight_cost) +
        (deductible_score * weight_deductible) +
        (other_score * weight_other)
    ) / total_weight

    return round(total_score, 2)

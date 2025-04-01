# parser/scoring.py

def score_document(data, weight_scope, weight_cost, weight_deductible, weight_other):
    def safe_get(key, default=0.0):
        val = data.get(key)
        try:
            return float(val) if val not in [None, "saknas", "okänt", "None"] else default
        except:
            return default

    premie = safe_get("premie")
    självrisk = safe_get("självrisk")
    maskiner = safe_get("maskiner")
    varor = safe_get("varor")
    byggnad = safe_get("byggnad")
    transport = safe_get("transport")
    produktansvar = safe_get("produktansvar")
    ansvar = safe_get("ansvar")
    rättsskydd = safe_get("rättsskydd")
    gdpr_ansvar = safe_get("gdpr_ansvar")

    scope_value = (
        maskiner +
        varor +
        byggnad +
        transport +
        produktansvar +
        ansvar +
        rättsskydd +
        gdpr_ansvar
    )

    # Enklare logik: högre scope, lägre premie/självrisk => högre score
    score = (
        (weight_scope * scope_value) -
        (weight_cost * premie) -
        (weight_deductible * självrisk) +
        (weight_other * 1000)
    )
    return round(score, 4)

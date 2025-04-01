# Parser/scoring.py
def score_document(data: dict, weight_scope: float, weight_cost: float, weight_deductible: float, weight_other: float) -> float:
    """
    Beräknar ett poängvärde för ett försäkringsdokument baserat på extraherade värden.
    
    Args:
        data (dict): Försäkringsdata.
        weight_scope (float): Vikt för omfattningsvärden.
        weight_cost (float): Vikt för premie.
        weight_deductible (float): Vikt för självrisk.
        weight_other (float): Övrig vikt.
    
    Returns:
        float: Poäng, avrundat till 4 decimaler.
    """
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

    score = (
        (weight_scope * scope_value) -
        (weight_cost * premie) -
        (weight_deductible * självrisk) +
        (weight_other * 1000)
    )
    return round(score, 4)

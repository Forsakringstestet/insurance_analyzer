import re

BASBELOPP_2025 = 58800

def parse_currency(val):
    val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
    match = re.search(r"(\d+(?:\.\d+)?)", val)
    return float(match.group(1)) if match else 0.0

def extract_feld(text, labels):
    for label in labels:
        match = re.search(rf"{label}[^0-9a-z]{{0,20}}([0-9\s.,]+)\s*(kr|sek)?", text, re.IGNORECASE)
        if match:
            return parse_currency(match.group(1))
    return 0.0

def extract_premie(text): return extract_feld(text, ["pris per år", "årspremie", "bruttopremie", "premie", "totalpris"])
def extract_sjalvrisk(text):
    text = text.lower()
    bas = re.search(r"(självrisk)[^0-9a-z]{0,10}([0-9.,]+)\s*(basbelopp|pbb)", text)
    if bas:
        try:
            return float(bas.group(2).replace(",", ".")) * BASBELOPP_2025
        except:
            pass
    return extract_feld(text, ["självrisk"])
def extract_karens(text):
    text = text.lower().replace("\xa0", " ").replace("\n", " ")
    patterns = [
        r"karens[^0-9a-z]{0,15}(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)",
        r"(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)\s*karens"
    ]
    for p in patterns:
        match = re.search(p, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"
    return "saknas"
def extract_ansvarstid(text):
    patterns = [
        r"ansvarstid\s*(?:på)?\s*:? ?(\d{1,2}) ?(mån|månad|månader|år)",
        r"gäller i\s*(\d{1,2}) ?(mån|månad|månader|år)"
    ]
    for p in patterns:
        match = re.search(p, text.lower())
        if match:
            val = int(match.group(1))
            return f"{val * 12} månader" if "år" in match.group(2) else f"{val} månader"
    return "saknas"

# 🔍 Specifika objektbelopp
def extract_maskiner(text): return extract_feld(text, ["maskiner", "maskin", "inventarier"])
def extract_varor(text): return extract_feld(text, ["lager", "varor"])
def extract_byggnad(text): return extract_feld(text, ["byggnad", "byggnader", "fastighet"])
def extract_transport(text): return extract_feld(text, ["transport", "frakt"])
def extract_rättsskydd(text): return extract_feld(text, ["rättsskydd"])
def extract_gdpr(text): return extract_feld(text, ["gdpr", "dataskydd", "integritet", "personuppgift", "privacy"])

def extract_ansvar(text): return extract_feld(text, ["ansvarsförsäkring", "generellt ansvar", "företagsansvar"])
def extract_produktansvar(text): return extract_feld(text, ["produktansvar"])

# ✅ Sammanställ
def extract_all_insurance_data(text: str) -> dict:
    return {
        "premie": extract_premie(text),
        "självrisk": extract_sjalvrisk(text),
        "karens": extract_karens(text),
        "ansvarstid": extract_ansvarstid(text),
        "maskiner": extract_maskiner(text),
        "varor": extract_varor(text),
        "byggnad": extract_byggnad(text),
        "transport": extract_transport(text),
        "rättsskydd": extract_rättsskydd(text),
        "gdpr_ansvar": extract_gdpr(text),
        "ansvar": extract_ansvar(text),
        "produktansvar": extract_produktansvar(text)
    }

import re

def parse_currency(val: str) -> float:
    val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
    match = re.search(r"(\d+(?:\.\d+)?)", val)
    return float(match.group(1)) if match else 0.0
def extract_premie(text: str) -> float:
    text = text.lower()
    patterns = [
        r"(premie|pris per år|totalpris|bruttopremie|årspremie)[^\d]{0,20}(\d[\d\s.,]+)",
        r"(totalt)[^\d]{0,15}(\d[\d\s.,]+)(\s*kr)?"
    ]
    for p in patterns:
        match = re.search(p, text)
        if match:
            return parse_currency(match.group(2))
    return 0.0
def extract_sjalvrisk(text: str) -> float:
    text = text.lower()

    basbelopp = re.search(r"(självrisk)[^\d]{0,10}([\d.,]+)\s*(basbelopp|pbb)", text)
    if basbelopp:
        try:
            return float(basbelopp.group(2).replace(",", ".")) * 58800
        except:
            pass

    match = re.search(r"(självrisk|självrisken)[^\d]{0,10}([\d\s.,]+)\s*(kr|sek)?", text)
    if match:
        return parse_currency(match.group(2))
    
    return 0.0
def extract_karens(text: str) -> str:
    text = text.lower()
    patterns = [
        r"karens[^0-9a-zA-Z]{0,15}(\d{1,3})\s*(dygn|dag(ar)?|tim(me|mar)?)",
        r"(\d{1,3})\s*(dygn|dag(ar)?|tim(me|mar)?)\s*karens"
    ]
    for p in patterns:
        match = re.search(p, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"
    return "saknas"
def extract_ansvarstid(text: str) -> str:
    patterns = [
        r"ansvarstid\s*(?:på)?\s*:? ?(\d{1,2}) ?(mån(ad|ader)?|år)",
        r"ersättningstid\s*:? ?(\d{1,2}) ?(mån(ad|ader)?|år)",
        r"gäller i\s*(\d{1,2}) ?(mån(ad|ader)?|år)"
    ]
    for p in patterns:
        match = re.search(p, text.lower())
        if match:
            antal = int(match.group(1))
            if "år" in match.group(2):
                antal *= 12
            return f"{antal} månader"
    return "saknas"
def extract_field(label: str, text: str) -> float:
    pattern = rf"{label}[^\d]{0,10}([\d\s.,]+)\s*(kr|sek)?"
    match = re.search(pattern, text.lower())
    return parse_currency(match.group(1)) if match else 0.0
def extract_all_insurance_data(text: str) -> dict:
    return {
        "premie": extract_premie(text),
        "självrisk": extract_sjalvrisk(text),
        "karens": extract_karens(text),
        "ansvarstid": extract_ansvarstid(text),
        "maskiner": extract_field("maskiner", text),
        "byggnad": extract_field("byggnad", text),
        "varor": extract_field("varor", text),
        "produktansvar": extract_field("produktansvar", text),
        "transport": extract_field("transport", text),
        "ansvar": extract_field("verksamhetsansvar", text),
        "rättsskydd": extract_field("rättsskydd", text),
        "gdpr ansvar": extract_field("gdpr", text)
    }

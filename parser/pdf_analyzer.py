import re

BASBELOPP_2025 = 58800

def parse_currency(val):
    val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
    match = re.search(r"(\d+(?:\.\d+)?)", val)
    return float(match.group(1)) if match else 0.0

def extract_premie(text: str) -> float:
    text = text.lower()
    patterns = [
        r"(pris per år|årspris|premie|bruttopremie|totalpris)[^\d]{0,20}(\d[\d\s.,]+)\s*(kr|sek)?",
        r"(pris|premie)[^:]{0,10}:\s?(\d[\d\s.,]+)\s*(kr|sek)?",
        r"(prisuppgift.*?)(\d[\d\s.,]+)\s*(kr|sek)?"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return parse_currency(match.group(2))
    return 0.0

def extract_sjalvrisk(text: str) -> float:
    text = text.lower()
    bas = re.search(r"(självrisk|självrisken)[^0-9a-z]{0,10}([0-9.,]+)\s*(basbelopp|pbb)", text)
    if bas:
        try:
            val = bas.group(2).replace(",", ".")
            return float(val) * BASBELOPP_2025
        except:
            pass
    kr = re.search(r"(självrisk|självrisken)[^0-9a-z]{0,10}([0-9\s.,]+)\s*(kr|sek)?", text)
    if kr:
        return parse_currency(kr.group(2))
    return 0.0

def extract_karens(text: str) -> str:
    text = text.lower().replace("\xa0", " ").replace("\n", " ")
    patterns = [
        r"karens[^0-9a-z]{0,15}(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)",
        r"(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)\s*karens"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)}".strip()
    return "saknas"

def extract_ansvarstid(text: str) -> str:
    patterns = [
        r"ansvarstid\s*(?:på)?\s*:? ?(\d{1,2}) ?(mån|månad|månader|år)",
        r"gäller i\s*(\d{1,2}) ?(mån|månad|månader|år)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            antal = int(match.group(1))
            if "år" in match.group(2):
                antal *= 12
            return f"{antal} månader"
    return "saknas"

def extract_maskiner(text: str) -> float:
    text = text.lower()
    match = re.search(r"(maskiner|maskinerier)[^0-9a-z]{0,15}([0-9\s.,]+)\s*(kr|sek)?", text)
    if match:
        return parse_currency(match.group(2))
    return 0.0

def extract_produktansvar(text: str) -> float:
    text = text.lower()
    match = re.search(r"(produktansvar|ansvar|verksamhetsansvar|generellt ansvar)[^0-9a-z]{0,15}([0-9\s.,]+)\s*(kr|sek)?", text)
    if match:
        return parse_currency(match.group(2))
    return 0.0

def extract_all_insurance_data(text: str) -> dict:
    return {
        "premie": extract_premie(text),
        "självrisk": extract_sjalvrisk(text),
        "karens": extract_karens(text),
        "ansvarstid": extract_ansvarstid(text),
        "maskiner": extract_maskiner(text),
        "produktansvar": extract_produktansvar(text)
    }

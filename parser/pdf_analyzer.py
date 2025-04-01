import re

BASBELOPP_2025 = 58800

def parse_currency(val):
    if not val:
        return 0.0
    val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
    match = re.search(r"(\d+(?:\.\d+)?)", val)
    return float(match.group(1)) if match else 0.0

def extract_field(label, text):
    pattern = rf"{label}[^\d]{{0,25}}([\d\s.,]+)\s*(kr|sek)?"
    match = re.search(pattern, text.lower())
    return parse_currency(match.group(1)) if match else 0.0

def extract_premie(text):
    patterns = [
        r"(totalpris|premie|årspremie|pris för tiden|totalt).*?([\d\s.,]+)\s*(kr|sek)?",
        r"försäkringspremie.*?([\d\s.,]+)\s*(kr|sek)?"
    ]
    for p in patterns:
        match = re.search(p, text.lower())
        if match:
            return parse_currency(match.group(2 if len(match.groups()) > 1 else 1))
    return 0.0

def extract_sjalvrisk(text):
    basbelopp = re.search(r"(självrisk|självrisken)[^0-9a-zA-Z]{0,10}([0-9.,]+)\s*(basbelopp|pbb)", text.lower())
    if basbelopp:
        try:
            return float(basbelopp.group(2).replace(",", ".")) * BASBELOPP_2025
        except:
            pass

    kronor = re.search(r"(självrisk|självrisken)[^0-9a-zA-Z]{0,10}([0-9\s.,]+)\s*(kr|sek)?", text.lower())
    if kronor:
        return parse_currency(kronor.group(2))

    procent = re.search(r"(självrisk).*?(\d{1,2})\s*%.*?(basbelopp|pbb)", text.lower())
    if procent:
        return (int(procent.group(2)) / 100) * BASBELOPP_2025

    return 0.0

def extract_karens(text):
    patterns = [
        r"karens.*?(\d{1,3})\s*(dygn|dagar|timmar|tim|h)",
        r"(\d{1,3})\s*(dygn|dagar|timmar|tim|h)\s*karens",
        r"karens\s*är\s*(\d{1,3})\s*(dygn|dagar|timmar|tim|h)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return f"{match.group(1)} {match.group(2)}"
    return "saknas"

def extract_ansvarstid(text):
    patterns = [
        r"(ersättningstid|försäkringstid|ansvarstid).*?(\d{1,2})\s*(månader|månad|år)",
        r"gäller i\s*(\d{1,2})\s*(månader|månad|år)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            antal = int(match.group(2 if "gäller" in pattern else 1))
            typ = match.group(3 if "gäller" in pattern else 2)
            return f"{antal * 12 if 'år' in typ else antal} månader"
    return "saknas"

# FÖRSÄKRINGSBLOCK

def extract_maskiner(text):
    return extract_field("maskiner( och inventarier)?", text)

def extract_varor(text):
    return extract_field("varor", text)

def extract_byggnad(text):
    return extract_field("byggnad(, verkstadsbyggnad)?", text)

def extract_transport(text):
    return extract_field("transport", text)

def extract_ansvar(text):
    return extract_field("verksamhetsansvar", text)

def extract_produktansvar(text):
    return extract_field("produktansvar( och ansvar för avlämnade arbeten)?", text)

def extract_gdpr(text):
    return extract_field("personuppgiftsansvar|gdpr", text)

def extract_rattsskydd(text):
    return extract_field("rättsskydd", text)

# FINAL

def extract_all_insurance_data(text: str) -> dict:
    return {
        "premie": extract_premie(text),
        "självrisk": extract_sjalvrisk(text),
        "karens": extract_karens(text),
        "ansvarstid": extract_ansvarstid(text),
        "maskiner": extract_maskiner(text),
        "produktansvar": extract_produktansvar(text),
        "varor": extract_varor(text),
        "byggnad": extract_byggnad(text),
        "transport": extract_transport(text),
        "ansvar": extract_ansvar(text),
        "rättsskydd": extract_rattsskydd(text),
        "gdpr_ansvar": extract_gdpr(text),
    }

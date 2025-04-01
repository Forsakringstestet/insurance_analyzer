import re

BASBELOPP_2025 = 58800

def parse_currency(val):
    val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
    match = re.search(r"(\d+(?:\.\d+)?)", val)
    return float(match.group(1)) if match else 0.0


def extract_premie(text):
    text = text.lower()
    for pattern in [
        r"(premie|totalpris|bruttopremie|årspremie|pris per år|totalt för försäkringen)[^\d]{0,15}(\d[\d\s.,]+)\s*(kr|sek)?",
        r"(försäkringskostnad|pris för tiden)[^\d]{0,15}(\d[\d\s.,]+)\s*(kr|sek)?"
    ]:
        match = re.search(pattern, text)
        if match:
            return parse_currency(match.group(2))
    return 0.0


def extract_sjalvrisk(text):
    text = text.lower()

    basbelopp = re.search(r"(självrisk|självrisken)[^0-9a-zA-Z]{0,10}([0-9.,]+)\s*(basbelopp|pbb)", text)
    if basbelopp:
        try:
            val = basbelopp.group(2).replace(",", ".")
            return float(val) * BASBELOPP_2025
        except:
            pass

    kronor = re.search(r"(självrisk|självrisken)[^0-9a-zA-Z]{0,10}([0-9\s.,]+)\s*(kr|sek)?", text)
    if kronor:
        raw = kronor.group(2).replace(" ", "").replace(".", "").replace(",", ".")
        try:
            return float(raw)
        except:
            pass

    return 0.0


def extract_karens(text):
    text = text.lower().replace("\n", " ").replace("\xa0", " ")
    patterns = [
        r"karens[^0-9a-zA-Z]{0,15}(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)",
        r"(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)\s*karens",
        r"karens\s*är\s*(\d{1,3})\s*(dygn|dagar|timmar|tim|h)",
        r"karens\s*(\d{1,3})\s*(dygn|dagar|timmar|tim|h)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)}".strip()
    return "saknas"


def extract_ansvarstid(text):
    patterns = [
        r"ansvarstid\s*(?:på)?\s*:? ?(\d{1,2}) ?(mån|månad|månader|år)",
        r"gäller i\s*(\d{1,2}) ?(mån|månad|månader|år)",
        r"försäkringstid\s*(\d{1,2}) ?(mån|månad|månader|år)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            antal = int(match.group(1))
            if "år" in match.group(2):
                antal *= 12
            return f"{antal} månader"
    return "saknas"


def extract_field(fieldname: str, text: str) -> float:
    pattern = rf"{fieldname}[^\d]{{0,15}}([\d\s.,]+)\s*(kr|sek)?"
    match = re.search(pattern, text.lower())
    return parse_currency(match.group(1)) if match else 0.0


def extract_maskiner(text: str) -> float:
    return extract_field("maskiner(ier)?|maskiner och inventarier", text)


def extract_byggnad(text: str) -> float:
    return extract_field("byggnad|verkstadsbyggnad|fastighet(er)?", text)


def extract_varor(text: str) -> float:
    return extract_field("varor|lager", text)


def extract_produktansvar(text: str) -> float:
    return extract_field("produktansvar", text)


def extract_ansvar(text: str) -> float:
    return extract_field("verksamhetsansvar|ansvarsförsäkring", text)


def extract_rattsskydd(text: str) -> float:
    return extract_field("rättsskydd", text)


def extract_gdpr_ansvar(text: str) -> float:
    return extract_field("gdpr ansvar|personuppgiftsansvar", text)


def extract_transport(text: str) -> float:
    return extract_field("transport|transportförsäkring", text)


def extract_all_insurance_data(text: str) -> dict:
    return {
        "premie": extract_premie(text),
        "självrisk": extract_sjalvrisk(text),
        "karens": extract_karens(text),
        "ansvarstid": extract_ansvarstid(text),
        "maskiner": extract_maskiner(text),
        "byggnad": extract_byggnad(text),
        "varor": extract_varor(text),
        "transport": extract_transport(text),
        "produktansvar": extract_produktansvar(text),
        "ansvar": extract_ansvar(text),
        "rättsskydd": extract_rattsskydd(text),
        "gdpr ansvar": extract_gdpr_ansvar(text)
    }

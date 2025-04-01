import re

BASBELOPP_2025 = 58800


def parse_currency(val: str) -> float:
    val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
    match = re.search(r"(\d+(?:\.\d+)?)", val)
    return float(match.group(1)) if match else 0.0


def extract_premie(text: str) -> float:
    text = text.lower().replace("\n", " ").replace("\xa0", " ")

    patterns = [
        r"(?:premie|totalpris|bruttopremie|årspremie|pris per år|kostnad per år)[^0-9]{0,15}(\d[\d\s.,]+)\s*(kr|sek)?",
        r"premie[^:]{0,10}: ?(\d[\d\s.,]+)\s*(kr|sek)?",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return parse_currency(match.group(1))
    return 0.0


def extract_sjalvrisk(text: str) -> float:
    text = text.lower().replace("\n", " ").replace("\xa0", " ")

    # Basbelopp
    match = re.search(r"(självrisk|självrisken)[^0-9]{0,10}([\d.,]+)\s*(basbelopp)", text)
    if match:
        try:
            return float(match.group(2).replace(",", ".")) * BASBELOPP_2025
        except:
            pass

    # Kronor (vanlig)
    match = re.search(r"(självrisk|självrisken)[^0-9]{0,10}([\d\s.,]+)\s*(kr|sek)?", text)
    if match:
        return parse_currency(match.group(2))

    # Friare formulering
    match = re.search(r"(självrisk.*?)\s(på|är|om)?\s?([\d\s.,]+)\s*(kr|sek)?", text)
    if match:
        return parse_currency(match.group(3))

    return 0.0


def extract_karens(text: str) -> str:
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


def extract_ansvarstid(text: str) -> str:
    text = text.lower().replace("\n", " ").replace("\xa0", " ")

    patterns = [
        r"ansvarstid\s*(?:på)?\s*:? ?(\d{1,2}) ?(mån|månad|månader|år)",
        r"gäller i\s*(\d{1,2}) ?(mån|månad|månader|år)",
        r"försäkringstid\s*(\d{1,2}) ?(mån|månad|månader|år)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            antal = int(match.group(1))
            if "år" in match.group(2):
                antal *= 12
            return f"{antal} månader"
    return "saknas"


def extract_all_insurance_data(text: str) -> dict:
    return {
        "premie": extract_premie(text),
        "självrisk": extract_sjalvrisk(text),
        "karens": extract_karens(text),
        "ansvarstid": extract_ansvarstid(text)
    }

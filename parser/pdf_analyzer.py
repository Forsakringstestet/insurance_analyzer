import re

BASBELOPP_2025 = 58800


def parse_currency(val: str) -> float:
    """Konverterar ett valfritt strängbelopp till float."""
    val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
    try:
        match = re.search(r"(\d+(?:\.\d+)?)", val)
        return float(match.group(1)) if match else 0.0
    except Exception:
        return 0.0


def extract_premie(text: str) -> float:
    """Extraherar premie-belopp från text."""
    text = text.lower()
    patterns = [
        r"(premie|totalpris|bruttopremie|årspremie|pris per år)[^\d]{0,15}(\d[\d\s.,]+)",
        r"premie[^:]{0,10}: ?(\d[\d\s.,]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return parse_currency(match.group(2 if match.lastindex > 1 else 1))
    return 0.0


def extract_sjalvrisk(text: str) -> float:
    """Extraherar självrisk i kr eller basbelopp."""
    text = text.lower()

    basbelopp = re.search(r"(självrisk|självrisken)[^0-9a-zA-Z]{0,10}([0-9.,]+)\s*(basbelopp)", text)
    if basbelopp:
        try:
            val = basbelopp.group(2).replace(",", ".")
            return float(val) * BASBELOPP_2025
        except:
            pass

    patterns = [
        r"(självrisk|självrisken)[^0-9a-zA-Z]{0,10}([0-9\s.,]+)\s*(kr|sek)?",
        r"(självrisk.*?)\s(på|är|om)?\s?([0-9\s.,]+)\s*(kr|sek)?"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            idx = 3 if match.lastindex >= 3 else 2
            return parse_currency(match.group(idx))
    return 0.0


def extract_karens(text: str) -> str:
    """Extraherar karens-tid."""
    text = text.lower().replace("\n", " ").replace("\xa0", " ")
    patterns = [
        r"karens[^0-9a-zA-Z]{0,15}(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)",
        r"(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)\s*karens",
        r"karens\s*är\s*(\d{1,3})\s*(dygn|dagar|timmar|tim|h)",
        r"karens\s*(\d{1,3})\s*(dygn|dagar|timmar|tim|h)"
    ]
    for p in patterns:
        match = re.search(p, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"
    return "saknas"


def extract_ansvarstid(text: str) -> str:
    """Extraherar ansvarstid som 12 månader / 24 månader osv."""
    patterns = [
        r"ansvarstid\s*(?:på)?\s*:? ?(\d{1,2}) ?(mån|månad|månader|år)",
        r"gäller i\s*(\d{1,2}) ?(mån|månad|månader|år)",
        r"försäkringstid\s*(\d{1,2}) ?(mån|månad|månader|år)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            antal = int(match.group(1))
            enhet = match.group(2)
            if "år" in enhet:
                antal *= 12
            return f"{antal} månader"
    return "saknas"


def extract_egendom(text: str) -> dict:
    """Extraherar belopp kopplat till maskiner, inventarier, varor etc."""
    text = text.lower()
    result = {}
    typer = ["maskiner", "inventarier", "lager", "varor", "egendom", "lös egendom"]
    for typ in typer:
        match = re.search(rf"{typ}[^0-9a-zA-Z]{{0,15}}(\d[\d\s.,]+)\s*(kr|sek)?", text)
        if match:
            result[typ] = parse_currency(match.group(1))
    return result


def extract_ansvar(text: str) -> dict:
    """Extraherar produktansvar, verksamhetsansvar, etc."""
    text = text.lower()
    result = {}
    typer = ["produktansvar", "verksamhetsansvar", "ansvarsförsäkring", "företagsansvar", "allmänt ansvar"]
    for typ in typer:
        match = re.search(rf"{typ}[^0-9a-zA-Z]{{0,15}}(\d[\d\s.,]+)\s*(kr|sek)?", text)
        if match:
            result[typ] = parse_currency(match.group(1))
    return result


def extract_all_insurance_data(text: str) -> dict:
    """Samlingsfunktion som returnerar alla extraherade fält från dokumentet."""
    egendom = extract_egendom(text)
    ansvar = extract_ansvar(text)

    return {
        "premie": extract_premie(text),
        "självrisk": extract_sjalvrisk(text),
        "karens": extract_karens(text),
        "ansvarstid": extract_ansvarstid(text),
        "maskiner": egendom.get("maskiner", 0.0),
        "produktansvar": ansvar.get("produktansvar", 0.0),
        "egendom": egendom,
        "ansvar": ansvar
    }

import re
from typing import Dict

# Hjälp: Konverterar text till float, med fallback

def normalize_number(text):
    try:
        cleaned = text.replace(" ", "").replace(".", "").replace(",", ".")
        return float(cleaned)
    except (ValueError, AttributeError):
        return 0.0

# === FÖRSÄKRINGSUTDRAG ===

def extract_premium(text: str) -> float:
    text = text.replace("\n", " ")
    for label in ["total premie", "pris per år", "pris totalt", "totalpris", "totalbelopp", "premie"]:
        match = re.search(rf"(?i){label}[^0-9]{{0,20}}([0-9\s.,]+)\s*kr?", text)
        if match:
            return normalize_number(match.group(1))
    return 0.0

def extract_deductible(text: str) -> str:
    match = re.search(r"(?i)(självrisk|självrisken)[^0-9]{0,20}([0-9\s.,%]+|[0-9]+\s*basbelopp)", text)
    return match.group(2).strip() if match else "saknas"

def extract_egendom(text: str) -> Dict:
    egendom = {}
    typer = ["maskiner", "inventarier", "lager", "varor", "egendom"]
    for typ in typer:
        match = re.search(rf"(?i){typ}[^0-9]{{0,20}}([0-9\s.,]+)\s*kr", text)
        if match:
            egendom[typ] = normalize_number(match.group(1))
    return egendom

def extract_ansvar(text: str) -> Dict:
    ansvar = {}
    typer = ["produktansvar", "verksamhetsansvar", "ansvarsförsäkring", "allmänt ansvar", "företagsansvar"]
    for typ in typer:
        match = re.search(rf"(?i){typ}[^0-9]{{0,20}}([0-9\s.,]+)\s*kr", text)
        if match:
            ansvar[typ] = normalize_number(match.group(1))
    return ansvar

def extract_karen_ansvarstid(text: str) -> Dict:
    karens = re.search(r"(?i)(karens|karensdagar)[^0-9]{0,20}(\d+\s*(dygn|dagar|timmar|tim|h))", text)
    ansvarstid = re.search(r"(?i)(ansvarstid)[^0-9]{0,20}(\d+\s*(månader|mån|dagar))", text)
    return {
        "karens": karens.group(2).strip() if karens else "saknas",
        "ansvarstid": ansvarstid.group(2).strip() if ansvarstid else "saknas"
    }

def get_omfattning_block(egendom: Dict, ansvar: Dict) -> str:
    eg = ", ".join([f"{k}: {v} kr" for k, v in egendom.items()]) or "Ingen egendom specificerad"
    an = ", ".join([f"{k}: {v} kr" for k, v in ansvar.items()]) or "Ingen ansvarsförsäkring hittad"
    return f"Egendom: {eg}\nAnsvar: {an}"

def extract_all_insurance_data(text: str) -> Dict:
    premie = extract_premium(text)
    sjalvrisk = extract_deductible(text)
    egendom = extract_egendom(text)
    ansvar = extract_ansvar(text)
    tider = extract_karen_ansvarstid(text)
    return {
        "premie": premie,
        "självrisk": sjalvrisk,
        "egendom": egendom,
        "ansvar": ansvar,
        "omfattning": get_omfattning_block(egendom, ansvar),
        **tider
    }

import re
from typing import Dict

BASBELOPP_2025 = 58800

def normalize_number(text):
    try:
        cleaned = text.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
        return float(cleaned)
    except Exception:
        return 0.0

def match_any_pattern(text: str, labels: list, suffix: str = r"\s*kr") -> float:
    for label in labels:
        match = re.search(rf"(?i){label}[^0-9]{{0,20}}([0-9\s.,]+){suffix}?", text)
        if match:
            return normalize_number(match.group(1))
    return 0.0

def extract_premium(text: str) -> float:
    return match_any_pattern(text, ["total premie", "pris totalt", "premie", "totalpris", "pris per år", "försäkringskostnad"])

def extract_deductible(text: str) -> float:
    match = re.search(r"(?i)(självrisk|självrisken)[^0-9]{0,20}([0-9\s.,]+)\s*basbelopp", text)
    if match:
        return normalize_number(match.group(2)) * BASBELOPP_2025
    return match_any_pattern(text, ["självrisk", "självrisken"])

def extract_dynamic_block(text: str, patterns: list, label: str) -> Dict:
    for pattern in patterns:
        match = re.search(rf"(?i){pattern}[^0-9]{{0,20}}([0-9\s.,]+)\s*(kr)?", text)
        if match:
            return {label: normalize_number(match.group(1))}
    return {}

def extract_egendom(text: str) -> Dict:
    egendom = {}
    egendom.update(extract_dynamic_block(text, ["maskiner", "maskinutrustning", "lös egendom"], "maskiner"))
    egendom.update(extract_dynamic_block(text, ["varor", "lager", "råvaror"], "varor"))
    egendom.update(extract_dynamic_block(text, ["inredning", "inventarier"], "inredning"))
    return egendom

def extract_ansvar(text: str) -> Dict:
    ansvar = {}
    ansvar.update(extract_dynamic_block(text, ["produktansvar"], "produktansvar"))
    ansvar.update(extract_dynamic_block(text, ["verksamhetsansvar", "allmänt ansvar"], "verksamhetsansvar"))
    ansvar.update(extract_dynamic_block(text, ["ansvarsförsäkring", "företagsansvar"], "ansvarsförsäkring"))
    ansvar.update(extract_dynamic_block(text, ["förmögenhetsbrott", "ekonomisk brottslighet"], "förmögenhetsbrott"))
    return ansvar

def extract_karen_ansvarstid(text: str) -> Dict:
    karens = re.search(r"(?i)(karens|karensdagar)[^0-9]{0,20}(\d+\s*(dygn|dagar|timmar|tim|h))", text)
    ansvarstid = re.search(r"(?i)(ansvarstid)[^0-9]{0,20}(\d+\s*(månader|mån|dagar|år))", text)
    return {
        "karens": karens.group(2).strip() if karens else "saknas",
        "ansvarstid": ansvarstid.group(2).strip() if ansvarstid else "saknas"
    }

def get_omfattning_block(egendom: Dict, ansvar: Dict) -> str:
    eg = ", ".join([f"{k}: {v:,.0f} kr" for k, v in egendom.items()]) or "Ingen egendom specificerad"
    an = ", ".join([f"{k}: {v:,.0f} kr" for k, v in ansvar.items()]) or "Ingen ansvarsförsäkring hittad"
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
        "maskiner": egendom.get("maskiner", 0.0),
        "produktansvar": ansvar.get("produktansvar", 0.0),
        "egendom": egendom,
        "ansvar": ansvar,
        "omfattning": get_omfattning_block(egendom, ansvar),
        **tider
    }

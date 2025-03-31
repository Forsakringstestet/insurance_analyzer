import re
from typing import Dict

# Hjälpfunktion för normalisering av belopp

def normalize_number(text):
    return float(text.replace(" ", "").replace(".", "").replace(",", "."))

def extract_premium(text):
    for label in ["total premie", "pris totalt", "totalpris", "totalbelopp", "premie"]:
        match = re.search(rf"(?i){label}[^0-9]{0,20}([0-9\s.,]+)\s*kr", text)
        if match:
            return normalize_number(match.group(1))
    return 0.0

def extract_deductible(text):
    match = re.search(r"(?i)(självrisk|självrisken)[^0-9]{0,20}([0-9\s.,%]+|[0-9]+\s*basbelopp)", text)
    return match.group(2).strip() if match else "saknas"

def extract_egendom(text):
    egendom = {}
    typer = ["maskiner", "inventarier", "lager", "varor", "egendom"]
    for typ in typer:
        match = re.search(rf"(?i){typ}[^0-9]{0,20}([0-9\s.,]+)\s*kr", text)
        if match:
            egendom[typ] = normalize_number(match.group(1))
    return egendom

def extract_ansvar(text):
    ansvar = {}
    typer = ["produktansvar", "verksamhetsansvar", "ansvarsförsäkring", "allmänt ansvar", "företagsansvar"]
    for typ in typer:
        match = re.search(rf"(?i){typ}[^0-9]{0,20}([0-9\s.,]+)\s*kr", text)
        if match:
            ansvar[typ] = normalize_number(match.group(1))
    return ansvar

def extract_karen_ansvarstid(text):
    karens = re.search(r"(?i)(karens|karensdagar)[^0-9]{0,20}(\d+\s*(dygn|dagar|timmar|tim|h))", text)
    ansvarstid = re.search(r"(?i)(ansvarstid)[^0-9]{0,20}(\d+\s*(månader|mån|dagar))", text)
    return {
        "karens": karens.group(2).strip() if karens else "saknas",
        "ansvarstid": ansvarstid.group(2).strip() if ansvarstid else "saknas"
    }

def extract_all_insurance_data(text: str) -> Dict:
    return {
        "premie": extract_premium(text),
        "självrisk": extract_deductible(text),
        "egendom": extract_egendom(text),
        "ansvar": extract_ansvar(text),
        **extract_karen_ansvarstid(text)
    }

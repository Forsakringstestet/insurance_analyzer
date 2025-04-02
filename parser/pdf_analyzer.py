import re
import streamlit as st

BASBELOPP_2025 = 58800

def parse_currency(val):
    try:
        val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
        match = re.search(r"(\d+(?:\.\d+)?)", val)
        return float(match.group(1)) if match else 0.0
    except Exception:
        return 0.0

def extract_field(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return parse_currency(match.group(1)) if match else 0.0

def extract_all_sjalvrisker(text: str) -> list:
    matches = re.findall(r"självrisk[^\n\r:]*[:\-]?\s*([\d\s.,]+\s*(kr|sek|%|pbb)?)", text, re.IGNORECASE)
    result = []
    for raw_value, unit in matches:
        clean_val = raw_value.replace(" ", "").replace(",", ".")
        try:
            if "%" in unit:
                val = f"{float(clean_val)} %"
            elif "pbb" in unit.lower():
                val = f"{float(clean_val)} pbb"
            else:
                val = f"{int(float(clean_val))} kr"
            if val not in result:
                result.append(val)
        except:
            continue
    return result

def extract_primary_sjalvrisk(text):
    sjalvrisker = extract_all_sjalvrisker(text)
    for val in sjalvrisker:
        if "kr" in val:
            return parse_currency(val)
        elif "pbb" in val:
            return float(val.split(" ")[0]) * BASBELOPP_2025
    return 0.0

def extract_all_belopp_for_area(text: str, area: str) -> list:
    matches = re.findall(rf"{area}[^\n\r:]*[:\-]?\s*([\d\s.,]+)\s*(kr|sek)?", text, re.IGNORECASE)
    values = set()
    for raw_value, _ in matches:
        cleaned = raw_value.replace(" ", "").replace(",", ".")
        try:
            values.add(f"{int(float(cleaned))} kr")
        except:
            continue
    return list(values)

def extract_primary_value_for_area(text: str, area: str) -> float:
    values = extract_all_belopp_for_area(text, area)
    for val in values:
        if "kr" in val:
            return float(val.replace(" kr", ""))
    return 0.0

def extract_karens(text):
    patterns = [
        r"karens[^0-9a-zA-Z]{0,15}(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)",
        r"(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)\s*karens",
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
            antal = int(match.group(2 if 'ersättningstid' in pattern else 1))
            enhet = match.group(3 if 'ersättningstid' in pattern else 2)
            return f"{antal * 12 if 'år' in enhet else antal} månader"
    return "saknas"

def extract_all_insurance_data(text: str) -> dict:
    try:
        return {
            "premie": extract_primary_value_for_area(text, "premie"),
            "självrisk": extract_primary_sjalvrisk(text),
            "karens": extract_karens(text),
            "ansvarstid": extract_ansvarstid(text),
            "byggnad": extract_primary_value_for_area(text, "byggnad"),
            "maskiner": extract_primary_value_for_area(text, "maskiner|inventarier|utrustning"),
            "varor": extract_primary_value_for_area(text, "varor|lager|förråd"),
            "transport": extract_primary_value_for_area(text, "transport|godsförsäkring"),
            "produktansvar": extract_primary_value_for_area(text, "produktansvar"),
            "ansvar": extract_primary_value_for_area(text, "verksamhetsansvar|ansvarsförsäkring"),
            "rättsskydd": extract_primary_value_for_area(text, "rättsskydd|juridiskt skydd"),
            "gdpr_ansvar": extract_primary_value_for_area(text, "gdpr|personuppgifter"),
        }
    except Exception as e:
        st.error(f"[PDF-analyzern kraschade] {e}")
        return {
            "premie": 0.0,
            "självrisk": 0.0,
            "karens": "saknas",
            "ansvarstid": "saknas",
            "byggnad": 0.0,
            "maskiner": 0.0,
            "varor": 0.0,
            "transport": 0.0,
            "produktansvar": 0.0,
            "ansvar": 0.0,
            "rättsskydd": 0.0,
            "gdpr_ansvar": 0.0,
        }

def score_document(data: dict, vikt_omfattning=40, vikt_premie=30, vikt_självrisk=20, vikt_övrigt=10) -> float:
    """
    Poängsätter ett försäkringsdokument utifrån viktade kriterier.
    """
    omfattning_score = (
        data.get("maskiner", 0)
        + data.get("produktansvar", 0)
        + data.get("byggnad", 0)
        + data.get("varor", 0)
        + data.get("transport", 0)
        + data.get("ansvar", 0)
        + data.get("rättsskydd", 0)
        + data.get("gdpr_ansvar", 0)
    )

    premie_score = 1000000 - data.get("premie", 0)
    sjalvrisk_score = 100000 - data.get("självrisk", 0)
    övrigt_score = 0

    total_score = (
        omfattning_score * (vikt_omfattning / 100)
        + premie_score * (vikt_premie / 100)
        + sjalvrisk_score * (vikt_självrisk / 100)
        + övrigt_score * (vikt_övrigt / 100)
    )

    return round(total_score, 2)

import re
import streamlit as st

BASBELOPP_2025 = 58800

def clean_text(text):
    return re.sub(r"\s+", " ", text).lower()

def parse_currency(val):
    try:
        val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
        match = re.search(r"(\d+(?:\.\d+)?)", val)
        return float(match.group(1)) if match else 0.0
    except Exception:
        return 0.0

def extract_field(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return parse_currency(match.group(1))
    return 0.0

def extract_total_premie(text):
    patterns = [
        r"total(?: premie|kostnad)?[^0-9]{0,15}([\d\s.,]+)\s*(kr|sek)?",
        r"premie.*?([\d\s.,]+)\s*(kr|sek)?",
        r"summa.*?([\d\s.,]+)\s*(kr|sek)?"
    ]
    return extract_field(patterns, text)

def extract_sjalvrisk(text):
    match = re.search(r"(självrisk)[^\d]{0,10}([\d\s.,]+)\s*(kr|sek|pbb)?", text, re.IGNORECASE)
    if match:
        val = parse_currency(match.group(2))
        unit = match.group(3) or ""
        return val * BASBELOPP_2025 if "pbb" in unit.lower() else val
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
        r"(ansvarstid|försäkringstid|ersättningstid).*?(\d{1,2})\s*(månader|månad|år)",
        r"gäller i\s*(\d{1,2})\s*(månader|månad|år)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            antal = int(match.group(2 if 'ersättningstid' in pattern else 1))
            enhet = match.group(3 if 'ersättningstid' in pattern else 2)
            return f"{antal * 12 if 'år' in enhet else antal} månader"
    return "saknas"

def extract_keyword_sum(keywords, text):
    total = 0.0
    for kw in keywords:
        pattern = rf"{kw}.*?([\d\s.,]+)\s*(kr|sek)?"
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            total += parse_currency(match[0])
    return total

def extract_all_insurance_data(text: str) -> dict:
    try:
        text = clean_text(text)

        return {
            "premie": extract_total_premie(text),
            "självrisk": extract_sjalvrisk(text),
            "karens": extract_karens(text),
            "ansvarstid": extract_ansvarstid(text),
            "byggnad": extract_keyword_sum(["byggnad", "fastighet", "byggnader"], text),
            "maskiner": extract_keyword_sum(["maskiner", "inventarier", "utrustning"], text),
            "varor": extract_keyword_sum(["varor", "lager", "förråd"], text),
            "transport": extract_keyword_sum(["transport", "godsförsäkring", "leverans"], text),
            "produktansvar": extract_keyword_sum(["produktansvar"], text),
            "ansvar": extract_keyword_sum(["verksamhetsansvar", "ansvarsförsäkring"], text),
            "rättsskydd": extract_keyword_sum(["rättsskydd", "juridiskt skydd"], text),
            "gdpr_ansvar": extract_keyword_sum(["gdpr", "personuppgifter"], text),
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

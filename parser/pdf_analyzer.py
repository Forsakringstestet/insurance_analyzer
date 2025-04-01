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


def extract_sum_by_keywords(keywords, text):
    total = 0.0
    for kw in keywords:
        pattern = rf"{kw}.*?([\d\s.,]+)\s*(kr|sek)?"
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            total += parse_currency(match[0])
    return total


def extract_total_premie(text):
    patterns = [
        r"totalt.*?SEK[\s]*([\d\s.,]+)",
        r"pris för tiden.*?SEK[\s]*([\d\s.,]+)",
        r"summa.*?SEK[\s]*([\d\s.,]+)",
        r"totalpris.*?([\d\s.,]+)\s*(kr|sek)?",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return parse_currency(match.group(1))
    return extract_sum_by_keywords(
        ["byggnad", "maskiner", "varor", "avbrott", "ansvar", "person", "rättsskydd"], text
    )


def extract_field(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return parse_currency(match.group(1)) if match else 0.0


def extract_sjalvrisk(text):
    match = re.search(r"(självrisk)[^\d]{0,10}([\d\s.,]+)\s*(kr|sek|pbb)?", text, re.IGNORECASE)
    if match:
        raw = match.group(2)
        unit = match.group(3) or ""
        val = parse_currency(raw)
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


def extract_byggnad(text):
    return extract_field(r"byggnad.*?([\d\s.,]+)\s*(kr|sek)?", text)


def extract_maskiner(text):
    return extract_field(r"(maskiner|maskinerier|inventarier).*?([\d\s.,]+)\s*(kr|sek)?", text)


def extract_varor(text):
    return extract_field(r"varor.*?([\d\s.,]+)\s*(kr|sek)?", text)


def extract_transport(text):
    return extract_field(r"(transport|godsförsäkring).*?([\d\s.,]+)\s*(kr|sek)?", text)


def extract_produktansvar(text):
    return extract_field(r"(produktansvar).*?([\d\s.,]+)\s*(kr|sek)?", text)


def extract_ansvar(text):
    return extract_field(r"(verksamhetsansvar).*?([\d\s.,]+)\s*(kr|sek)?", text)


def extract_rattsskydd(text):
    return extract_field(r"(rättsskydd).*?([\d\s.,]+)\s*(kr|sek)?", text)


def extract_gdpr_ansvar(text):
    return extract_field(r"(gdpr).*?([\d\s.,]+)\s*(kr|sek)?", text)


def extract_all_insurance_data(text: str) -> dict:
    try:
        return {
            "premie": extract_total_premie(text),
            "självrisk": extract_sjalvrisk(text),
            "karens": extract_karens(text),
            "ansvarstid": extract_ansvarstid(text),
            "byggnad": extract_byggnad(text),
            "maskiner": extract_maskiner(text),
            "varor": extract_varor(text),
            "transport": extract_transport(text),
            "produktansvar": extract_produktansvar(text),
            "ansvar": extract_ansvar(text),
            "rättsskydd": extract_rattsskydd(text),
            "gdpr_ansvar": extract_gdpr_ansvar(text),
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

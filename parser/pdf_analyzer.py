import re

BASBELOPP_2025 = 58800

def clean_float(text):
    if not text:
        return 0.0
    try:
        return float(text.replace(" ", "").replace(".", "").replace(",", "."))
    except:
        return 0.0

def extract_premie(text):
    text = text.lower()
    match = re.search(r"(premie|pris totalt|totalpris|totalbelopp)[^\d]{0,10}([\d\s.,]+)\s*(kr|sek)?", text)
    return clean_float(match.group(2)) if match else 0.0

def extract_sjalvrisk(text):
    text = text.lower()
    match = re.search(r"sj[aä]lvrisken?.{0,30}?([\d.,]+)\s*(kr|sek|basbelopp)?", text)
    if match:
        val = clean_float(match.group(1))
        if match.group(2) and "basbelopp" in match.group(2):
            return val * BASBELOPP_2025
        return val
    return 0.0

def extract_karens(text):
    text = text.lower()
    patterns = [
        r"karens\s*(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)",
        r"karens[^\d]{0,10}(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)",
        r"(\d{1,3})\s*(dygn|dagar|dag|timmar|tim|h)\s*karens"
    ]
    for p in patterns:
        match = re.search(p, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"
    return "saknas"

def extract_ansvarstid(text):
    text = text.lower()
    match = re.search(r"ansvarstid\s*(\d{1,2})\s*(m[aå]n(ader)?|[aå]r)", text)
    if match:
        antal = int(match.group(1))
        enhet = match.group(2)
        if "år" in enhet:
            return f"{antal * 12} månader"
        return f"{antal} månader"
    return "saknas"

def extract_maskiner(text):
    match = re.search(r"maskiner.?inventarier.{0,20}?([\d\s.,]+)\s*kr", text, re.IGNORECASE)
    return clean_float(match.group(1)) if match else 0.0

def extract_varor(text):
    match = re.search(r"varor.{0,20}?([\d\s.,]+)\s*kr", text, re.IGNORECASE)
    return clean_float(match.group(1)) if match else 0.0

def extract_ansvar(text):
    match = re.search(r"ansvarsf[oö]rs[aä]kring.*?([\d\s.,]+)\s*kr", text, re.IGNORECASE)
    return clean_float(match.group(1)) if match else 0.0

def extract_produktansvar(text):
    match = re.search(r"produktansvar.*?([\d\s.,]+)\s*kr", text, re.IGNORECASE)
    return clean_float(match.group(1)) if match else 0.0

def extract_all_insurance_data(text):
    return {
        "premie": extract_premie(text),
        "självrisk": extract_sjalvrisk(text),
        "karens": extract_karens(text),
        "ansvarstid": extract_ansvarstid(text),
        "maskiner": extract_maskiner(text),
        "varor": extract_varor(text),
        "ansvar": extract_ansvar(text),
        "produktansvar": extract_produktansvar(text)
    }

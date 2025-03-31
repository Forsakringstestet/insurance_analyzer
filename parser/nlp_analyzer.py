import re

def extract_scope(text):
    return re.findall(r"(omfattning|täcker|inkluderar)[:\s]+(.+?)\n", text, re.IGNORECASE)

def extract_exclusions(text):
    return re.findall(r"undantag[:\s]+(.+?)\n", text, re.IGNORECASE)

def extract_deductible(text):
    match = re.search(r"självrisk[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(1).replace(',', '.') if match else "0"

def extract_premium(text):
    match = re.search(r"premie[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(1).replace(',', '.') if match else "0"

def extract_amount(text):
    match = re.search(r"(belopp|försäkringsbelopp)[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(2).replace(',', '.') if match else "0"

def extract_clauses(text):
    return re.findall(r"(särskilda villkor|klausul)[:\s]+(.+?)\n", text, re.IGNORECASE)

def extract_property_amount(text):
    match = re.search(r"(egendomsbelopp|egendom)[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(2).replace(',', '.') if match else "0"

def extract_liability_limit(text):
    match = re.search(r"(ansvarsbelopp|ansvarsgräns)[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(2).replace(',', '.') if match else "0"

def extract_downtime_days(text):
    match = re.search(r"(karensdagar|karens)[:\s]*(\d+)", text, re.IGNORECASE)
    return match.group(1) if match else "0"

def extract_interruption_duration(text):
    match = re.search(r"(ansvarstid|avbrottstid)[:\s]*(\d+)", text, re.IGNORECASE)
    return match.group(1) if match else "0"

def extract_insurance_data(text: str) -> dict:
    return {
        "omfattning": extract_scope(text),
        "undantag": extract_exclusions(text),
        "självrisk": extract_deductible(text),
        "premie": extract_premium(text),
        "belopp": extract_amount(text),
        "klausuler": extract_clauses(text),
        "egendom": extract_property_amount(text),
        "ansvar": extract_liability_limit(text),
        "karens": extract_downtime_days(text),
        "avbrott": extract_interruption_duration(text),
    }

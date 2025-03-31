import re

def extract_insurance_data(text: str) -> dict:
    data = {
        "omfattning": extract_scope(text),
        "undantag": extract_exclusions(text),
        "självrisk": extract_deductibles(text),
        "premie": extract_cost(text),
        "belopp": extract_limits(text),
        "klausuler": extract_clauses(text)
    }
    return data

def extract_scope(text):
    match = re.search(r"(Omfattning|Täckning):(.+?)(\n|$)", text, re.IGNORECASE)
    return match.group(2).strip() if match else "Ej hittad"

def extract_exclusions(text):
    exclusions = re.findall(r"(undantag|ej gäller för):(.+?)(\n|$)", text, re.IGNORECASE)
    return [e[1].strip() for e in exclusions] if exclusions else []

def extract_deductibles(text):
    match = re.search(r"(Självrisk|Egen risk):\s*(\d+[.,]?\d*)", text, re.IGNORECASE)
    return match.group(2) if match else "Ej angiven"

def extract_cost(text):
    match = re.search(r"(Premie|Kostnad):\s*(\d+[.,]?\d*)", text, re.IGNORECASE)
    return match.group(2) if match else "Ej angiven"

def extract_limits(text):
    match = re.search(r"(Försäkringsbelopp|Ansvarsgräns):\s*(\d+[.,]?\d*)", text, re.IGNORECASE)
    return match.group(2) if match else "Ej angivet"

def extract_clauses(text):
    return re.findall(r"(§|Klausul)\s*\d+[^:]*:\s*(.+?)(\n|$)", text)

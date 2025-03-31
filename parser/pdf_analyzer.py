import re

def clean_number(val):
    return val.replace(" ", "").replace(".", "").replace(",", ".")

def extract_total_premium(text):
    match = re.search(r"(?i)premie[^0-9]{0,10}([0-9\s.,]+)\s*kr", text)
    return clean_number(match.group(1)) if match else "0"

def extract_deductible(text):
    match = re.search(r"(?i)(självrisk|självrisken)[^0-9]{0,10}([0-9\s.,]+|[0-9]+%|[0-9]+ basbelopp)", text)
    return match.group(2) if match else "0"

def extract_property_insurance(text):
    return re.findall(r"(?i)(maskiner|inventarier|varor)[^0-9]{0,10}([0-9\s.,]+)\s*kr", text)

def extract_liability_limits(text):
    return re.findall(r"(?i)(produktansvar|verksamhetsansvar|nyckelförlust|hyrd lokal)[^0-9]{0,10}([0-9\s.,]+)\s*kr", text)

def extract_interruption_info(text):
    karens = re.search(r"(?i)(karens|karensdagar)[^0-9]{0,10}(\d+)", text)
    ansvarstid = re.search(r"(?i)(ansvarstid)[^0-9]{0,10}(\d+)", text)
    return {
        "karens": karens.group(2) if karens else "okänt",
        "ansvarstid": ansvarstid.group(2) if ansvarstid else "okänt"
    }

def extract_total_premium(text):
    match = re.search(r"(?i)premie.*?([0-9][0-9\s.,]+)\\s*kr", text)
    return clean_number(match.group(1)) if match else "0"

def extract_deductible(text):
    match = re.search(r"(självrisk|självrisken).*?([0-9]+|[0-9]+\\s*%|[0-9,.]+\\s*kr|[0-9,.]+\\s*basbelopp)", text, re.IGNORECASE)
    return match.group(2) if match else "0"

def extract_property_insurance(text):
    return re.findall(r"(maskiner.*?|varor.*?)[:\\s]+([0-9\\s.,]+)\\s*kr", text, re.IGNORECASE)

def extract_liability_limits(text):
    return re.findall(r"(produktansvar|verksamhetsansvar|nyckelförlust|hyrd lokal).*?([0-9\\s.,]+)\\s*kr", text, re.IGNORECASE)

def extract_interruption_info(text):
    karens = re.search(r"(karens|karensdagar)[:\\s]*(\\d+)", text)
    ansvarstid = re.search(r"(ansvarstid)[:\\s]*(\\d+)", text)
    return {
        "karens": karens.group(2) if karens else "okänt",
        "ansvarstid": ansvarstid.group(2) if ansvarstid else "okänt"
    }

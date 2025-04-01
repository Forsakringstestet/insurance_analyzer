# Parser/nlp_analyzer.py
import re

def extract_scope(text: str) -> list:
    """
    Extraherar 'omfattning' från texten.
    
    Args:
        text (str): Inmatad text.
        
    Returns:
        list: Lista med matchande omfattningar.
    """
    return re.findall(r"(omfattning|täcker|inkluderar)[:\s]+(.+?)\n", text, re.IGNORECASE)

def extract_exclusions(text: str) -> list:
    """
    Extraherar undantag från texten.
    
    Args:
        text (str): Inmatad text.
        
    Returns:
        list: Lista med undantag.
    """
    return re.findall(r"undantag[:\s]+(.+?)\n", text, re.IGNORECASE)

def extract_deductible(text: str) -> str:
    """
    Extraherar självrisk.
    """
    match = re.search(r"självrisk[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(1).replace(',', '.') if match else "0"

def extract_premium(text: str) -> str:
    """
    Extraherar premie.
    """
    match = re.search(r"premie[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(1).replace(',', '.') if match else "0"

def extract_amount(text: str) -> str:
    """
    Extraherar belopp.
    """
    match = re.search(r"(belopp|försäkringsbelopp)[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(2).replace(',', '.') if match else "0"

def extract_clauses(text: str) -> list:
    """
    Extraherar särskilda villkor eller klausuler.
    """
    return re.findall(r"(särskilda villkor|klausul)[:\s]+(.+?)\n", text, re.IGNORECASE)

def extract_property_amount(text: str) -> str:
    """
    Extraherar egendomsbelopp.
    """
    match = re.search(r"(egendomsbelopp|egendom)[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(2).replace(',', '.') if match else "0"

def extract_liability_limit(text: str) -> str:
    """
    Extraherar ansvarsgräns.
    """
    match = re.search(r"(ansvarsbelopp|ansvarsgräns)[:\s]*([0-9.,]+)", text, re.IGNORECASE)
    return match.group(2).replace(',', '.') if match else "0"

def extract_downtime_days(text: str) -> str:
    """
    Extraherar karensdagar.
    """
    match = re.search(r"(karensdagar|karens)[:\s]*(\d+)", text, re.IGNORECASE)
    return match.group(1) if match else "0"

def extract_interruption_duration(text: str) -> str:
    """
    Extraherar ansvarstid eller avbrottstid.
    """
    match = re.search(r"(ansvarstid|avbrottstid)[:\s]*(\d+)", text, re.IGNORECASE)
    return match.group(1) if match else "0"

def extract_insurance_data(text: str) -> dict:
    """
    Extraherar samlad försäkringsdata från text.
    
    Returns:
        dict: Innehåller olika extraherade värden.
    """
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

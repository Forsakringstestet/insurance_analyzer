# recommender.py

def generate_recommendation(data: dict, industry: str = "") -> dict:
    """
    Genererar rekommenderade försäkringsnivåer baserat på bransch och nuvarande skydd.

    Args:
        data (dict): Försäkringsdata.
        industry (str): Branschinformation (valfri).

    Returns:
        dict: Rekommenderade nivåer per fält.
    """
    recommendation = {}

    # Basnivåer per bransch (kan utökas och förbättras)
    branschstandard = {
        "Bygg": {
            "produktansvar": 10000000,
            "maskiner": 1000000,
            "självrisk": 5000,
        },
        "IT": {
            "gdpr_ansvar": 2000000,
            "rättsskydd": 1000000,
            "självrisk": 10000,
        },
        "Transport": {
            "transport": 1000000,
            "ansvar": 5000000,
            "självrisk": 10000,
        },
        "Handel": {
            "varor": 1000000,
            "byggnad": 5000000,
        },
        "Industri": {
            "maskiner": 1500000,
            "produktansvar": 15000000,
        },
        "Fastighet": {
            "byggnad": 20000000,
            "ansvar": 5000000
        },
        "Konsult": {
            "rättsskydd": 200000,
            "gdpr_ansvar": 1000000
        },
        "Offentlig sektor": {
            "produktansvar": 20000000,
            "gdpr_ansvar": 3000000
        }
    }

    branschkrav = branschstandard.get(industry, {})

    for key, val in branschkrav.items():
        current = data.get(key, 0)
        if isinstance(current, (int, float)) and current < val:
            recommendation[key] = val

    return recommendation

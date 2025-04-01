# recommender.py
def generate_recommendation(data: dict) -> str:
    """
    Genererar en rekommendation baserat på innehållet i 'omfattning'-fältet.
    
    Args:
        data (dict): Försäkringsdata.
    
    Returns:
        str: Rekommendation baserat på identifierade nyckelord.
    """
    omfattning = data.get("omfattning", "").lower()
    if "bygg" in omfattning:
        return "Rekommenderat: Öka ansvarsnivå p.g.a. hög risk inom byggbranschen."
    elif "it" in omfattning:
        return "Rekommenderat: Se över cyberskydd och avbrottsersättning."
    return "Ingen särskild branschrekommendation hittades."

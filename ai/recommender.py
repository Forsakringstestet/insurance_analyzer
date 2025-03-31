def generate_recommendation(data):
    if "bygg" in data.get("omfattning", "").lower():
        return "Rekommenderat: Öka ansvarsnivå p.g.a. hög risk inom byggbranschen."
    elif "it" in data.get("omfattning", "").lower():
        return "Rekommenderat: Se över cyberskydd och avbrottsersättning."
    return "Ingen särskild branschrekommendation hittades."

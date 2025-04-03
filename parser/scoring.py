import streamlit as st

# Viktning av olika försäkringsmoment i poängsättningen
DEFAULT_WEIGHTS = {
    "premie": 25,
    "självrisk": 15,
    "omfattning": 45,
    "branschbonus": 15,
}

# Maxgränser för normalisering (exempel)
MAX_VALUES = {
    "premie": 50000,
    "självrisk": 20000,
    "maskiner": 1000000,
    "produktansvar": 10000000,
    "ansvar": 5000000,
    "byggnad": 2000000,
    "varor": 1000000,
    "transport": 1000000,
    "rättsskydd": 50000,
    "gdpr_ansvar": 1000000,
}

def normalize(value: float, max_value: float) -> float:
    try:
        return min(float(value) / max_value, 1.0)
    except:
        return 0.0

def score_document(data: dict, industry: str = "", weights: dict = DEFAULT_WEIGHTS) -> float:
    try:
        # Normaliserad poäng: ju lägre premie & självrisk desto bättre
        premie_score = 1.0 - normalize(data.get("premie", 0), MAX_VALUES["premie"])
        sjalvrisk_score = 1.0 - normalize(data.get("självrisk", 0), MAX_VALUES["självrisk"])

        # Omfattning: ju större skydd desto högre poäng
        omfattning_keys = ["maskiner", "produktansvar", "ansvar", "byggnad", "varor", "transport", "rättsskydd", "gdpr_ansvar"]
        omfattning_score = sum([
            normalize(data.get(k, 0), MAX_VALUES.get(k, 1))
            for k in omfattning_keys
        ]) / len(omfattning_keys)

        # Branschspecifik bonus
        bonus = 0.0
        if industry.lower() == "it":
            bonus += normalize(data.get("gdpr_ansvar", 0), MAX_VALUES["gdpr_ansvar"])
        elif industry.lower() in ["bygg", "entreprenad"]:
            bonus += 1.0 if data.get("självrisk", 0) < 10000 else 0.0
        elif industry.lower() in ["handel"]:
            bonus += normalize(data.get("varor", 0), MAX_VALUES["varor"])
        elif industry.lower() in ["transport"]:
            bonus += normalize(data.get("transport", 0), MAX_VALUES["transport"])

        # Total viktad poäng 0-100
        total_score = (
            premie_score * weights["premie"] +
            sjalvrisk_score * weights["självrisk"] +
            omfattning_score * weights["omfattning"] +
            bonus * weights["branschbonus"]
        ) / 100.0 * 100

        return round(total_score, 2)

    except Exception as e:
        st.warning(f"[Poängberäkning misslyckades] {e}")
        return 0.0

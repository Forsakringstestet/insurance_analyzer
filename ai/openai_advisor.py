import streamlit as st
import openai
import json
import re

# Initiera OpenAI-klientet
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# AI-FÖRSÄKRINGSRÅDGIVNING (GPT-3.5)
# -----------------------------
def ask_openai(data: dict, recommendations: dict = None, industry: str = "") -> str:
    try:
        rec_text = ""
        if recommendations:
            rec_text += "\n\nRekommenderade belopp enligt AI:\n"
            for key, val in recommendations.items():
                if isinstance(val, (int, float)) and val > 0:
                    rec_text += f"- {key.capitalize()}: {int(val):,} kr\n"

        prompt = f"""
Du är en avancerad försäkringsrådgivare för B2B. Du analyserar skyddsnivån i ett företags försäkring.

Bransch: {industry if industry else "Ej specificerad"}

Analysera skyddet baserat på:
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')} kr
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}
- Maskiner: {data.get('maskiner', 'okänd')} kr
- Produktansvar: {data.get('produktansvar', 'okänd')} kr
- GDPR: {data.get('gdpr_ansvar', 'okänd')} kr
- Rättsskydd: {data.get('rättsskydd', 'okänd')} kr
- Transport: {data.get('transport', 'okänd')} kr
{rec_text}

Gör:
1. Identifiera försäkringsskyddets styrkor och svagheter
2. Identifiera riskfaktorer och ev. brister
3. Ge konkreta förbättringsförslag

Max 3 tydliga punkter. Korta svar. Svenska. Inga övriga förklaringar.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.3,
            messages=[
                {"role": "system", "content": "Du är en försäkringsexpert."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[AI-fel] {str(e)}"

# -----------------------------
# AI-EXTRAKTION AV FÖRSÄKRINGSFÄLT (GPT-3.5)
# -----------------------------
def ask_openai_extract(text: str, industry: str = "") -> dict:
    try:
        prompt = f"""
Du är expert på svenska försäkringsbrev. Extrahera och returnera ENDAST en JSON enligt detta format.

OBS:
- Tolka belopp med "kr", ":-", "basbelopp" (58 800 kr år 2025) eller %.
- Om fältet saknas: returnera 0 för belopp eller "saknas" för text.
- Ingen extra förklaring.

Format:
{{
  "premie": float,
  "självrisk": float,
  "karens": "text",
  "ansvarstid": "text",
  "maskiner": float,
  "produktansvar": float,
  "byggnad": float,
  "rättsskydd": float,
  "transport": float,
  "varor": float,
  "ansvar": float,
  "gdpr_ansvar": float
}}

Text:
{text}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.0,
            messages=[
                {"role": "system", "content": "Du är en försäkringsanalytiker som alltid returnerar JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            raise ValueError("JSON-struktur kunde inte identifieras.")

    except Exception as e:
        st.warning(f"AI-extraktion misslyckades: {e}")
        return {
            "premie": 0.0,
            "självrisk": 0.0,
            "karens": "saknas",
            "ansvarstid": "saknas",
            "maskiner": 0.0,
            "produktansvar": 0.0,
            "byggnad": 0.0,
            "rättsskydd": 0.0,
            "transport": 0.0,
            "varor": 0.0,
            "ansvar": 0.0,
            "gdpr_ansvar": 0.0
        }

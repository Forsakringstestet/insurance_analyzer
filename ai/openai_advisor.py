import streamlit as st
import openai
import json
import re

# GPT-3.5: AI-försäkringsrådgivning
def ask_openai(data: dict, industry: str = "") -> str:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:
Analysera ett försäkringsdokument för ett företag inom branschen: {industry}.

Ge konkreta och praktiska råd kring:
1. Försäkringsskyddets styrkor och svagheter
2. Riskfaktorer och förbättringsförslag

Data:
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')} kr
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}
- Maskiner: {data.get('maskiner', 'okänd')} kr
- Produktansvar: {data.get('produktansvar', 'okänd')} kr
- Ansvar: {data.get('ansvar', 'okänd')} kr

Svar i form av max 3 tydliga punkter på svenska.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en försäkringsexpert."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[AI-fel] {str(e)}"


# GPT-3.5: AI-extraktion av fält från text

def ask_openai_extract(text: str, industry: str = "") -> dict:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en expert på svenska försäkringsbrev. Extrahera och returnera ENDAST en JSON enligt strukturen nedan. 

✅ Tolka siffror även om de står med "kr", ":-", "basbelopp" (58 800 kr år 2025) eller procent.
✅ Tolkning ska göras även om siffrorna står i löptext eller olika format.
✅ Om fältet saknas, returnera 0 för belopp eller "saknas" för text.

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
            temperature=0.2,
            messages=[
                {"role": "system", "content": "Du är en försäkringsanalytiker som returnerar exakt JSON utan extra text."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()

        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            json_data = json.loads(match.group())
        else:
            raise ValueError("Kunde inte hitta korrekt JSON-struktur i svaret.")

        return json_data

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

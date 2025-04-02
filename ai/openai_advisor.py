import streamlit as st
import openai
import json

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
Du är en försäkringsexpert. Extrahera följande fält ur försäkringsdokumentet nedan. Returnera ENDAST en JSON utan extra text.

Fält:
{{
  "premie": float,               # SEK
  "självrisk": float,            # SEK
  "karens": "text",             # Exempel: "1 dygn"
  "ansvarstid": "text",         # Exempel: "12 månader"
  "maskiner": float,             # SEK
  "produktansvar": float,       # SEK
  "byggnad": float,             # SEK
  "rättsskydd": float,         # SEK
  "transport": float,           # SEK
  "varor": float,               # SEK
  "ansvar": float,              # SEK
  "gdpr_ansvar": float          # SEK
}}

Text:
{text}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en försäkringsanalytiker."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            st.warning("AI-extraktion misslyckades: Kunde inte tolka JSON")
            return {}

    except Exception as e:
        st.warning(f"AI-extraktion misslyckades: [GPT-fel] {str(e)}")
        return {}

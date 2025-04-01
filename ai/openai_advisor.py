import streamlit as st
import openai
import json

# GPT-4 klient
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ✪ Rådgivning baserat på extraherad försäkringsdata
def ask_openai(data: dict, industry: str = "") -> str:
    try:
        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:
Analysera ett PDF-dokument som innehåller företagets försäkringspolicy, avtal och relevanta uppgifter.
Ge konkreta och praktiska råd kring försäkringsskyddets omfattning, riskfaktorer och förbättringsförslag.

- Bransch: {industry}
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')}
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}
- Maskiner: {data.get('maskiner', 'okänd')} kr
- Byggnad: {data.get('byggnad', 'okänd')} kr
- Varor: {data.get('varor', 'okänd')} kr
- Produktansvar: {data.get('produktansvar', 'okänd')} kr
- Rättsskydd: {data.get('rättsskydd', 'okänd')} kr
- GDPR ansvar: {data.get('gdpr_ansvar', 'okänd')} kr

1. Lista fördelar (max 3).
2. Lista nackdelar (max 3).
3. Ge förbättringsförslag (max 3) och sammanfatta.
Svara tydligt på svenska.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du är en försäkringsexpert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[AI-fel] {str(e)}"

# ✪ AI-driven extraktion av försäkringsdata ur fritext (PDF)
def ask_openai_extract(text: str) -> dict:
    try:
        prompt = f"""
Texten nedan kommer från ett försäkringsbrev eller offert.
Extrahera följande värden och returnera ENBART en giltig JSON-struktur exakt enligt exemplet nedan:

{{
  "premie": 12345,
  "självrisk": 10000,
  "karens": "1 dygn",
  "ansvarstid": "24 månader",
  "maskiner": 700000,
  "produktansvar": 1000000,
  "byggnad": 1000000,
  "rättsskydd": 300000,
  "ansvar": 1000000,
  "varor": 100000,
  "transport": 100000,
  "gdpr_ansvar": 500000
}}

Text:
{text}
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du är en expert på att tolka försäkringshandlingar och skapa korrekt JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        return {
            "premie": 0,
            "självrisk": 0,
            "karens": "saknas",
            "ansvarstid": "saknas",
            "maskiner": 0,
            "produktansvar": 0,
            "byggnad": 0,
            "rättsskydd": 0,
            "ansvar": 0,
            "varor": 0,
            "transport": 0,
            "gdpr_ansvar": 0,
            "fel": f"[GPT-fel] {str(e)}"
        }

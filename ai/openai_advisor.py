import streamlit as st
import openai
import json

# GPT-3.5 AI-försäkringsrådgivare

def ask_openai(data: dict, industry: str = "") -> str:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:
Analysera ett försäkringsdokument för ett företag.
Fokusera på att ge konkreta och praktiska råd kring försäkringsskyddets omfattning, identifiera centrala riskfaktorer anpassade efter företagets bransch.
Uteslut kommentarer om dokumentets struktur eller grammatik.

- Bransch: {industry}
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')}
- Omfattning: {data.get('omfattning', 'Ingen data')}
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}
- Maskiner: {data.get('maskiner', 'okänd')} kr
- Produktansvar: {data.get('produktansvar', 'okänd')} kr

Baserat på ovan:
1. Lista fördelar och nackdelar.
2. Ge förbättringsförslag i punktform.
3. Max 3 tydliga punkter på svenska.
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


# GPT-3.5 AI-drivna extraktion av fält från PDF

def ask_openai_extract(text: str) -> dict:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en försäkringsexpert. Extrahera följande data från försäkringsdokumentet nedan. Svara ENDAST med en korrekt formatterad JSON enligt strukturen:

{{
  "premie": float,
  "självrisk": float,
  "karens": "text",
  "ansvarstid": "text",
  "maskiner": float,
  "produktansvar": float,
  "byggnad": float,
  "varor": float,
  "transport": float,
  "ansvar": float,
  "rättsskydd": float,
  "gdpr_ansvar": float
}}

Exempel:
{{
  "premie": 15837.0,
  "självrisk": 10000.0,
  "karens": "1 dygn",
  "ansvarstid": "12 månader",
  "maskiner": 700000.0,
  "produktansvar": 10000000.0,
  "byggnad": 200000.0,
  "varor": 100000.0,
  "transport": 100000.0,
  "ansvar": 10000000.0,
  "rättsskydd": 300000.0,
  "gdpr_ansvar": 10000000.0
}}

Text att analysera:
{text}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en försäkringsexpert."},
                {"role": "user", "content": prompt}
            ]
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        return {
            "premie": 0.0,
            "självrisk": 0.0,
            "karens": "saknas",
            "ansvarstid": "saknas",
            "maskiner": 0.0,
            "produktansvar": 0.0,
            "byggnad": 0.0,
            "varor": 0.0,
            "transport": 0.0,
            "ansvar": 0.0,
            "rättsskydd": 0.0,
            "gdpr_ansvar": 0.0,
            "fel": f"[GPT-fel] {str(e)}"
        }

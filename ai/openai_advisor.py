import streamlit as st
import openai
import json

# ✅ OpenAI-klient med API-nyckel
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🔹 GPT-3.5 för AI-rekommendationer baserat på extraherade värden
def ask_openai(data: dict, industry: str = "") -> str:
    try:
        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:
- Analysera ett företags försäkringsbrev eller offert
- Ge konkreta och praktiska för- och nackdelar med försäkringen
- Ge förbättringsförslag för riskhantering och skydd

Bransch: {industry}
Premie: {data.get("premie", "okänd")} kr
Självrisk: {data.get("självrisk", "okänd")} kr
Maskiner: {data.get("maskiner", "okänd")} kr
Byggnad: {data.get("byggnad", "okänd")} kr
Varor: {data.get("varor", "okänd")} kr
Produktansvar: {data.get("produktansvar", "okänd")} kr
Transport: {data.get("transport", "okänd")} kr
Ansvar: {data.get("ansvar", "okänd")} kr
Rättsskydd: {data.get("rättsskydd", "okänd")} kr
GDPR ansvar: {data.get("gdpr_ansvar", "okänd")} kr
Karens: {data.get("karens", "okänd")}
Ansvarstid: {data.get("ansvarstid", "okänd")}

Svara på svenska i denna struktur:
1. Fördelar:
2. Nackdelar:
3. Förbättringsförslag:
4. Sammanfattning i punktform:
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en erfaren försäkringsanalytiker."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[AI-fel] {str(e)}"


# 🔹 GPT-3.5 för AI-baserad datatolkning från hela PDF-texten
def ask_openai_extract(text: str) -> dict:
    try:
        prompt = f"""
Texten nedan kommer från ett försäkringsbrev eller en offert. Extrahera följande fält och returnera ENDAST en giltig JSON-struktur enligt exemplet nedan.

Exempel:
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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en expert på försäkringsdokument och JSON-extraktion."},
                {"role": "user", "content": prompt}
            ]
        )

        raw_json = response.choices[0].message.content.strip()
        return json.loads(raw_json)

    except Exception as e:
        return {
            "premie": 0.0,
            "självrisk": 0.0,
            "karens": "saknas",
            "ansvarstid": "saknas",
            "maskiner": 0.0,
            "produktansvar": 0.0,
            "byggnad": 0.0,
            "rättsskydd": 0.0,
            "ansvar": 0.0,
            "varor": 0.0,
            "transport": 0.0,
            "gdpr_ansvar": 0.0,
            "fel": f"[GPT-fel] {str(e)}"
        }

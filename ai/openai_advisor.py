import streamlit as st
import openai
import json

# 🔹 GPT-3.5 för AI-rådgivning baserat på extraherade värden
def ask_openai(data: dict, industry: str = "") -> str:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en erfaren AI-försäkringsrådgivare med expertis inom företagsförsäkring.
Din uppgift är att granska ett försäkringsdokument och ge:
1. För- och nackdelar med nuvarande försäkringsskydd
2. Praktiska förbättringsförslag
3. Kort sammanfattning i tre tydliga punkter på svenska

Följande data har extraherats ur dokumentet:

- Bransch: {industry}
- Premie: {data.get('premie', 'saknas')} kr
- Självrisk: {data.get('självrisk', 'saknas')} kr
- Karens: {data.get('karens', 'saknas')}
- Ansvarstid: {data.get('ansvarstid', 'saknas')}
- Maskiner: {data.get('maskiner', 'saknas')} kr
- Produktansvar: {data.get('produktansvar', 'saknas')} kr
- Rättsskydd: {data.get('rättsskydd', 'saknas')} kr
- GDPR-ansvar: {data.get('gdpr_ansvar', 'saknas')} kr

Analysera detta som om du ger rådgivning till ett riktigt företag.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en expert inom företagsförsäkring och AI-rådgivning."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ [AI-fel] {str(e)}"

# 🔹 GPT-3.5-driven strukturell extraktion av nyckelvärden
def ask_openai_extract(text: str, industry: str = "") -> dict:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        extraction_prompt = f"""
Du ska extrahera nyckeldata från följande försäkringstext. Returnera **endast en giltig JSON-struktur** enligt nedan:

Format:
{{
  "premie": float,                   # Belopp i SEK, konvertera från t.ex. "0,5 basbelopp"
  "självrisk": float,                # Belopp i SEK
  "karens": "text",                  # T.ex. "1 dygn" eller "saknas"
  "ansvarstid": "text",              # T.ex. "24 månader" eller "saknas"
  "maskiner": float,                 # Belopp i SEK
  "produktansvar": float,            # Belopp i SEK
  "byggnad": float,                  # Belopp i SEK
  "varor": float,                    # Belopp i SEK
  "transport": float,               # Belopp i SEK
  "ansvar": float,                  # Belopp i SEK
  "rättsskydd": float,              # Belopp i SEK
  "gdpr_ansvar": float              # Belopp i SEK
}}

Texten gäller ett företag inom branschen: {industry}

Text att analysera:
{text}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en AI som extraherar strukturerad försäkringsdata från text."},
                {"role": "user", "content": extraction_prompt}
            ]
        )

        # Säker JSON-parsing
        response_text = response.choices[0].message.content.strip()
        return json.loads(response_text)

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

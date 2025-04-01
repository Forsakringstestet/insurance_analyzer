import streamlit as st
import openai

# 🔹 GPT-3.5 för AI-rekommendationer baserat på extraherade värden
def ask_openai(data: dict, industry: str = "") -> str:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:
Analysera ett PDF-dokument som innehåller företagets försäkringspolicy, avtal och övriga relevanta dokument.
Fokusera på att ge konkreta och praktiska råd kring försäkringsskyddets omfattning, samt identifiera centrala riskfaktorer anpassade efter företagets specifika bransch.
Utesluta analyser av dokumentets struktur eller formella uppbyggnad – din bedömning ska enbart grunda sig på innehållet och dess praktiska konsekvenser.

- Bransch: {industry}
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')}
- Omfattning: {data.get('omfattning', 'Ingen data')}
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}
- Maskiner: {data.get('maskiner', 'okänd')}
- Produktansvar: {data.get('produktansvar', 'okänd')}

Baserat på ovan:
1. Kommentera kort för- och nackdelar.
2. Ge förbättringsförslag.
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


# 🔹 GPT-3.5 för AI-driven extraktion av premie, självrisk, ansvarstid osv från hela PDF:en
def ask_openai_extract(text: str) -> dict:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
Texten nedan kommer från ett försäkringsbrev eller offert.
Du ska tolka värdena och returnera en JSON-struktur exakt enligt följande format:

{{
  "premie": <float i kr>,
  "självrisk": <float i kr>,
  "karens": "<timmar eller dagar>",
  "ansvarstid": "<antal månader>",
  "maskiner": <float i kr>,
  "produktansvar": <float i kr>
}}

Text:
{text}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en expert på att läsa försäkringsvillkor."},
                {"role": "user", "content": prompt}
            ],
            response_format="json"
        )

        return eval(response.choices[0].message.content)

    except Exception as e:
        return {
            "premie": 0.0,
            "självrisk": 0.0,
            "karens": "saknas",
            "ansvarstid": "saknas",
            "maskiner": 0.0,
            "produktansvar": 0.0,
            "fel": f"[GPT-fel] {str(e)}"
        }

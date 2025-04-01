# ai/openai_advisor.py

import streamlit as st
import openai
import json
import logging

# Sätt global OpenAI API-nyckel (secrets hanteras av Streamlit)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

def ask_openai(data: dict, industry: str = "") -> str:
    """
    Skicka en förfrågan till GPT-3.5 för att få AI-baserade försäkringsrekommendationer.

    Args:
        data (dict): Försäkringsdata.
        industry (str): Branschspecifik information (valfritt).

    Returns:
        str: Rekommendationen från AI.
    """
    try:
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en försäkringsexpert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.exception("Fel vid anrop till OpenAI")
        return f"[AI-fel] {str(e)}"

def ask_openai_extract(text: str) -> dict:
    """
    Skicka text till GPT-3.5 för att extrahera försäkringsdata och returnera det som ett dictionary.

    Args:
        text (str): Textutdrag från ett försäkringsbrev eller offert.

    Returns:
        dict: Extraherad data enligt angivet JSON-format.
    """
    try:
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en expert på att läsa försäkringsvillkor."},
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logging.exception("Fel vid extrahering med OpenAI")
        return {
            "premie": 0.0,
            "självrisk": 0.0,
            "karens": "saknas",
            "ansvarstid": "saknas",
            "maskiner": 0.0,
            "produktansvar": 0.0,
            "fel": f"[GPT-fel] {str(e)}"
        }

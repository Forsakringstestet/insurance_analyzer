# 📍 ai/openai_advisor.py
import streamlit as st
from openai import OpenAI

if "OPENAI_API_KEY" not in st.secrets:
    raise ValueError("OPENAI_API_KEY is missing from secrets.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask_openai(data: dict, industry: str = "") -> str:
    try:
        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:

Analysera ett PDF-dokument som innehåller företagets försäkringspolicy, avtal och övriga relevanta dokument.

Fokusera på att ge konkreta och praktiska råd kring försäkringsskyddets omfattning, samt identifiera centrala riskfaktorer anpassade efter företagets specifika bransch.

Utesluta analyser av dokumentets struktur eller formella uppbyggnad – din bedömning ska enbart grunda sig på innehållet och dess praktiska konsekvenser.

Svara med högst 5 korta och tydliga punkter.

Om viktig information saknas, ställ följdfrågor för att klargöra nödvändig kontext.
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

def ask_openai_with_fulltext(text: str, industry: str = "") -> str:
    try:
        prompt = f"""
Du är en försäkringsspecialist som analyserar ett försäkringsdokument.

Bransch: {industry}

Nedan följer innehållet i dokumentet:
--- START DOKUMENT ---
{text[:7000]}
--- SLUT DOKUMENT ---

1. Summera dokumentets försäkringsinnehåll.
2. Kommentera kort för- och nackdelar.
3. Ge konkreta förbättringsförslag inom försäkringsskydd.
4. Max 3 punkter, skriv på enkel svenska.
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

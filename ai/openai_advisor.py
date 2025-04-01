# 📍 ai/openai_advisor.py
import streamlit as st
from openai import OpenAI

if "OPENAI_API_KEY" not in st.secrets:
    raise ValueError("OPENAI_API_KEY is missing from secrets.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask_openai(data: dict, industry: str = "") -> str:
    try:
        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med omfattande expertis inom försäkringsbranschen. Din uppgift är att analysera ett helt PDF-dokument som innehåller företagets försäkringspolicy, avtal och relevanta dokument. Utifrån din analys ska du:

Sammanfatta: Identifiera och sammanfatta de viktigaste delarna i dokumentet.

Förbättringar: Rekommendera specifika ändringar och förbättringar för att optimera försäkringsskyddet, anpassat efter företagets bransch och unika verksamhetsförhållanden.

Riskanalys: Lista och förklara viktiga risker att beakta, inklusive potentiella försäkringsluckor, över- eller underförsäkring samt andra relevanta riskfaktorer som är särskilt viktiga för företagets bransch.

Implementering: Ge konkreta exempel på hur föreslagna ändringar kan implementeras och vilka effekter de kan medföra.

Kvalitetssäkring: Säkerställ att alla rekommendationer är baserade på dokumentets innehåll, gällande försäkringsregler och aktuell branschkunskap. Om nödvändig information saknas, ställ relevanta uppföljande frågor för att klargöra kontexten."

Använd ett tydligt, strukturerat och professionellt språk i dina svar, med hänsyn till företagets specifika bransch och behov.
Skriv max 5 korta punkter i klartext på svenska.
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

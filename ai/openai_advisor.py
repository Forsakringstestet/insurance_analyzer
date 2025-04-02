import streamlit as st
import openai
import json

# GPT-3.5 för AI-rekommendationer baserat på extraherade värden
def ask_openai(data: dict, industry: str = "") -> str:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:
Analysera ett PDF-dokument som innehåller företagets försäkringspolicy, avtal och övriga relevanta dokument.
Fokusera på att ge konkreta och praktiska råd kring försäkringsskyddets omfattning, samt identifiera centrala riskfaktorer anpassade efter företagets specifika bransch.
Uteslut analyser av dokumentets struktur eller formella uppbyggnad – din bedömning ska enbart grunda sig på innehållet och dess praktiska konsekvenser.

- Bransch: {industry}
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')}
- Omfattning: Maskiner: {data.get('maskiner', 'okänd')} | Produktansvar: {data.get('produktansvar', 'okänd')} | Ansvar: {data.get('ansvar', 'okänd')}
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}

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


# GPT-3.5 för AI-driven extraktion av försäkringsdata i JSON-format
def ask_openai_extract(text: str, industry: str = "") -> dict:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en försäkringsexpert. Extrahera följande fält ur ett försäkringsdokument i fri text.
Returnera endast en giltig JSON-struktur (inga kommentarer eller förklaringar).

Om ett värde anges som "0,5 basbelopp", räkna om det till SEK (1 basbelopp = 58 800 SEK).

Struktur:
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

Text att analysera:
{text}
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en expert på att läsa försäkringsvillkor."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()

        # Försök tolka som JSON
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                return data
            else:
                st.warning("AI-extraktion misslyckades: JSON var inte ett dictionary-objekt.")
                return {}
        except json.JSONDecodeError:
            st.warning("AI-extraktion misslyckades: Kunde inte tolka JSON")
            return {}

    except Exception as e:
        st.warning(f"AI-extraktion misslyckades: [GPT-fel] {str(e)}")
        return {}

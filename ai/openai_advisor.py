import streamlit as st
import openai
import json

# ✨ GPT-3.5 för AI-rekommendationer baserat på extraherade fält
def ask_openai(data: dict, industry: str = "") -> str:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:
Analysera ett försäkringsdokument som innehåller policy, avtal och villkor.
Fokusera på att ge konkreta råd kring skyddets omfattning och riskfaktorer utifrån bransch.

- Bransch: {industry}
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')}
- Maskiner: {data.get('maskiner', 'okänd')} kr
- Produktansvar: {data.get('produktansvar', 'okänd')} kr
- Ansvar: {data.get('ansvar', 'okänd')} kr
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}

1. Kommentera för- och nackdelar.
2. Ge konkreta förbättringsförslag.
3. Max 3 punkter på svenska.
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


# ✨ GPT-3.5 för AI-driven extraktion av premie, självrisk, ansvarstid osv

def ask_openai_extract(text: str, industry: str = "") -> dict:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en försäkringsexpert. Extrahera följande fält ur dokumentet nedan:
Returnera ENDAST en korrekt JSON utan inledning eller eftertext.

Format:
{{
  "premie": float,
  "självrisk": float,
  "karens": "str",
  "ansvarstid": "str",
  "maskiner": float,
  "produktansvar": float,
  "byggnad": float,
  "rättsskydd": float,
  "transport": float,
  "varor": float,
  "ansvar": float,
  "gdpr_ansvar": float
}}

Text:
{text}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en expert på försäkringsvillkor."},
                {"role": "user", "content": prompt}
            ]
        )

        # Försök att plocka ut JSON ur svaret, använd JSON-lokaliserare om något slinker in före/efter
        content = response.choices[0].message.content.strip()
        start = content.find("{")
        end = content.rfind("}") + 1
        if start == -1 or end == -1:
            raise ValueError("Ingen giltig JSON hittades i GPT-svaret.")

        cleaned_json = content[start:end]
        return json.loads(cleaned_json)

    except Exception as e:
        st.warning(f"AI-extraktion misslyckades: {str(e)}")
        return {}

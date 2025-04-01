import streamlit as st
import openai
import json

# 🔹 AI-rådgivning baserat på extraherade nyckelvärden
def ask_openai(data: dict, industry: str = "") -> str:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:
Analysera ett företags försäkringspolicy och identifiera styrkor, svagheter och ge förbättringsförslag.
Uteslut all bedömning av dokumentstruktur, fokusera på innehåll.

- Bransch: {industry}
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')}
- Maskiner: {data.get('maskiner', 'okänd')} kr
- Varor: {data.get('varor', 'okänd')} kr
- Byggnad: {data.get('byggnad', 'okänd')} kr
- Produktansvar: {data.get('produktansvar', 'okänd')} kr
- Rättsskydd: {data.get('rättsskydd', 'okänd')} kr
- Ansvar: {data.get('ansvar', 'okänd')} kr
- GDPR-ansvar: {data.get('gdpr_ansvar', 'okänd')} kr
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}

Baserat på ovan:
1. Lista fördelar
2. Lista nackdelar
3. Ge 2–3 tydliga förbättringsförslag på svenska
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


# 🔹 Finjusterad GPT-extraktion för svenska försäkrings-PDF:er
def ask_openai_extract(text: str) -> dict:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        prompt = f"""
Du är en expert på att tolka svenska försäkringsbrev och offerter från bolag som Trygg-Hansa, LF, IF, Dina Försäkringar m.fl.
Din uppgift är att identifiera och extrahera värden till följande JSON-fält, exakt som nedan:

{
  "premie": float,
  "självrisk": float,               # Belopp i SEK, konvertera från t.ex. "0,5 basbelopp"
  "karens": "text",
  "ansvarstid": "text",
  "maskiner": float,
  "produktansvar": float,
  "byggnad": float,
  "rättsskydd": float,
  "ansvar": float,
  "varor": float,
  "transport": float,
  "gdpr_ansvar": float
}

🧠 Observera:
- Alla belopp ska konverteras till svenska kronor (SEK).
- Basbelopp för 2025 är 58 800 kr. Om självrisk anges i t.ex. "0,2 pbb" ska det konverteras till 11760 kr.
- Om ett fält inte hittas, ange 0 för siffror eller "saknas" för text.
- Returnera ENDAST korrekt JSON, utan kommentarer.

Text att analysera:
{text}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en expert på att läsa och extrahera försäkringsdata i JSON-format."},
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.choices[0].message.content.strip()

        if not raw.startswith("{"):
            raise ValueError("Inget giltigt JSON-svar från GPT:\n" + raw)

        return json.loads(raw)

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

import streamlit as st
import openai
import json

# 🔹 GPT-3.5 för AI-rekommendationer baserat på extraherade värden
def ask_openai(data: dict, industry: str = "") -> str:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
Du är en avancerad AI-försäkringsrådgivare med djup branschkunskap. Din uppgift är att:
Analysera ett försäkringsdokument för ett företag.
Du ska:
1. Kommentera för- och nackdelar utifrån det skydd och de risker som dokumentet beskriver.
2. Ge förbättringsförslag som om du vore försäkringsmäklare – konkret, praktiskt och branschanpassat.
3. Utelämna formalia och fokusera på verkligt skyddsvärde och brister.

Data för bedömning:
- Bransch: {industry}
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')}
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}
- Maskiner: {data.get('maskiner', 'okänd')} kr
- Produktansvar: {data.get('produktansvar', 'okänd')} kr
- GDPR ansvar: {data.get('gdpr_ansvar', 'okänd')} kr
- Byggnad: {data.get('byggnad', 'okänd')} kr
- Rättsskydd: {data.get('rättsskydd', 'okänd')} kr

Gör en översikt:
1. Fördelar
2. Risker / svagheter
3. Förbättringsförslag (max 3 punkter, svenska)
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


# 🔹 GPT-3.5 för AI-baserad extraktion från fri text i PDF:er
def ask_openai_extract(text: str) -> dict:
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        prompt = f"""
Texten nedan kommer från ett försäkringsbrev eller offert.
Identifiera och extrahera så korrekt som möjligt de följande fälten och returnera som JSON:

- premie (float)
- självrisk (float i kronor, välj den viktigaste om flera anges)
- karens (str)
- ansvarstid (str, i månader eller år)
- maskiner (float)
- produktansvar (float)
- byggnad (float)
- rättsskydd (float)
- gdpr_ansvar (float)

Format:
{{
  "premie": ...,
  "självrisk": ...,
  "karens": "...",
  "ansvarstid": "...",
  "maskiner": ...,
  "produktansvar": ...,
  "byggnad": ...,
  "rättsskydd": ...,
  "gdpr_ansvar": ...
}}

Text:
{text}
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du är en expert på att tolka försäkringsvillkor."},
                {"role": "user", "content": prompt}
            ],
            response_format="json"
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
            "rättsskydd": 0.0,
            "gdpr_ansvar": 0.0,
            "fel": f"[GPT-fel] {str(e)}"
        }

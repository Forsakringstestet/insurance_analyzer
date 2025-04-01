import streamlit as st
from openai import OpenAI

if "OPENAI_API_KEY" not in st.secrets:
    raise ValueError("OPENAI_API_KEY is missing from secrets.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def ask_openai(data: dict, industry: str = "") -> str:
    try:
        prompt = f"""
Du är en försäkringsspecialist som analyserar dokument baserat på följande uppgifter:

- Bransch: {industry}
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')}
- Omfattning: {data.get('omfattning', 'Ingen data')}
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}

Baserat på ovan:
1. Kommentera kort för- och nackdelar.
2. Ge konkreta förbättringsförslag för detta företag inom sin bransch.
3. Skriv max 3 korta punkter i klartext på svenska.
"""

        response = client.completions.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
        )

        return response.choices[0].text.strip()

    except Exception as e:
        return f"[AI-fel] {str(e)}"

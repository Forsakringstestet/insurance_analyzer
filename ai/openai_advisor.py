import openai
import streamlit as st

if "OPENAI_API_KEY" not in st.secrets:
    raise ValueError("OPENAI_API_KEY is missing from Streamlit secrets.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

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

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # <- you can change to gpt-4 if you have access
            messages=[
                {"role": "system", "content": "Du är en försäkringsexpert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[AI-fel] {str(e)}"

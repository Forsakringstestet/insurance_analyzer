import streamlit as st
import openai

def ask_openai(data: dict, industry: str = "") -> str:
    try:
        openai.api_key = st.secrets["openai_api_key"]

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

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du är en försäkringsexpert."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[AI-fel] {str(e)}"

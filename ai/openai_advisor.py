from openai import OpenAI
import streamlit as st
import time

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def ask_openai(data, industry: str = "generell"):
    prompt = f"""
Du är en AI-specialist inom företagsförsäkringar.

Analysera följande försäkringsdata och ge en rekommendation anpassad till branschen: {industry}

Data:
- Omfattning: {data['omfattning']}
- Undantag: {', '.join(data['undantag'])}
- Självrisk: {data['självrisk']}
- Premie: {data['premie']}
- Belopp: {data['belopp']}
- Klausuler: {data['klausuler']}

Ge ett konkret förslag: höj/sänk försäkringsbelopp, omförhandla klausuler, förbättra omfattning, etc.
"""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                return f\"OpenAI fel: {e}\"
            time.sleep(2)  # vänta innan nytt försök
try:
    recommendation = ask_openai(data, industry=industry)
except Exception as e:
    recommendation = f\"Kunde ej hämta AI-råd: {e}\"

import openai
import streamlit as st

def ask_openai(data, industry: str = "generell"):
    openai.api_key = st.secrets["openai"]["api_key"]

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
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message["content"]

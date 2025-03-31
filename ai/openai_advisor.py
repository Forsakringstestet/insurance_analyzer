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
def ask_openai_compare(all_data: list, industry: str = "generell"):
    summary_input = "\n\n".join([
        f"Dokument: {item['filename']}\n"
        f"- Omfattning: {item['data']['omfattning']}\n"
        f"- Undantag: {', '.join(item['data']['undantag'])}\n"
        f"- Självrisk: {item['data']['självrisk']}\n"
        f"- Premie: {item['data']['premie']}\n"
        f"- Belopp: {item['data']['belopp']}\n"
        f"- Klausuler: {item['data']['klausuler']}\n"
        f"- Poäng: {item['score']}\n"
        for item in all_data
    ])

    prompt = f"""
Du är en AI-upphandlare specialiserad på försäkringar.

Jämför följande dokument (upp till 10) inom branschen: {industry}.

Välj det mest gynnsamma, och motivera beslutet med tydliga argument kring premie, självrisk, omfattning och undantag.

{summary_input}

Svara i punktform. Föreslå ev. kompletteringar.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

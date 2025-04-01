import os
from openai import OpenAI

client = OpenAI()

def ask_openai(data: dict, industry: str = "") -> str:
    prompt = f"""
Du är en försäkringsspecialist som analyserar ett dokument baserat på:

- Bransch: {industry}
- Premie: {data.get('premie', 'okänd')} kr
- Självrisk: {data.get('självrisk', 'okänd')}
- Omfattning:
{data.get('omfattning', 'Ingen data')}
- Karens: {data.get('karens', 'okänd')}
- Ansvarstid: {data.get('ansvarstid', 'okänd')}

⚖️ Kommentera kort på dokumentets styrkor/svagheter.
🔧 Ge konkreta förbättringsförslag.
🧠 Skriv max 3 punkter i klartext på svenska.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du är en försäkringsexpert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[AI-fel] {str(e)}"

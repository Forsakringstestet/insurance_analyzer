import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(data: dict, industry: str = "") -> str:
    try:
        prompt = f"""
        Du är en försäkringsspecialist som analyserar dokument baserat på följande uppgifter:

        - Bransch: {industry}
        - Premie: {data.get('premie', 'okänd')} kr
        - Självrisk: {data.get('självrisk', 'okänd')}
        - Omfattning:
{data.get('omfattning', 'Ingen data')}
        - Karens: {data.get('karens', 'okänt')}
        - Ansvarstid: {data.get('ansvarstid', 'okänt')}

        Baserat på ovan: 
        1. Kommentera kort för- och nackdelar.
        2. Ge konkreta förbättringsförslag för detta företag inom sin bransch.
        3. Skriv max 3 korta punkter i klartext på svenska.
        """

from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Du är en försäkringsexpert..."},
        {"role": "user", "content": prompt}
    ]
)

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[AI-fel] {str(e)}"

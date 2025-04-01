import streamlit as st
import pandas as pd


def display_results(analysis_results):
    st.subheader("📊 Sammanställning & Jämförelse")

    # Tabellformat
    rows = []
    for item in analysis_results:
        data = item["data"]
        rows.append({
            "Filnamn": item["filename"],
            "Poäng": round(item["score"], 2),
            "Premie (kr)": data.get("premie", 0),
            "Självrisk (kr)": data.get("självrisk", 0),
            "Maskiner (kr)": data.get("maskiner", 0),
            "Produktansvar (kr)": data.get("produktansvar", 0),
            "Karens": data.get("karens", "okänt"),
            "Ansvarstid": data.get("ansvarstid", "okänt"),
        })

    df = pd.DataFrame(rows)

    # Färgkodning för Poäng (grön → röd)
    def highlight_score(val):
        if val >= 80:
            color = 'lightgreen'
        elif val >= 50:
            color = 'khaki'
        else:
            color = 'salmon'
        return f'background-color: {color}'

    st.dataframe(df.style.applymap(highlight_score, subset=['Poäng']))

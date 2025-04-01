# Utils/visualizer.py
import streamlit as st
import pandas as pd

def display_results(analysis_results: list) -> None:
    """
    Visar en sammanställning av analyserade resultat med färgkodad poäng.
    
    Args:
        analysis_results (list): Lista med dictionaries innehållande 'filename', 'score' och 'data'.
    """
    st.subheader("📊 Sammanställning & Jämförelse")
    rows = []
    for item in analysis_results:
        data = item.get("data", {})
        rows.append({
            "Filnamn": item.get("filename", ""),
            "Poäng": round(item.get("score", 0), 2),
            "Premie (kr)": data.get("premie", 0),
            "Självrisk (kr)": data.get("självrisk", 0),
            "Maskiner (kr)": data.get("maskiner", 0),
            "Produktansvar (kr)": data.get("produktansvar", 0),
            "Karens": data.get("karens", "okänt"),
            "Ansvarstid": data.get("ansvarstid", "okänt"),
        })
    
    df = pd.DataFrame(rows)
    
    def highlight_score(val):
        if val >= 80:
            color = 'lightgreen'
        elif val >= 50:
            color = 'khaki'
        else:
            color = 'salmon'
        return f'background-color: {color}'
    
    st.dataframe(df.style.applymap(highlight_score, subset=['Poäng']))

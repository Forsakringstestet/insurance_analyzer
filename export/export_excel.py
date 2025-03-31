import pandas as pd
import streamlit as st
from io import BytesIO

def export_summary_excel(results):
    df = pd.DataFrame([{
        "Fil": r["filename"],
        "Poäng": r["score"],
        "Omfattning": r["data"]["omfattning"],
        "Självrisk": r["data"]["självrisk"],
        "Premie": r["data"]["premie"],
        "Belopp": r["data"]["belopp"],
        "Rekommendation": r["recommendation"]
    } for r in results])
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Analys')
    st.download_button("Ladda ner Excel", output.getvalue(), file_name="analys.xlsx")

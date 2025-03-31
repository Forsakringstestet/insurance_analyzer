import pandas as pd
import streamlit as st
import plotly.express as px

def display_results(results: list):
    st.subheader("📊 Jämförelse av försäkringsdokument")

    df = pd.DataFrame([{
        "Fil": r["filename"],
        "Omfattning": len(r["data"]["omfattning"]),
        "Premie": float(r["data"]["premie"]),
        "Självrisk": float(r["data"]["självrisk"]),
        "Belopp": float(r["data"]["belopp"]),
        "Poäng": r["score"],
    } for r in results])

    st.dataframe(df)

    fig = px.bar(df, x="Fil", y="Poäng", color="Poäng", color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

def display_results(results):
    if not results:
        st.warning("Inga analyserade dokument att visa.")
        return

    table_data = []
    for r in results:
        row = {
            "Fil": r["filename"],
            "Premie": r["data"].get("premie", 0),
            "Självrisk": r["data"].get("självrisk", 0),
            "Maskiner": r["data"].get("egendom", {}).get("maskiner", 0),
            "Produktansvar": r["data"].get("ansvar", {}).get("produktansvar", 0),
            "Karens": r["data"].get("karens", "-"),
            "Ansvarstid": r["data"].get("ansvarstid", "-"),
            "Poäng": r["score"]
        }
        table_data.append(row)

    df = pd.DataFrame(table_data)
    st.subheader("📊 Jämförelse av försäkringsdokument")
    st.dataframe(df)

    fig = px.bar(df, x="Fil", y="Poäng", color="Poäng", text_auto=True,
                 color_continuous_scale="RdYlGn", height=400)
    st.plotly_chart(fig, use_container_width=True)

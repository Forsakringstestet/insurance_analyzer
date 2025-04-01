import streamlit as st
import pandas as pd

def render_comparison_table(results):
    rows = []

    for r in results:
        d = r["data"]
        rows.append({
            "Dokument": r["filename"],
            "Premie": d.get("premie", 0),
            "Självrisk": d.get("självrisk", 0),
            "Maskiner": d.get("maskiner", 0),
            "Varor": d.get("varor", 0),
            "Byggnad": d.get("byggnad", 0),
            "Transport": d.get("transport", 0),
            "Produktansvar": d.get("produktansvar", 0),
            "Ansvar": d.get("ansvar", 0),
            "Rättsskydd": d.get("rättsskydd", 0),
            "GDPR ansvar": d.get("gdpr_ansvar", 0),
            "Karens": d.get("karens", "okänt"),
            "Ansvarstid": d.get("ansvarstid", "okänt"),
            "Poäng": r.get("score", 0)
        })

    df = pd.DataFrame(rows)

    def colorize(val, col):
        if pd.isna(val) or isinstance(val, str):
            return ""
        if col in ["Poäng", "Maskiner", "Varor", "Byggnad", "Transport", "Produktansvar", "Ansvar", "Rättsskydd", "GDPR ansvar"]:
            return "background-color: lightgreen" if val == df[col].max() else ""
        elif col in ["Premie", "Självrisk"]:
            return "background-color: lightgreen" if val == df[col].min() else ""
        return ""

    styled = df.style.apply(lambda x: [colorize(v, x.name) for v in x], axis=1)

    st.subheader("📊 Jämförelsetabell med färgkodning")
    st.dataframe(styled, use_container_width=True)

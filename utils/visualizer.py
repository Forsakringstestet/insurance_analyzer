import streamlit as st
import pandas as pd


def render_comparison_table(results: list):
    if not results:
        st.info("Inga dokument att jämföra.")
        return

    rows = []
    for r in results:
        d = r["data"]
        rows.append({
            "Filnamn": r["filename"],
            "Poäng": round(r.get("score", 0)),
            "Premie (kr)": round(d.get("premie", 0)),
            "Självrisk (kr)": round(d.get("självrisk", 0)),
            "Maskiner (kr)": round(d.get("maskiner", 0)),
            "Produktansvar (kr)": round(d.get("produktansvar", 0)),
            "Ansvar (kr)": round(d.get("ansvar", 0)),
            "Rättsskydd (kr)": round(d.get("rättsskydd", 0)),
            "GDPR ansvar (kr)": round(d.get("gdpr_ansvar", 0)),
            "Karens": d.get("karens", "saknas"),
            "Ansvarstid": d.get("ansvarstid", "saknas")
        })

    df = pd.DataFrame(rows)

    def highlight_score(val):
        if isinstance(val, (int, float)):
            if val >= 900000:
                return "background-color: lightgreen"
            elif val >= 700000:
                return "background-color: khaki"
            else:
                return "background-color: salmon"
        return ""

    styled_df = df.style.applymap(highlight_score, subset=["Poäng"])

    st.dataframe(styled_df, use_container_width=True)

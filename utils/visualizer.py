import streamlit as st
import pandas as pd

def render_comparison_table(results):
    st.subheader("📊 Jämförelsetabell med färgkodning")

    rows = []
    for result in results:
        row = {
            "Dokument": result["filename"],
            "Premie": result["data"].get("premie", 0),
            "Självrisk": result["data"].get("självrisk", 0),
            "Maskiner": result["data"].get("maskiner", 0),
            "Varor": result["data"].get("varor", 0),
            "Byggnad": result["data"].get("byggnad", 0),
            "Transport": result["data"].get("transport", 0),
            "Produktansvar": result["data"].get("produktansvar", 0),
            "Ansvar": result["data"].get("ansvar", 0),
            "Rättsskydd": result["data"].get("rättsskydd", 0),
            "GDPR ansvar": result["data"].get("gdpr_ansvar", 0)
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.round(0).astype(object)
    st.dataframe(df, use_container_width=True)

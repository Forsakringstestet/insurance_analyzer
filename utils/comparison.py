# Utils/comparison.py
import streamlit as st
import pandas as pd

def render_comparison_table(results: list) -> None:
    """
    Renderar en jämförelsetabell med färgkodning via Streamlit.
    
    Args:
        results (list): Lista med dictionaries innehållande försäkringsdata.
    """
    rows = []
    
    def safe_val(val):
        if isinstance(val, (int, float)):
            return val
        try:
            return float(str(val).replace(" ", "").replace(",", "."))
        except:
            return 0.0
    
    for r in results:
        d = r.get("data", {})
        rows.append({
            "Dokument": r.get("filename", ""),
            "Premie": safe_val(d.get("premie", 0)),
            "Självrisk": safe_val(d.get("självrisk", 0)),
            "Maskiner": safe_val(d.get("maskiner", 0)),
            "Varor": safe_val(d.get("varor", 0)),
            "Byggnad": safe_val(d.get("byggnad", 0)),
            "Transport": safe_val(d.get("transport", 0)),
            "Produktansvar": safe_val(d.get("produktansvar", 0)),
            "Ansvar": safe_val(d.get("ansvar", 0)),
            "Rättsskydd": safe_val(d.get("rättsskydd", 0)),
            "GDPR ansvar": safe_val(d.get("gdpr_ansvar", 0)),
            "Karens": d.get("karens", "saknas"),
            "Ansvarstid": d.get("ansvarstid", "saknas"),
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

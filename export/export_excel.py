# export/export_excel.py

import pandas as pd
import tempfile
import streamlit as st

def export_summary_excel(results):
    rows = []

    for r in results:
        d = r["data"]
        rows.append({
            "Filnamn": r["filename"],
            "Poäng": r.get("score", 0),
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
            "Karens": d.get("karens", "saknas"),
            "Ansvarstid": d.get("ansvarstid", "saknas")
        })

    df = pd.DataFrame(rows)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        df.to_excel(tmp.name, index=False)
        st.download_button("📊 Ladda ner Excel", data=open(tmp.name, "rb"), file_name="forsakringsjämforelse.xlsx")

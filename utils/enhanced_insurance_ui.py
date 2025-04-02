import streamlit as st
import pandas as pd

def display_pretty_summary(data):
    """
    Visar en summering av ett enskilt dokument eller lista av dokument i en fin layout.
    """
    if isinstance(data, dict):
        docs = [data]
    else:
        docs = data

    for entry in docs:
        filename = entry["filename"] if isinstance(entry, dict) else ""
        d = entry["data"] if isinstance(entry, dict) else entry

        with st.container():
            st.markdown(f"### 📄 {filename}")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Premie", f"{int(d.get('premie', 0))} kr")
                st.metric("Självrisk", f"{int(d.get('självrisk', 0))} kr")
                st.metric("Poäng", int(entry.get("score", 0)))
            with col2:
                st.metric("Maskiner", f"{int(d.get('maskiner', 0))} kr")
                st.metric("Produktansvar", f"{int(d.get('produktansvar', 0))} kr")
                st.metric("Ansvar", f"{int(d.get('ansvar', 0))} kr")
            with col3:
                st.metric("GDPR ansvar", f"{int(d.get('gdpr_ansvar', 0))} kr")
                st.metric("Rättsskydd", f"{int(d.get('rättsskydd', 0))} kr")
                st.metric("Transport", f"{int(d.get('transport', 0))} kr")

            st.caption(f"Karens: {d.get('karens', 'saknas')} | Ansvarstid: {d.get('ansvarstid', 'saknas')}")
            st.markdown("---")

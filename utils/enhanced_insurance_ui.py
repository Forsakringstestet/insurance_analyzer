# utils/enhanced_insurance_ui.py

import streamlit as st
import pandas as pd

# utils/enhanced_insurance_ui.py

import streamlit as st

def display_pretty_summary(results: list):
    if not results:
        st.warning("Ingen data att visa.")
        return

    doc = results[0]["data"]  # Tar första dokumentet

    st.subheader("🧾 Sammanfattning")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("💰 Premie", f"{doc.get('premie', 0):,.0f} kr")
        st.metric("📉 Självrisk", f"{doc.get('självrisk', 0):,.0f} kr")
        st.metric("⏳ Karens", doc.get("karens", "saknas"))
        st.metric("📆 Ansvarstid", doc.get("ansvarstid", "saknas"))

    with col2:
        st.metric("🏗️ Maskiner", f"{doc.get('maskiner', 0):,.0f} kr")
        st.metric("📦 Varor", f"{doc.get('varor', 0):,.0f} kr")
        st.metric("🏠 Byggnad", f"{doc.get('byggnad', 0):,.0f} kr")
        st.metric("🚛 Transport", f"{doc.get('transport', 0):,.0f} kr")

    st.markdown("---")

# utils/enhanced_insurance_ui.py

import streamlit as st
import pandas as pd

def display_pretty_summary(data: dict):
    st.subheader("🧾 Sammanfattning")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("💰 Premie", f"{data.get('premie', 0):,.0f} kr")
        st.metric("📉 Självrisk", f"{data.get('självrisk', 0):,.0f} kr")
        st.metric("⏳ Karens", data.get("karens", "saknas"))
        st.metric("📆 Ansvarstid", data.get("ansvarstid", "saknas"))

    with col2:
        st.metric("🏗️ Maskiner", f"{data.get('maskiner', 0):,.0f} kr")
        st.metric("📦 Varor", f"{data.get('varor', 0):,.0f} kr")
        st.metric("🏠 Byggnad", f"{data.get('byggnad', 0):,.0f} kr")
        st.metric("📦 Transport", f"{data.get('transport', 0):,.0f} kr")

    st.markdown("---")

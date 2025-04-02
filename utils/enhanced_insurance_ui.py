import streamlit as st
import pandas as pd

def display_pretty_summary(analysis_results):
    st.subheader("📑 Sammanfattning")

    for result in analysis_results:
        doc = result["data"]
        filename = result["filename"]

        with st.expander(f"📄 {filename}", expanded=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("💰 Premie", f"{float(doc.get('premie', 0) or 0):,.0f} kr")
                st.metric("🛠 Maskiner", f"{float(doc.get('maskiner', 0) or 0):,.0f} kr")
                st.metric("🏠 Byggnad", f"{float(doc.get('byggnad', 0) or 0):,.0f} kr")

            with col2:
                st.metric("💣 Självrisk", f"{float(doc.get('självrisk', 0) or 0):,.0f} kr")
                st.metric("📦 Varor", f"{float(doc.get('varor', 0) or 0):,.0f} kr")
                st.metric("🚛 Transport", f"{float(doc.get('transport', 0) or 0):,.0f} kr")

            with col3:
                st.metric("🧪 Produktansvar", f"{float(doc.get('produktansvar', 0) or 0):,.0f} kr")
                st.metric("⚖️ Ansvar", f"{float(doc.get('ansvar', 0) or 0):,.0f} kr")
                st.metric("📜 Rättsskydd", f"{float(doc.get('rättsskydd', 0) or 0):,.0f} kr")

            col4, col5 = st.columns(2)
            with col4:
                st.metric("⏳ Karens", doc.get("karens", "saknas"))
            with col5:
                st.metric("📆 Ansvarstid", doc.get("ansvarstid", "saknas"))

            st.divider()
            st.write("📊 Fullständig data:")
            st.json(doc)

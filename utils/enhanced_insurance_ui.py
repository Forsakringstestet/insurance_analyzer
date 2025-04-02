import streamlit as st
from typing import Union

def display_pretty_summary(data: Union[list, dict]):
    entries = data if isinstance(data, list) else [data]

    for entry in entries:
        filename = entry.get("filename", "Okänt dokument")
        st.subheader(f"📄 Sammanfattning: {filename}")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 Premie", f"{int(entry.get('premie', 0)):,} kr")
            st.metric("🏢 Byggnad", f"{int(entry.get('byggnad', 0)):,} kr")
            st.metric("📦 Varor", f"{int(entry.get('varor', 0)):,} kr")

        with col2:
            st.metric("⚙️ Maskiner", f"{int(entry.get('maskiner', 0)):,} kr")
            st.metric("📦 Transport", f"{int(entry.get('transport', 0)):,} kr")
            st.metric("🔐 Självrisk", f"{int(entry.get('självrisk', 0)):,} kr")

        with col3:
            st.metric("📄 Produktansvar", f"{int(entry.get('produktansvar', 0)):,} kr")
            st.metric("🛡 Ansvar", f"{int(entry.get('ansvar', 0)):,} kr")
            st.metric("⚖ Rättsskydd", f"{int(entry.get('rättsskydd', 0)):,} kr")

        st.write(f"**Karens:** {entry.get('karens', 'saknas')}")
        st.write(f"**Ansvarstid:** {entry.get('ansvarstid', 'saknas')}")
        st.divider()

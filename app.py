import streamlit as st
import fitz  # PyMuPDF
import os
from parser import pdf_extractor, pdf_analyzer
from utils.visualizer import render_comparison_table
from utils.enhanced_insurance_ui import display_pretty_summary
from openai_advisor import ask_openai, ask_openai_extract
from export.export_excel import export_summary_excel

st.set_page_config(page_title="📊 AI Försäkringsanalys & Offertjämförelse", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .block-container { padding-top: 2rem; }
        .st-bb { background-color: #e3f2fd; border-left: 5px solid #2196f3; padding: 0.5em; }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Jämför & Analysera Försäkringsbrev, Offert & Villkor")
st.caption("AI-driven extraktion & analys av PDF:er inom företagsförsäkring")

industry = st.sidebar.selectbox("Välj bransch:", [
    "Tillverkning", "Bygg & Entreprenad", "IT & Konsult", "Transport & Logistik", "Handel", "Annan"
])

uploaded_files = st.file_uploader("Ladda upp ett eller flera PDF-dokument", type="pdf", accept_multiple_files=True)

analysis_results = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        filename = uploaded_file.name
        st.markdown(f"**🔍 Analys av:** {filename}")

        text = pdf_extractor.extract_text_from_pdf(uploaded_file)
        parser_data = pdf_analyzer.extract_all_insurance_data(text)

        ai_data = ask_openai_extract(text, industry)

        if not ai_data or not isinstance(ai_data, dict):
            st.warning("AI-extraktion misslyckades: Kunde inte tolka JSON")
        else:
            ai_data["score"] = pdf_analyzer.score_document(ai_data)

        combined_data = ai_data if ai_data and ai_data.get("premie") else parser_data
        analysis_results.append({
            "filename": filename,
            "score": ai_data.get("score") if ai_data else 0,
            "data": combined_data
        })

        # AI-rådgivning
        if ai_data and ai_data.get("premie", 0) > 0:
            ai_advice = ask_openai(ai_data, industry)
            with st.expander("🤖 AI-rådgivning"):
                st.markdown(ai_advice)

        # Sammanställning (ny design)
        with st.expander("📊 Sammanfattning & Jämförelse"):
            display_pretty_summary([{
                "filename": filename,
                **combined_data
            }])

        # Visa extraherad text
        with st.expander(f"📄 Visa extraherad text för {filename}"):
            st.code(text)

# Jämförelsetabell
if analysis_results:
    st.subheader("📊 Jämförelsetabell med färgkodning")
    render_comparison_table(analysis_results)

    st.subheader("📥 Exportera resultat")
    export_summary_excel(analysis_results)

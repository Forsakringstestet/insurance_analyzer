import streamlit as st
import os
from parser import pdf_extractor, pdf_analyzer
from ai.openai_advisor import ask_openai, ask_openai_extract
from utils.visualizer import render_comparison_table
from utils.enhanced_insurance_ui import display_pretty_summary, configure_sidebar
from export import export_excel, export_pdf, export_word

# Konfigurera sidopanel
configure_sidebar()

st.set_page_config(
    page_title="Försäkringsanalys",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💼 Jämför & Analysera Försäkringsbrev, Offerter & Villkor")

# Ladda upp PDF-filer
uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer", type="pdf", accept_multiple_files=True)

analysis_results = []

if uploaded_files:
    st.divider()
    st.subheader("📂 Extraktion & AI-analys")

    for file in uploaded_files:
        filename = file.name
        with st.expander(f"Visa extraherad text för {filename}"):
            text = pdf_extractor.extract_text_from_pdf(file)
            st.text_area("Extraherad text", text, height=200)

        # AI-baserad extraktion
        with st.expander(f"🤖 AI-förslag på extraktion från {filename}", expanded=True):
            ai_data = ask_openai_extract(text)
            st.json(ai_data)

        # AI-rekommendationer
        with st.expander(f"💬 AI-rådgivning för {filename}"):
            advice = ask_openai(ai_data)
            st.write(advice)

        # Scoring och sammanställning
        ai_data["filename"] = filename
        ai_data["score"] = pdf_analyzer.score_document(
            ai_data,
            vikt_omfattning=40,
            vikt_premie=30,
            vikt_självrisk=20,
            vikt_övrigt=10,
        )

        analysis_results.append({
            "filename": filename,
            "data": ai_data,
            "score": ai_data["score"]
        })

    # Visa tabeller och sammanställningar
    st.divider()
    st.subheader("📊 Jämförelsetabell med färgkodning")
    render_comparison_table(analysis_results)

    st.divider()
    display_pretty_summary(analysis_results)

    st.subheader("📤 Exportera resultat")
    export_format = st.selectbox("Välj format", ["Excel", "PDF", "Word"])
    if st.button("Exportera resultat"):
        if export_format == "Excel":
            export_excel.export_summary_excel(analysis_results)
        elif export_format == "PDF":
            export_pdf.export_summary_pdf(analysis_results)
        elif export_format == "Word":
            export_word.generate_procurement_word(analysis_results)

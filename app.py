import streamlit as st
import fitz  # PyMuPDF
from parser import pdf_extractor, pdf_analyzer
from ai.openai_advisor import ask_openai, ask_openai_extract
from utils.visualizer import render_comparison_table
from utils.enhanced_insurance_ui import display_pretty_summary
from export.export_excel import export_summary_excel

st.set_page_config(
    page_title="Försäkringsanalys AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Jämför & Analysera Försäkringsbrev, Offert & Villkor")
st.caption("Ladda upp dina PDF:er nedan för att analysera premie, omfattning, självrisk m.m.")

# Branschval i sidopanelen
industry = st.sidebar.selectbox("🔧 Välj bransch för AI-rådgivning", [
    "Tillverkning", "IT & Tech", "Bygg & Fastighet", "Handel", "Konsultverksamhet", "Transport", "Övrigt"]
)

uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer", type="pdf", accept_multiple_files=True)

analysis_results = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown(f"#### 🧾 Analys av: {uploaded_file.name}")

        # 1. Läs PDF
        text = pdf_extractor.extract_text_from_pdf(uploaded_file)

        # 2. AI-baserad dataextraktion
        ai_data = ask_openai_extract(text, industry)
        if not ai_data:
            st.warning("AI-extraktion misslyckades: Kunde inte tolka JSON")
            continue

        # 3. Poängsätt dokumentet
        ai_data["score"] = pdf_analyzer.score_document(ai_data)

        # 4. AI-rekommendation
        with st.expander("🤖 AI-rådgivning"):
            st.markdown(ask_openai(ai_data, industry))

        # 5. Spara i lista för summering/jämförelse
        analysis_results.append({
            "filename": uploaded_file.name,
            "score": ai_data["score"],
            "data": ai_data
        })

# 6. Summeringstabell
if analysis_results:
    st.divider()
    st.subheader("📊 Jämförelsetabell med färgkodning")
    render_comparison_table(analysis_results)

    st.subheader("🧮 Sammanställning & Jämförelse")
    display_pretty_summary(analysis_results)

    export_summary_excel(analysis_results)

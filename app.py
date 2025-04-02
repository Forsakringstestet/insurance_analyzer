import streamlit as st
from Parser import pdf_extractor, pdf_analyzer
from ai.openai_advisor import ask_openai, ask_openai_extract
from Export import export_excel
from Utils.visualizer import render_comparison_table
from Utils.enhanced_insurance_ui import display_pretty_summary

st.set_page_config(page_title="AI Försäkringsanalys", layout="wide")

st.sidebar.title("📁 Ladda upp och analysera PDF")
industry = st.sidebar.selectbox("Välj bransch (används för AI-analys)", [
    "Tillverkning", "Bygg", "Konsult", "Transport", "IT", "Detaljhandel", "Annat"
])

st.title("Jämför & Analysera Försäkringsbrev, Offerter & Villkor")

uploaded_files = st.sidebar.file_uploader("Ladda upp en eller flera PDF:er", type=["pdf"], accept_multiple_files=True)
analysis_results = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.expander(f"✏️ Analys av: {uploaded_file.name}", expanded=True):
            text = pdf_extractor.extract_text_from_pdf(uploaded_file)

            ai_data = ask_openai_extract(text, industry)
            if ai_data.get("fel"):
                st.warning(f"AI-extraktion misslyckades: {ai_data['fel']}")
                continue

            ai_data["score"] = pdf_analyzer.score_document(ai_data)

            st.subheader("📊 Sammanfattning")
            display_pretty_summary(ai_data)

            with st.expander("🤖 AI-rådgivning"):
                advice = ask_openai(ai_data, industry)
                st.markdown(advice)

            analysis_results.append({
                "filename": uploaded_file.name,
                "data": ai_data,
                "score": ai_data["score"]
            })

    st.divider()
    st.subheader(":bar_chart: Jämförelsetabell med färgkodning")
    render_comparison_table(analysis_results)

    st.subheader(":scroll: Sammanställning & Jämförelse")
    display_pretty_summary(analysis_results)

    st.markdown("### 📥 Exportera resultat")
    excel_data = export_excel.export_summary_excel(analysis_results)
    if excel_data:
        st.download_button(
            label="📅 Ladda ner Excel-fil",
            data=excel_data,
            file_name="forsakringsanalys.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("📂 Vänligen ladda upp en eller flera försäkrings-PDF:er i sidopanelen för att starta analysen.")

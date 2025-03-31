import streamlit as st
import pandas as pd
from parser.pdf_extractor import extract_text_from_pdf
from parser.pdf_analyzer import extract_total_premium, extract_deductible, extract_property_insurance, extract_liability_limits, extract_interruption_info
from parser.scoring import score_document
from ai.openai_advisor import ask_openai
from utils.visualizer import display_results
from export.export_pdf import export_summary_pdf
from export.export_excel import export_summary_excel
from export.export_word import generate_procurement_word

st.set_page_config(page_title="Försäkringsanalys", layout="wide")
st.title("📄 Jämför & Analysera Försäkringsbrev, Offerter & Villkor")

uploaded_files = st.file_uploader("Ladda upp flera PDF-filer för jämförelse", type="pdf", accept_multiple_files=True)

if not uploaded_files:
    st.warning("⚠️ Du måste ladda upp minst ett PDF-dokument.")
    st.stop()

weight_scope = st.slider("Vikt: Omfattning", 0, 100, 40)
weight_cost = st.slider("Vikt: Premie", 0, 100, 30)
weight_deductible = st.slider("Vikt: Självrisk", 0, 100, 20)
weight_other = st.slider("Vikt: Övrigt", 0, 100, 10)

industry = st.text_input("Ange bransch (t.ex. bygg, IT, vård)", value="bygg")
analysis_results = []

for file in uploaded_files:
    raw_text = extract_text_from_pdf(file)

    # Ny avancerad extraktion
    premie = extract_total_premium(raw_text)
    sjalvrisk = extract_deductible(raw_text)
    egendom = dict(extract_property_insurance(raw_text))
    ansvar = dict(extract_liability_limits(raw_text))
    avbrott = extract_interruption_info(raw_text)

    # Packa till enhetlig data
    data = {
        "premie": float(premie.replace(" ", "").replace(",", ".")) if premie else 0.0,
        "självrisk": sjalvrisk,
        "belopp": egendom.get("maskiner", 0),
        "egendom": egendom,
        "ansvar": ansvar,
        **avbrott
    }

    score = score_document(data, weight_scope, weight_cost, weight_deductible, weight_other)

    try:
        recommendation = ask_openai(data, industry=industry)
    except Exception as e:
        recommendation = f"Kunde inte hämta AI-rekommendation: {e}"

    analysis_results.append({
        "filename": file.name,
        "data": data,
        "score": score,
        "recommendation": recommendation
    })

display_results(analysis_results)

with st.expander("📘 AI Rekommendationer per Dokument"):
    for r in analysis_results:
        st.markdown(f"### {r['filename']}")
        st.markdown(r["recommendation"])

st.subheader("📤 Exportera resultat")
if analysis_results:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Exportera till PDF"):
            export_summary_pdf(analysis_results)
    with col2:
        if st.button("Exportera till Excel"):
            export_summary_excel(analysis_results)
    with col3:
        if st.button("Exportera till Word"):
            generate_procurement_word(analysis_results)
else:
    st.info("Inga resultat att exportera.")

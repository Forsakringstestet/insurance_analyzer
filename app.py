import streamlit as st
from parser.pdf_extractor import extract_text_from_pdf
from parser.nlp_analyzer import extract_insurance_data
from parser.scoring import score_document
from ai.recommender import generate_recommendation
from utils.visualizer import display_results
from export.export_pdf import export_summary_pdf
from export.export_excel import export_summary_excel
from export.export_word import export_summary_word

st.set_page_config(page_title="Försäkringsanalys", layout="wide")

st.title("📄 Försäkringsbrev- & Villkorsanalys")

uploaded_files = st.file_uploader("Ladda upp PDF-filer", type="pdf", accept_multiple_files=True)

if uploaded_files:
    weight_scope = st.slider("Vikt: Omfattning", 0, 100, 40)
    weight_cost = st.slider("Vikt: Premie", 0, 100, 30)
    weight_deductible = st.slider("Vikt: Självrisk", 0, 100, 20)
    weight_other = st.slider("Vikt: Övrigt", 0, 100, 10)

    analysis_results = []

    for file in uploaded_files:
        raw_text = extract_text_from_pdf(file)
        data = extract_insurance_data(raw_text)
        score = score_document(data, weight_scope, weight_cost, weight_deductible, weight_other)
        recommendation = generate_recommendation(data)
        result = {
            "filename": file.name,
            "data": data,
            "score": score,
            "recommendation": recommendation
        }
        analysis_results.append(result)

    display_results(analysis_results)

    st.subheader("📤 Exportera resultat")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Exportera till PDF"):
            export_summary_pdf(analysis_results)
    with col2:
        if st.button("Exportera till Excel"):
            export_summary_excel(analysis_results)
    with col3:
        if st.button("Exportera till Word"):
            export_summary_word(analysis_results)

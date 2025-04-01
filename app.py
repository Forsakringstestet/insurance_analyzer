import streamlit as st
import fitz
import pandas as pd
from ai.recommender import generate_recommendation
from ai.openai_advisor import ask_openai, ask_openai_extract
from parser import pdf_analyzer, scoring, pdf_extractor
from utils import comparison, visualizer
from export import export_excel, export_pdf, export_word

st.set_page_config(layout="wide")
st.title("📄 Jämför & Analysera Försäkringsbrev, Offerter & Villkor")

uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer", type=["pdf"], accept_multiple_files=True)

weight_scope = st.slider("Vikt: Omfattning", 0, 100, 40)
weight_cost = st.slider("Vikt: Premie", 0, 100, 30)
weight_deductible = st.slider("Vikt: Självrisk", 0, 100, 20)
weight_other = st.slider("Vikt: Övrigt (karens/ansvarstid)", 0, 100, 10)
industry = st.text_input("Ange bransch (t.ex. bygg, IT, vård)", "Ingenjörsfirma")

analysis_results = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f"🔍 Analyserar {uploaded_file.name}..."):
            text = pdf_extractor.extract_text_from_pdf(uploaded_file)
            parser_data = pdf_analyzer.extract_all_insurance_data(text)

            with st.expander(f"📄 Visa extraherad text för {uploaded_file.name}"):
                st.code(text)

            with st.expander(f"🔎 Parser-data för {uploaded_file.name}", expanded=False):
                st.json(parser_data)

            ai_data = ask_openai_extract(text)
            with st.expander(f"🤖 AI-förslag på extraktion från {uploaded_file.name}", expanded=True):
                st.json(ai_data)

            # Välj AI-data om den innehåller fler icke-nollvärden än parser-datan
            parser_non_zero = sum(1 for k, v in parser_data.items() if isinstance(v, (int, float)) and v > 0)
            ai_non_zero = sum(1 for k, v in ai_data.items() if isinstance(v, (int, float)) and v > 0)
            final_data = ai_data if ai_non_zero >= parser_non_zero else parser_data

            score = scoring.score_document(
                final_data,
                weight_scope / 100,
                weight_cost / 100,
                weight_deductible / 100,
                weight_other / 100
            )

            result = {
                "filename": uploaded_file.name,
                "data": final_data,
                "score": score
            }
            analysis_results.append(result)

            with st.expander(f"📌 AI-rådgivning för {uploaded_file.name}"):
                ai_advice = ask_openai(final_data, industry)
                st.markdown(ai_advice)

            with st.expander(f"📌 Enkel rekommendation för {uploaded_file.name}"):
                simple_rec = generate_recommendation(final_data)
                st.markdown(simple_rec)

if analysis_results:
    visualizer.display_results(analysis_results)
    comparison.render_comparison_table(analysis_results)

    with st.expander("📤 Exportera resultat"):
        col1, col2, col3 = st.columns(3)
        with col1:
            export_pdf.export_summary_pdf(analysis_results)
        with col2:
            export_excel.export_summary_excel(analysis_results)
        with col3:
            export_word.generate_procurement_word(analysis_results)

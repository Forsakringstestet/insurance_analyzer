import streamlit as st
from parser import pdf_extractor, pdf_analyzer
from ai.openai_advisor import ask_openai, ask_openai_extract
from recommender import generate_recommendation
from export import export_excel, export_pdf, export_word
from utils import comparison, visualizer

st.set_page_config(page_title="Försäkringsanalys AI", layout="wide")
st.title("📄 Jämför & Analysera Försäkringsbrev, Offerter & Villkor")

uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer", type=["pdf"], accept_multiple_files=True)

weight_scope = st.slider("Vikt: Omfattning", 0, 100, 40)
weight_cost = st.slider("Vikt: Premie", 0, 100, 30)
weight_deductible = st.slider("Vikt: Självrisk", 0, 100, 20)
weight_other = st.slider("Vikt: Övrigt (karens/ansvarstid)", 0, 100, 10)
industry = st.text_input("Ange bransch (t.ex. bygg, IT, vård)", "Ingenjörsfirma")

results = []

if uploaded_files:
    for file in uploaded_files:
        with st.expander(f"📄 Visa extraherad text för {file.name}"):
            text = pdf_extractor.extract_text_from_pdf(file)
            st.text_area("Extraherad text", text, height=200)

        parser_data = pdf_analyzer.extract_all_insurance_data(text)

        with st.expander(f"🧠 AI-förslag på extraktion från {file.name}"):
            ai_data = ask_openai_extract(text)
            st.json(ai_data)

        data = ai_data if ai_data.get("premie", 0) > 0 else parser_data

        with st.expander(f"🧾 Parser-data för {file.name}"):
            st.json(parser_data)

        with st.expander(f"💬 AI-rådgivning för {file.name}"):
            advice = ask_openai(data, industry)
            st.markdown(advice)

        results.append({
            "filename": file.name,
            "data": data,
            "score": data.get("score", 0)
        })

if results:
    visualizer.display_results(results)
    comparison.render_comparison_table(results)

    st.subheader("📤 Exportera resultat")
    col1, col2, col3 = st.columns(3)
    with col1:
        export_pdf.export_summary_pdf(results)
    with col2:
        export_excel.export_summary_excel(results)
    with col3:
        export_word.generate_procurement_word(results)

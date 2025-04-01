import streamlit as st
from ai.openai_advisor import ask_openai, ask_openai_extract
from recommender import generate_recommendation
from export import export_excel, export_pdf, export_word
from utils import comparison, visualizer
from parser import pdf_extractor, scoring

st.set_page_config(page_title="AI Försäkringsanalys", layout="wide")
st.title("🤖 Jämför & Analysera Försäkringsbrev, Offerter & Villkor")

uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    weight_scope = st.slider("Vikt: Omfattning", 0, 100, 40)
    weight_premium = st.slider("Vikt: Premie", 0, 100, 30)
    weight_deductible = st.slider("Vikt: Självrisk", 0, 100, 20)
    weight_other = st.slider("Vikt: Övrigt (karens/ansvarstid)", 0, 100, 10)

    industry = st.text_input("Ange bransch (t.ex. bygg, IT, vård)", "")

    analysis_results = []

    for file in uploaded_files:
        with st.expander(f"📄 Visa extraherad text för {file.name}"):
            raw_text = pdf_extractor.extract_text_from_pdf(file)
            st.text_area("Extraherad text", raw_text, height=200)

        # 🔍 AI-baserad extraktion
        ai_data = ask_openai_extract(raw_text)
        score = scoring.score_document(ai_data, weight_scope, weight_premium, weight_deductible, weight_other)
        ai_data["score"] = score

        # 🔮 AI-rekommendation
        ai_comment = ask_openai(ai_data, industry)

        with st.expander(f"🤖 AI-förslag på extraktion från {file.name}"):
            st.json(ai_data)

        with st.expander(f"🧠 AI-rådgivning för {file.name}"):
            st.markdown(ai_comment)

        analysis_results.append({
            "filename": file.name,
            "data": ai_data,
            "score": score
        })

    # 📊 Jämförelse & Visualisering
    comparison.render_comparison_table(analysis_results)
    visualizer.display_results(analysis_results)

    # 💾 Export
    st.markdown("---")
    export_format = st.selectbox("📤 Exportera resultat", ["PDF", "Excel", "Word"])
    if export_format == "Excel":
        export_excel.export_summary_excel(analysis_results)
    elif export_format == "PDF":
        export_pdf.export_summary_pdf(analysis_results)
    elif export_format == "Word":
        export_word.generate_procurement_word(analysis_results)

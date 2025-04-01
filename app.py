import streamlit as st
from parser import pdf_extractor
from ai.openai_advisor import ask_openai, ask_openai_extract
from ai.recommender import generate_recommendation
from export import export_excel, export_pdf, export_word
from utils import comparison, visualizer

st.set_page_config(page_title="AI-försäkringsanalys", layout="wide")

st.title("Jämför & Analysera Försäkringsbrev, Offerter & Villkor")

uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer", type=["pdf"], accept_multiple_files=True)

industry = st.text_input("Ange bransch (t.ex. bygg, IT, vård)", "Ingenjörsfirma")

weight_scope = st.slider("Vikt: Omfattning", 0, 100, 40)
weight_cost = st.slider("Vikt: Premie", 0, 100, 30)
weight_deductible = st.slider("Vikt: Självrisk", 0, 100, 20)
weight_other = st.slider("Vikt: Övrigt (karens/ansvarstid)", 0, 100, 10)

analysis_results = []

if uploaded_files:
    for file in uploaded_files:
        text = pdf_extractor.extract_text_from_pdf(file)

        ai_data = ask_openai_extract(text)

        score = (
            weight_scope * (
                ai_data.get("maskiner", 0) +
                ai_data.get("varor", 0) +
                ai_data.get("byggnad", 0) +
                ai_data.get("transport", 0) +
                ai_data.get("produktansvar", 0) +
                ai_data.get("ansvar", 0) +
                ai_data.get("rättsskydd", 0) +
                ai_data.get("gdpr_ansvar", 0)
            )
            - weight_cost * ai_data.get("premie", 0)
            - weight_deductible * ai_data.get("självrisk", 0)
            + weight_other * 1000
        )
        ai_data["score"] = round(score, 2)

        recommendation = ask_openai(ai_data, industry)
        simple_recommendation = generate_recommendation(ai_data)

        result = {
            "filename": file.name,
            "text": text,
            "data": ai_data,
            "score": ai_data["score"],
            "recommendation": recommendation,
            "simple_recommendation": simple_recommendation
        }
        analysis_results.append(result)

    st.subheader("💡 AI-rådgivning per Dokument")
    for r in analysis_results:
        with st.expander(f"AI-rådgivning för {r['filename']}"):
            st.markdown(r["recommendation"])

    comparison.render_comparison_table(analysis_results)
    visualizer.display_results(analysis_results)

    with st.expander("⬇️ Exportera resultat"):
        export_format = st.selectbox("Välj exportformat", ["Excel", "PDF", "Word"])
        if st.button("Exportera sammanställning"):
            if export_format == "Excel":
                export_excel.export_summary_excel(analysis_results)
            elif export_format == "PDF":
                export_pdf.export_summary_pdf(analysis_results)
            elif export_format == "Word":
                export_word.generate_procurement_word(analysis_results)

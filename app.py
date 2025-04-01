import streamlit as st
from parser import pdf_extractor, pdf_analyzer, scoring
from ai.openai_advisor import ask_openai, ask_openai_extract
from recommender import generate_recommendation
from export import export_excel, export_pdf, export_word
from utils import comparison, visualizer

def app():
    st.title("🌐 Jämför & Analysera Försäkringsbrev, Offerter & Villkor")
    st.markdown("Ladda upp en eller flera PDF-filer")

    uploaded_files = st.file_uploader("", type=["pdf"], accept_multiple_files=True)
    industry = st.text_input("Ange bransch (t.ex. bygg, IT, vård)", "")

    # Vikter för poängsberäkning
    weight_scope = st.slider("Vikt: Omfattning", 0, 100, 40)
    weight_cost = st.slider("Vikt: Premie", 0, 100, 30)
    weight_deductible = st.slider("Vikt: Självrisk", 0, 100, 20)
    weight_other = st.slider("Vikt: Övrigt (karens/ansvarstid)", 0, 100, 10)

    results = []

    if uploaded_files:
        for file in uploaded_files:
            with st.spinner(f"Analyserar {file.name}..."):
                text = pdf_extractor.extract_text_from_pdf(file)

                # Extraktion
                ai_data = ask_openai_extract(text)
                fallback_data = pdf_analyzer.extract_all_insurance_data(text)

                # Välj AI-data om den verkar ha korrekt premie etc
                insurance_data = ai_data if ai_data.get("premie", 0) > 0 else fallback_data

                # Räkna poäng
                score = scoring.score_document(insurance_data, weight_scope, weight_cost, weight_deductible, weight_other)

                # AI-rådgivning (baserad på den data vi valde)
                recommendation = ask_openai(insurance_data, industry)
                simple_rec = generate_recommendation(insurance_data)

                # Visa resultat per fil
                with st.expander(f"📄 Parser-data för {file.name}", expanded=False):
                    st.json(fallback_data)

                with st.expander(f"🤖 AI-extraktion från {file.name}", expanded=True):
                    st.json(ai_data)

                with st.expander(f"💡 AI-rådgivning för {file.name}", expanded=True):
                    st.markdown(recommendation)
                    st.markdown(f"**Enkel rekommendation:** {simple_rec}")

                results.append({
                    "filename": file.name,
                    "data": insurance_data,
                    "score": score
                })

        # Jämförelse & visualisering
        visualizer.display_results(results)
        comparison.render_comparison_table(results)

        # Export
        with st.expander("📆 Exportera resultat"):
            col1, col2, col3 = st.columns(3)
            with col1: export_pdf.export_summary_pdf(results)
            with col2: export_excel.export_summary_excel(results)
            with col3: export_word.generate_procurement_word(results)

if __name__ == "__main__":
    app()

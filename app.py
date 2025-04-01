import streamlit as st
from parser import pdf_extractor, pdf_analyzer, scoring
from ai.openai_advisor import ask_openai, ask_openai_extract
from recommender import generate_recommendation
from export import export_excel, export_pdf, export_word
from utils import comparison, visualizer
from utils.enhanced_insurance_ui import display_pretty_summary

def app():
    st.set_page_config(page_title="Försäkringsanalys", layout="wide")
    st.title("📄 Jämför & Analysera Försäkringsbrev, Offert & Villkor")

    uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer", type=["pdf"], accept_multiple_files=True)
    industry = st.text_input("Ange bransch (t.ex. bygg, IT, vård)", "Ingenjörsfirma")

    # Vikter
    vikt_scope = st.slider("Vikt: Omfattning", 0, 100, 40) / 100
    vikt_cost = st.slider("Vikt: Premie", 0, 100, 30) / 100
    vikt_deductible = st.slider("Vikt: Självrisk", 0, 100, 20) / 100
    vikt_other = st.slider("Vikt: Övrigt (karens/ansvarstid)", 0, 100, 10) / 100

    if uploaded_files:
        analysis_results = []

        for file in uploaded_files:
            text = pdf_extractor.extract_text_from_pdf(file)
            with st.expander(f"Visa extraherad text för {file.name}"):
                st.text_area("Extraherad text", text, height=200)

            # Försök med parser (fallback)
            parsed_data = pdf_analyzer.extract_all_insurance_data(text)

            # Testa AI-extraktion
            ai_data = ask_openai_extract(text)
            if ai_data.get("fel"):
                st.warning(f"⚠️ AI-extraktion misslyckades: {ai_data['fel']}")
                data_to_use = parsed_data
            else:
                data_to_use = ai_data

            score = scoring.score_document(data_to_use, vikt_scope, vikt_cost, vikt_deductible, vikt_other)
            data_to_use["score"] = score

            analysis_results.append({
                "filename": file.name,
                "data": data_to_use,
                "score": score
            })

            # Visa AI-analys
            ai_rek = ask_openai(data_to_use, industry)
            with st.expander(f"🤖 AI-rådgivning för {file.name}"):
                st.markdown(ai_rek)

            # Visa branschspecifik regelbaserad rekommendation
            with st.expander(f"📌 Enkel regelbaserad rekommendation för {file.name}"):
                st.write(generate_recommendation(data_to_use))

        # Visuellt
        comparison.render_comparison_table(analysis_results)
        visualizer.display_results(analysis_results)
        display_pretty_summary(analysis_results)

        # Export
        with st.expander("📤 Exportera resultat"):
            export_format = st.selectbox("Välj format", ["PDF", "Excel", "Word"])
            if st.button("Exportera sammanställning"):
                if export_format == "PDF":
                    export_pdf.export_summary_pdf(analysis_results)
                elif export_format == "Excel":
                    export_excel.export_summary_excel(analysis_results)
                elif export_format == "Word":
                    export_word.generate_procurement_word(analysis_results)

if __name__ == "__main__":
    app()

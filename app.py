import streamlit as st
from parser import pdf_extractor, pdf_analyzer, scoring
from ai.openai_advisor import ask_openai, ask_openai_extract
from export import export_excel, export_pdf, export_word
from utils import comparison, visualizer, enhanced_insurance_ui

st.set_page_config(
    page_title="RiskRadar – AI-försäkringsanalys",
    page_icon="📄",
    layout="wide"
)

def app():
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/OpenAI_Logo.svg/512px-OpenAI_Logo.svg.png", width=150)
    st.sidebar.title("🧠 AI-rådgivare")
    st.sidebar.info("Ladda upp en eller flera PDF:er med försäkringsdokument för att analysera och jämföra erbjudanden.")

    st.title("📘 Jämför & Analysera Försäkringsbrev, Offerter & Villkor")

    uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer", type=["pdf"], accept_multiple_files=True)

    if not uploaded_files:
        st.warning("⬆️ Vänligen ladda upp minst en PDF.")
        return

    weight_omfattning = st.slider("Vikt: Omfattning", 0, 100, 40)
    weight_premie = st.slider("Vikt: Premie", 0, 100, 30)
    weight_sjalvrisk = st.slider("Vikt: Självrisk", 0, 100, 20)
    weight_ovrigt = st.slider("Vikt: Övrigt (karens/ansvarstid)", 0, 100, 10)
    industry = st.text_input("Ange bransch (t.ex. bygg, IT, vård)", "Ingenjörsfirma")

    analysis_results = []

    for uploaded_file in uploaded_files:
        with st.expander(f"🔍 AI-rådgivning för {uploaded_file.name}", expanded=False):
            text = pdf_extractor.extract_text_from_pdf(uploaded_file)

            # 🔎 AI-driven extraktion istället för parser
            ai_data = ask_openai_extract(text)

            if "fel" in ai_data:
                st.warning(f"⚠️ AI-extraktion misslyckades: {ai_data['fel']}")
                continue

            ai_data["score"] = scoring.score_document(
                ai_data,
                weight_omfattning,
                weight_premie,
                weight_sjalvrisk,
                weight_ovrigt
            )

            analysis_results.append({
                "filename": uploaded_file.name,
                "data": ai_data,
                "score": ai_data["score"]
            })

            # AI-rådgivning
            ai_rek = ask_openai(ai_data, industry)
            st.markdown("#### 💬 AI-rådgivning")
            st.info(ai_rek)

    if analysis_results:
        enhanced_insurance_ui.display_pretty_summary(analysis_results)
        visualizer.display_results(analysis_results)
        comparison.render_comparison_table(analysis_results)

        st.download_button("📥 Exportera till Excel", data=export_excel.export_summary_excel(analysis_results), file_name="analys.xlsx")

if __name__ == "__main__":
    app()

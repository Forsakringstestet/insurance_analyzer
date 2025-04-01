# 📘 app.py – huvudfilen för din finans-inriktade försäkringsapp
import streamlit as st
from parser import pdf_extractor, pdf_analyzer
from ai.openai_advisor import ask_openai, ask_openai_extract
from export import export_excel, export_pdf, export_word
from utils.comparison import render_comparison_table
from utils.visualizer import display_results
from utils.enhanced_insurance_ui import display_pretty_summary
import base64

st.set_page_config(page_title="RiskRadar AI", page_icon="📘", layout="wide")

# 📘 Sidopanel: Appinformation
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Finance_icon.svg/768px-Finance_icon.svg.png", width=60)
    st.title("RiskRadar AI")
    st.caption("AI-stödd jämförelse av försäkringsbrev")
    st.markdown("""
    **Version:** 1.1.0  
    **Utvecklare:** Forsakringstestet  
    [GitHub-repo](https://github.com/Forsakringstestet/insurance_analyzer)
    """)

# 📘 Huvudrubrik
st.markdown("""
<style>
    h1 {color: #003366; font-size: 36px; margin-bottom: 10px;}
    .st-emotion-cache-1v0mbdj {background-color: #f0f6ff !important; padding: 1rem; border-radius: 0.5rem;}
</style>
<h1>📊 Jämför & Analysera Försäkringsbrev, Offerter & Villkor</h1>
""", unsafe_allow_html=True)

# 📁 Filuppladdning
uploaded_files = st.file_uploader("**Ladda upp en eller flera PDF:er** (t.ex. offert eller försäkringsbrev)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    industry = st.text_input("📁 Ange bransch (ex: bygg, IT, tillverkning)", "Ingenjörsfirma")

    with st.expander("⚙️ Vikter för poängsättning", expanded=False):
        weight_coverage = st.slider("Vikt: Omfattning", 0, 100, 40)
        weight_premium = st.slider("Vikt: Premie", 0, 100, 30)
        weight_deductible = st.slider("Vikt: Självrisk", 0, 100, 20)
        weight_other = st.slider("Vikt: Övrigt (karens/ansvarstid)", 0, 100, 10)

    analysis_results = []

    for file in uploaded_files:
        text = pdf_extractor.extract_text_from_pdf(file)
        st.expander(f"📝 Visa extraherad text för {file.name}", expanded=False).write(text)

        # AI-baserad extraktion
        ai_data = ask_openai_extract(text)
        if "fel" in ai_data:
            st.warning(f"⚠️ AI-extraktion misslyckades: {ai_data['fel']}")
            continue

        ai_data["score"] = pdf_analyzer.score_document(
            ai_data, weight_coverage, weight_premium, weight_deductible, weight_other
        )
        analysis_results.append({"filename": file.name, "data": ai_data, "score": ai_data["score"]})

        with st.expander(f"💡 AI-rådgivning för {file.name}"):
            st.markdown(ask_openai(ai_data, industry))

    # ✅ Visa resultatsammanfattning
    st.markdown("## 📘 Sammanfattning")
    display_pretty_summary(analysis_results)

    # ✅ Visa jämförelsetabeller
    render_comparison_table(analysis_results)
    display_results(analysis_results)

    # ✅ Exportera
    st.markdown("## 📦 Exportera resultat")
    export_format = st.selectbox("Välj format", ["Excel", "PDF", "Word"])
    if st.button("💾 Exportera till fil"):
        if export_format == "Excel":
            export_excel.export_summary_excel(analysis_results)
        elif export_format == "PDF":
            export_pdf.export_summary_pdf(analysis_results)
        elif export_format == "Word":
            export_word.generate_procurement_word(analysis_results)

else:
    st.info("Ladda upp minst en PDF för att komma igång med analysen.")

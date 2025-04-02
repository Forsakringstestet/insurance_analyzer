import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.let_it_rain import rain
from parser import pdf_extractor, pdf_analyzer
from openai_advisor import ask_openai, ask_openai_extract

# ----------------- UI STYLING -----------------
st.set_page_config(
    page_title="Insurelytics AI",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #f9fafb;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }
    .upload-box {
        border: 2px dashed #60a5fa;
        border-radius: 1rem;
        padding: 2rem;
        background-color: #eff6ff;
        text-align: center;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-top: 2rem;
        color: #1e3a8a;
    }
    .metric-card > div {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 1rem !important;
        padding: 1rem !important;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
st.sidebar.image("https://img.icons8.com/fluency/96/ai.png", width=60)
st.sidebar.markdown("## Insurelytics AI")
st.sidebar.markdown("Smarta jämförelser och rådgivning för företagsförsäkring")
industry = st.sidebar.selectbox("📌 Välj din bransch:", [
    "Tillverkning", "Bygg & Entreprenad", "IT & Konsult", "Transport", "Handel", "Annat"])

st.sidebar.markdown("---")
st.sidebar.markdown("""⚙️ **Version:** 1.0.0  
💡 Utvecklad för försäkringsmäklare och bolag  
📞 support@insurelytics.se
""")

# ----------------- HERO HEADER -----------------
colored_header(
    label="Jämför & Analysera Försäkringsbrev med AI",
    description="Ladda upp dina PDF:er för att få en datadriven översikt och rekommendationer",
    color_name="blue-70"
)

# ----------------- FILE UPLOAD -----------------
st.markdown('<div class="upload-box">\n📄 <strong>Släpp dina försäkringsbrev här</strong><br>eller klicka för att välja PDF:er\n</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

analysis_results = []

if uploaded_files:
    for file in uploaded_files:
        st.markdown(f"### 🧾 Analys av: {file.name}")

        # 1. Extrahera text från PDF
        text = pdf_extractor.extract_text_from_pdf(file)

        # 2. Anropa AI-extraktion
        ai_data = ask_openai_extract(text, industry)
        if not ai_data:
            st.warning("AI-extraktion misslyckades: JSON kunde inte tolkas korrekt.")
            continue

        # 3. Räkna ut score
        ai_data["score"] = pdf_analyzer.score_document(ai_data)

        # 4. Visa sammanfattning
        st.markdown("#### 📊 Sammanfattning")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Premie", f"{ai_data.get('premie', 0):,.0f} kr")
        col2.metric("🛠 Maskiner", f"{ai_data.get('maskiner', 0):,.0f} kr")
        col3.metric("🚚 Transport", f"{ai_data.get('transport', 0):,.0f} kr")
        col4.metric("🧾 Produktansvar", f"{ai_data.get('produktansvar', 0):,.0f} kr")

        style_metric_cards()

        # 5. Visa AI-råd
        st.markdown("#### 🤖 AI-rådgivning")
        st.success(ask_openai(ai_data, industry))

        # 6. Lagra för jämförelsetabell
        analysis_results.append({
            "filename": file.name,
            "data": ai_data,
            "score": ai_data["score"]
        })

    # ----------------- COMPARISON TABLE -----------------
    st.markdown("<div class='section-title'>📊 Jämförelsetabell</div>", unsafe_allow_html=True)
    df = pd.DataFrame([{ "Filnamn": r["filename"], **r["data"] } for r in analysis_results])
    st.dataframe(df, use_container_width=True, height=240)
else:
    rain(
        emoji="📄",
        font_size=25,
        falling_speed=3,
        animation_length="infinite"
    )

# ----------------- LOGOTYPIDÉ -----------------
st.markdown("""<br><br><center>
<img src="https://img.icons8.com/fluency/96/graph-report.png" width="50" />
<h4 style='margin-top: 0;'>Insurelytics AI</h4>
<span style='color:gray'>Datadriven analys av försäkringsdokument</span>
</center><br><br>""", unsafe_allow_html=True)

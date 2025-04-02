import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header

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
    .element-container .stMetric {
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

if uploaded_files:
    for file in uploaded_files:
        st.markdown(f"### 🧾 Analys av: {file.name}")

        # Placeholder: Resultat från AI och parser
        st.markdown("#### 📊 Sammanfattning")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Premie", "15 423 kr")
        col2.metric("🛠 Maskiner", "700 000 kr")
        col3.metric("🚚 Transport", "100 000 kr")
        col4.metric("🧾 Produktansvar", "10 000 000 kr")

        st.markdown("#### 🤖 AI-rådgivning")
        st.success("1. Inget kostnad för premie eller självrisk.\n\n2. Tydligt produktansvar för industrin.\n\n3. Kan förbättra egendomsskyddet.")

    # ----------------- COMPARISON TABLE -----------------
st.markdown("<div class='section-title'>📊 Jämförelsetabell</div>", unsafe_allow_html=True)

# Dynamisk placeholder-tabell med samma längd som antal uppladdade filer
placeholder_data = []
for f in uploaded_files:
    placeholder_data.append({
        "Filnamn": f.name,
        "Premie": 0,
        "Maskiner": 0,
        "Transport": 0,
        "Produktansvar": 0
    })

df = pd.DataFrame(placeholder_data)
st.dataframe(df, use_container_width=True, height=200)


# ----------------- LOGOTYPIDÉ -----------------
st.markdown("""<br><br><center>
<img src="https://img.icons8.com/fluency/96/graph-report.png" width="50" />
<h4 style='margin-top: 0;'>Insurelytics AI</h4>
<span style='color:gray'>Datadriven analys av försäkringsdokument</span>
</center><br><br>""", unsafe_allow_html=True)

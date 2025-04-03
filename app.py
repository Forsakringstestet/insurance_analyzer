import streamlit as st
import pandas as pd
import re

# Imports
from parser.pdf_extractor import extract_text_from_pdf
from parser.pdf_analyzer import extract_all_insurance_data  # fallback
from parser.scoring import score_document
from ai.openai_advisor import ask_openai_extract, ask_openai
from ai.recommender import generate_recommendation
from export.export_excel import export_summary_excel
from export.export_pdf import export_summary_pdf

# Page setup
st.set_page_config(page_title="Försäkringsanalys", page_icon="🛡️", layout="wide")
ACCENT_COLOR = "#2563EB"

# Sidebar
st.sidebar.header("Inställningar")
industry_options = [
    "Ej valt", "Handel", "Industri", "IT", "Bygg", "Transport",
    "Konsult", "Fastighet", "Offentlig sektor", "Annat"
]
selected_industry = st.sidebar.selectbox("Välj bransch för analysen:", industry_options)

st.title("Försäkringsanalys med AI")
st.write("Ladda upp dina försäkringsdokument (PDF) för att få en AI-driven analys, sammanfattning och rekommendationer.")

# File upload
uploaded_files = st.file_uploader(
    "📄 Välj en eller flera PDF-filer att analysera", type=["pdf"], accept_multiple_files=True
)

all_data = []

if uploaded_files:
    for file in uploaded_files:
        st.markdown(f"### 📂 Analys av fil: *{file.name}*")

        try:
            raw_text = extract_text_from_pdf(file)
        except Exception as e:
            st.error(f"❌ Kunde inte läsa PDF-filen *{file.name}*: {e}")
            continue

        if not raw_text.strip():
            st.warning(f"⚠️ Ingen text hittades i *{file.name}*. Hoppar över.")
            continue

        # AI-extraktion eller fallback till parser
        try:
            data = ask_openai_extract(raw_text, selected_industry)
            if not isinstance(data, dict) or not data:
                raise ValueError("Ingen data från AI")
        except Exception as e:
            st.warning(f"⚠️ AI-extraktion misslyckades ({e}), använder fallback-parser.")
            data = extract_all_insurance_data(raw_text)

        # Konvertera numeriska fält
        numeric_fields = [
            "premie", "självrisk", "byggnad", "fastighet", "varor", "maskiner",
            "produktansvar", "rättsskydd", "gdpr_ansvar", "transport"
        ]
        for key in numeric_fields:
            try:
                if key in data and isinstance(data[key], str):
                    val = data[key].lower().replace("kr", "").replace("sek", "").replace(" ", "").replace(".", "").replace(",", ".")
                    match = re.search(r"(\d+(?:\.\d+)?)", val)
                    data[key] = float(match.group(1)) if match else 0.0
                elif key in data:
                    data[key] = float(data[key])
                else:
                    data[key] = 0.0
            except:
                data[key] = 0.0

        # Ansvarstid
        if not str(data.get("ansvarstid", "")).strip():
            data["ansvarstid"] = "saknas"

        # Scoring
        try:
            score = score_document(data, industry=selected_industry)
        except:
            score = 0.0

        all_data.append({"filename": file.name, "data": data, "score": score})

        # Sammanfattning
        st.subheader("📋 Sammanfattning")
        st.markdown(f"**\u00c5rspremie:** {int(data.get('premie', 0)):,} kr".replace(",", " "))
        st.markdown(f"**Självrisk:** {int(data.get('självrisk', 0)):,} kr".replace(",", " "))
        st.markdown(f"**Ansvarstid:** {data.get('ansvarstid', 'saknas')}")

        prop_fields = ["byggnad", "fastighet", "varor", "maskiner"]
        prop_vals = {k: data[k] for k in prop_fields if data.get(k, 0) > 0}
        if prop_vals:
            total = sum(prop_vals.values())
            detail = ", ".join([f"{k.capitalize()}: {int(v):,} kr".replace(",", " ") for k, v in prop_vals.items()])
            st.markdown(f"**Egendomsskydd:** {int(total):,} kr".replace(",", " ") + f" _(fördelat på {detail})_")

        liab_fields = ["produktansvar", "rättsskydd", "gdpr_ansvar"]
        liab_vals = {k: data[k] for k in liab_fields if data.get(k, 0) > 0}
        if liab_vals:
            st.markdown("**Ansvarsskydd:** " + ", ".join([f"{k.capitalize()}: {int(v):,} kr".replace(",", " ") for k, v in liab_vals.items()]))

        st.markdown(f"**Poäng:** {score} / 100")

        # Export
        try:
            excel_bytes = export_summary_excel(data)
            st.download_button("📥 Ladda ner sammanfattning (Excel)", data=excel_bytes, file_name=f"Sammanfattning_{file.name}.xlsx")
        except:
            pass
        try:
            pdf_bytes = export_summary_pdf(data)
            st.download_button("📥 Ladda ner sammanfattning (PDF)", data=pdf_bytes, file_name=f"Sammanfattning_{file.name}.pdf")
        except:
            pass

        # AI-rådgivning
        st.subheader("💡 AI-rådgivning")
        try:
            recs = generate_recommendation(data, selected_industry)
            advice = ask_openai(data, recs, selected_industry)
            st.markdown(advice)
        except Exception as e:
            st.warning(f"⚠️ Kunde inte generera AI-råd: {e}")

# Jämförelsetabell
if all_data:
    st.markdown("---")
    st.subheader("📊 Jämförelsetabell")
    rows = []
    for entry in all_data:
        d = entry["data"]
        rows.append({
            "Filnamn": entry["filename"],
            "Poäng": entry.get("score", 0),
            "Premie": d.get("premie", 0),
            "Självrisk": d.get("självrisk", 0),
            "Maskiner": d.get("maskiner", 0),
            "Transport": d.get("transport", 0),
            "Produktansvar": d.get("produktansvar", 0),
            "Ansvar": d.get("ansvar", 0)
        })

    df = pd.DataFrame(rows)
    st.dataframe(df.style.format("{:.0f}"), use_container_width=True)

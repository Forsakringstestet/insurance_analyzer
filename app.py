import streamlit as st
import pandas as pd
import re

# Import necessary modules from the project
from parser.pdf_extractor import extract_text_from_pdf
from parser.pdf_analyzer import extract_all_insurance_data  # fallback
from parser.scoring import score_document
from ai.openai_advisor import ask_openai_extract, ask_openai
from ai.recommender import generate_recommendation
from export.export_excel import export_summary_excel
from export.export_pdf import export_summary_pdf

st.set_page_config(page_title="Försäkringsanalys", page_icon="🛡️", layout="wide")
ACCENT_COLOR = "#2563EB"

st.sidebar.header("Inställningar")
industry_options = ["Ej valt", "Handel", "Industri", "IT", "Bygg", "Annat"]
selected_industry = st.sidebar.selectbox("Välj bransch för analysen:", industry_options)

st.title("Försäkringsanalys med AI")
st.write("Ladda upp dina försäkringsdokument (PDF) för att få en AI-driven analys, sammanfattning och rekommendationer.")

uploaded_files = st.file_uploader("📄 Välj en eller flera PDF-filer att analysera", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.markdown(f"## 📁 Analys av fil: *{file.name}*")
        try:
            raw_text = extract_text_from_pdf(file)
        except Exception as e:
            st.error(f"❌ Kunde inte läsa PDF-filen *{file.name}*: {e}")
            continue

        if not raw_text or raw_text.strip() == "":
            st.error(f"❌ Ingen läsbar text hittades i *{file.name}*.")
            continue

        try:
            data = ask_openai_extract(raw_text, selected_industry)
        except Exception as e:
            st.warning(f"🔄 AI-extraktion misslyckades, använder parser. ({e})")
            data = extract_all_insurance_data(raw_text)

        numeric_fields = ["premie", "självrisk", "karens", "byggnad", "fastighet", "varor", 
                           "maskiner", "produktansvar", "rättsskydd", "gdpr_ansvar"]
        for key in numeric_fields:
            if key in data and data[key] is not None:
                if isinstance(data[key], str):
                    cleaned = data[key].lower().replace("kr", "").replace("sek", "").replace(" ", "").replace(".", "").replace(",", ".")
                    try:
                        match = re.search(r"(\d+(?:\.\d+)?)", cleaned)
                        data[key] = float(match.group(1)) if match else 0.0
                    except:
                        data[key] = 0.0
                else:
                    try:
                        data[key] = float(data[key])
                    except:
                        data[key] = 0.0

        premium_val = data.get("premie", 0.0) or 0.0
        ansvarstid_val = data.get("ansvarstid", None)
        ansvarstid_missing = (ansvarstid_val is None) or (isinstance(ansvarstid_val, str) and ansvarstid_val.strip() == "")
        if premium_val == 0.0 and ansvarstid_missing:
            st.warning(f"⚠️ Kunde inte hitta premie eller ansvarstid i *{file.name}*. Hoppar över analysen.")
            continue

        try:
            score_val = score_document(data, selected_industry)
        except Exception:
            score_val = None

        st.markdown(f"### <span style='color:{ACCENT_COLOR};'>📋 Sammanfattning</span>", unsafe_allow_html=True)
        if "premie" in data:
            st.write(f"**Årspremie:** {int(premium_val):,} kr".replace(",", " "))
        if "självrisk" in data and data["självrisk"] not in [0, 0.0]:
            st.write(f"**Självrisk:** {int(data['självrisk']):,} kr".replace(",", " "))
        if "ansvarstid" in data and str(data["ansvarstid"]).strip():
            st.write(f"**Ansvarstid:** {data['ansvarstid']}")

        property_fields = ["byggnad", "fastighet", "varor", "maskiner"]
        prop_values = {f: data[f] for f in property_fields if f in data and isinstance(data[f], (int, float)) and data[f] > 0}
        if prop_values:
            total_prop = sum(prop_values.values())
            details = ", ".join([f"{name.capitalize()}: {int(val):,} kr".replace(",", " ") for name, val in prop_values.items()])
            st.write(f"**Summa egendomsskydd:** {int(total_prop):,} kr".replace(",", " ") + f" _(fördelat på {details})_")

        liability_fields = ["produktansvar", "rättsskydd", "gdpr_ansvar"]
        liab_values = {f: data[f] for f in liability_fields if f in data and isinstance(data[f], (int, float)) and data[f] > 0}
        if liab_values:
            details = ", ".join([f"{name.capitalize()}: {int(val):,} kr".replace(",", " ") for name, val in liab_values.items()])
            st.write(f"**Ansvarsskydd:** {details}")

        if score_val is not None:
            st.write(f"**Försäkringsskydd poäng:** {score_val}/100")

        try:
            excel_bytes = export_summary_excel(data)
            st.download_button(label="💾 Ladda ner sammanfattning (Excel)", data=excel_bytes, file_name=f"Analys_{file.name}.xlsx")
        except Exception:
            pass
        try:
            pdf_bytes = export_summary_pdf(data)
            st.download_button(label="💾 Ladda ner sammanfattning (PDF)", data=pdf_bytes, file_name=f"Analys_{file.name}.pdf")
        except Exception:
            pass

        st.markdown(f"### <span style='color:{ACCENT_COLOR};'>📊 Jämförelsetabell</span>", unsafe_allow_html=True)
        try:
            if selected_industry and selected_industry != "Ej valt":
                recommendations = generate_recommendation(data, selected_industry)
            else:
                recommendations = generate_recommendation(data)
        except Exception as e:
            recommendations = None
            st.warning(f"⚠️ Kunde inte generera rekommendationer: {e}")

        if recommendations and isinstance(recommendations, dict):
            compare_fields = list(dict.fromkeys(recommendations.keys()))
            exclude_keys = ["premie", "självrisk", "karens", "ansvarstid"]
            compare_fields = [k for k in compare_fields if k.lower() not in exclude_keys]
            if compare_fields:
                comp_rows = []
                for field in compare_fields:
                    current_val = data.get(field, 0)
                    rec_val = recommendations.get(field, 0)
                    curr_str = f"{int(current_val):,} kr".replace(",", " ") if isinstance(current_val, (int, float)) else str(current_val)
                    rec_str = f"{int(rec_val):,} kr".replace(",", " ") if isinstance(rec_val, (int, float)) else str(rec_val)
                    comp_rows.append({"Försäkringsmoment": field.capitalize(), "Nuvarande": curr_str, "Rekommenderat": rec_str})
                comp_df = pd.DataFrame(comp_rows)
                st.table(comp_df)
            else:
                st.write("*(Inga relevanta försäkringsbelopp att jämföra.)*")
        else:
            st.write("*(Inga rekommendationer tillgängliga för jämförelse.)*")

        st.markdown(f"### <span style='color:{ACCENT_COLOR};'>💡 AI-rådgivning</span>", unsafe_allow_html=True)
        try:
            if recommendations:
                if selected_industry and selected_industry != "Ej valt":
                    advisor_text = ask_openai(data, recommendations, selected_industry)
                else:
                    advisor_text = ask_openai(data, recommendations)
            else:
                if selected_industry and selected_industry != "Ej valt":
                    advisor_text = ask_openai(data, selected_industry)
                else:
                    advisor_text = ask_openai(data)
        except Exception as e:
            advisor_text = None
            st.error(f"❌ Kunde inte generera AI-rådgivning för *{file.name}*: {e}")

        if advisor_text:
            st.write(advisor_text)
        else:
            st.write("*(Ingen AI-rådgivning tillgänglig för detta dokument.)*")

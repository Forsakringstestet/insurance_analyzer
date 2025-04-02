import streamlit as st
import pandas as pd
import re

# Import necessary modules from the project
from parser.pdf_extractor import extract_text_from_pdf
from parser.pdf_analyzer import extract_all_insurance_data  # (May be used as fallback if needed)
from parser.scoring import score_document
from ai.openai_advisor import ask_openai_extract, ask_openai
from ai.recommender import generate_recommendation
from export.export_excel import export_summary_excel
from export.export_pdf import export_summary_pdf

# Page configuration with Tailwind-inspired color and icon
st.set_page_config(page_title="Försäkringsanalys", page_icon="🛡️", layout="wide")
ACCENT_COLOR = "#2563EB"  # Tailwind-inspired accent color (blue-600)

# Sidebar: Industry selection
st.sidebar.header("Inställningar")
industry_options = ["Ej valt", "Handel", "Industri", "IT", "Bygg", "Annat"]
selected_industry = st.sidebar.selectbox("Välj bransch för analysen:", industry_options)

# Main title and description
st.title("Försäkringsanalys med AI")
st.write("Ladda upp dina försäkringsdokument (PDF) för att få en AI-driven analys, sammanfattning och rekommendationer.")

# File uploader (allows multiple PDFs)
uploaded_files = st.file_uploader("📄 Välj en eller flera PDF-filer att analysera", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    # Loop through each uploaded file
    for file in uploaded_files:
        st.markdown(f"## 📁 Analys av fil: *{file.name}*")
        # Extract text from PDF
        try:
            raw_text = extract_text_from_pdf(file)
        except Exception as e:
            st.error(f"❌ Kunde inte läsa PDF-filen *{file.name}*: {e}")
            continue
        if not raw_text or raw_text.strip() == "":
            st.error(f"❌ Ingen läsbar text hittades i *{file.name}*.")
            continue

        # AI-driven data extraction (GPT)
        try:
            data = ask_openai_extract(raw_text)
        except Exception as e:
            st.error(f"❌ AI-driven dataextraktion misslyckades för *{file.name}*: {e}")
            continue
        if not isinstance(data, dict):
            st.error(f"❌ AI-extraktionen returnerade ett oväntat format för *{file.name}*.")
            continue

        # Sanitize and unify data types for numeric fields
        numeric_fields = ["premie", "självrisk", "karens", "byggnad", "fastighet", "varor", 
                           "maskiner", "produktansvar", "rättsskydd", "gdpr_ansvar"]
        for key in numeric_fields:
            if key in data and data[key] is not None:
                if isinstance(data[key], str):
                    # Remove currency symbols and spaces, replace comma with dot for float conversion
                    cleaned = data[key].lower().replace("kr", "").replace("sek", "")
                    cleaned = cleaned.replace(" ", "").replace(".", "").replace(",", ".")
                    try:
                        # Extract first number in the string
                        match = re.search(r"(\d+(?:\.\d+)?)", cleaned)
                        data[key] = float(match.group(1)) if match else 0.0
                    except:
                        data[key] = 0.0
                else:
                    # Ensure numeric values are float
                    try:
                        data[key] = float(data[key])
                    except:
                        data[key] = 0.0

        # Check for extraction success (if premium is 0 and ansvarstid missing, skip analysis)
        premium_val = data.get("premie", 0.0) or 0.0
        ansvarstid_val = data.get("ansvarstid", None)
        ansvarstid_missing = (ansvarstid_val is None) or (isinstance(ansvarstid_val, str) and ansvarstid_val.strip() == "")
        if premium_val == 0.0 and ansvarstid_missing:
            st.warning(f"⚠️ Kunde inte hitta premie eller ansvarstid i *{file.name}*. Hoppar över analysen för detta dokument.")
            continue

        # Calculate an overall score for the document (if applicable)
        try:
            score_val = score_document(data)
        except Exception:
            score_val = None

        # Summary Section
        st.markdown(f"### <span style='color:{ACCENT_COLOR};'>📋 Sammanfattning</span>", unsafe_allow_html=True)
        # Display key extracted information
        if "premie" in data:
            st.write(f"**Årspremie:** {int(premium_val):,} kr".replace(",", " "))
        if "självrisk" in data and data["självrisk"] not in [0, 0.0]:
            st.write(f"**Självrisk:** {int(data['självrisk']):,} kr".replace(",", " "))
        if "ansvarstid" in data and str(data["ansvarstid"]).strip():
            st.write(f"**Ansvarstid:** {data['ansvarstid']}")  # e.g. "12 månader" (visas som text)
        # Summaries of coverage fields
        # Egendomsskydd (property coverage) total
        property_fields = ["byggnad", "fastighet", "varor", "maskiner"]
        prop_values = {f: data[f] for f in property_fields if f in data and isinstance(data[f], (int, float)) and data[f] > 0}
        if prop_values:
            total_prop = sum(prop_values.values())
            details = ", ".join([f"{name.capitalize()}: {int(val):,} kr".replace(",", " ") for name, val in prop_values.items()])
            st.write(f"**Summa egendomsskydd:** {int(total_prop):,} kr".replace(",", " ") + f" _(fördelat på {details})_")
        # Ansvarsskydd (liability coverage) details
        liability_fields = ["produktansvar", "rättsskydd", "gdpr_ansvar"]
        liab_values = {f: data[f] for f in liability_fields if f in data and isinstance(data[f], (int, float)) and data[f] > 0}
        if liab_values:
            details = ", ".join([f"{name.capitalize()}: {int(val):,} kr".replace(",", " ") for name, val in liab_values.items()])
            st.write(f"**Ansvarsskydd:** {details}")
        # Overall score if available
        if score_val is not None:
            st.write(f"**Försäkringsskydd poäng:** {score_val}/100")

        # Export summary buttons (Excel/PDF)
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

        # Comparison Table Section
        st.markdown(f"### <span style='color:{ACCENT_COLOR};'>📊 Jämförelsetabell</span>", unsafe_allow_html=True)
        # Generate recommendations using the same extracted data
        try:
            # Pass industry to recommender if selected (exclude "Ej valt")
            if selected_industry and selected_industry != "Ej valt":
                recommendations = generate_recommendation(data, selected_industry)
            else:
                recommendations = generate_recommendation(data)
        except Exception as e:
            recommendations = None
            st.warning(f"⚠️ Kunde inte generera rekommendationer: {e}")
        # Prepare data for comparison table
        if recommendations and isinstance(recommendations, dict):
            # Determine fields to compare (all keys in recommendations, and corresponding current values if present)
            compare_fields = []
            for key in recommendations.keys():
                compare_fields.append(key)
            # Include current data keys that have recommendations (avoid duplicates)
            compare_fields = list(dict.fromkeys(compare_fields))  # preserve order, remove dupes
            # Filter out non-coverage fields
            exclude_keys = ["premie", "självrisk", "karens", "ansvarstid"]
            compare_fields = [k for k in compare_fields if k.lower() not in exclude_keys]
            if compare_fields:
                comp_rows = []
                for field in compare_fields:
                    current_val = data.get(field, 0)
                    rec_val = recommendations.get(field, 0)
                    # Format values
                    if isinstance(current_val, (int, float)):
                        curr_str = f"{int(current_val):,} kr".replace(",", " ")
                    else:
                        curr_str = str(current_val)
                    if isinstance(rec_val, (int, float)):
                        rec_str = f"{int(rec_val):,} kr".replace(",", " ")
                    else:
                        rec_str = str(rec_val)
                    comp_rows.append({
                        "Försäkringsmoment": field.capitalize(),
                        "Nuvarande": curr_str,
                        "Rekommenderat": rec_str
                    })
                comp_df = pd.DataFrame(comp_rows)
                st.table(comp_df)  # display the comparison table
            else:
                st.write("*(Inga relevanta försäkringsbelopp att jämföra.)*")
        else:
            st.write("*(Inga rekommendationer tillgängliga för jämförelse.)*")

        # AI Advice Section
        st.markdown(f"### <span style='color:{ACCENT_COLOR};'>💡 AI-rådgivning</span>", unsafe_allow_html=True)
        try:
            # Provide data (and recommendations/industry if available) to the AI advisor for context
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
        # Display AI advice
        if advisor_text:
            st.write(advisor_text)
        else:
            st.write("*(Ingen AI-rådgivning tillgänglig för detta dokument.)*")

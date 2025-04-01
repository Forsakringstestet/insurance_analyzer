# app.py

import streamlit as st
import logging
import openai

# -- Egna moduler --
from parser.pdf_extractor import extract_text_from_pdf
from parser.pdf_analyzer import extract_all_insurance_data
from parser.scoring import score_document
from ai.openai_advisor import ask_openai_extract, ask_openai
from ai.recommender import generate_recommendation
from export.export_excel import export_summary_excel
from export.export_pdf import export_summary_pdf
from export.export_word import generate_procurement_word
from utils.comparison import render_comparison_table
from utils.visualizer import display_results


def main():
    """
    Huvudfunktion för Streamlit-appen. Hanterar filuppladdning av PDF:er,
    extraherar och analyserar data, visar resultat, och ger möjlighet
    till export i olika format.
    """
    # 1. Grundläggande app-inställningar
    st.set_page_config(page_title="Försäkringsanalys", layout="wide")
    st.title("Jämför & Analysera Försäkringsbrev, Offert & Villkor")

    # 2. Logging-konfiguration (valfritt men användbart vid felsökning)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    # 3. Kontrollera OpenAI-nyckel i Streamlit Secrets
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("Ingen OpenAI-nyckel funnen i Streamlit secrets. Lägg till `OPENAI_API_KEY` i `.streamlit/secrets.toml`.")
        st.stop()
    else:
        openai.api_key = st.secrets["OPENAI_API_KEY"]

    # 4. Uppladdning av en eller flera PDF-filer
    uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer", type=["pdf"], accept_multiple_files=True)
    if not uploaded_files:
        st.info("Vänligen ladda upp minst en PDF-fil för att fortsätta.")
        return

    # 5. Justerbara vikter för scoring (om du vill att användaren ska kunna styra logiken)
    st.sidebar.header("Vikter för Poängberäkning")
    weight_scope = st.sidebar.slider("Vikt: Omfattning (scope)", 0.0, 10.0, 1.0, 0.1)
    weight_cost = st.sidebar.slider("Vikt: Kostnad (premie)", 0.0, 10.0, 1.0, 0.1)
    weight_deductible = st.sidebar.slider("Vikt: Självrisk", 0.0, 10.0, 1.0, 0.1)
    weight_other = st.sidebar.slider("Vikt: Övrigt", 0.0, 10.0, 1.0, 0.1)

    # 6. Huvudloop för varje PDF-fil: extrahera text, analysera, AI-beräkning, scoring, etc.
    analysis_results = []
    for file in uploaded_files:
        # 6a. Extrahera text från PDF
        try:
            pdf_text = extract_text_from_pdf(file)
        except Exception as e:
            st.error(f"Kunde inte extrahera text från {file.name}: {e}")
            continue

        # 6b. Analysera data med pdf_analyzer
        data = extract_all_insurance_data(pdf_text)

        # 6c. Beräkna en "score" baserat på extraherade värden (scoring.py)
        doc_score = score_document(data, weight_scope, weight_cost, weight_deductible, weight_other)

        # 6d. (Valfritt) Anropa GPT-3.5 för att extrahera info eller generera rekommendationer
        # Exempel: extraktion via AI
        # ai_extracted_data = ask_openai_extract(pdf_text)
        # data.update(ai_extracted_data)  # Slå ihop AI-data med parser-data

        # Exempel: Generera en AI-baserad kort rådgivning
        # (Här använder vi en enkel branschsträng, men du kan låta användaren välja bransch i en selectbox)
        industry = "Bygg"  # eller "IT", "Handel", etc.
        ai_recommendation = ask_openai(data, industry)

        # 6e. Generera en enkel regelbaserad rekommendation (recommender.py)
        local_recommendation = generate_recommendation(data)

        # 6f. Samla allt i en resultatslista
        analysis_results.append({
            "filename": file.name,
            "data": data,
            "score": doc_score,
            "ai_recommendation": ai_recommendation,
            "local_recommendation": local_recommendation
        })

    # 7. Visualisera resultat
    if analysis_results:
        # 7a. Visa en enklare sammanställning i tabell
        display_results(analysis_results)

        # 7b. Visa en mer avancerad jämförelsetabell med färgkodning
        render_comparison_table(analysis_results)

        # 7c. Visa AI-rekommendationer
        st.subheader("AI-rekommendationer")
        for item in analysis_results:
            st.markdown(f"**{item['filename']}**")
            st.write(item["ai_recommendation"])
            st.write(f"**Regelbaserad rekommendation:** {item['local_recommendation']}")
            st.write("---")

        # 8. Exportera resultat (PDF, Excel, Word)
        st.subheader("Exportera resultat")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Exportera till PDF"):
                export_summary_pdf(analysis_results)
        with col2:
            if st.button("Exportera till Excel"):
                export_summary_excel(analysis_results)
        with col3:
            if st.button("Exportera till Word"):
                generate_procurement_word(analysis_results)


if __name__ == "__main__":
    main()

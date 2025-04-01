# main.py
import streamlit as st
from Parser import pdf_extractor, pdf_analyzer, scoring
from openai_advisor import ask_openai, ask_openai_extract
from recommender import generate_recommendation
from Export import export_excel, export_pdf, export_word
from Utils import comparison, visualizer

def main():
    st.title("AI-försäkringsrådgivare")
    
    # Ladda upp en PDF-fil
    uploaded_file = st.file_uploader("Ladda upp en PDF med försäkringsdokument", type=["pdf"])
    if uploaded_file:
        text = pdf_extractor.extract_text_from_pdf(uploaded_file)
        st.text_area("Extraherad text", text, height=200)
        
        # Extrahera data med parsern
        insurance_data = pdf_analyzer.extract_all_insurance_data(text)
        
        # Gör en scoring (använd vikter från config om så önskas)
        score = scoring.score_document(insurance_data, 1.0, 1.0, 1.0, 1.0)
        insurance_data["score"] = score  # Lägg in poängen i datan
        
        st.write("Extraherad data:", insurance_data)
        
        # Generera AI-rekommendation
        recommendation = ask_openai(insurance_data)
        st.write("AI-rekommendation:", recommendation)
        
        # Generera en enkel rekommendation baserat på innehållet
        simple_recommendation = generate_recommendation(insurance_data)
        st.write("Enkel rekommendation:", simple_recommendation)
        
        # Visa jämförelsetabell (exempel med ett enda dokument)
        results = [{
            "filename": uploaded_file.name,
            "data": insurance_data,
            "score": score
        }]
        comparison.render_comparison_table(results)
        visualizer.display_results(results)
        
        # Låt användaren välja exportformat
        export_format = st.selectbox("Välj exportformat", ["Excel", "PDF", "Word"])
        if st.button("Exportera sammanställning"):
            if export_format == "Excel":
                export_excel.export_summary_excel(results)
            elif export_format == "PDF":
                export_pdf.export_summary_pdf(results)
            elif export_format == "Word":
                export_word.generate_procurement_word(results)

if __name__ == "__main__":
    main()

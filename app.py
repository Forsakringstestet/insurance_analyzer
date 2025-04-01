import streamlit as st
from parser import pdf_extractor, pdf_analyzer, scoring
from ai.openai_advisor import ask_openai, ask_openai_extract
from ai.recommender import generate_recommendation
from export import export_excel, export_pdf, export_word
from utils import comparison, visualizer

def main():
    st.title("AI-försäkringsrådgivare")
    
    # Ladda upp en PDF-fil
    uploaded_file = st.file_uploader("Ladda upp en PDF med försäkringsdokument", type=["pdf"])
    if uploaded_file:
        text = pdf_extractor.extract_text_from_pdf(uploaded_file)
        st.text_area("Extraherad text", text, height=200)
        
        # Extrahera data med parsern
        insurance_data = pdf_analyzer.extract_all_insurance_data(text)
        
        # Gör en scoring (här används vikterna 1.0, men du kan anpassa eller importera från en config-fil)
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

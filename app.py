import streamlit as st
from parser import pdf_extractor, pdf_analyzer, scoring
from ai.openai_advisor import ask_openai, ask_openai_extract
from ai.recommender import generate_recommendation
from export import export_excel, export_pdf, export_word
from utils import comparison, visualizer

def main():
    st.title("AI-försäkringsrådgivare")

    # Placera exportformatvalet i sidopanelen
    st.sidebar.header("Inställningar")
    export_format = st.sidebar.selectbox("Välj exportformat", ["Excel", "PDF", "Word"])
    
    # Tillåt att flera PDF:er laddas upp
    uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer med försäkringsdokument", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        results = []
        for uploaded_file in uploaded_files:
            # Skapa en expander för att visa den extraherade texten för varje fil
            with st.expander(f"Visa extraherad text för {uploaded_file.name}"):
                text = pdf_extractor.extract_text_from_pdf(uploaded_file)
                st.text_area("Extraherad text", text, height=200)

            # Extrahera data med parsern
            insurance_data = pdf_analyzer.extract_all_insurance_data(text)
            
            # Gör en scoring (du kan justera vikterna eller importera dem från en config-fil)
            score = scoring.score_document(insurance_data, 1.0, 1.0, 1.0, 1.0)
            insurance_data["score"] = score
            
            # Visa den extraherade datan i en separat expander
            with st.expander(f"Visa extraherad data för {uploaded_file.name}"):
                st.write(insurance_data)
            
            # Generera och visa AI-rådgivning
            with st.expander(f"AI-rådgivning för {uploaded_file.name}"):
                ai_recommendation = ask_openai(insurance_data)
                st.write(ai_recommendation)
            
            # Generera och visa en enkel rekommendation
            with st.expander(f"Enkel rekommendation för {uploaded_file.name}"):
                simple_recommendation = generate_recommendation(insurance_data)
                st.write(simple_recommendation)
            
            # Samla resultatet
            results.append({
                "filename": uploaded_file.name,
                "data": insurance_data,
                "score": score
            })
        
        # Visa jämförelsetabell och sammanställning med färgkodning
        st.subheader("Jämförelsetabell")
        comparison.render_comparison_table(results)
        st.subheader("Sammanställning")
        visualizer.display_results(results)
        
        # Exportera sammanställning
        if st.button("Exportera sammanställning"):
            if export_format == "Excel":
                export_excel.export_summary_excel(results)
            elif export_format == "PDF":
                export_pdf.export_summary_pdf(results)
            elif export_format == "Word":
                export_word.generate_procurement_word(results)

if __name__ == "__main__":
    main()

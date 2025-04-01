import streamlit as st
from parser import pdf_extractor, pdf_analyzer, scoring
from ai.openai_advisor import ask_openai, ask_openai_extract
from ai.recommender import generate_recommendation
from export import export_excel, export_pdf, export_word
from utils import comparison, visualizer

def main():
    st.title("AI-försäkringsrådgivare")
    st.sidebar.header("Inställningar")
    export_format = st.sidebar.selectbox("Välj exportformat", ["Excel", "PDF", "Word"])

    uploaded_files = st.file_uploader("Ladda upp en eller flera PDF-filer med försäkringsdokument", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        results = []
        for uploaded_file in uploaded_files:
            with st.expander(f"Visa extraherad text för {uploaded_file.name}"):
                text = pdf_extractor.extract_text_from_pdf(uploaded_file)
                st.text_area("Extraherad text", text, height=200)

            # Primär extraktion: lokal parser
            insurance_data = pdf_analyzer.extract_all_insurance_data(text)
            score = scoring.score_document(insurance_data, 1.0, 1.0, 1.0, 1.0)
            insurance_data["score"] = score

            # Kör AI-extraktion som fallback om parsern misslyckas
            needs_ai = any(
                v in [0.0, "saknas", "okänd"]
                for k, v in insurance_data.items() if k not in ["score"]
            )
            ai_extracted = None
            if needs_ai:
                with st.spinner("Analyserar dokument med AI..."):
                    ai_extracted = ask_openai_extract(text)

            # Visa extraherad data
            with st.expander(f"Parser-data för {uploaded_file.name}"):
                st.write(insurance_data)

            if ai_extracted:
                with st.expander(f"📎 AI-förslag på extraktion från {uploaded_file.name}"):
                    st.write(ai_extracted)

            # AI-rådgivning
            with st.expander(f"AI-rådgivning för {uploaded_file.name}"):
                ai_recommendation = ask_openai(insurance_data)
                st.write(ai_recommendation)

            # Enkel regelbaserad rekommendation
            with st.expander(f"Enkel rekommendation för {uploaded_file.name}"):
                simple_recommendation = generate_recommendation(insurance_data)
                st.write(simple_recommendation)

            results.append({
                "filename": uploaded_file.name,
                "data": insurance_data,
                "score": score
            })

        st.subheader("Jämförelsetabell")
        comparison.render_comparison_table(results)
        st.subheader("Sammanställning")
        visualizer.display_results(results)

        if st.button("Exportera sammanställning"):
            if export_format == "Excel":
                export_excel.export_summary_excel(results)
            elif export_format == "PDF":
                export_pdf.export_summary_pdf(results)
            elif export_format == "Word":
                export_word.generate_procurement_word(results)

if __name__ == "__main__":
    main()

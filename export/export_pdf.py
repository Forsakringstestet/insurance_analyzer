from fpdf import FPDF
import streamlit as st

def export_summary_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for r in results:
        pdf.cell(200, 10, txt=f"Fil: {r['filename']}", ln=True)
        for k, v in r["data"].items():
            pdf.cell(200, 10, txt=f"{k.capitalize()}: {v}", ln=True)
        pdf.cell(200, 10, txt=f"Poäng: {r['score']}", ln=True)
        pdf.cell(200, 10, txt=f"Rekommendation: {r['recommendation']}", ln=True)
        pdf.ln(5)
    st.download_button("Ladda ner PDF", pdf.output(dest='S').encode('latin-1'), file_name="analys.pdf")

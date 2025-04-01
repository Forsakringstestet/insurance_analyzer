# Export/export_pdf.py
from fpdf import FPDF
import streamlit as st
import tempfile

def export_summary_pdf(results: list) -> None:
    """
    Exporterar en sammanställning av analyserade data till en PDF-fil.
    
    Args:
        results (list): Lista med dictionaries innehållande 'filename' och 'data'.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Jämförelse av Försäkringsdokument", ln=True, align="C")
    pdf.ln(10)
    
    for r in results:
        data = r.get("data", {})
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt=r.get("filename", "Utan filnamn"), ln=True)
        pdf.set_font("Arial", size=10)
    
        for label, key in [
            ("Poäng", "score"),
            ("Premie", "premie"),
            ("Självrisk", "självrisk"),
            ("Maskiner", "maskiner"),
            ("Varor", "varor"),
            ("Byggnad", "byggnad"),
            ("Transport", "transport"),
            ("Produktansvar", "produktansvar"),
            ("Ansvar", "ansvar"),
            ("Rättsskydd", "rättsskydd"),
            ("GDPR ansvar", "gdpr_ansvar"),
            ("Karens", "karens"),
            ("Ansvarstid", "ansvarstid"),
        ]:
            val = data.get(key, r.get(key, "saknas"))
            pdf.cell(60, 8, txt=f"{label}:", ln=0)
            pdf.cell(60, 8, txt=f"{val}", ln=1)
    
        pdf.ln(5)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        pdf.output(f.name)
        with open(f.name, "rb") as file:
            st.download_button("📄 Ladda ner PDF", data=file.read(), file_name="forsakringsjämforelse.pdf")

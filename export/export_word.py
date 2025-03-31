from docx import Document
import streamlit as st
from io import BytesIO

def export_summary_word(results):
    doc = Document()
    doc.add_heading('Försäkringsanalys', 0)
    for r in results:
        doc.add_heading(r["filename"], level=1)
        for k, v in r["data"].items():
            doc.add_paragraph(f"{k.capitalize()}: {v}")
        doc.add_paragraph(f"Poäng: {r['score']}")
        doc.add_paragraph(f"Rekommendation: {r['recommendation']}")
    output = BytesIO()
    doc.save(output)
    st.download_button("Ladda ner Word", output.getvalue(), file_name="analys.docx")

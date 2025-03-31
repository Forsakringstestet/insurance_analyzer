from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_procurement_word(results):
    doc = Document()

    # Titel
    doc.add_heading('Upphandlingsunderlag – Försäkringsanalys', 0)

    intro = doc.add_paragraph("Detta dokument utgör ett automatiserat upphandlingsunderlag för analys och jämförelse av försäkringsbrev, offerter och villkor. Underlaget har genererats med hjälp av AI och omfattar nyckelfaktorer, riskbedömningar och förslag på åtgärder anpassade efter bransch och behov.")
    intro.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    doc.add_page_break()

    # Resultat
    for r in results:
        doc.add_heading(f"Dokument: {r['filename']}", level=1)

        table = doc.add_table(rows=1, cols=2)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Faktor'
        hdr_cells[1].text = 'Värde'

        for k, v in r["data"].items():
            row_cells = table.add_row().cells
            row_cells[0].text = k.capitalize()
            row_cells[1].text = str(v)

        doc.add_paragraph(f"\nTotal Poäng: {r['score']*100:.0f}/100", style="Intense Quote")

        doc.add_paragraph("AI-baserad rekommendation:")
        doc.add_paragraph(r["recommendation"])

        doc.add_page_break()

    # Avslutning
    doc.add_heading("Slutsats & Rekommendation", level=1)
    doc.add_paragraph("Det rekommenderas att försäkringsgivare ombeds justera självrisksnivåer, omfattning och beloppsgränser enligt ovanstående analys. En fortsatt dialog med branschspecifik rådgivare är att föredra.")

    doc.add_paragraph("Underlaget kan bifogas i kommande offertförfrågan för att möjliggöra en likvärdig och transparent upphandling.")

    output = BytesIO()
    doc.save(output)
    st.download_button("Ladda ner Upphandlingsunderlag (Word)", output.getvalue(), file_name="upphandling.docx")

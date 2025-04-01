# Parser/pdf_extractor.py
import fitz

def extract_text_from_pdf(file) -> str:
    """
    Extraherar text från en PDF-fil med hjälp av PyMuPDF (fitz).
    
    Args:
        file: Filobjekt med PDF-data.
    
    Returns:
        str: Extraherad text från PDF:en.
    """
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

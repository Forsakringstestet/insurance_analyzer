# Export/export_excel.py
import pandas as pd
from io import BytesIO

def export_summary_excel(results: list) -> BytesIO:
    """
    Returnerar en Excel-fil som en BytesIO-ström baserat på försäkringsanalyser.

    Args:
        results (list): Lista med dictionaries innehållande 'filename', 'score' och 'data'.

    Returns:
        BytesIO: En ström som kan användas i st.download_button
    """
    rows = []
    for r in results:
        d = r.get("data", {})
        rows.append({
            "Filnamn": r.get("filename", ""),
            "Poäng": r.get("score", 0),
            "Premie": d.get("premie", 0),
            "Självrisk": d.get("självrisk", 0),
            "Maskiner": d.get("maskiner", 0),
            "Varor": d.get("varor", 0),
            "Byggnad": d.get("byggnad", 0),
            "Transport": d.get("transport", 0),
            "Produktansvar": d.get("produktansvar", 0),
            "Ansvar": d.get("ansvar", 0),
            "Rättsskydd": d.get("rättsskydd", 0),
            "GDPR ansvar": d.get("gdpr_ansvar", 0),
            "Karens": d.get("karens", "saknas"),
            "Ansvarstid": d.get("ansvarstid", "saknas")
        })

    df = pd.DataFrame(rows)
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sammanställning")
    excel_file.seek(0)
    return excel_file

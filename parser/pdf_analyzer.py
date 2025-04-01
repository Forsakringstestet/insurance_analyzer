import re

def parse_currency(text):
    text = text.replace(" ", "").replace(",", ".")
    match = re.search(r"(\d+(\.\d+)?)", text)
    return float(match.group(1)) if match else 0.0

def extract_all_insurance_data(text: str) -> dict:
    data = {
        "premie": 0.0,
        "självrisk": 0.0,
        "maskiner": 0.0,
        "produktansvar": 0.0,
        "karens": "",
        "ansvarstid": ""
    }

    text = text.lower()

    # ---- premie ----
    m = re.search(r"(premie|pris totalt|totalpris|pris per år|bruttopremie)[^\d]{0,15}(\d[\d\s,.]+) ?kr", text)
    if m:
        data["premie"] = parse_currency(m.group(2))

    # ---- självrisk ----
    sj = re.search(r"(självrisk)[^\d]{0,10}(\d[\d\s,.]*) ?(kr|basbelopp)?", text)
    if sj:
        val = sj.group(2)
        if "basbelopp" in sj.group(0):
            # basbelopp to SEK
            val = float(val.replace(",", ".")) * 58800
        data["självrisk"] = parse_currency(str(val))

    # ---- maskiner & inventarier ----
    mi = re.search(r"(maskiner|maskinförsäkring|maskiner/inventarier).*?(\d[\d\s,.]+) ?kr", text)
    if mi:
        data["maskiner"] = parse_currency(mi.group(2))

    # ---- produktansvar / ansvar ----
    pa = re.search(r"(produktansvar|ansvarsförsäkring).*?(\d[\d\s,.]+) ?kr", text)
    if pa:
        data["produktansvar"] = parse_currency(pa.group(2))

    # ---- karens ----
    kar = re.search(r"(karens|väntetid)[^\d]{0,15}(\d{1,2}) ?(dygn|dagar|timmar)", text)
    if kar:
        data["karens"] = f"{kar.group(2)} {kar.group(3)}"

    # ---- ansvarstid ----
    ans = re.search(r"(ansvarstid|avbrottstid).*?(\d{1,2}) ?(månader|mån)", text)
    if ans:
        data["ansvarstid"] = f"{ans.group(2)} månader"

    return data

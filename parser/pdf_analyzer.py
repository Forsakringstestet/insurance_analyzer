import re
import streamlit as st
from ai.openai_advisor import ask_openai_extract

BASBELOPP_2025 = 58800

def parse_currency(val: str) -> float:
    val = val.replace(" ", "").replace(".", "").replace(",", ".").replace(":-", "")
    match = re.search(r"(\d+(?:\.\d+)?)", val)
    return float(match.group(1)) if match else 0.0

def extract_premie(text): ...
def extract_sjalvrisk(text): ...
def extract_karens(text): ...
def extract_ansvarstid(text): ...
def extract_maskiner(text): ...
def extract_produktansvar(text): ...
# Se tidigare version för full kod ovan ↑

def extract_all_insurance_data(text: str) -> dict:
    # 1. Kör lokala extraktioner
    data = {
        "premie": extract_premie(text),
        "självrisk": extract_sjalvrisk(text),
        "karens": extract_karens(text),
        "ansvarstid": extract_ansvarstid(text),
        "maskiner": extract_maskiner(text),
        "produktansvar": extract_produktansvar(text)
    }

    # 2. Om något saknas — fråga GPT
    needs_ai = any([
        data["premie"] == 0,
        data["självrisk"] == 0,
        data["karens"] == "saknas",
        data["ansvarstid"] == "saknas",
        data["maskiner"] == 0,
        data["produktansvar"] == 0,
    ])

    if needs_ai:
        ai_data = ask_openai_extract(text)
        for key in data:
            if data[key] in [0, "saknas"] and key in ai_data:
                data[key] = ai_data[key]

    return data

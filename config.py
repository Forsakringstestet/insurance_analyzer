# config.py
"""
Central konfigurationsfil för projektet.
Här samlar du alla globala konstanter och inställningar.
"""

# Basbelopp för 2025 – kan ändras vid behov
BASBELOPP_2025 = 58800

# Exempel på vikter för scoring (kan justeras eller göras konfigurerbara)
SCORING_WEIGHTS = {
    "weight_scope": 1.0,
    "weight_cost": 1.0,
    "weight_deductible": 1.0,
    "weight_other": 1.0,
}
# .streamlit/config.toml
[theme]
primaryColor = "#004c99"
backgroundColor = "#f5f8fa"
secondaryBackgroundColor = "#e0e6ed"
textColor = "#0c1c3c"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false

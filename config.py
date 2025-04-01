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

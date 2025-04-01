# Funktion som lägger till visuell indikator beroende på score
import streamlit as st


def render_score_indicator(score: float):
    if score >= 90:
        st.success(f"🌟 Utmärkt försäkringsskydd (Poäng: {round(score)})")
    elif score >= 70:
        st.info(f"✅ Bra försäkringsskydd (Poäng: {round(score)})")
    elif score >= 50:
        st.warning(f"⚠️ Tveksamt skydd (Poäng: {round(score)})")
    else:
        st.error(f"❌ Otillräckligt försäkringsskydd (Poäng: {round(score)})")


# Exempel: Kalla denna efter scoren räknats ut
# render_score_indicator(score)

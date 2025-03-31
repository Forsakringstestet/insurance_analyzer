import streamlit as st
import plotly.graph_objects as go

def display_results(results):
    for result in results:
        st.markdown(f"### 📄 {result['filename']}")
        st.write("**Extraherad information:**", result["data"])
        st.write("**Poäng:**", result["score"])
        st.write("**AI-rekommendation:**", result["recommendation"])
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = result["score"] * 100,
            title = {'text': "Totalbedömning"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "green" if result["score"] >= 0.75 else "orange" if result["score"] >= 0.5 else "red"},
            }))
        st.plotly_chart(fig, use_container_width=True)

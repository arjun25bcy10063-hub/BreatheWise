import streamlit as st


def render_risk_card(risk):
    st.subheader("Your Personalized Risk")
    st.progress(risk.overall_score / 100)
    st.metric("Risk Score", f"{risk.overall_score}/100", risk.overall_level)
    cols = st.columns(3)
    cols[0].metric("Air Risk", risk.air_risk)
    cols[1].metric("Weather Risk", risk.weather_risk)
    cols[2].metric("Exposure Risk", risk.exposure_risk)
    st.write(risk.explanation)

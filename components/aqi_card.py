import streamlit as st

from utils.formatting import aqi_label


def render_aqi_card(aqi):
    if aqi.us_aqi is None:
        st.metric("AQI", "—")
        return
    st.metric("AQI", f"{aqi.us_aqi:.0f}", aqi_label(aqi.us_aqi))
    cols = st.columns(5)
    cols[0].metric("PM2.5", _fmt(aqi.pm2_5))
    cols[1].metric("PM10", _fmt(aqi.pm10))
    cols[2].metric("NO₂", _fmt(aqi.no2))
    cols[3].metric("O₃", _fmt(aqi.ozone))
    cols[4].metric("CO", _fmt(aqi.co))


def _fmt(value):
    return "—" if value is None else f"{value:.1f}"

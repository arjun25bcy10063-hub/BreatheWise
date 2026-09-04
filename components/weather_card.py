import streamlit as st


def render_weather_card(weather):
    st.metric("Temperature", f"{weather.temperature_c:.0f} °C" if weather.temperature_c is not None else "—")
    cols = st.columns(4)
    cols[0].metric("Feels like", f"{weather.apparent_temperature_c:.0f} °C" if weather.apparent_temperature_c is not None else "—")
    cols[1].metric("Humidity", f"{weather.humidity_pct:.0f}%" if weather.humidity_pct is not None else "—")
    cols[2].metric("Wind", f"{weather.wind_speed_kmh:.0f} km/h" if weather.wind_speed_kmh is not None else "—")
    cols[3].metric("UV", f"{weather.uv_index:.0f}" if weather.uv_index is not None else "—")

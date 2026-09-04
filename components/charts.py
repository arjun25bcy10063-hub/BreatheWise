import pandas as pd
import plotly.express as px
import streamlit as st


def render_trend_chart(rows):
    if not rows:
        st.info("Not enough stored data for a trend chart yet.")
        return
    df = pd.DataFrame([dict(row) for row in rows])
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.sort_values("timestamp")
    for column, title, y_label in [
        ("us_aqi", "AQI Trend", "AQI"),
        ("pm2_5", "PM2.5 Trend", "µg/m³"),
        ("temperature_c", "Temperature Trend", "°C"),
    ]:
        if column not in df.columns or df[column].notna().sum() == 0:
            continue
        fig = px.line(df, x="timestamp", y=column, title=title, labels={column: y_label, "timestamp": "Time"})
        fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)

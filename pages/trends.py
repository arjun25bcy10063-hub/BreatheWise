from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from database.database import get_profile, get_trend_data, init_db

init_db()

st.markdown(
    """
    <style>
    .tr-wrap{max-width:1250px;margin:0 auto 2rem}
    .tr-hero{padding:1.45rem 1.55rem;border-radius:24px;background:linear-gradient(135deg,#123b36,#0f766e);color:white;box-shadow:0 18px 40px rgba(17,59,54,.13);margin-bottom:1.1rem}
    .tr-kicker{font-size:.72rem;font-weight:850;letter-spacing:.14em;text-transform:uppercase;opacity:.78}
    .tr-title{font-size:2.15rem;font-weight:900;letter-spacing:-.045em;line-height:1.08;margin:.4rem 0 .45rem}
    .tr-sub{font-size:.9rem;line-height:1.55;color:rgba(255,255,255,.8)}
    .tr-card{background:#fff;border:1px solid #e4ece9;border-radius:20px;padding:1.05rem;box-shadow:0 10px 28px rgba(21,52,48,.05);height:100%}
    .tr-label{font-size:.72rem;font-weight:850;letter-spacing:.08em;text-transform:uppercase;color:#71817d}
    .tr-value{font-size:1.75rem;font-weight:900;color:#17312e;margin-top:.35rem}
    .tr-note{font-size:.76rem;color:#71817d;line-height:1.5}
    .tr-info{padding:.95rem 1rem;border-radius:15px;background:#f5faf8;border:1px solid #e1ece8;color:#536560;font-size:.8rem;line-height:1.5}
    </style>
    """,
    unsafe_allow_html=True,
)


def esc(value):
    return escape(str(value))


profile = get_profile()

st.markdown(
    f"""
    <div class="tr-wrap">
        <div class="tr-hero">
            <div class="tr-kicker">Environment over time</div>
            <div class="tr-title">
                See how your environment is changing.
            </div>
            <div class="tr-sub">
                Collected readings for
                {esc(profile.location_name if profile else "your location")}
                help you understand recent air-quality and weather patterns.
            </div>
        </div>
    """,
    unsafe_allow_html=True,
)

if not profile:
    st.warning("Complete your profile first.")
    st.page_link(
        "pages/profile.py",
        label="Open Profile",
        icon="👤",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

rows = get_trend_data(
    profile.user_id,
    limit=168,
)

if not rows:
    st.info(
        "Not enough stored readings yet. Open the Dashboard and allow it to collect data over time."
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

df = pd.DataFrame(
    [dict(r) for r in rows]
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
)

for column in [
    "us_aqi",
    "pm2_5",
    "pm10",
    "temperature_c",
    "humidity_pct",
    "uv_index",
]:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

df = (
    df.dropna(subset=["timestamp"])
    .sort_values("timestamp")
)

latest = df.iloc[-1]
valid_days = df["timestamp"].dt.date.nunique()

aqi_series = df["us_aqi"].dropna()
pm25_series = df["pm2_5"].dropna()

latest_aqi = (
    "—"
    if pd.isna(latest.get("us_aqi"))
    else f"{latest['us_aqi']:.0f}"
)

average_aqi = (
    "—"
    if aqi_series.empty
    else f"{aqi_series.mean():.0f}"
)

peak_pm25 = (
    "—"
    if pm25_series.empty
    else f"{pm25_series.max():.1f}"
)

c1, c2, c3, c4 = st.columns(4)

summary_cards = [
    (
        c1,
        "Latest AQI",
        latest_aqi,
        "Most recent stored reading",
    ),
    (
        c2,
        "Average AQI",
        average_aqi,
        "Across collected readings",
    ),
    (
        c3,
        "Peak PM2.5",
        peak_pm25,
        "Highest stored value",
    ),
    (
        c4,
        "Days tracked",
        str(valid_days),
        "Based on collected snapshots",
    ),
]

for col, label, value, note in summary_cards:
    with col:
        st.markdown(
            f"""
            <div class="tr-card">
                <div class="tr-label">{esc(label)}</div>
                <div class="tr-value">{esc(value)}</div>
                <div class="tr-note">{esc(note)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    "<div style='height:.6rem'></div>",
    unsafe_allow_html=True,
)

tabs = st.tabs(
    [
        "AQI",
        "PM2.5",
        "Temperature",
        "Humidity",
    ]
)


def show_chart(
    tab,
    column,
    title,
    y_label,
    suffix="",
):
    with tab:
        if column not in df.columns:
            st.info("No data available for this metric yet.")
            return

        data = df[
            ["timestamp", column]
        ].dropna()

        if data.empty:
            st.info("No data available for this metric yet.")
            return

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=data["timestamp"],
                y=data[column],
                mode="lines+markers",
                line=dict(
                    width=3,
                    color="#0f766e",
                ),
                marker=dict(
                    size=5,
                    color="#0f766e",
                ),
                hovertemplate=(
                    f"%{{x}}<br>"
                    f"{title}: %{{y:.1f}}"
                    f"{suffix}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            height=390,
            margin=dict(
                l=0,
                r=0,
                t=18,
                b=0,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                title=None,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#edf2f0",
                title=y_label,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
            },
        )

        latest_value = data.iloc[-1][column]
        min_value = data[column].min()
        max_value = data[column].max()

        s1, s2, s3 = st.columns(3)

        s1.metric(
            "Latest",
            f"{latest_value:.1f}{suffix}",
        )

        s2.metric(
            "Lowest",
            f"{min_value:.1f}{suffix}",
        )

        s3.metric(
            "Highest",
            f"{max_value:.1f}{suffix}",
        )


show_chart(
    tabs[0],
    "us_aqi",
    "AQI",
    "AQI",
)

show_chart(
    tabs[1],
    "pm2_5",
    "PM2.5",
    "µg/m³",
)

show_chart(
    tabs[2],
    "temperature_c",
    "Temperature",
    "°C",
    "°C",
)

show_chart(
    tabs[3],
    "humidity_pct",
    "Humidity",
    "%",
    "%",
)

st.markdown(
    """
    <div class="tr-card" style="margin-top:1rem">
        <div class="tr-label">How to read this page</div>
        <div class="tr-note" style="margin-top:.4rem">
            The charts are based on readings stored when the Dashboard
            refreshes. More visits produce a richer trend history.
        </div>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)
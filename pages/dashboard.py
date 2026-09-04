from datetime import datetime, timezone
from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from agents.advisory_agent import generate_advisory
from agents.alert_agent import build_alert
from agents.risk_agent import assess_risk
from agents.safety_agent import validate_advisory_safety
from database.database import (
    get_latest_risk_score,
    get_profile,
    get_trend_data,
    init_db,
    save_alert,
    save_snapshot,
)
from services.aqi_service import get_air_quality
from services.weather_service import get_weather
from utils.formatting import aqi_label

init_db()

st.markdown(
    """
    <style>
    .bw-hero{padding:1.65rem 1.7rem;border-radius:24px;background:linear-gradient(135deg,#123b36,#0f766e);color:#fff;box-shadow:0 18px 40px rgba(17,59,54,.14);margin-bottom:1.15rem}
    .bw-kicker{font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;opacity:.78}
    .bw-title{font-size:2.35rem;font-weight:900;letter-spacing:-.045em;line-height:1.05;margin:.45rem 0 .5rem}
    .bw-sub{font-size:.95rem;color:rgba(255,255,255,.8);max-width:780px;line-height:1.6}
    .bw-meta{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-top:1.1rem;font-size:.8rem;color:rgba(255,255,255,.72)}
    .bw-live{display:inline-flex;align-items:center;gap:.45rem;padding:.34rem .68rem;border-radius:999px;background:rgba(255,255,255,.12);font-weight:800;color:#e5fffa}
    .bw-dot{width:8px;height:8px;border-radius:50%;background:#63e6be}
    .bw-section{font-size:1.08rem;font-weight:850;color:#17312e;margin:1.25rem 0 .65rem}
    .bw-card{background:#fff;border:1px solid #e4ece9;border-radius:19px;padding:1rem 1.05rem;box-shadow:0 10px 28px rgba(21,52,48,.055);height:100%}
    .bw-label{font-size:.72rem;font-weight:850;letter-spacing:.08em;text-transform:uppercase;color:#70817d}
    .bw-value{font-size:2rem;font-weight:900;line-height:1.05;color:#122825;margin-top:.38rem}
    .bw-small{font-size:.78rem;color:#72827e;line-height:1.45;margin-top:.4rem}
    .bw-aqi-big{font-size:3.6rem;font-weight:950;line-height:1;color:#122825;letter-spacing:-.06em}
    .bw-badge{display:inline-block;padding:.34rem .62rem;border-radius:999px;font-size:.7rem;font-weight:850;margin-top:.5rem}
    .low{background:#dcfce7;color:#166534}
    .moderate{background:#fef3c7;color:#92400e}
    .high{background:#fee2e2;color:#991b1b}
    .bw-risk{background:#102f2b;border-radius:24px;padding:1.35rem;color:white;box-shadow:0 18px 38px rgba(16,47,43,.16);height:100%}
    .bw-risk-kicker{font-size:.72rem;font-weight:850;letter-spacing:.12em;text-transform:uppercase;color:#b9ddd4}
    .bw-risk-score{font-size:4.5rem;font-weight:950;line-height:.95;letter-spacing:-.07em;margin-top:.35rem}
    .bw-risk-copy{color:#d5ebe6;font-size:.88rem;line-height:1.55;margin-top:.8rem}
    .bw-breakdown{background:#fff;border:1px solid #e4ece9;border-radius:24px;padding:1.25rem;box-shadow:0 10px 28px rgba(21,52,48,.055);height:100%}
    .bw-factor{margin:.95rem 0}
    .bw-factor-row{display:flex;justify-content:space-between;gap:.6rem;font-size:.8rem;color:#425854;font-weight:750;margin-bottom:.32rem}
    .bw-track{height:9px;border-radius:999px;background:#edf2f0;overflow:hidden}
    .bw-fill{height:100%;border-radius:999px;background:#0f766e}
    .bw-advisory{background:linear-gradient(180deg,#fff,#f5fbf9);border:1px solid #d7ebe5;border-radius:24px;padding:1.3rem;box-shadow:0 10px 28px rgba(21,52,48,.055)}
    .bw-ai{display:flex;gap:.75rem;align-items:flex-start}
    .bw-ai-icon{width:42px;height:42px;border-radius:13px;background:#e5f5f1;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex:0 0 auto}
    .bw-ai-title{font-size:1rem;font-weight:900;color:#17312e}
    .bw-ai-sub{font-size:.75rem;color:#73837f;margin-top:.18rem}
    .bw-summary{margin-top:.9rem;color:#28443f;font-size:1rem;line-height:1.62;font-weight:650}
    .bw-action{margin-top:.55rem;padding:.72rem .78rem;border-radius:14px;background:#fff;border:1px solid #e1ece8;color:#29433e;font-size:.85rem}
    .bw-action strong{color:#0f766e}
    .bw-mini{font-size:.72rem;font-weight:850;letter-spacing:.08em;text-transform:uppercase;color:#71827e;margin-top:1rem}
    .bw-callout{margin-top:.42rem;padding:.84rem .9rem;border-radius:15px;background:#fff9ed;border:1px solid #f2e2be;color:#6c4d0c;font-size:.84rem;line-height:1.5}
    .bw-alert{padding:1rem 1.05rem;border-radius:18px;background:#fff5f4;border:1px solid #f1d7d3}
    .bw-alert-title{font-weight:900;color:#9a3521}
    .bw-muted{font-size:.78rem;color:#71827d;line-height:1.5}
    .bw-forecast{padding:.86rem .7rem;text-align:center}
    .bw-day{font-size:.72rem;font-weight:850;color:#75847f;text-transform:uppercase}
    .bw-temp{font-size:1.2rem;font-weight:900;color:#17312e;margin-top:.35rem}
    .bw-forecast-small{font-size:.72rem;color:#75847f;margin-top:.22rem}
    .bw-note{padding:.8rem .9rem;border-radius:14px;background:#f7faf9;border:1px solid #e5eeeb;color:#536560;font-size:.78rem;line-height:1.5}
    @media (max-width:900px){
        .bw-title{font-size:1.9rem}
        .bw-risk-score{font-size:3.4rem}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def esc(value):
    return escape(str(value))


def fmt(value, suffix="", decimals=0):
    if value is None:
        return "—"
    try:
        return f"{float(value):.{decimals}f}{suffix}"
    except (TypeError, ValueError):
        return "—"


def risk_class(level):
    value = (level or "").lower()
    if "high" in value:
        return "high"
    if "moderate" in value:
        return "moderate"
    return "low"


def risk_pct(level):
    return {
        "low": 28,
        "moderate": 54,
        "high": 82,
    }.get(risk_class(level), 35)


def weather_label(code):
    mapping = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",
        61: "Light rain",
        63: "Rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Rain showers",
        82: "Heavy showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with hail",
    }
    return mapping.get(code, "Current conditions")


def metric_card(label, value, sub, foot=""):
    st.markdown(
        f"""
        <div class="bw-card">
            <div class="bw-label">{esc(label)}</div>
            <div class="bw-value">{esc(value)}</div>
            <div class="bw-small">
                <strong>{esc(sub)}</strong><br>{esc(foot)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(profile, updated_text):
    left, right = st.columns([4.8, 1.2])

    with left:
        st.markdown(
            '<div class="bw-kicker">Personal environmental intelligence</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="bw-title">Your environment, understood.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="bw-sub">Live weather and air-quality conditions translated into guidance for your current profile.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="bw-meta">
                <span>📍 {esc(profile.location_name or "Your location")}</span>
                <span>Personalized for {esc(profile.age_group)} · {esc(profile.occupation)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            '<div style="text-align:right"><span class="bw-live"><span class="bw-dot"></span>LIVE</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="text-align:right;margin-top:.55rem;font-size:.72rem;color:#d9ece7">{esc(updated_text)}</div>',
            unsafe_allow_html=True,
        )


def render_aqi_panel(aqi):
    st.markdown('<div class="bw-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="bw-label">Air quality</div>',
        unsafe_allow_html=True,
    )

    value = aqi.us_aqi

    if value is None:
        st.markdown(
            '<div class="bw-aqi-big">—</div><div class="bw-muted">Current AQI unavailable</div>',
            unsafe_allow_html=True,
        )
    else:
        label = aqi_label(value)
        status_class = risk_class(
            "High" if value > 100 else "Moderate" if value > 50 else "Low"
        )

        st.markdown(
            f"""
            <div class="bw-aqi-big">{fmt(value, decimals=0)}</div>
            <span class="bw-badge {status_class}">{esc(label)}</span>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:.45rem"></div>', unsafe_allow_html=True)

    pollutants = [
        ("PM2.5", aqi.pm2_5),
        ("PM10", aqi.pm10),
        ("NO₂", aqi.no2),
        ("O₃", aqi.ozone),
        ("SO₂", aqi.so2),
        ("CO", aqi.co),
    ]

    cols = st.columns(3)

    for col, (label, value) in zip(cols, pollutants):
        with col:
            st.markdown(
                f"""
                <div style="
                    padding:.58rem .52rem;
                    border:1px solid #e8efed;
                    border-radius:12px;
                    margin-top:.5rem
                ">
                    <div class="bw-label">{esc(label)}</div>
                    <div style="font-weight:850;color:#17312e;margin-top:.2rem">
                        {esc(fmt(value, decimals=1))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def render_risk(risk):
    left, right = st.columns([1.0, 1.35], gap="large")

    with left:
        score = max(0, min(100, int(risk.overall_score)))
        cls = risk_class(risk.overall_level)

        st.markdown(
            f"""
            <div class="bw-risk">
                <div class="bw-risk-kicker">Your personalized risk</div>
                <div class="bw-risk-score">{score}</div>
                <div style="font-size:.8rem;color:#b9ddd4;margin-top:.18rem">
                    out of 100
                </div>
                <span class="bw-badge {cls}"
                    style="margin-top:.75rem;background:rgba(255,255,255,.14);color:#fff">
                    {esc(risk.overall_level.upper())}
                </span>
                <div class="bw-risk-copy">
                    {esc(risk.explanation)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            '<div class="bw-breakdown"><div class="bw-section" style="margin-top:0">Risk breakdown</div>',
            unsafe_allow_html=True,
        )

        breakdown = [
            ("Air quality", risk.air_risk),
            ("Weather", risk.weather_risk),
            ("Exposure", risk.exposure_risk),
        ]

        for name, level in breakdown:
            pct = risk_pct(level)

            st.markdown(
                f"""
                <div class="bw-factor">
                    <div class="bw-factor-row">
                        <span>{esc(name)}</span>
                        <span>{esc(level)}</span>
                    </div>
                    <div class="bw-track">
                        <div class="bw-fill" style="width:{pct}%"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if risk.factors:
            st.markdown(
                '<div class="bw-mini" style="margin-top:.6rem">Main contributors</div>',
                unsafe_allow_html=True,
            )

            for factor in risk.factors[:5]:
                st.markdown(
                    f'<div style="margin-top:.38rem;font-size:.8rem;color:#4e625d">• {esc(factor)}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)


def render_advisory(advisory):
    st.markdown('<div class="bw-advisory">', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="bw-ai">
            <div class="bw-ai-icon">🤖</div>
            <div>
                <div class="bw-ai-title">Personalized guidance for today</div>
                <div class="bw-ai-sub">
                    Based on your profile and current environmental conditions
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="bw-summary">{esc(advisory.summary)}</div>',
        unsafe_allow_html=True,
    )

    if advisory.actions:
        st.markdown(
            '<div class="bw-mini">Recommended actions</div>',
            unsafe_allow_html=True,
        )

        for action in advisory.actions[:3]:
            st.markdown(
                f'<div class="bw-action"><strong>✓</strong>&nbsp;&nbsp;{esc(action)}</div>',
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="bw-mini">Outdoor guidance</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="bw-callout">{esc(advisory.outdoor_guidance)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="bw-mini">Why this advice is different for you</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="bw-muted">{esc(advisory.personalization_reason)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="margin-top:.85rem;font-size:.7rem;color:#81908c">{esc(advisory.disclaimer)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def render_trend_preview(rows):
    if not rows:
        st.markdown(
            '<div class="bw-note">Trend data will appear as the app collects snapshots.</div>',
            unsafe_allow_html=True,
        )
        return

    df = pd.DataFrame([dict(r) for r in rows])

    if "timestamp" not in df.columns or "us_aqi" not in df.columns:
        st.markdown(
            '<div class="bw-note">Trend data is not available yet.</div>',
            unsafe_allow_html=True,
        )
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["us_aqi"] = pd.to_numeric(df["us_aqi"], errors="coerce")

    df = (
        df.dropna(subset=["timestamp", "us_aqi"])
        .sort_values("timestamp")
        .tail(48)
    )

    if df.empty:
        st.markdown(
            '<div class="bw-note">Trend data is not available yet.</div>',
            unsafe_allow_html=True,
        )
        return

    fig = go.Figure(
        go.Scatter(
            x=df["timestamp"],
            y=df["us_aqi"],
            mode="lines+markers",
            line=dict(width=3, color="#0f766e"),
            marker=dict(size=4, color="#0f766e"),
            hovertemplate="%{x}<br>AQI: %{y:.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        height=250,
        margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(
            showgrid=True,
            gridcolor="#edf2f0",
            title=None,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )


def render_forecast(weather):
    if not weather.daily:
        return

    st.markdown(
        '<div class="bw-section">7-day outlook</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(min(7, len(weather.daily)))

    for i, (col, day) in enumerate(zip(cols, weather.daily[:7])):
        date_value = pd.to_datetime(day.get("date"), errors="coerce")

        day_label = (
            date_value.strftime("%a")
            if not pd.isna(date_value)
            else f"Day {i + 1}"
        )

        with col:
            st.markdown(
                f"""
                <div class="bw-card bw-forecast">
                    <div class="bw-day">{esc(day_label)}</div>
                    <div class="bw-temp">
                        {esc(fmt(day.get("temperature_max"), "°", 0))}
                    </div>
                    <div class="bw-forecast-small">
                        Low {esc(fmt(day.get("temperature_min"), "°", 0))}
                    </div>
                    <div class="bw-forecast-small">
                        UV {esc(fmt(day.get("uv_max"), "", 0))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def run_dashboard():
    profile = get_profile()

    if not profile or profile.latitude is None or profile.longitude is None:
        st.markdown(
            """
            <div class="bw-hero">
                <div class="bw-kicker">Get started</div>
                <div class="bw-title">Set up your environment profile.</div>
                <div class="bw-sub">
                    Choose your location and exposure profile to unlock
                    personalized environmental guidance.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Open Profile", type="primary"):
            st.switch_page("pages/profile.py")

        return

    _, refresh_col = st.columns([8, 1])

    with refresh_col:
        if st.button("↻ Refresh", use_container_width=True):
            st.rerun()

    updated = datetime.now(timezone.utc).astimezone().strftime(
        "%d %b %Y · %I:%M %p"
    )

    render_header(profile, updated)

    try:
        with st.spinner("Updating your environment..."):
            weather = get_weather(
                profile.latitude,
                profile.longitude,
            )

            aqi = get_air_quality(
                profile.latitude,
                profile.longitude,
            )

            risk = assess_risk(
                weather,
                aqi,
                profile,
            )

            advisory = generate_advisory(
                weather,
                aqi,
                risk,
                profile,
            )

            if not validate_advisory_safety(advisory, risk):
                st.error(
                    "The current advisory could not pass a safety check. Please refresh."
                )
                return

            previous_score = get_latest_risk_score(profile.user_id)
            alert = build_alert(risk, previous_score)

            save_snapshot(
                profile.user_id,
                weather,
                aqi,
                risk,
                advisory,
            )

            if alert:
                save_alert(profile.user_id, alert)

        st.markdown(
            '<div class="bw-section">Current conditions</div>',
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4, gap="medium")

        with c1:
            metric_card(
                "Temperature",
                fmt(weather.temperature_c, "°C"),
                weather_label(weather.weather_code),
                f"Feels like {fmt(weather.apparent_temperature_c, '°C')}",
            )

        with c2:
            metric_card(
                "Humidity",
                fmt(weather.humidity_pct, "%"),
                "Relative humidity",
                f"Wind {fmt(weather.wind_speed_kmh, ' km/h')}",
            )

        with c3:
            metric_card(
                "UV index",
                fmt(weather.uv_index, "", 0),
                "Sun exposure",
                "Higher values need extra protection",
            )

        with c4:
            metric_card(
                "Precipitation",
                fmt(weather.precipitation_mm, " mm", 1),
                "Current precipitation",
                "Local conditions",
            )

        st.markdown(
            '<div class="bw-section">Air quality</div>',
            unsafe_allow_html=True,
        )

        render_aqi_panel(aqi)

        st.markdown(
            '<div class="bw-section">Your personalized risk</div>',
            unsafe_allow_html=True,
        )

        render_risk(risk)

        st.markdown(
            '<div class="bw-section">What should you do?</div>',
            unsafe_allow_html=True,
        )

        left, right = st.columns([1.5, 1], gap="large")

        with left:
            render_advisory(advisory)

        with right:
            st.markdown('<div class="bw-card">', unsafe_allow_html=True)

            st.markdown(
                '<div class="bw-label">Profile used for personalization</div>',
                unsafe_allow_html=True,
            )

            profile_rows = [
                ("Age group", profile.age_group),
                ("Health sensitivity", profile.health_sensitivity),
                ("Occupation", profile.occupation),
            ]

            for label, value in profile_rows:
                st.markdown(
                    f"""
                    <div style="
                        display:flex;
                        justify-content:space-between;
                        gap:.7rem;
                        padding:.72rem 0;
                        border-bottom:1px solid #edf2f0;
                        font-size:.82rem
                    ">
                        <span style="color:#6e7f7b">{esc(label)}</span>
                        <strong style="color:#17312e">{esc(value)}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                '<div class="bw-mini">Risk change</div>',
                unsafe_allow_html=True,
            )

            comparison = (
                f"{previous_score} → {risk.overall_score}"
                if previous_score is not None
                else f"New → {risk.overall_score}"
            )

            st.markdown(
                f"""
                <div style="
                    font-size:1.55rem;
                    font-weight:900;
                    color:#17312e;
                    margin-top:.3rem
                ">
                    {esc(comparison)}
                </div>
                <div class="bw-muted">
                    Compared with the previous stored assessment.
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="bw-section">Current alert</div>',
            unsafe_allow_html=True,
        )

        if alert:
            st.markdown(
                f"""
                <div class="bw-alert">
                    <div class="bw-alert-title">
                        ⚠ {esc(alert.title)}
                    </div>
                    <div class="bw-muted" style="margin-top:.35rem;color:#75453a">
                        {esc(alert.message)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="bw-card"
                     style="background:#f3faf7;border-color:#dcebe5">
                    <strong style="color:#23634f">
                        ✓ No active environmental alert
                    </strong>
                    <div class="bw-muted" style="margin-top:.25rem">
                        Conditions are being monitored for changes.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div class="bw-section">Recent trend</div>',
            unsafe_allow_html=True,
        )

        t1, t2 = st.columns([1.5, 1], gap="large")

        with t1:
            render_trend_preview(
                get_trend_data(
                    profile.user_id,
                    limit=48,
                )
            )

        with t2:
            st.markdown('<div class="bw-card">', unsafe_allow_html=True)

            st.markdown(
                '<div class="bw-label">Environmental snapshot</div>',
                unsafe_allow_html=True,
            )

            snapshot = [
                ("AQI", fmt(aqi.us_aqi, decimals=0)),
                ("PM2.5", fmt(aqi.pm2_5, decimals=1)),
                ("Temperature", fmt(weather.temperature_c, "°C")),
                ("Humidity", fmt(weather.humidity_pct, "%")),
            ]

            for label, value in snapshot:
                st.markdown(
                    f"""
                    <div style="
                        display:flex;
                        justify-content:space-between;
                        padding:.7rem 0;
                        border-bottom:1px solid #edf2f0;
                        font-size:.82rem
                    ">
                        <span style="color:#71827e">{esc(label)}</span>
                        <strong style="color:#17312e">{esc(value)}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                """
                <div class="bw-note" style="margin-top:.8rem">
                    Use the Trends page for a longer view of collected
                    environmental readings.
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

        render_forecast(weather)

        st.markdown(
            """
            <div class="bw-note" style="margin-top:1.4rem;text-align:center">
                BreatheWise AI provides environmental guidance and is not a
                medical diagnosis or substitute for professional care.
            </div>
            """,
            unsafe_allow_html=True,
        )

    except Exception as exc:
        st.error(
            "Unable to update live environmental data right now."
        )
        st.caption(str(exc))


run_dashboard()
import html
from datetime import datetime

import pandas as pd
import streamlit as st

from database.database import get_alert_history, get_profile, init_db

# ---------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------
init_db()

st.markdown(
    """
    <style>
    .history-hero {
        padding: 1.6rem 1.7rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #123b36, #0f766e);
        color: white;
        margin-bottom: 1.3rem;
        box-shadow: 0 18px 40px rgba(17, 59, 54, 0.14);
    }

    .history-kicker {
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        opacity: 0.78;
    }

    .history-title {
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin-top: 0.35rem;
        line-height: 1.08;
    }

    .history-subtitle {
        margin-top: 0.45rem;
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.92rem;
        line-height: 1.5;
    }

    .history-summary {
        padding: 1rem 1.1rem;
        border: 1px solid #e3ece9;
        border-radius: 18px;
        background: white;
        box-shadow: 0 8px 24px rgba(21, 52, 48, 0.05);
    }

    .summary-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 800;
        color: #73827e;
    }

    .summary-number {
        font-size: 1.9rem;
        font-weight: 900;
        color: #17312e;
        margin-top: 0.2rem;
    }

    .alert-title {
        font-size: 1rem;
        font-weight: 850;
        color: #17312e;
    }

    .alert-message {
        color: #53645f;
        font-size: 0.86rem;
        line-height: 1.6;
        margin-top: 0.5rem;
    }

    .alert-time {
        font-size: 0.72rem;
        color: #7a8985;
        margin-top: 0.25rem;
    }

    .high-badge {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        border-radius: 999px;
        background: #fee2e2;
        color: #991b1b;
        font-size: 0.67rem;
        font-weight: 850;
        text-transform: uppercase;
    }

    .moderate-badge {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        border-radius: 999px;
        background: #fef3c7;
        color: #92400e;
        font-size: 0.67rem;
        font-weight: 850;
        text-transform: uppercase;
    }

    .low-badge {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        border-radius: 999px;
        background: #dcfce7;
        color: #166534;
        font-size: 0.67rem;
        font-weight: 850;
        text-transform: uppercase;
    }

    .other-badge {
        display: inline-block;
        padding: 0.3rem 0.6rem;
        border-radius: 999px;
        background: #e8efed;
        color: #52635f;
        font-size: 0.67rem;
        font-weight: 850;
        text-transform: uppercase;
    }

    .empty-history {
        padding: 2.5rem 1rem;
        text-align: center;
        border: 1px dashed #dce7e4;
        border-radius: 20px;
        background: white;
        color: #71817d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def safe_text(value):
    """Safely convert values to displayable text."""
    if value is None:
        return ""
    return html.escape(str(value))


def get_badge_class(level):
    level = str(level or "").lower()

    if "high" in level:
        return "high-badge"

    if "moderate" in level:
        return "moderate-badge"

    if "low" in level:
        return "low-badge"

    return "other-badge"


def format_timestamp(timestamp):
    """Convert stored timestamp to a readable local timestamp."""
    if not timestamp:
        return "Time unavailable"

    try:
        dt = datetime.fromisoformat(
            str(timestamp).replace("Z", "+00:00")
        )

        return dt.astimezone().strftime(
            "%d %b %Y · %I:%M %p"
        )

    except (ValueError, TypeError):
        return str(timestamp)


# ---------------------------------------------------------
# PROFILE
# ---------------------------------------------------------
profile = get_profile()

st.markdown(
    f"""
    <div class="history-hero">
        <div class="history-kicker">Alerts & History</div>
        <div class="history-title">Your environmental alert history.</div>
        <div class="history-subtitle">
            Review previous alerts generated for
            {safe_text(profile.location_name if profile else "your location")}.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# PROFILE CHECK
# ---------------------------------------------------------
if not profile:
    st.warning("Complete your profile first.")

    if st.button(
        "Open Profile",
        type="primary",
        use_container_width=False,
    ):
        st.switch_page("pages/profile.py")

    st.stop()


# ---------------------------------------------------------
# LOAD HISTORY
# ---------------------------------------------------------
rows = get_alert_history(
    profile.user_id,
    limit=50,
)


# ---------------------------------------------------------
# EMPTY STATE
# ---------------------------------------------------------
if not rows:
    st.markdown(
        """
        <div class="empty-history">
            <div style="font-size:2rem;">🔔</div>
            <div style="
                font-size:1rem;
                font-weight:850;
                color:#38524c;
                margin-top:.45rem;
            ">
                No alerts yet
            </div>
            <div style="
                margin-top:.3rem;
                font-size:.82rem;
            ">
                Environmental alerts will appear here when
                significant risk conditions are detected.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


# ---------------------------------------------------------
# SUMMARY COUNTS
# ---------------------------------------------------------
df = pd.DataFrame(
    [dict(row) for row in rows]
)

risk_values = df["risk_level"].astype(str)

total_alerts = len(df)

high_alerts = int(
    risk_values.str.contains(
        "high",
        case=False,
        na=False,
    ).sum()
)

moderate_alerts = int(
    risk_values.str.contains(
        "moderate",
        case=False,
        na=False,
    ).sum()
)

low_alerts = int(
    risk_values.str.contains(
        "low",
        case=False,
        na=False,
    ).sum()
)


# ---------------------------------------------------------
# SUMMARY CARDS
# ---------------------------------------------------------
st.markdown(
    "### Alert overview"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="history-summary">
            <div class="summary-label">Total alerts</div>
            <div class="summary-number">{total_alerts}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="history-summary">
            <div class="summary-label">High risk</div>
            <div class="summary-number">{high_alerts}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="history-summary">
            <div class="summary-label">Moderate</div>
            <div class="summary-number">{moderate_alerts}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
        <div class="history-summary">
            <div class="summary-label">Low risk</div>
            <div class="summary-number">{low_alerts}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    "<div style='height:0.7rem'></div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# FILTER
# ---------------------------------------------------------
filter_value = st.selectbox(
    "Filter alerts",
    [
        "All",
        "High",
        "Moderate",
        "Low",
    ],
)

filtered_rows = rows

if filter_value != "All":
    filtered_rows = [
        row
        for row in rows
        if filter_value.lower()
        in str(row["risk_level"]).lower()
    ]


# ---------------------------------------------------------
# FILTER EMPTY STATE
# ---------------------------------------------------------
if not filtered_rows:
    st.info(
        f"No {filter_value.lower()} alerts were found."
    )
    st.stop()


# ---------------------------------------------------------
# ALERT CARDS
# ---------------------------------------------------------
st.markdown(
    "### Previous alerts"
)

for row in filtered_rows:

    risk_level = str(
        row["risk_level"] or "Unknown"
    )

    title = str(
        row["title"] or "Environmental alert"
    )

    message = str(
        row["message"] or "No additional details available."
    )

    timestamp = format_timestamp(
        row["timestamp"]
    )

    badge_class = get_badge_class(
        risk_level
    )

    with st.container(border=True):

        top_left, top_right = st.columns(
            [3.7, 1.3]
        )

        with top_left:

            st.markdown(
                f"""
                <span class="{badge_class}">
                    {safe_text(risk_level)}
                </span>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="alert-title">
                    {safe_text(title)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with top_right:

            st.markdown(
                f"""
                <div class="alert-time" style="text-align:right;">
                    {safe_text(timestamp)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="alert-message">
                {safe_text(message)}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# FOOTER NOTE
# ---------------------------------------------------------
st.markdown(
    """
    <div style="
        margin-top:1.3rem;
        padding:.85rem 1rem;
        border-radius:15px;
        background:#f5faf8;
        border:1px solid #e1ece8;
        color:#61726d;
        font-size:.76rem;
        line-height:1.5;
        text-align:center;
    ">
        BreatheWise AI provides environmental guidance and is not
        a medical diagnosis or substitute for professional care.
    </div>
    """,
    unsafe_allow_html=True,
)
# app.py

import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="BreatheWise AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# GLOBAL STYLING
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- App background ---------- */
    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(15,118,110,.055), transparent 28%),
            radial-gradient(circle at 90% 10%, rgba(22,101,52,.035), transparent 24%),
            #f6faf8;
    }

    /* ---------- Main content width ---------- */
    .block-container {
        max-width: 1450px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102f2b 0%, #123b36 100%);
        border-right: 1px solid rgba(255,255,255,.07);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }

    [data-testid="stSidebar"] * {
        color: #e9f5f2;
    }

    /* ---------- Sidebar brand ---------- */
    .bw-side-brand {
        padding: .55rem .35rem 1.15rem .35rem;
        margin-bottom: .55rem;
        border-bottom: 1px solid rgba(255,255,255,.10);
    }

    .bw-side-logo {
        display: flex;
        align-items: center;
        gap: .65rem;
    }

    .bw-side-icon {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 13px;
        background: rgba(255,255,255,.11);
        font-size: 1.2rem;
    }

    .bw-side-title {
        font-size: 1.08rem;
        font-weight: 900;
        letter-spacing: -.025em;
        line-height: 1.05;
    }

    .bw-side-subtitle {
        margin-top: .22rem;
        font-size: .67rem;
        color: rgba(233,245,242,.62);
        line-height: 1.4;
    }

    /* ---------- Sidebar information cards ---------- */
    .bw-side-card {
        margin-top: .85rem;
        padding: .82rem .85rem;
        border-radius: 15px;
        background: rgba(255,255,255,.065);
        border: 1px solid rgba(255,255,255,.075);
    }

    .bw-side-label {
        font-size: .63rem;
        letter-spacing: .1em;
        text-transform: uppercase;
        font-weight: 850;
        color: rgba(233,245,242,.58);
    }

    .bw-side-value {
        margin-top: .25rem;
        font-size: .83rem;
        font-weight: 800;
        color: #ffffff;
    }

    .bw-side-small {
        margin-top: .18rem;
        font-size: .69rem;
        color: rgba(233,245,242,.63);
        line-height: 1.45;
    }

    .bw-live-status {
        display: inline-flex;
        align-items: center;
        gap: .4rem;
        padding: .31rem .55rem;
        border-radius: 999px;
        background: rgba(99,230,190,.11);
        color: #b7f4df;
        font-size: .66rem;
        font-weight: 850;
    }

    .bw-live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #63e6be;
        box-shadow: 0 0 0 4px rgba(99,230,190,.08);
    }

    /* ---------- Hide default Streamlit decoration ---------- */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border-radius: 12px;
        font-weight: 800;
    }

    /* ---------- Inputs ---------- */
    input,
    textarea,
    [data-baseweb="select"] > div {
        border-radius: 11px !important;
    }

    /* ---------- Links ---------- */
    a {
        text-decoration: none !important;
    }

    /* ---------- Mobile improvements ---------- */
    @media (max-width: 900px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "app_initialized" not in st.session_state:
    st.session_state.app_initialized = True

# ---------------------------------------------------------
# SIDEBAR BRANDING
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="bw-side-brand">
            <div class="bw-side-logo">
                <div class="bw-side-icon">🌿</div>
                <div>
                    <div class="bw-side-title">BreatheWise AI</div>
                    <div class="bw-side-subtitle">
                        Personalized environmental intelligence
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # LIVE STATUS
    # -----------------------------------------------------
    st.markdown(
        """
        <div class="bw-side-card">
            <span class="bw-live-status">
                <span class="bw-live-dot"></span>
                LIVE MONITORING
            </span>
            <div class="bw-side-small">
                Weather and air-quality conditions are updated
                from connected environmental data sources.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# PAGE NAVIGATION
# ---------------------------------------------------------
dashboard_page = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="🏠",
    default=True,
)

profile_page = st.Page(
    "pages/profile.py",
    title="My Profile",
    icon="👤",
)

trends_page = st.Page(
    "pages/trends.py",
    title="Trends",
    icon="📈",
)

history_page = st.Page(
    "pages/history.py",
    title="Alert History",
    icon="🔔",
)

navigation = st.navigation(
    {
        "BreatheWise": [
            dashboard_page,
            profile_page,
            trends_page,
            history_page,
        ]
    }
)

# ---------------------------------------------------------
# RUN SELECTED PAGE
# ---------------------------------------------------------
navigation.run()
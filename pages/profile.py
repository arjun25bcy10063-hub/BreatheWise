from html import escape

import streamlit as st

from database.database import get_profile, init_db, save_profile
from models.schemas import UserProfile
from services.location_service import search_locations
from utils.constants import (
    AGE_GROUPS,
    HEALTH_SENSITIVITY_OPTIONS,
    OCCUPATIONS,
)

init_db()

st.markdown(
    """
    <style>
    .pf-wrap{max-width:1000px;margin:0 auto 2rem}
    .pf-hero{padding:1.55rem 1.6rem;border-radius:24px;background:linear-gradient(135deg,#123b36,#0f766e);color:white;box-shadow:0 18px 40px rgba(17,59,54,.13);margin-bottom:1.15rem}
    .pf-kicker{font-size:.72rem;font-weight:850;letter-spacing:.14em;text-transform:uppercase;opacity:.78}
    .pf-title{font-size:2.2rem;font-weight:900;letter-spacing:-.045em;line-height:1.08;margin:.4rem 0 .45rem}
    .pf-sub{font-size:.92rem;line-height:1.55;color:rgba(255,255,255,.8)}
    .pf-card{background:#fff;border:1px solid #e4ece9;border-radius:21px;padding:1.25rem;box-shadow:0 10px 28px rgba(21,52,48,.055);margin-bottom:1rem}
    .pf-section{font-size:1rem;font-weight:850;color:#17312e;margin-bottom:.7rem}
    .pf-note{padding:.8rem .9rem;border-radius:14px;background:#f5faf8;border:1px solid #e1ece8;color:#5a6d68;font-size:.78rem;line-height:1.5}
    .pf-location{padding:.9rem 1rem;border-radius:16px;background:#eef8f5;border:1px solid #d8ece6;color:#205c50;margin-top:.7rem}
    .pf-chip{display:inline-block;padding:.33rem .6rem;border-radius:999px;background:#e8f4f1;color:#2e665b;font-size:.72rem;font-weight:800;margin:.18rem .18rem 0 0}
    .pf-help{font-size:.76rem;color:#71817d;line-height:1.5}
    </style>
    """,
    unsafe_allow_html=True,
)


def esc(value):
    return escape(str(value))


existing = get_profile() or UserProfile()

st.markdown(
    """
    <div class="pf-hero">
        <div class="pf-kicker">Personalization</div>
        <div class="pf-title">Build your environment profile.</div>
        <div class="pf-sub">
            Your profile helps BreatheWise interpret the same environmental
            conditions differently for different people.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="pf-wrap">', unsafe_allow_html=True)

st.markdown(
    '<div class="pf-card"><div class="pf-section">1 · Choose your location</div>',
    unsafe_allow_html=True,
)

with st.form("location_search_form"):
    city = st.text_input(
        "Search city or location",
        value=existing.location_name,
        placeholder="Enter a city or location",
    )

    search = st.form_submit_button(
        "Search location",
        use_container_width=True,
    )

if search:
    if not city.strip():
        st.warning("Enter a location to search.")
    else:
        try:
            results = search_locations(city.strip())

            if results:
                st.session_state["location_results"] = results
            else:
                st.session_state.pop("location_results", None)
                st.warning("No matching locations found.")

        except Exception as exc:
            st.error("Location search failed.")
            st.caption(str(exc))

results = st.session_state.get("location_results", [])
selected_location = None

if results:
    labels = [
        f"{r.name}, {r.country}" if r.country else r.name
        for r in results
    ]

    selected_label = st.selectbox(
        "Select the matching location",
        labels,
        key="profile_location_choice",
    )

    selected_location = results[labels.index(selected_label)]

    st.markdown(
        f"""
        <div class="pf-location">
            📍 <strong>{esc(selected_location.name)}</strong>
            {f", {esc(selected_location.country)}"
             if selected_location.country else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

elif existing.location_name and existing.latitude is not None:
    st.markdown(
        f"""
        <div class="pf-note">
            Saved location:
            <strong>{esc(existing.location_name)}</strong>.
            Search again to choose a different location.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<div class="pf-card"><div class="pf-section">2 · Tell us about your exposure profile</div>',
    unsafe_allow_html=True,
)

with st.form("profile_form"):
    age_index = (
        AGE_GROUPS.index(existing.age_group)
        if existing.age_group in AGE_GROUPS
        else 1
    )

    health_index = (
        HEALTH_SENSITIVITY_OPTIONS.index(existing.health_sensitivity)
        if existing.health_sensitivity in HEALTH_SENSITIVITY_OPTIONS
        else 0
    )

    occupation_index = (
        OCCUPATIONS.index(existing.occupation)
        if existing.occupation in OCCUPATIONS
        else 0
    )

    age_group = st.selectbox(
        "Age group",
        AGE_GROUPS,
        index=age_index,
    )

    health = st.selectbox(
        "Health sensitivity",
        HEALTH_SENSITIVITY_OPTIONS,
        index=health_index,
    )

    occupation = st.selectbox(
        "Occupation / exposure",
        OCCUPATIONS,
        index=occupation_index,
    )

    st.markdown(
        '<div class="pf-help">These categories are used only to personalize environmental guidance.</div>',
        unsafe_allow_html=True,
    )

    save = st.form_submit_button(
        "Save profile",
        type="primary",
        use_container_width=True,
    )

if save:
    current_city = city.strip()

    if selected_location is not None:
        location_name = selected_location.name
        latitude = selected_location.latitude
        longitude = selected_location.longitude

    elif (
        current_city
        and current_city == existing.location_name
        and existing.latitude is not None
        and existing.longitude is not None
    ):
        location_name = existing.location_name
        latitude = existing.latitude
        longitude = existing.longitude

    else:
        st.error(
            "Search and select a location before saving a new location."
        )

        location_name = None
        latitude = None
        longitude = None

    if location_name is not None:
        profile = UserProfile(
            user_id=1,
            age_group=age_group,
            health_sensitivity=health,
            occupation=occupation,
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
        )

        save_profile(profile)

        st.session_state.pop(
            "location_results",
            None,
        )

        st.success("Profile saved successfully.")
        st.switch_page("pages/dashboard.py")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<div class="pf-card"><div class="pf-section">What your profile changes</div>',
    unsafe_allow_html=True,
)

current_age = age_group if "age_group" in locals() else existing.age_group
current_health = health if "health" in locals() else existing.health_sensitivity
current_occupation = (
    occupation
    if "occupation" in locals()
    else existing.occupation
)

for chip in [current_age, current_health, current_occupation]:
    st.markdown(
        f'<span class="pf-chip">{esc(chip)}</span>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="pf-note" style="margin-top:.75rem">
        The app uses these categories to personalize environmental guidance.
        It does not diagnose conditions or replace professional medical care.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div></div>", unsafe_allow_html=True)
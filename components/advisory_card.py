import streamlit as st


def render_advisory_card(advisory):
    st.subheader("Personalized Advisory")
    st.info(advisory.summary)
    for action in advisory.actions:
        st.write(f"✓ {action}")
    st.write(f"**Outdoor guidance:** {advisory.outdoor_guidance}")
    st.write(f"**Why this advice:** {advisory.personalization_reason}")
    st.caption(advisory.disclaimer)

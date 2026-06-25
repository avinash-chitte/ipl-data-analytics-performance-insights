"""
app.py — IPL Intelligence Hub: Analytics & Match Prediction Platform
Main entry point. Handles navigation, global filters, data loading, and page routing.
"""

import streamlit as st
import sys
import os
import logging

# ── Logging Setup ──
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-20s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ipl_hub")

# ── Ensure src/ is importable ──
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.constants import APP_TITLE, APP_SUBTITLE, APP_ICON, NAV_PAGES
from src.styles import inject_css, section_divider
from src.data_loader import load_data
from src.preprocessing import engineer_features

# ── Page Config ──
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject CSS ──
inject_css()

# ── Load & Process Data ──
raw_df = load_data()
ipl_df = engineer_features(raw_df)

# ──────────────────────────────────────────────
# SIDEBAR — Navigation + Global Filters
# ──────────────────────────────────────────────
with st.sidebar:
    # Branding
    st.markdown(f"""
    <div style="text-align:center; padding:1.2rem 0 1rem;">
        <span style="font-size:2.8rem;">{APP_ICON}</span>
        <h2 style="margin:0.4rem 0 0; font-weight:800; font-size:1.15rem;
                    letter-spacing:-0.01em; color:#fafafa;">
            {APP_TITLE}
        </h2>
        <p style="margin:0; font-size:0.7rem; color:#52525b; font-weight:500;">
            {APP_SUBTITLE}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:0; border-top:1px solid #1e1e24; margin:0.5rem 0 1rem;'/>",
                unsafe_allow_html=True)

    # Navigation
    st.markdown("""
    <p style="font-size:0.68rem; color:#52525b; font-weight:600;
              text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.3rem;">
        Navigation
    </p>
    """, unsafe_allow_html=True)

    page_labels = list(NAV_PAGES.keys())
    selected_page = st.radio(
        "nav", options=page_labels, index=0, label_visibility="collapsed",
    )
    page_key = NAV_PAGES[selected_page]

    st.markdown("<hr style='border:0; border-top:1px solid #1e1e24; margin:1rem 0;'/>",
                unsafe_allow_html=True)

    # Global Filters
    st.markdown("""
    <p style="font-size:0.68rem; color:#52525b; font-weight:600;
              text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.3rem;">
        Filters
    </p>
    """, unsafe_allow_html=True)

    years = sorted(ipl_df["year"].unique())
    min_yr, max_yr = int(min(years)), int(max(years))
    yr_range = st.slider("Season Range", min_yr, max_yr, (min_yr, max_yr), key="yr_range")

    teams_list = sorted(ipl_df["batting_team"].dropna().unique().tolist())
    selected_teams = st.multiselect("Filter Teams", teams_list, default=teams_list[:6], key="teams")

    # Sidebar footer
    st.markdown("""
    <div style="position:fixed; bottom:0; padding:0.8rem 1rem; font-size:0.65rem; color:#3f3f46;">
        Built with Streamlit & Plotly<br>
        © 2025 IPL Intelligence Hub
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# APPLY GLOBAL FILTERS
# ──────────────────────────────────────────────
filtered_df = ipl_df[
    (ipl_df["year"] >= yr_range[0]) & (ipl_df["year"] <= yr_range[1])
].copy()

if selected_teams:
    filtered_df = filtered_df[
        filtered_df["batting_team"].isin(selected_teams) |
        filtered_df["bowling_team"].isin(selected_teams)
    ]

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex; align-items:center; gap:12px; margin-bottom:0.2rem;">
    <span style="font-size:2.2rem;">{APP_ICON}</span>
    <div>
        <h1 style="margin:0; font-size:1.8rem; font-weight:900; letter-spacing:-0.025em; color:#fafafa;">
            {APP_TITLE}
        </h1>
        <p style="margin:0; font-size:0.78rem; color:#52525b; font-weight:500;">
            {APP_SUBTITLE}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

section_divider()

# ──────────────────────────────────────────────
# PAGE ROUTING
# ──────────────────────────────────────────────
if page_key == "overview":
    from views.overview import render
    render(ipl_df, filtered_df)

elif page_key == "team_performance":
    from views.team_performance import render
    render(ipl_df, filtered_df, teams_list)

elif page_key == "player_explorer":
    from views.player_explorer import render
    render(ipl_df, filtered_df)

elif page_key == "venue_intelligence":
    from views.venue_intelligence import render
    render(ipl_df, filtered_df)

elif page_key == "powerplay_death":
    from views.powerplay_death import render
    render(ipl_df, filtered_df)

elif page_key == "match_predictor":
    from views.match_predictor import render
    render(ipl_df, filtered_df)

elif page_key == "key_insights":
    from views.key_insights import render
    render(ipl_df, filtered_df)

"""
constants.py — IPL Intelligence Hub
Central configuration: team colors, phase definitions, app metadata.
"""

# ──────────────────────────────────────────────
# App Metadata
# ──────────────────────────────────────────────
APP_TITLE = "IPL Intelligence Hub"
APP_SUBTITLE = "Analytics & Match Prediction Platform  •  2008–2025"
APP_VERSION = "2.0.0"
APP_ICON = "🏏"

# ──────────────────────────────────────────────
# Navigation Pages
# ──────────────────────────────────────────────
NAV_PAGES = {
    "📊 Overview": "overview",
    "⚔️ Team Performance": "team_performance",
    "🧑‍💻 Player Explorer": "player_explorer",
    "🏟️ Venue Intelligence": "venue_intelligence",
    "⚡ Powerplay & Death": "powerplay_death",
    "🤖 Match Predictor": "match_predictor",
    "💡 Key Insights": "key_insights",
}

# ──────────────────────────────────────────────
# Official IPL Team Colors (all 13 franchises)
# ──────────────────────────────────────────────
TEAM_COLORS = {
    "Chennai Super Kings": "#F7E115",
    "Mumbai Indians": "#004B87",
    "Royal Challengers Bangalore": "#EC1C24",
    "Royal Challengers Bengaluru": "#EC1C24",
    "Kolkata Knight Riders": "#2E0854",
    "Rajasthan Royals": "#EA1B85",
    "Delhi Capitals": "#000080",
    "Delhi Daredevils": "#DD1F26",
    "Punjab Kings": "#DD1F26",
    "Kings XI Punjab": "#DD1F26",
    "Sunrisers Hyderabad": "#FF822A",
    "Deccan Chargers": "#0D2240",
    "Gujarat Titans": "#1B252C",
    "Lucknow Super Giants": "#0057E7",
    "Rising Pune Supergiant": "#D11D5B",
    "Rising Pune Supergiants": "#D11D5B",
    "Kochi Tuskers Kerala": "#FF8000",
    "Pune Warriors": "#2F4F4F",
    "Gujarat Lions": "#FF7C24",
}

# Curated palette for generic charts
CHART_PALETTE = [
    "#2563eb", "#f97316", "#10b981", "#8b5cf6",
    "#ec4899", "#f59e0b", "#06b6d4", "#ef4444",
    "#84cc16", "#6366f1", "#14b8a6", "#e11d48",
]

# ──────────────────────────────────────────────
# Match Phase Definitions
# ──────────────────────────────────────────────
PHASE_BINS = [-1, 5, 14, 20]
PHASE_LABELS = ["Powerplay", "Middle Overs", "Death Overs"]
PHASE_COLORS = {
    "Powerplay": "#2563eb",
    "Middle Overs": "#f59e0b",
    "Death Overs": "#ef4444",
}

# ──────────────────────────────────────────────
# ML Model Config
# ──────────────────────────────────────────────
MODEL_FEATURES = [
    "runs_needed",
    "balls_remaining",
    "wickets_lost",
    "required_run_rate",
    "current_run_rate",
]
MODEL_TEST_YEAR_CUTOFF = 2023

# ──────────────────────────────────────────────
# Simulated Data Config
# ──────────────────────────────────────────────
SIM_TEAMS = [
    "Chennai Super Kings", "Mumbai Indians",
    "Royal Challengers Bangalore", "Kolkata Knight Riders",
    "Rajasthan Royals", "Delhi Capitals",
    "Punjab Kings", "Sunrisers Hyderabad",
]
SIM_VENUES = [
    "Wankhede Stadium", "M Chinnaswamy Stadium",
    "MA Chidambaram Stadium", "Eden Gardens",
    "Rajiv Gandhi Intl Cricket Stadium",
    "Arun Jaitley Stadium", "Narendra Modi Stadium",
    "IS Bindra Stadium", "Sawai Mansingh Stadium",
]
SIM_BATTERS = [
    "V Kohli", "RG Sharma", "S Dhawan", "DA Warner",
    "SK Raina", "MS Dhoni", "AB de Villiers", "CH Gayle",
    "KL Rahul", "SA Yadav", "F du Plessis", "JC Buttler",
    "SV Samson", "HH Pandya", "RR Pant",
]
SIM_BOWLERS = [
    "YS Chahal", "DJ Bravo", "PP Chawla", "A Mishra",
    "R Ashwin", "SP Narine", "SL Malinga", "JJ Bumrah",
    "B Kumar", "T Natarajan", "Rashid Khan", "K Rabada",
    "MA Starc", "TA Boult", "Mohammed Shami",
]

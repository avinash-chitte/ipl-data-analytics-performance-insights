import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add src/ to path to enable preprocessing imports
sys.path.append(os.path.abspath('src'))

# ----------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="IPL Analytics & Insights",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# 2. SESSION STATE & THEME SETUP
# ----------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

IS_DARK = st.session_state.theme == "dark"

# Define theme colors for CSS
bg_color = "#09090b" if IS_DARK else "#ffffff"
bg_subtle = "#0c0c0f" if IS_DARK else "#f9fafb"
card_color = "#0c0c0f" if IS_DARK else "#ffffff"
card_hover = "#131316" if IS_DARK else "#f4f4f5"
border_color = "#1e1e24" if IS_DARK else "#e4e4e7"
border_subtle = "#16161a" if IS_DARK else "#f0f0f2"
text_color = "#fafafa" if IS_DARK else "#09090b"
text_dim = "#52525b" if IS_DARK else "#a1a1aa"
shadow_style = "none" if IS_DARK else "0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03)"
green_color = "#22c55e" if IS_DARK else "#16a34a"
green_muted = "rgba(34,197,94,0.12)" if IS_DARK else "rgba(22,163,74,0.08)"
red_color = "#ef4444" if IS_DARK else "#dc2626"
red_muted = "rgba(239,68,68,0.12)" if IS_DARK else "rgba(220,38,38,0.08)"

# Inject Custom CSS
st.markdown(f"""
<style>
    /* Global Styles */
    :root {{
        --bg: {bg_color};
        --bg-subtle: {bg_subtle};
        --card: {card_color};
        --card-hover: {card_hover};
        --border: {border_color};
        --border-subtle: {border_subtle};
        --text: {text_color};
        --text-muted: #71717a;
        --text-dim: {text_dim};
        --accent: #2563eb;
        --shadow: {shadow_style};
        --radius: 10px;
        --green: {green_color};
        --green-muted: {green_muted};
        --red: {red_color};
        --red-muted: {red_muted};
    }}
    
    /* Hide Streamlit default components */
    header[data-testid="stHeader"], footer, .stDeployButton {{
        display: none !important;
    }}
    
    /* App container padding overrides */
    .block-container {{
        padding: 2rem 2.5rem 3rem !important;
        max-width: 1360px !important;
    }}
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', -apple-system, sans-serif !important;
    }}
    
    /* Custom Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: var(--bg-subtle) !important;
        border-right: 1px solid var(--border) !important;
    }}
    
    /* Card Styles */
    .metric-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.1rem 1.3rem;
        box-shadow: var(--shadow);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .metric-card:hover {{
        border-color: var(--accent);
        transform: translateY(-2px);
    }}
    .metric-label {{
        font-size: 0.78rem;
        color: var(--text-muted);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .metric-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text);
        letter-spacing: -0.03em;
        margin-top: 0.25rem;
    }}
    .metric-delta {{
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 0.4rem;
        padding: 2px 8px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        gap: 3px;
    }}
    .delta-up {{
        color: var(--green);
        background: var(--green-muted);
    }}
    .delta-down {{
        color: var(--red);
        background: var(--red-muted);
    }}
    
    /* Chart Container Wrapping */
    .chart-wrap {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.2rem;
        box-shadow: var(--shadow);
        margin-bottom: 1.25rem;
    }}
    .chart-title {{
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text);
    }}
    .chart-subtitle {{
        font-size: 0.73rem;
        color: var(--text-dim);
        margin-bottom: 0.8rem;
    }}
    
    /* Custom HTML Table Styles */
    .data-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.8rem;
        margin: 0.5rem 0;
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
    }}
    .data-table th {{
        text-align: left;
        padding: 0.75rem 0.9rem;
        background: var(--bg-subtle);
        color: var(--text-muted);
        font-weight: 600;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid var(--border);
    }}
    .data-table td {{
        padding: 0.75rem 0.9rem;
        color: var(--text);
        border-bottom: 1px solid var(--border-subtle);
    }}
    .data-table tr:last-child td {{
        border-bottom: none;
    }}
    .data-table tr:hover {{
        background-color: var(--card-hover);
    }}
    
    /* Badges */
    .badge {{
        display: inline-block;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 500;
    }}
    .badge-csk {{ color: #F7E115; background: rgba(247,225,21,0.12); }}
    .badge-mi {{ color: #3B82F6; background: rgba(59,130,246,0.12); }}
    .badge-rcb {{ color: #EF4444; background: rgba(239,68,68,0.12); }}
    .badge-kkr {{ color: #A78BFA; background: rgba(167,139,250,0.12); }}
    
    /* Tabs styling overrides */
    button[data-baseweb="tab"] {{
        background: transparent !important;
        color: var(--text-muted) !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.1rem !important;
        border: 1px solid transparent !important;
        border-radius: 7px !important;
        margin-right: 4px;
        transition: all 0.2s ease;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: var(--text) !important;
        background: var(--card) !important;
        border-color: var(--border) !important;
    }}
    [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{
        display: none !important;
    }}
    [data-baseweb="tab-list"] {{
        background: var(--bg-subtle) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 4px;
        gap: 2px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. HELPER FUNCTIONS: DATA LOADING & PREPROCESSING
# ----------------------------------------------------
@st.cache_data
def get_dashboard_data():
    """
    Loads raw IPL data and executes the feature engineering script.
    Generates realistic simulated data if local files are missing.
    """
    try:
        # Check standard paths
        paths_to_try = ['data/IPL.csv', '../data/IPL.csv', 'IPL.csv']
        df_raw = None
        for p in paths_to_try:
            if os.path.exists(p):
                df_raw = pd.read_csv(p)
                break
        if df_raw is None:
            # Try load kaggle path
            if os.path.exists('/kaggle/input/ipl-dataset2008-2025/IPL.csv'):
                df_raw = pd.read_csv('/kaggle/input/ipl-dataset2008-2025/IPL.csv')
                
        if df_raw is None:
            raise FileNotFoundError("IPL.csv not found locally.")
            
        # Parse dates
        df_raw['date'] = pd.to_datetime(df_raw['date'])
        df_raw['year'] = df_raw['date'].dt.year
        df_raw['season'] = df_raw['year'].astype(str)
        
    except Exception as e:
        # Fallback to simulated data structure
        np.random.seed(42)
        n_balls = 15000
        mock_matches = 80
        
        teams = ['Chennai Super Kings', 'Mumbai Indians', 'Royal Challengers Bangalore', 
                 'Kolkata Knight Riders', 'Rajasthan Royals', 'Delhi Capitals', 'Punjab Kings', 'Sunrisers Hyderabad']
        venues = ['Wankhede Stadium', 'M Chinnaswamy Stadium', 'MA Chidambaram Stadium', 'Eden Gardens', 'Rajiv Gandhi International Stadium']
        batters_pool = ['V Kohli', 'RG Sharma', 'S Dhawan', 'DA Warner', 'SK Raina', 'MS Dhoni', 'AB de Villiers', 'CH Gayle', 'KL Rahul']
        bowlers_pool = ['YS Chahal', 'DJ Bravo', 'PP Chawla', 'A Mishra', 'R Ashwin', 'SP Narine', 'SL Malinga', 'JJ Bumrah', 'B Kumar']
        
        mock_data = {
            'match_id': np.random.randint(100001, 100001 + mock_matches, size=n_balls),
            'date': pd.date_range(start='2008-04-18', end='2025-06-01', periods=n_balls),
            'innings': np.random.choice([1, 2], p=[0.5, 0.5], size=n_balls),
            'batting_team': np.random.choice(teams, size=n_balls),
            'over': np.random.randint(0, 20, size=n_balls),
            'ball': np.random.randint(1, 7, size=n_balls),
            'valid_ball': np.ones(n_balls, dtype=int),
            'batter': np.random.choice(batters_pool, size=n_balls),
            'bat_pos': np.random.randint(1, 8, size=n_balls),
            'runs_batter': np.random.choice([0, 1, 2, 4, 6], p=[0.38, 0.38, 0.08, 0.11, 0.05], size=n_balls),
            'runs_extras': np.random.choice([0, 1, 4], p=[0.94, 0.05, 0.01], size=n_balls),
            'bowler': np.random.choice(bowlers_pool, size=n_balls),
            'wicket_kind': np.random.choice([None, 'caught', 'bowled', 'lbw', 'run out'], p=[0.95, 0.03, 0.01, 0.007, 0.003], size=n_balls),
            'player_out': [None]*n_balls,
            'runs_target': [175.0]*n_balls,
            'toss_winner': np.random.choice(teams, size=n_balls),
            'toss_decision': np.random.choice(['field', 'bat'], size=n_balls),
            'venue': np.random.choice(venues, size=n_balls),
            'city': np.random.choice(['Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad'], size=n_balls)
        }
        
        df_raw = pd.DataFrame(mock_data)
        df_raw['runs_total'] = df_raw['runs_batter'] + df_raw['runs_extras']
        df_raw['runs_bowler'] = df_raw['runs_total']
        df_raw['bowler_wicket'] = df_raw['wicket_kind'].isin(['caught', 'bowled', 'lbw']).astype(int)
        df_raw['year'] = df_raw['date'].dt.year
        df_raw['season'] = df_raw['year'].astype(str)
        # Assign matching match winner
        df_raw['match_won_by'] = np.random.choice(teams, size=n_balls)
    
    # Preprocessing & Engineering
    df = df_raw.sort_values(by=['match_id', 'innings', 'over', 'ball']).reset_index(drop=True)
    df['is_four'] = (df['runs_total'] == 4) & (df['runs_extras'] == 0)
    df['is_six'] = (df['runs_total'] == 6) & (df['runs_extras'] == 0)
    df['is_boundary'] = df['is_four'] | df['is_six']
    df['is_dot'] = (df['runs_total'] == 0) & (df['valid_ball'] == 1)
    df['is_wicket'] = df['wicket_kind'].notna().astype(int)
    
    # Cumulative aggregates
    df['cumulative_runs'] = df.groupby(['match_id', 'innings', 'batting_team'])['runs_total'].cumsum()
    df['cumulative_wickets'] = df.groupby(['match_id', 'innings', 'batting_team'])['is_wicket'].cumsum()
    df['balls_remaining'] = 120 - (df['over'] * 6 + df['ball'].clip(upper=6))
    df['balls_remaining'] = df['balls_remaining'].clip(lower=0)
    
    # Target calculations
    df['runs_needed'] = (df['runs_target'] - df['cumulative_runs']).clip(lower=0)
    df['required_run_rate'] = np.where(df['balls_remaining'] > 0, (df['runs_needed'] * 6) / df['balls_remaining'], 0)
    df['current_run_rate'] = np.where(120 - df['balls_remaining'] > 0, (df['cumulative_runs'] * 6) / (120 - df['balls_remaining']), 0)
    df['wickets_lost'] = df['cumulative_wickets']
    
    # Categorize match phase
    df['match_phase'] = pd.cut(df['over'], bins=[-1, 5, 14, 20], labels=['Powerplay', 'Middle Overs', 'Death Overs'])
    
    return df

# Initialize Data
ipl_df = get_dashboard_data()

# ----------------------------------------------------
# 4. TRAINING ML WIN PREDICTION MODEL (Cached)
# ----------------------------------------------------
@st.cache_resource
def get_trained_win_model(df):
    """
    Trains a Logistic Regression model on second innings live match runs.
    """
    from sklearn.linear_model import LogisticRegression
    # Filter 2nd Innings
    chase_df = df[df['innings'] == 2].copy()
    chase_df = chase_df.dropna(subset=['runs_target', 'runs_total', 'balls_remaining', 'match_won_by', 'batting_team'])
    chase_df['chase_won'] = (chase_df['batting_team'] == chase_df['match_won_by']).astype(int)
    
    model_features = ['runs_needed', 'balls_remaining', 'wickets_lost', 'required_run_rate', 'current_run_rate']
    X = chase_df[model_features]
    y = chase_df['chase_won']
    
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X, y)
    return lr

win_model = get_trained_win_model(ipl_df)

# Plotly default Layout config
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#71717a" if not IS_DARK else "#a1a1aa", size=11),
    margin=dict(l=40, r=20, t=30, b=40),
    xaxis=dict(
        gridcolor="rgba(0,0,0,0.06)" if not IS_DARK else "rgba(255,255,255,0.06)",
        zerolinecolor="rgba(0,0,0,0.06)" if not IS_DARK else "rgba(255,255,255,0.06)",
        tickfont=dict(size=10, color="#71717a"),
    ),
    yaxis=dict(
        gridcolor="rgba(0,0,0,0.06)" if not IS_DARK else "rgba(255,255,255,0.06)",
        zerolinecolor="rgba(0,0,0,0.06)" if not IS_DARK else "rgba(255,255,255,0.06)",
        tickfont=dict(size=10, color="#71717a"),
    ),
)

# Team Color palettes
TEAM_COLORS = {
    'Chennai Super Kings': '#F7E115', 'Mumbai Indians': '#004B87',
    'Royal Challengers Bangalore': '#EC1C24', 'Kolkata Knight Riders': '#2E0854',
    'Rajasthan Royals': '#EA1B85', 'Delhi Capitals': '#000080',
    'Punjab Kings': '#DD1F26', 'Sunrisers Hyderabad': '#FF822A',
    'Gujarat Titans': '#1B252C', 'Lucknow Super Giants': '#0057E7'
}

# ----------------------------------------------------
# 5. DASHBOARD LAYOUT & BRANDING HEADER
# ----------------------------------------------------
head_left, head_right = st.columns([7, 1.2])
with head_left:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 2.2rem;">🏏</span>
        <div>
            <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; letter-spacing: -0.02em; color: var(--text);">
                IPL Performance Insights
            </h1>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); font-weight: 500;">
                DATA-DRIVEN T20 ANALYTICS & INTERACTIVE DASHBOARD (2008-2025)
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
with head_right:
    theme_label = "☀️ Light Mode" if IS_DARK else "🌙 Dark Mode"
    st.button(theme_label, on_click=toggle_theme, use_container_width=True)

st.markdown("<hr style='border: 0; border-top: 1px solid var(--border); margin: 1rem 0 1.5rem;' />", unsafe_allow_html=True)

# ----------------------------------------------------
# 6. SIDEBAR INTERACTIVE FILTERS
# ----------------------------------------------------
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 1.5rem;">
    <span style="font-size: 2.5rem;">🏏</span>
    <h3 style="margin: 0.5rem 0; font-weight: 700; font-size: 1.1rem;">Dashboard Filters</h3>
</div>
""", unsafe_allow_html=True)

# Seasons Slider
seasons = sorted(ipl_df['year'].unique())
min_yr, max_yr = int(ipl_df['year'].min()), int(ipl_df['year'].max())
selected_year_range = st.sidebar.slider(
    "Select Season Range",
    min_value=min_yr,
    max_value=max_yr,
    value=(min_yr, max_yr)
)

# Teams filter
teams_list = sorted(list(set(ipl_df['batting_team'].dropna().unique())))
selected_teams = st.sidebar.multiselect(
    "Filter by Teams",
    options=teams_list,
    default=teams_list[:6]  # default select top 6
)

# Apply filters
filtered_df = ipl_df[
    (ipl_df['year'] >= selected_year_range[0]) & 
    (ipl_df['year'] <= selected_year_range[1])
]
if selected_teams:
    filtered_df = filtered_df[
        filtered_df['batting_team'].isin(selected_teams) | 
        filtered_df['bowling_team'].isin(selected_teams)
    ]

# Helper to render metric cards
def render_metric_card(label, value, delta=None, delta_type="up"):
    delta_class = "delta-up" if delta_type == "up" else "delta-down"
    arrow = "↑" if delta_type == "up" else "↓"
    delta_html = f'<div class="metric-delta {delta_class}">{arrow} {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# 7. PAGE TABS & INTERACTIVE VISUALIZATIONS
# ----------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 Summary & Scoring", 
    "🥇 Cap Winners", 
    "⚔️ Team Performance", 
    "🏟️ Venue Intelligence", 
    "🤖 Live Win Predictor"
])

# ------------------ TAB 1: SUMMARY ------------------
with tab1:
    # Calculations
    matches_played = filtered_df['match_id'].nunique()
    total_runs = filtered_df['runs_total'].sum()
    total_wickets = filtered_df['is_wicket'].sum()
    sixes = filtered_df['is_six'].sum()
    fours = filtered_df['is_four'].sum()
    runs_per_ball = total_runs / max(len(filtered_df), 1)
    boundary_pct = ((fours + sixes) / max(len(filtered_df), 1) * 100)
    
    # KPI Grid
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        render_metric_card("Matches Played", f"{matches_played:,}")
    with kpi2:
        render_metric_card("Total Runs Scored", f"{total_runs:,}")
    with kpi3:
        render_metric_card("Total Wickets Taken", f"{total_wickets:,}")
    with kpi4:
        render_metric_card("Sixes / Fours Hit", f"{sixes:,} / {fours:,}", delta=f"{boundary_pct:.1f}% Boundary%", delta_type="up")
        
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # Scoring Trends & Toss Decisions Subplots
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Season-Wise Scoring Trends</div>
            <div class="chart-subtitle">Average runs and run-rate progression across seasons</div>
        """, unsafe_allow_html=True)
        # Calculate season rates
        s_trends = filtered_df.groupby('year').agg({
            'match_id': 'nunique',
            'runs_total': 'sum',
            'valid_ball': 'sum'
        }).reset_index()
        s_trends['Avg_Runs'] = (s_trends['runs_total'] / s_trends['match_id']).round(1)
        s_trends['RPO'] = ((s_trends['runs_total'] / s_trends['valid_ball']) * 6).round(2)
        
        fig_score = go.Figure()
        fig_score.add_trace(go.Scatter(x=s_trends['year'], y=s_trends['Avg_Runs'], mode='lines+markers', name='Avg Runs/Match', line=dict(color='#2563eb', width=3.5)))
        fig_score.update_layout(**PLOT_LAYOUT, height=350, margin=dict(l=40, r=20, t=10, b=30))
        st.plotly_chart(fig_score, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Toss Winner Advantage (Win%)</div>
            <div class="chart-subtitle">Percentage of times the toss winner also wins the match</div>
        """, unsafe_allow_html=True)
        match_df = filtered_df.groupby('match_id').first().reset_index()
        match_df['toss_winner_won'] = (match_df['toss_winner'] == match_df['match_won_by']).astype(int)
        
        # Win percentages
        toss_wins = match_df['toss_winner_won'].value_counts(normalize=True) * 100
        labels = ['Toss Winner Won', 'Toss Loser Won']
        colors = ['#10B981', '#EF4444']
        
        fig_toss = go.Figure(data=[go.Pie(labels=labels, values=toss_wins.values, hole=.4, marker_colors=colors)])
        fig_toss.update_layout(**PLOT_LAYOUT, height=350, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_toss, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------ TAB 2: CAP WINNERS ------------------
with tab2:
    st.markdown("### 🥇 Season-by-Season Cap Awards")
    st.markdown("Discover the players who dominated the batting and bowling scoreboards each season.")
    
    col_bat, col_bowl = st.columns(2)
    with col_bat:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Orange Cap Winners (Highest Runs)</div>
            <div class="chart-subtitle">Leading run scorers by season</div>
        """, unsafe_allow_html=True)
        # Aggregation
        bat_season = filtered_df.groupby(['year', 'batter'])['runs_batter'].sum().reset_index()
        orange_caps = bat_season.loc[bat_season.groupby('year')['runs_batter'].idxmax()].sort_values('year', ascending=False)
        
        rows = ""
        for idx, r in orange_caps.iterrows():
            rows += f"<tr><td>{r['year']}</td><td><b>{r['batter']}</b></td><td>{r['runs_batter']:,} runs</td></tr>"
            
        st.markdown(f"""
        <table class="data-table">
            <thead><tr><th>Season</th><th>Player Name</th><th>Total Runs</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_bowl:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Purple Cap Winners (Highest Wickets)</div>
            <div class="chart-subtitle">Leading wicket takers by season</div>
        """, unsafe_allow_html=True)
        bowl_season = filtered_df.groupby(['year', 'bowler'])['bowler_wicket'].sum().reset_index()
        purple_caps = bowl_season.loc[bowl_season.groupby('year')['bowler_wicket'].idxmax()].sort_values('year', ascending=False)
        
        rows = ""
        for idx, r in purple_caps.iterrows():
            rows += f"<tr><td>{r['year']}</td><td><b>{r['bowler']}</b></td><td>{r['bowler_wicket']} wickets</td></tr>"
            
        st.markdown(f"""
        <table class="data-table">
            <thead><tr><th>Season</th><th>Player Name</th><th>Wickets</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ------------------ TAB 3: TEAM PERFORMANCE ------------------
with tab3:
    st.markdown("### ⚔️ Compare Team Performances")
    
    # Multiselect for specific teams comparison
    comp_teams = st.multiselect("Select Teams to Compare", options=teams_list, default=teams_list[:3])
    
    if len(comp_teams) > 0:
        # Match statistics
        m_batting = ipl_df.groupby(['year', 'batting_team'])['match_id'].nunique().reset_index()
        m_batting.columns = ['Year', 'Team', 'Matches']
        m_wins = ipl_df.groupby(['year', 'match_won_by'])['match_id'].nunique().reset_index()
        m_wins.columns = ['Year', 'Team', 'Wins']
        
        perf = pd.merge(m_batting, m_wins, on=['Year', 'Team'], how='left').fillna(0)
        perf['Win_Pct'] = (perf['Wins'] / perf['Matches'] * 100).round(1)
        
        perf = perf[perf['Team'].isin(comp_teams)]
        
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Win Percentage Evolution</div>
            <div class="chart-subtitle">Season-by-season win rate of selected teams</div>
        """, unsafe_allow_html=True)
        
        fig_team = go.Figure()
        for t in comp_teams:
            t_data = perf[perf['Team'] == t].sort_values('Year')
            color = TEAM_COLORS.get(t, '#9CA3AF')
            fig_team.add_trace(go.Scatter(x=t_data['Year'], y=t_data['Win_Pct'], mode='lines+markers', name=t, line=dict(color=color, width=2.5)))
            
        fig_team.update_layout(**PLOT_LAYOUT, height=400, yaxis_title="Win Percentage (%)")
        st.plotly_chart(fig_team, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please select at least one team to display performance trends.")

# ------------------ TAB 4: VENUE INTELLIGENCE ------------------
with tab4:
    st.markdown("### 🏟️ Venue Scouting & Performance Benchmarks")
    
    # Group by venue
    v_stats = filtered_df.groupby('venue').agg({
        'match_id': 'nunique',
        'runs_total': 'sum',
        'valid_ball': 'sum',
        'is_wicket': 'sum'
    }).reset_index()
    v_stats.columns = ['Venue', 'Matches', 'Total_Runs', 'Total_Balls', 'Wickets']
    v_stats = v_stats[v_stats['Matches'] >= 5].reset_index(drop=True)
    v_stats['Avg_Runs'] = (v_stats['Total_Runs'] / v_stats['Matches']).round(1)
    v_stats['RPO'] = ((v_stats['Total_Runs'] / v_stats['Total_Balls']) * 6).round(2)
    
    top_v = v_stats.nlargest(10, 'Avg_Runs')
    
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">Highest Scoring Stadiums</div>
        <div class="chart-subtitle">Average runs scored per match (min 5 matches)</div>
    """, unsafe_allow_html=True)
    
    fig_v = px.bar(top_v, x='Avg_Runs', y='Venue', orientation='h', color='Avg_Runs', color_continuous_scale='Blues')
    fig_v.update_layout(**PLOT_LAYOUT, height=400, coloraxis_showscale=False)
    st.plotly_chart(fig_v, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ TAB 5: WIN PREDICTOR ------------------
with tab5:
    st.markdown("### 🤖 Live Match Win Probability Predictor")
    st.markdown("Provide the current parameters of a second innings chase to predict victory likelihood.")
    
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        target = st.number_input("Target Score to Chase", min_value=50, max_value=300, value=180)
        curr_score = st.number_input("Current Batting Score", min_value=0, max_value=300, value=120)
        wickets_lost = st.slider("Wickets Lost", min_value=0, max_value=9, value=3)
        
    with col_in2:
        overs_bowled = st.slider("Overs Bowled (e.g. 15.2 overs)", min_value=0.0, max_value=19.5, step=0.1, value=14.0)
        
        # Convert over.ball input to balls remaining
        o = int(overs_bowled)
        b = int((overs_bowled - o) * 10)
        if b > 6:
            b = 6
        balls_remaining = 120 - (o * 6 + b)
        
        # Calculate model derived features
        runs_needed = max(target - curr_score, 0)
        
        st.write(f"**Balls Remaining**: {balls_remaining}")
        st.write(f"**Runs Needed to Win**: {runs_needed}")
        
    # Button triggers prediction
    predict_clicked = st.button("Calculate Probability 🚀", use_container_width=True)
    
    if predict_clicked or 'pred_prob' in st.session_state:
        # Calculate rates
        rrr = (runs_needed * 6) / max(balls_remaining, 1)
        balls_played = 120 - balls_remaining
        crr = (curr_score * 6) / max(balls_played, 1)
        
        features = np.array([[runs_needed, balls_remaining, wickets_lost, rrr, crr]])
        prob = win_model.predict_proba(features)[:, 1][0]
        st.session_state.pred_prob = prob
        
        st.markdown("<hr style='border-top: 1px solid var(--border); margin: 1.5rem 0;' />", unsafe_allow_html=True)
        
        pred_col1, pred_col2 = st.columns([1, 1])
        with pred_col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: var(--bg-subtle); border: 1px solid var(--border); border-radius: var(--radius);">
                <h4 style="margin: 0; color: var(--text-muted); font-size: 0.85rem; font-weight: 600;">CHASING TEAM WIN PROBABILITY</h4>
                <div style="font-size: 3.5rem; font-weight: 800; color: var(--accent); margin: 0.5rem 0;">
                    {prob*100:.1f}%
                </div>
                <div class="badge badge-mi" style="padding: 4px 12px; font-size: 0.8rem;">
                    {"High Win Likelihood" if prob >= 0.65 else ("Low Win Likelihood" if prob <= 0.35 else "Balanced Contest")}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with pred_col2:
            # Gauge Plot
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Chasing Probability Gauge"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#2563eb"},
                    'steps': [
                        {'range': [0, 35], 'color': "rgba(239,68,68,0.12)"},
                        {'range': [35, 65], 'color': "rgba(245,158,11,0.12)"},
                        {'range': [65, 100], 'color': "rgba(34,197,94,0.12)"}
                    ],
                }
            ))
            fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(family="DM Sans", color=text_color), height=200, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

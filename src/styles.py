"""
styles.py — IPL Intelligence Hub
Complete CSS injection system with premium styling, responsive design, and component renderers.
"""

import streamlit as st


def inject_css():
    """Inject the full custom CSS into the Streamlit app."""
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        /* ── Reset & Foundation ── */
        :root {
            --bg: #09090b;
            --bg-subtle: #0c0c0f;
            --card: #111114;
            --card-hover: #18181b;
            --border: #1e1e24;
            --border-subtle: #16161a;
            --text: #fafafa;
            --text-muted: #71717a;
            --text-dim: #52525b;
            --accent: #2563eb;
            --accent-soft: rgba(37, 99, 235, 0.12);
            --green: #22c55e;
            --green-muted: rgba(34, 197, 94, 0.12);
            --red: #ef4444;
            --red-muted: rgba(239, 68, 68, 0.12);
            --amber: #f59e0b;
            --amber-muted: rgba(245, 158, 11, 0.12);
            --radius: 12px;
            --radius-sm: 8px;
            --shadow: none;
            --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        /* ── Global Overrides ── */
        header[data-testid="stHeader"], footer, .stDeployButton {
            display: none !important;
        }

        .block-container {
            padding: 1.5rem 2.5rem 3rem !important;
            max-width: 1400px !important;
        }

        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"],
        .main, .block-container, section[data-testid="stMain"] {
            background-color: var(--bg) !important;
            color: var(--text) !important;
            font-family: var(--font) !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0a0d 0%, #0c0c0f 100%) !important;
            border-right: 1px solid var(--border) !important;
        }
        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: var(--text) !important;
        }
        [data-testid="stSidebar"] .stRadio > label {
            color: var(--text-muted) !important;
            font-size: 0.82rem !important;
        }
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
            padding: 0.55rem 0.8rem !important;
            border-radius: var(--radius-sm) !important;
            transition: all 0.2s ease !important;
            font-weight: 500 !important;
            font-size: 0.88rem !important;
        }
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
            background: var(--card) !important;
        }
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
            background: var(--accent-soft) !important;
            color: var(--accent) !important;
        }

        /* ── KPI Metric Cards ── */
        .kpi-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.2rem 1.4rem;
            transition: transform 0.2s ease, border-color 0.25s ease;
            position: relative;
            overflow: hidden;
        }
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent), #7c3aed);
            opacity: 0;
            transition: opacity 0.25s ease;
        }
        .kpi-card:hover {
            border-color: var(--accent);
            transform: translateY(-3px);
        }
        .kpi-card:hover::before { opacity: 1; }
        .kpi-label {
            font-size: 0.72rem;
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .kpi-value {
            font-size: 1.9rem;
            font-weight: 800;
            color: var(--text);
            letter-spacing: -0.03em;
            margin-top: 0.3rem;
            line-height: 1.1;
        }
        .kpi-delta {
            font-size: 0.73rem;
            font-weight: 500;
            margin-top: 0.5rem;
            padding: 3px 10px;
            border-radius: 6px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .delta-up { color: var(--green); background: var(--green-muted); }
        .delta-down { color: var(--red); background: var(--red-muted); }
        .delta-neutral { color: var(--amber); background: var(--amber-muted); }

        /* ── Chart Containers ── */
        .chart-container {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.3rem 1.5rem;
            margin-bottom: 1.25rem;
            transition: border-color 0.2s ease;
        }
        .chart-container:hover { border-color: #27272a; }
        .chart-header {
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.15rem;
        }
        .chart-subheader {
            font-size: 0.75rem;
            color: var(--text-dim);
            margin-bottom: 1rem;
        }

        /* ── Data Tables ── */
        .styled-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 0.82rem;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            overflow: hidden;
        }
        .styled-table th {
            text-align: left;
            padding: 0.8rem 1rem;
            background: var(--bg-subtle);
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            border-bottom: 1px solid var(--border);
        }
        .styled-table td {
            padding: 0.75rem 1rem;
            color: var(--text);
            border-bottom: 1px solid var(--border-subtle);
        }
        .styled-table tr:last-child td { border-bottom: none; }
        .styled-table tr:hover { background-color: var(--card-hover); }

        /* ── Section Divider ── */
        .section-divider {
            border: 0;
            border-top: 1px solid var(--border);
            margin: 1.5rem 0;
        }

        /* ── Insight Cards ── */
        .insight-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.3rem 1.5rem;
            margin-bottom: 1rem;
            border-left: 4px solid var(--accent);
        }
        .insight-number {
            font-size: 0.7rem;
            font-weight: 700;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .insight-title {
            font-size: 1rem;
            font-weight: 700;
            color: var(--text);
            margin: 0.3rem 0;
        }
        .insight-body {
            font-size: 0.83rem;
            color: var(--text-muted);
            line-height: 1.5;
        }

        /* ── Tabs Override ── */
        button[data-baseweb="tab"] {
            background: transparent !important;
            color: var(--text-muted) !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.2rem !important;
            border: 1px solid transparent !important;
            border-radius: 8px !important;
            margin-right: 4px;
            transition: all 0.2s ease;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--text) !important;
            background: var(--card) !important;
            border-color: var(--border) !important;
        }
        [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {
            display: none !important;
        }
        [data-baseweb="tab-list"] {
            background: var(--bg-subtle) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            padding: 4px;
            gap: 2px !important;
        }

        /* ── Buttons ── */
        .stButton > button {
            border-radius: var(--radius-sm) !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            transition: all 0.2s ease !important;
        }

        /* ── Responsive ── */
        @media (max-width: 768px) {
            .block-container {
                padding: 1rem 1rem 2rem !important;
            }
            .kpi-value { font-size: 1.5rem; }
            .kpi-label { font-size: 0.68rem; }
        }
    </style>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Component Renderers
# ──────────────────────────────────────────────

def render_kpi_card(label: str, value: str, delta: str = None, delta_type: str = "up"):
    """Render a premium KPI metric card."""
    delta_class = {"up": "delta-up", "down": "delta-down", "neutral": "delta-neutral"}.get(delta_type, "delta-neutral")
    arrow = {"up": "↑", "down": "↓", "neutral": "→"}.get(delta_type, "→")
    delta_html = f'<div class="kpi-delta {delta_class}">{arrow} {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def chart_header(title: str, subtitle: str = ""):
    """Render a chart section header inside a chart container."""
    sub_html = f'<div class="chart-subheader">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="chart-header">{title}</div>
    {sub_html}
    """, unsafe_allow_html=True)


def section_divider():
    """Render a subtle horizontal divider."""
    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)


def render_insight_card(number: int, title: str, body: str):
    """Render a numbered business insight card."""
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-number">Insight #{number:02d}</div>
        <div class="insight-title">{title}</div>
        <div class="insight-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)


def render_html_table(headers: list, rows: list):
    """Render a styled HTML table from header list and row list-of-lists."""
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for row in rows:
        tds = "".join(f"<td>{c}</td>" for c in row)
        body += f"<tr>{tds}</tr>"
    st.markdown(f"""
    <table class="styled-table">
        <thead><tr>{th}</tr></thead>
        <tbody>{body}</tbody>
    </table>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Plotly Layout Defaults
# ──────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#a1a1aa", size=11),
    margin=dict(l=40, r=20, t=35, b=40),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        zerolinecolor="rgba(255,255,255,0.05)",
        tickfont=dict(size=10, color="#71717a"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        zerolinecolor="rgba(255,255,255,0.05)",
        tickfont=dict(size=10, color="#71717a"),
    ),
    legend=dict(
        font=dict(size=11, color="#a1a1aa"),
        bgcolor="rgba(0,0,0,0)",
    ),
    hoverlabel=dict(
        bgcolor="#18181b",
        bordercolor="#27272a",
        font=dict(color="#fafafa", size=12),
    ),
)


def update_plotly_layout(fig, **kwargs):
    """
    Update a plotly figure's layout, merging kwargs on top of PLOTLY_LAYOUT
    to avoid keyword argument duplication errors.
    """
    layout = dict(PLOTLY_LAYOUT)
    for k in list(kwargs.keys()):
        if k in layout and isinstance(layout[k], dict) and isinstance(kwargs[k], dict):
            layout[k] = dict(layout[k], **kwargs[k])
            del kwargs[k]
    fig.update_layout(**layout, **kwargs)


"""
overview.py — IPL Intelligence Hub
Page 1: KPI cards, season scoring trends, toss analysis, boundary evolution.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from src.styles import render_kpi_card, chart_header, section_divider, update_plotly_layout
from src.constants import CHART_PALETTE
from src.preprocessing import build_match_summary


def render(df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Render the Overview page."""

    st.markdown("""
    <div style="margin-bottom: 0.5rem;">
        <h2 style="margin:0; font-weight:800; letter-spacing:-0.02em; color:#fafafa;">
            Dashboard Overview
        </h2>
        <p style="margin:0; font-size:0.82rem; color:#71717a;">
            High-level tournament statistics and season-wise trends
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_divider()

    # ── KPI Calculations ──
    matches = filtered_df["match_id"].nunique()
    total_runs = int(filtered_df["runs_total"].sum())
    total_wickets = int(filtered_df["is_wicket"].sum())
    total_sixes = int(filtered_df["is_six"].sum())
    total_fours = int(filtered_df["is_four"].sum())
    boundary_pct = round((total_fours + total_sixes) / max(len(filtered_df), 1) * 100, 1)

    # Highest team innings score
    team_innings = filtered_df.groupby(["match_id", "innings", "batting_team"])["runs_total"].sum()
    highest_score = int(team_innings.max()) if len(team_innings) > 0 else 0
    highest_team = ""
    if len(team_innings) > 0:
        idx = team_innings.idxmax()
        highest_team = idx[2] if isinstance(idx, tuple) else ""

    # Most successful team
    match_summary = build_match_summary(filtered_df)
    if len(match_summary) > 0:
        win_counts = match_summary["match_won_by"].value_counts()
        most_wins_team = win_counts.index[0] if len(win_counts) > 0 else "N/A"
        most_wins_count = int(win_counts.iloc[0]) if len(win_counts) > 0 else 0
    else:
        most_wins_team, most_wins_count = "N/A", 0

    # ── KPI Cards Row ──
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        render_kpi_card("Total Matches", f"{matches:,}")
    with k2:
        render_kpi_card("Total Runs", f"{total_runs:,}", f"{boundary_pct}% from boundaries", "up")
    with k3:
        render_kpi_card("Total Wickets", f"{total_wickets:,}")
    with k4:
        render_kpi_card("Highest Team Score", f"{highest_score}", highest_team, "neutral")
    with k5:
        render_kpi_card("Most Successful Team", f"{most_wins_count} W", most_wins_team, "up")

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    # ── Row 1: Scoring Trends + Toss Impact ──
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_header("Season-Wise Scoring Trends", "Average runs per match and run rate progression")

        trends = filtered_df.groupby("year").agg(
            matches=("match_id", "nunique"),
            total_runs=("runs_total", "sum"),
            total_balls=("valid_ball", "sum"),
        ).reset_index()
        trends["avg_runs"] = (trends["total_runs"] / trends["matches"]).round(1)
        trends["rpo"] = ((trends["total_runs"] / trends["total_balls"]) * 6).round(2)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trends["year"], y=trends["avg_runs"],
            mode="lines+markers", name="Avg Runs/Match",
            line=dict(color="#2563eb", width=3),
            marker=dict(size=7),
        ))
        fig.add_trace(go.Scatter(
            x=trends["year"], y=trends["rpo"],
            mode="lines+markers", name="Run Rate (RPO)",
            line=dict(color="#f97316", width=2.5, dash="dot"),
            marker=dict(size=6, symbol="diamond"),
            yaxis="y2",
        ))
        update_plotly_layout(
            fig, height=370,
            yaxis=dict(title=dict(text="Avg Runs", font=dict(size=11, color="#71717a"))),
            yaxis2=dict(
                title=dict(text="RPO", font=dict(size=11, color="#71717a")),
                overlaying="y", side="right",
                gridcolor="rgba(255,255,255,0.03)",
                tickfont=dict(size=10, color="#71717a"),
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_header("Toss Winner Advantage", "How often does the toss winner win the match?")

        if len(match_summary) > 0:
            toss_won = match_summary["toss_winner_won"].mean() * 100
            toss_lost = 100 - toss_won
            labels = ["Toss Winner Won", "Toss Loser Won"]
            values = [toss_won, toss_lost]
            colors = ["#10b981", "#ef4444"]

            fig_toss = go.Figure(data=[go.Pie(
                labels=labels, values=values, hole=0.5,
                marker_colors=colors,
                textinfo="percent+label",
                textfont=dict(size=12, color="#fafafa"),
                hovertemplate="%{label}: %{value:.1f}%<extra></extra>",
            )])
            update_plotly_layout(fig_toss, height=370, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_toss, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No match data available.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 2: Boundary Evolution ──
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    chart_header("Boundary Evolution", "Fours and sixes hit per season — tracking the aggression shift")

    boundary_trends = filtered_df.groupby("year").agg(
        fours=("is_four", "sum"),
        sixes=("is_six", "sum"),
        matches=("match_id", "nunique"),
    ).reset_index()
    boundary_trends["fours_per_match"] = (boundary_trends["fours"] / boundary_trends["matches"]).round(1)
    boundary_trends["sixes_per_match"] = (boundary_trends["sixes"] / boundary_trends["matches"]).round(1)

    fig_b = go.Figure()
    fig_b.add_trace(go.Bar(
        x=boundary_trends["year"], y=boundary_trends["fours_per_match"],
        name="Fours / Match", marker_color="#3b82f6", marker_cornerradius=4,
    ))
    fig_b.add_trace(go.Bar(
        x=boundary_trends["year"], y=boundary_trends["sixes_per_match"],
        name="Sixes / Match", marker_color="#8b5cf6", marker_cornerradius=4,
    ))
    update_plotly_layout(
        fig_b, height=340, barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_b, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

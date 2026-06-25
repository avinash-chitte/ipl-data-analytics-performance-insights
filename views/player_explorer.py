"""
player_explorer.py — IPL Intelligence Hub
Page 3: Player search, profile cards, phase-wise breakdown, season MVPs.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from src.styles import render_kpi_card, chart_header, section_divider, render_html_table, update_plotly_layout
from src.constants import CHART_PALETTE, PHASE_COLORS
from src.preprocessing import (
    compute_batter_stats, compute_bowler_stats,
    compute_player_season_stats, compute_season_mvps,
)


def render(df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Render the Player Explorer page."""

    st.markdown("""
    <div style="margin-bottom:0.5rem;">
        <h2 style="margin:0; font-weight:800; color:#fafafa;">Player Explorer</h2>
        <p style="margin:0; font-size:0.82rem; color:#71717a;">
            Search any player, view career stats, phase-wise performance, and season MVPs
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_divider()

    tab_bat, tab_bowl, tab_mvp = st.tabs(["🏏 Batting Explorer", "🎯 Bowling Explorer", "⭐ Season MVPs"])

    # ── Tab 1: Batting Explorer ──
    with tab_bat:
        batter_stats = compute_batter_stats(filtered_df)
        all_batters = batter_stats[batter_stats["balls_faced"] >= 30]["batter"].tolist()

        selected_batter = st.selectbox("Search Batter", options=all_batters, index=0, key="bat_search")

        if selected_batter:
            p = batter_stats[batter_stats["batter"] == selected_batter].iloc[0]

            # Profile KPIs
            pk1, pk2, pk3, pk4, pk5 = st.columns(5)
            with pk1:
                render_kpi_card("Matches", str(int(p["matches"])))
            with pk2:
                render_kpi_card("Total Runs", f"{int(p['runs']):,}")
            with pk3:
                render_kpi_card("Strike Rate", str(p["strike_rate"]))
            with pk4:
                render_kpi_card("Fours / Sixes", f"{int(p['fours'])} / {int(p['sixes'])}")
            with pk5:
                render_kpi_card("Boundary %", f"{p['boundary_pct']}%")

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)

            # Season-by-season trend
            with c1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                chart_header("Season-by-Season Runs", f"{selected_batter}'s run progression")

                season_stats = compute_player_season_stats(filtered_df, selected_batter, "batter")
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=season_stats["year"], y=season_stats["runs"],
                    marker_color="#2563eb", marker_cornerradius=4,
                    text=season_stats["runs"], textposition="outside",
                    textfont=dict(size=10, color="#a1a1aa"),
                ))
                update_plotly_layout(fig, height=350, yaxis_title="Runs")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            # Phase-wise performance
            with c2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                chart_header("Phase-Wise Breakdown", "Runs and strike rate by match phase")

                phase_data = filtered_df[filtered_df["batter"] == selected_batter].groupby("match_phase").agg(
                    runs=("runs_batter", "sum"),
                    balls=("valid_ball", "sum"),
                ).reset_index()
                phase_data["sr"] = ((phase_data["runs"] / phase_data["balls"].clip(lower=1)) * 100).round(1)

                phase_colors = [PHASE_COLORS.get(str(p), "#71717a") for p in phase_data["match_phase"]]

                fig_p = go.Figure()
                fig_p.add_trace(go.Bar(
                    x=phase_data["match_phase"].astype(str),
                    y=phase_data["runs"],
                    marker_color=phase_colors,
                    marker_cornerradius=4,
                    name="Runs",
                    text=phase_data.apply(lambda r: f"{int(r['runs'])} ({r['sr']} SR)", axis=1),
                    textposition="outside",
                    textfont=dict(size=10, color="#a1a1aa"),
                ))
                update_plotly_layout(fig_p, height=350, yaxis_title="Runs")
                st.plotly_chart(fig_p, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2: Bowling Explorer ──
    with tab_bowl:
        bowler_stats = compute_bowler_stats(filtered_df)
        all_bowlers = bowler_stats[bowler_stats["balls_bowled"] >= 30]["bowler"].tolist()

        selected_bowler = st.selectbox("Search Bowler", options=all_bowlers, index=0, key="bowl_search")

        if selected_bowler:
            b = bowler_stats[bowler_stats["bowler"] == selected_bowler].iloc[0]

            bk1, bk2, bk3, bk4, bk5 = st.columns(5)
            with bk1:
                render_kpi_card("Matches", str(int(b["matches"])))
            with bk2:
                render_kpi_card("Wickets", str(int(b["wickets"])))
            with bk3:
                render_kpi_card("Economy", str(b["economy"]))
            with bk4:
                render_kpi_card("Bowling SR", str(b["bowling_sr"]))
            with bk5:
                render_kpi_card("Dot Ball %", f"{b['dot_pct']}%")

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)

            with c1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                chart_header("Season-by-Season Wickets", f"{selected_bowler}'s wicket progression")

                season_bowl = compute_player_season_stats(filtered_df, selected_bowler, "bowler")
                fig_bw = go.Figure()
                fig_bw.add_trace(go.Bar(
                    x=season_bowl["year"], y=season_bowl["wickets"],
                    marker_color="#8b5cf6", marker_cornerradius=4,
                    text=season_bowl["wickets"], textposition="outside",
                    textfont=dict(size=10, color="#a1a1aa"),
                ))
                update_plotly_layout(fig_bw, height=350, yaxis_title="Wickets")
                st.plotly_chart(fig_bw, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                chart_header("Phase-Wise Economy", "Economy rate across match phases")

                phase_bowl = filtered_df[filtered_df["bowler"] == selected_bowler].groupby("match_phase").agg(
                    runs_conceded=("runs_bowler", "sum"),
                    balls=("valid_ball", "sum"),
                    wickets=("bowler_wicket", "sum"),
                ).reset_index()
                phase_bowl["economy"] = ((phase_bowl["runs_conceded"] / phase_bowl["balls"].clip(lower=1)) * 6).round(2)

                phase_colors = [PHASE_COLORS.get(str(p), "#71717a") for p in phase_bowl["match_phase"]]

                fig_bp = go.Figure()
                fig_bp.add_trace(go.Bar(
                    x=phase_bowl["match_phase"].astype(str),
                    y=phase_bowl["economy"],
                    marker_color=phase_colors,
                    marker_cornerradius=4,
                    text=phase_bowl.apply(lambda r: f"{r['economy']} ({int(r['wickets'])}W)", axis=1),
                    textposition="outside",
                    textfont=dict(size=10, color="#a1a1aa"),
                ))
                update_plotly_layout(fig_bp, height=350, yaxis_title="Economy Rate")
                st.plotly_chart(fig_bp, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 3: Season MVPs ──
    with tab_mvp:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_header("Most Valuable Players by Season",
                     "Custom MVP Score = (Runs/10) + (Wickets×15) + (Boundaries×2)")

        mvps = compute_season_mvps(filtered_df)
        headers = ["Season", "Player", "Runs", "Wickets", "MVP Score"]
        rows = [
            [str(int(r["year"])), r["player"], str(int(r["runs"])),
             str(int(r["wickets"])), str(r["mvp_score"])]
            for _, r in mvps.iterrows()
        ]
        render_html_table(headers, rows)
        st.markdown("</div>", unsafe_allow_html=True)

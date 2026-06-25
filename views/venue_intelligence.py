"""
venue_intelligence.py — IPL Intelligence Hub
Page 4: Venue comparison dashboard, scoring benchmarks, pace vs spin classification.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from src.styles import render_kpi_card, chart_header, section_divider, render_html_table, update_plotly_layout
from src.constants import CHART_PALETTE


def render(df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Render the Venue Intelligence page."""

    st.markdown("""
    <div style="margin-bottom:0.5rem;">
        <h2 style="margin:0; font-weight:800; color:#fafafa;">Venue Intelligence</h2>
        <p style="margin:0; font-size:0.82rem; color:#71717a;">
            Stadium scoring benchmarks, innings comparisons, and venue character profiles
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_divider()

    # ── Aggregate venue stats ──
    v_stats = filtered_df.groupby("venue").agg(
        matches=("match_id", "nunique"),
        total_runs=("runs_total", "sum"),
        total_balls=("valid_ball", "sum"),
        wickets=("is_wicket", "sum"),
        sixes=("is_six", "sum"),
        fours=("is_four", "sum"),
        boundaries=("is_boundary", "sum"),
    ).reset_index()
    v_stats = v_stats[v_stats["matches"] >= 3].reset_index(drop=True)
    v_stats["avg_runs"] = (v_stats["total_runs"] / v_stats["matches"]).round(1)
    v_stats["rpo"] = ((v_stats["total_runs"] / v_stats["total_balls"].clip(lower=1)) * 6).round(2)
    v_stats["boundary_pct"] = ((v_stats["boundaries"] / v_stats["total_balls"].clip(lower=1)) * 100).round(1)
    v_stats["sixes_per_match"] = (v_stats["sixes"] / v_stats["matches"]).round(1)

    # ── KPIs ──
    if len(v_stats) > 0:
        top_venue = v_stats.nlargest(1, "avg_runs").iloc[0]
        total_venues = len(v_stats)
        avg_rpo = v_stats["rpo"].mean().round(2)

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi_card("Venues Analyzed", str(total_venues))
        with k2:
            render_kpi_card("Highest Scoring", f"{top_venue['avg_runs']}", top_venue["venue"][:25], "up")
        with k3:
            render_kpi_card("Avg Run Rate", str(avg_rpo), "Across all venues", "neutral")
        with k4:
            most_sixes = v_stats.nlargest(1, "sixes_per_match").iloc[0]
            render_kpi_card("Most Sixes/Match", str(most_sixes["sixes_per_match"]),
                            most_sixes["venue"][:25], "up")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    tab_scoring, tab_compare, tab_character = st.tabs([
        "📊 Scoring Rankings", "🔄 1st vs 2nd Innings", "🎯 Venue Character"
    ])

    # ── Tab 1: Top Scoring Venues ──
    with tab_scoring:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_header("Highest Scoring Stadiums", "Average total runs per match (min 3 matches)")

        top_v = v_stats.nlargest(12, "avg_runs")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_v["avg_runs"],
            y=top_v["venue"],
            orientation="h",
            marker=dict(
                color=top_v["avg_runs"],
                colorscale=[[0, "#1e3a5f"], [0.5, "#2563eb"], [1, "#60a5fa"]],
                cornerradius=4,
            ),
            text=top_v["avg_runs"],
            textposition="outside",
            textfont=dict(size=11, color="#a1a1aa"),
        ))
        update_plotly_layout(
            fig,
            height=max(350, len(top_v) * 40),
            xaxis_title="Avg Runs per Match",
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2: 1st vs 2nd Innings Comparison ──
    with tab_compare:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_header("1st vs 2nd Innings Average Scores", "Which venues favor chasing?")

        inn_runs = filtered_df.groupby(["venue", "match_id", "innings"])["runs_total"].sum().reset_index()
        avg_inn = inn_runs.groupby(["venue", "innings"])["runs_total"].mean().unstack(fill_value=0).reset_index()

        if 1 in avg_inn.columns and 2 in avg_inn.columns:
            avg_inn.columns = ["venue", "avg_1st", "avg_2nd"]
            # Filter for venues with enough data
            venue_counts = inn_runs.groupby("venue")["match_id"].nunique().reset_index()
            venue_counts.columns = ["venue", "matches"]
            avg_inn = avg_inn.merge(venue_counts, on="venue")
            avg_inn = avg_inn[avg_inn["matches"] >= 5].nlargest(10, "avg_1st")
            avg_inn["avg_1st"] = avg_inn["avg_1st"].round(1)
            avg_inn["avg_2nd"] = avg_inn["avg_2nd"].round(1)

            fig_inn = go.Figure()
            fig_inn.add_trace(go.Bar(
                y=avg_inn["venue"], x=avg_inn["avg_1st"],
                orientation="h", name="1st Innings",
                marker_color="#2563eb", marker_cornerradius=4,
            ))
            fig_inn.add_trace(go.Bar(
                y=avg_inn["venue"], x=avg_inn["avg_2nd"],
                orientation="h", name="2nd Innings",
                marker_color="#f97316", marker_cornerradius=4,
            ))
            update_plotly_layout(
                fig_inn, barmode="group",
                height=max(350, len(avg_inn) * 50),
                xaxis_title="Average Innings Score",
                yaxis=dict(autorange="reversed"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig_inn, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Not enough innings data for comparison.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 3: Venue Character (Boundary% + RPO) ──
    with tab_character:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_header("Venue Character Profile",
                     "Boundary percentage vs Run Rate — identify batting-friendly vs bowler-friendly venues")

        qualified = v_stats[v_stats["matches"] >= 5].copy()

        if len(qualified) > 0:
            fig_char = go.Figure()
            fig_char.add_trace(go.Scatter(
                x=qualified["rpo"],
                y=qualified["boundary_pct"],
                mode="markers+text",
                text=qualified["venue"].str.slice(0, 18),
                textposition="top center",
                textfont=dict(size=9, color="#a1a1aa"),
                marker=dict(
                    size=qualified["sixes_per_match"] * 4 + 8,
                    color=qualified["avg_runs"],
                    colorscale="Blues",
                    line=dict(width=1, color="#27272a"),
                    showscale=True,
                    colorbar=dict(title="Avg Runs", tickfont=dict(color="#71717a"), titlefont=dict(color="#71717a")),
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "RPO: %{x}<br>"
                    "Boundary%: %{y}%<br>"
                    "<extra></extra>"
                ),
            ))
            # Add quadrant lines at medians
            median_rpo = qualified["rpo"].median()
            median_bp = qualified["boundary_pct"].median()
            fig_char.add_hline(y=median_bp, line_dash="dash", line_color="rgba(255,255,255,0.15)")
            fig_char.add_vline(x=median_rpo, line_dash="dash", line_color="rgba(255,255,255,0.15)")

            update_plotly_layout(
                fig_char, height=480,
                xaxis_title="Run Rate (RPO)",
                yaxis_title="Boundary %",
            )
            st.plotly_chart(fig_char, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Not enough venue data for character analysis.")
        st.markdown("</div>", unsafe_allow_html=True)

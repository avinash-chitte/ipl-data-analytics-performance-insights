"""
powerplay_death.py — IPL Intelligence Hub
Page 5: Powerplay vs Death overs deep dive, phase trends, death specialists.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from src.styles import render_kpi_card, chart_header, section_divider, render_html_table, update_plotly_layout
from src.constants import PHASE_COLORS, CHART_PALETTE
from src.preprocessing import compute_phase_stats, compute_phase_by_season, compute_death_specialists


def render(df: pd.DataFrame, filtered_df: pd.DataFrame):
    """Render the Powerplay & Death Overs page."""

    st.markdown("""
    <div style="margin-bottom:0.5rem;">
        <h2 style="margin:0; font-weight:800; color:#fafafa;">Powerplay & Death Overs</h2>
        <p style="margin:0; font-size:0.82rem; color:#71717a;">
            Phase-wise run rates, boundary distribution, and death-overs specialists
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_divider()

    # ── Phase KPIs ──
    phase_stats = compute_phase_stats(filtered_df)

    if len(phase_stats) > 0:
        k1, k2, k3 = st.columns(3)
        phases = ["Powerplay", "Middle Overs", "Death Overs"]
        cols = [k1, k2, k3]
        for col, phase_name in zip(cols, phases):
            row = phase_stats[phase_stats["match_phase"] == phase_name]
            if len(row) > 0:
                row = row.iloc[0]
                with col:
                    render_kpi_card(
                        f"{phase_name} Run Rate",
                        f"{row['run_rate']} RPO",
                        f"{row['boundary_pct']}% boundaries · {row['dot_pct']}% dots",
                        "up" if row["run_rate"] > 8 else "neutral",
                    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    tab_trends, tab_dist, tab_specialists = st.tabs([
        "📈 Phase Trends", "📊 Phase Distribution", "💪 Death Specialists"
    ])

    # ── Tab 1: Phase-wise run rate evolution ──
    with tab_trends:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_header("Phase-Wise Run Rate Evolution",
                     "How run rates in Powerplay, Middle, and Death overs have changed over seasons")

        phase_season = compute_phase_by_season(filtered_df)

        fig = go.Figure()
        for phase_name in ["Powerplay", "Middle Overs", "Death Overs"]:
            p_data = phase_season[phase_season["match_phase"] == phase_name].sort_values("year")
            color = PHASE_COLORS.get(phase_name, "#71717a")
            fig.add_trace(go.Scatter(
                x=p_data["year"], y=p_data["run_rate"],
                mode="lines+markers", name=phase_name,
                line=dict(color=color, width=2.5),
                marker=dict(size=6),
            ))
        update_plotly_layout(
            fig, height=400,
            yaxis_title="Run Rate (RPO)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 2: Phase Distribution (runs, boundaries, wickets) ──
    with tab_dist:
        if len(phase_stats) > 0:
            c1, c2 = st.columns(2)

            with c1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                chart_header("Runs by Phase", "Share of total runs in each phase")

                colors = [PHASE_COLORS.get(str(p), "#71717a") for p in phase_stats["match_phase"]]
                fig_runs = go.Figure(data=[go.Pie(
                    labels=phase_stats["match_phase"].astype(str),
                    values=phase_stats["total_runs"],
                    hole=0.5,
                    marker_colors=colors,
                    textinfo="percent+label",
                    textfont=dict(size=12, color="#fafafa"),
                )])
                update_plotly_layout(fig_runs, height=340, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_runs, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                chart_header("Wickets by Phase", "Which phase is most dangerous?")

                fig_wkts = go.Figure(data=[go.Pie(
                    labels=phase_stats["match_phase"].astype(str),
                    values=phase_stats["wickets"],
                    hole=0.5,
                    marker_colors=colors,
                    textinfo="percent+label",
                    textfont=dict(size=12, color="#fafafa"),
                )])
                update_plotly_layout(fig_wkts, height=340, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_wkts, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            # Boundary breakdown bar chart
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("Fours vs Sixes by Phase")

            fig_bd = go.Figure()
            fig_bd.add_trace(go.Bar(
                x=phase_stats["match_phase"].astype(str),
                y=phase_stats["fours"],
                name="Fours", marker_color="#3b82f6", marker_cornerradius=4,
            ))
            fig_bd.add_trace(go.Bar(
                x=phase_stats["match_phase"].astype(str),
                y=phase_stats["sixes"],
                name="Sixes", marker_color="#8b5cf6", marker_cornerradius=4,
            ))
            update_plotly_layout(
                fig_bd, height=340, barmode="group",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig_bd, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 3: Death Overs Specialists ──
    with tab_specialists:
        bat_death, bowl_death = compute_death_specialists(filtered_df)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("🔥 Top Death Overs Batters", "Highest strike rate in overs 16-20 (min 60 balls)")

            if len(bat_death) > 0:
                fig_bd = go.Figure()
                fig_bd.add_trace(go.Bar(
                    x=bat_death["strike_rate"],
                    y=bat_death["batter"],
                    orientation="h",
                    marker_color="#ef4444",
                    marker_cornerradius=4,
                    text=bat_death.apply(lambda r: f"SR: {r['strike_rate']} ({int(r['runs'])} runs)", axis=1),
                    textposition="outside",
                    textfont=dict(size=10, color="#a1a1aa"),
                ))
                update_plotly_layout(
                    fig_bd,
                    height=max(300, len(bat_death) * 38),
                    xaxis_title="Strike Rate",
                    yaxis=dict(autorange="reversed"),
                )
                st.plotly_chart(fig_bd, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Not enough data for death overs batting analysis.")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("🛡️ Top Death Overs Bowlers", "Best economy in overs 16-20 (min 60 balls)")

            if len(bowl_death) > 0:
                fig_bw = go.Figure()
                fig_bw.add_trace(go.Bar(
                    x=bowl_death["economy"],
                    y=bowl_death["bowler"],
                    orientation="h",
                    marker_color="#10b981",
                    marker_cornerradius=4,
                    text=bowl_death.apply(lambda r: f"Econ: {r['economy']} ({int(r['wickets'])}W)", axis=1),
                    textposition="outside",
                    textfont=dict(size=10, color="#a1a1aa"),
                ))
                update_plotly_layout(
                    fig_bw,
                    height=max(300, len(bowl_death) * 38),
                    xaxis_title="Economy Rate",
                    yaxis=dict(autorange="reversed"),
                )
                st.plotly_chart(fig_bw, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Not enough data for death overs bowling analysis.")
            st.markdown("</div>", unsafe_allow_html=True)

"""
team_performance.py — IPL Intelligence Hub
Page 2: Team comparison, head-to-head analysis, consistency rankings, cap winners.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from src.styles import render_kpi_card, chart_header, section_divider, render_html_table, update_plotly_layout
from src.constants import TEAM_COLORS, CHART_PALETTE
from src.preprocessing import compute_head_to_head, compute_team_consistency


def render(df: pd.DataFrame, filtered_df: pd.DataFrame, teams_list: list):
    """Render the Team Performance page."""

    st.markdown("""
    <div style="margin-bottom:0.5rem;">
        <h2 style="margin:0; font-weight:800; color:#fafafa;">Team Performance</h2>
        <p style="margin:0; font-size:0.82rem; color:#71717a;">
            Compare franchises, explore head-to-head records, and rank team consistency
        </p>
    </div>
    """, unsafe_allow_html=True)

    section_divider()

    tab_compare, tab_h2h, tab_consistency, tab_caps = st.tabs([
        "📈 Win % Trends", "⚔️ Head-to-Head", "🏅 Consistency Rankings", "🏆 Cap Winners"
    ])

    # ── Tab 1: Win % Evolution ──
    with tab_compare:
        comp_teams = st.multiselect(
            "Select teams to compare",
            options=teams_list,
            default=teams_list[:4] if len(teams_list) >= 4 else teams_list,
            key="team_compare",
        )

        if comp_teams:
            m_bat = df.groupby(["year", "batting_team"])["match_id"].nunique().reset_index()
            m_bat.columns = ["Year", "Team", "Matches"]
            m_win = df.groupby(["year", "match_won_by"])["match_id"].nunique().reset_index()
            m_win.columns = ["Year", "Team", "Wins"]

            perf = m_bat.merge(m_win, on=["Year", "Team"], how="left").fillna(0)
            perf["Win_Pct"] = (perf["Wins"] / perf["Matches"].clip(lower=1) * 100).round(1)
            perf = perf[perf["Team"].isin(comp_teams)]

            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("Win Percentage Evolution", "Season-by-season win rate of selected franchises")

            fig = go.Figure()
            for t in comp_teams:
                t_data = perf[perf["Team"] == t].sort_values("Year")
                color = TEAM_COLORS.get(t, "#9ca3af")
                fig.add_trace(go.Scatter(
                    x=t_data["Year"], y=t_data["Win_Pct"],
                    mode="lines+markers", name=t,
                    line=dict(color=color, width=2.5),
                    marker=dict(size=6),
                ))
            update_plotly_layout(
                fig, height=420,
                yaxis_title="Win %",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Select at least one team to display trends.")

    # ── Tab 2: Head-to-Head ──
    with tab_h2h:
        c1, c2 = st.columns(2)
        with c1:
            team_a = st.selectbox("Team A", options=teams_list, index=0, key="h2h_a")
        with c2:
            remaining = [t for t in teams_list if t != team_a]
            team_b = st.selectbox("Team B", options=remaining, index=0, key="h2h_b")

        h2h = compute_head_to_head(df, team_a, team_b)

        if h2h["total"] > 0:
            hk1, hk2, hk3 = st.columns(3)
            with hk1:
                render_kpi_card("Total Matches", str(h2h["total"]))
            with hk2:
                render_kpi_card(team_a, f"{h2h['team_a_wins']} Wins",
                                f"{round(h2h['team_a_wins']/h2h['total']*100)}%", "up")
            with hk3:
                render_kpi_card(team_b, f"{h2h['team_b_wins']} Wins",
                                f"{round(h2h['team_b_wins']/h2h['total']*100)}%",
                                "up" if h2h["team_b_wins"] > h2h["team_a_wins"] else "down")

            # Donut chart
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("Head-to-Head Win Share")

            color_a = TEAM_COLORS.get(team_a, "#2563eb")
            color_b = TEAM_COLORS.get(team_b, "#ef4444")

            fig_h2h = go.Figure(data=[go.Pie(
                labels=[team_a, team_b],
                values=[h2h["team_a_wins"], h2h["team_b_wins"]],
                hole=0.55, marker_colors=[color_a, color_b],
                textinfo="label+value",
                textfont=dict(size=12, color="#fafafa"),
            )])
            update_plotly_layout(fig_h2h, height=320, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_h2h, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

            # Recent form table
            if "recent" in h2h and len(h2h["recent"]) > 0:
                st.markdown("**Recent Encounters (Last 5)**")
                recent = h2h["recent"][["year", "venue", "match_won_by"]].copy()
                recent.columns = ["Season", "Venue", "Winner"]
                headers = recent.columns.tolist()
                rows = recent.values.tolist()
                render_html_table(headers, rows)
        else:
            st.info(f"No head-to-head records found between {team_a} and {team_b} in the selected range.")

    # ── Tab 3: Consistency Rankings ──
    with tab_consistency:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        chart_header("Team Consistency Index", "Ranking franchises by sustained win percentage (min 5 seasons)")

        consistency = compute_team_consistency(df)

        if len(consistency) > 0:
            fig_con = go.Figure()
            colors = [TEAM_COLORS.get(t, "#71717a") for t in consistency["team"]]
            fig_con.add_trace(go.Bar(
                x=consistency["consistency_index"],
                y=consistency["team"],
                orientation="h",
                marker_color=colors,
                marker_cornerradius=4,
                text=consistency["consistency_index"],
                textposition="outside",
                textfont=dict(size=11, color="#a1a1aa"),
            ))
            update_plotly_layout(
                fig_con, height=max(350, len(consistency) * 45),
                xaxis_title="Consistency Index",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig_con, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Not enough data to compute consistency rankings.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Tab 4: Cap Winners ──
    with tab_caps:
        c_bat, c_bowl = st.columns(2)

        with c_bat:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("🟠 Orange Cap Winners", "Highest run scorers by season")

            bat_season = filtered_df.groupby(["year", "batter"])["runs_batter"].sum().reset_index()
            orange = bat_season.loc[bat_season.groupby("year")["runs_batter"].idxmax()].sort_values("year", ascending=False)

            headers = ["Season", "Player", "Runs"]
            rows = [[str(r["year"]), r["batter"], f"{int(r['runs_batter']):,}"] for _, r in orange.iterrows()]
            render_html_table(headers, rows)
            st.markdown("</div>", unsafe_allow_html=True)

        with c_bowl:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            chart_header("🟣 Purple Cap Winners", "Highest wicket takers by season")

            bowl_season = filtered_df.groupby(["year", "bowler"])["bowler_wicket"].sum().reset_index()
            purple = bowl_season.loc[bowl_season.groupby("year")["bowler_wicket"].idxmax()].sort_values("year", ascending=False)

            headers = ["Season", "Player", "Wickets"]
            rows = [[str(r["year"]), r["bowler"], str(int(r["bowler_wicket"]))] for _, r in purple.iterrows()]
            render_html_table(headers, rows)
            st.markdown("</div>", unsafe_allow_html=True)

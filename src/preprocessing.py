"""
preprocessing.py — IPL Intelligence Hub
Feature engineering pipeline and analytical aggregation functions.
"""

import numpy as np
import pandas as pd
import streamlit as st
import logging

from src.constants import PHASE_BINS, PHASE_LABELS

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Feature Engineering
# ──────────────────────────────────────────────

@st.cache_data(show_spinner="Engineering features…")
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply full feature engineering pipeline to raw ball-by-ball data.
    Creates boundary flags, cumulative aggregates, run rates, and match phases.
    """
    logger.info("Starting feature engineering pipeline...")
    df = df.sort_values(by=["match_id", "innings", "over", "ball"]).reset_index(drop=True)

    # Boundary & dot ball flags
    df["is_four"] = ((df["runs_batter"] == 4) & (df["runs_extras"] == 0)).astype(int)
    df["is_six"] = ((df["runs_batter"] == 6) & (df["runs_extras"] == 0)).astype(int)
    df["is_boundary"] = (df["is_four"] | df["is_six"]).astype(int)
    df["is_dot"] = ((df["runs_total"] == 0) & (df["valid_ball"] == 1)).astype(int)
    df["is_wicket"] = df["wicket_kind"].notna().astype(int)

    # Match phase
    df["match_phase"] = pd.cut(df["over"], bins=PHASE_BINS, labels=PHASE_LABELS)

    # Cumulative aggregates per innings
    df["cumulative_runs"] = df.groupby(["match_id", "innings", "batting_team"])["runs_total"].cumsum()
    df["cumulative_wickets"] = df.groupby(["match_id", "innings", "batting_team"])["is_wicket"].cumsum()

    # Balls remaining in 20-over innings
    df["balls_remaining"] = 120 - (df["over"] * 6 + df["ball"].clip(upper=6))
    df["balls_remaining"] = df["balls_remaining"].clip(lower=0)

    # Chase context (2nd innings only)
    df["runs_needed"] = np.where(
        df["innings"] == 2,
        (df["runs_target"] - df["cumulative_runs"]).clip(lower=0),
        np.nan,
    )
    df["required_run_rate"] = np.where(
        (df["innings"] == 2) & (df["balls_remaining"] > 0),
        (df["runs_needed"] * 6) / df["balls_remaining"],
        0,
    )
    balls_bowled = 120 - df["balls_remaining"]
    df["current_run_rate"] = np.where(
        balls_bowled > 0,
        (df["cumulative_runs"] * 6) / balls_bowled,
        0,
    )
    df["wickets_lost"] = df["cumulative_wickets"]

    logger.info(f"Feature engineering complete. Shape: {df.shape}")
    return df


# ──────────────────────────────────────────────
# Match-Level Summary
# ──────────────────────────────────────────────

@st.cache_data
def build_match_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Build a match-level summary table from ball-by-ball data."""
    match_df = df.groupby("match_id").agg(
        date=("date", "first"),
        year=("year", "first"),
        venue=("venue", "first"),
        city=("city", "first"),
        toss_winner=("toss_winner", "first"),
        toss_decision=("toss_decision", "first"),
        match_won_by=("match_won_by", "first"),
    ).reset_index()

    # Total runs per innings in each match
    inn_runs = df.groupby(["match_id", "innings"])["runs_total"].sum().unstack(fill_value=0)
    inn_runs.columns = ["innings_1_runs", "innings_2_runs"]
    match_df = match_df.merge(inn_runs, on="match_id", how="left")

    # Toss winner won match?
    match_df["toss_winner_won"] = (match_df["toss_winner"] == match_df["match_won_by"]).astype(int)

    return match_df


# ──────────────────────────────────────────────
# Head-to-Head
# ──────────────────────────────────────────────

@st.cache_data
def compute_head_to_head(df: pd.DataFrame, team_a: str, team_b: str) -> dict:
    """Compute head-to-head stats between two teams."""
    # Get matches where both teams played
    matches_a_bat = df[df["batting_team"] == team_a]["match_id"].unique()
    matches_b_bat = df[df["batting_team"] == team_b]["match_id"].unique()
    h2h_match_ids = set(matches_a_bat) & set(matches_b_bat)

    if not h2h_match_ids:
        return {"total": 0, "team_a_wins": 0, "team_b_wins": 0, "records": pd.DataFrame()}

    h2h_df = df[df["match_id"].isin(h2h_match_ids)]
    match_results = h2h_df.groupby("match_id").first()[["year", "venue", "match_won_by"]].reset_index()

    total = len(match_results)
    a_wins = (match_results["match_won_by"] == team_a).sum()
    b_wins = (match_results["match_won_by"] == team_b).sum()

    # Recent form (last 5)
    recent = match_results.sort_values("year", ascending=False).head(5)

    return {
        "total": total,
        "team_a_wins": int(a_wins),
        "team_b_wins": int(b_wins),
        "records": match_results,
        "recent": recent,
    }


# ──────────────────────────────────────────────
# Player Statistics
# ──────────────────────────────────────────────

@st.cache_data
def compute_batter_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate batting stats per player across all seasons."""
    stats = df.groupby("batter").agg(
        matches=("match_id", "nunique"),
        runs=("runs_batter", "sum"),
        balls_faced=("valid_ball", "sum"),
        fours=("is_four", "sum"),
        sixes=("is_six", "sum"),
        boundaries=("is_boundary", "sum"),
        dots_faced=("is_dot", "sum"),
    ).reset_index()
    stats["strike_rate"] = ((stats["runs"] / stats["balls_faced"].clip(lower=1)) * 100).round(1)
    stats["avg_per_match"] = (stats["runs"] / stats["matches"].clip(lower=1)).round(1)
    stats["boundary_pct"] = ((stats["boundaries"] / stats["balls_faced"].clip(lower=1)) * 100).round(1)
    return stats.sort_values("runs", ascending=False).reset_index(drop=True)


@st.cache_data
def compute_bowler_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate bowling stats per player across all seasons."""
    stats = df.groupby("bowler").agg(
        matches=("match_id", "nunique"),
        wickets=("bowler_wicket", "sum"),
        runs_conceded=("runs_bowler", "sum"),
        balls_bowled=("valid_ball", "sum"),
        dots=("is_dot", "sum"),
    ).reset_index()
    stats["economy"] = ((stats["runs_conceded"] / stats["balls_bowled"].clip(lower=1)) * 6).round(2)
    stats["bowling_sr"] = (stats["balls_bowled"] / stats["wickets"].clip(lower=1)).round(1)
    stats["dot_pct"] = ((stats["dots"] / stats["balls_bowled"].clip(lower=1)) * 100).round(1)
    stats["wkts_per_match"] = (stats["wickets"] / stats["matches"].clip(lower=1)).round(2)
    return stats.sort_values("wickets", ascending=False).reset_index(drop=True)


@st.cache_data
def compute_player_season_stats(df: pd.DataFrame, player: str, role: str = "batter") -> pd.DataFrame:
    """Get season-by-season stats for a specific player."""
    if role == "batter":
        stats = df[df["batter"] == player].groupby("year").agg(
            runs=("runs_batter", "sum"),
            balls=("valid_ball", "sum"),
            fours=("is_four", "sum"),
            sixes=("is_six", "sum"),
            matches=("match_id", "nunique"),
        ).reset_index()
        stats["strike_rate"] = ((stats["runs"] / stats["balls"].clip(lower=1)) * 100).round(1)
    else:
        stats = df[df["bowler"] == player].groupby("year").agg(
            wickets=("bowler_wicket", "sum"),
            runs_conceded=("runs_bowler", "sum"),
            balls=("valid_ball", "sum"),
            matches=("match_id", "nunique"),
        ).reset_index()
        stats["economy"] = ((stats["runs_conceded"] / stats["balls"].clip(lower=1)) * 6).round(2)
    return stats


# ──────────────────────────────────────────────
# Phase Analysis
# ──────────────────────────────────────────────

@st.cache_data
def compute_phase_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute aggregate stats for each match phase."""
    phase = df.groupby("match_phase").agg(
        total_runs=("runs_total", "sum"),
        total_balls=("valid_ball", "sum"),
        boundaries=("is_boundary", "sum"),
        wickets=("is_wicket", "sum"),
        sixes=("is_six", "sum"),
        fours=("is_four", "sum"),
        dots=("is_dot", "sum"),
    ).reset_index()
    phase["run_rate"] = ((phase["total_runs"] / phase["total_balls"].clip(lower=1)) * 6).round(2)
    phase["boundary_pct"] = ((phase["boundaries"] / phase["total_balls"].clip(lower=1)) * 100).round(1)
    phase["dot_pct"] = ((phase["dots"] / phase["total_balls"].clip(lower=1)) * 100).round(1)
    return phase


@st.cache_data
def compute_phase_by_season(df: pd.DataFrame) -> pd.DataFrame:
    """Compute phase-wise run rates per season for trend analysis."""
    phase_season = df.groupby(["year", "match_phase"]).agg(
        total_runs=("runs_total", "sum"),
        total_balls=("valid_ball", "sum"),
    ).reset_index()
    phase_season["run_rate"] = ((phase_season["total_runs"] / phase_season["total_balls"].clip(lower=1)) * 6).round(2)
    return phase_season


@st.cache_data
def compute_death_specialists(df: pd.DataFrame, top_n: int = 10):
    """Find top death overs batters and bowlers (overs 16-19)."""
    death = df[df["over"] >= 15].copy()

    # Top batters in death overs
    bat_death = death.groupby("batter").agg(
        runs=("runs_batter", "sum"),
        balls=("valid_ball", "sum"),
        sixes=("is_six", "sum"),
    ).reset_index()
    bat_death["strike_rate"] = ((bat_death["runs"] / bat_death["balls"].clip(lower=1)) * 100).round(1)
    bat_death = bat_death[bat_death["balls"] >= 60].nlargest(top_n, "strike_rate")

    # Top bowlers in death overs
    bowl_death = death.groupby("bowler").agg(
        wickets=("bowler_wicket", "sum"),
        runs_conceded=("runs_bowler", "sum"),
        balls=("valid_ball", "sum"),
        dots=("is_dot", "sum"),
    ).reset_index()
    bowl_death["economy"] = ((bowl_death["runs_conceded"] / bowl_death["balls"].clip(lower=1)) * 6).round(2)
    bowl_death = bowl_death[bowl_death["balls"] >= 60].nsmallest(top_n, "economy")

    return bat_death, bowl_death


# ──────────────────────────────────────────────
# Team Consistency
# ──────────────────────────────────────────────

@st.cache_data
def compute_team_consistency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank teams by consistency index.
    Consistency = mean win% with low standard deviation across seasons.
    """
    # Matches played per team per season
    m_bat = df.groupby(["year", "batting_team"])["match_id"].nunique().reset_index()
    m_bat.columns = ["year", "team", "matches"]

    # Wins per team per season
    m_win = df.groupby(["year", "match_won_by"])["match_id"].nunique().reset_index()
    m_win.columns = ["year", "team", "wins"]

    perf = m_bat.merge(m_win, on=["year", "team"], how="left").fillna(0)
    perf["win_pct"] = (perf["wins"] / perf["matches"].clip(lower=1) * 100).round(1)

    # Filter teams with at least 5 seasons
    team_seasons = perf.groupby("team")["year"].nunique().reset_index()
    team_seasons.columns = ["team", "seasons_played"]
    qualified = team_seasons[team_seasons["seasons_played"] >= 5]["team"].tolist()

    perf_q = perf[perf["team"].isin(qualified)]

    consistency = perf_q.groupby("team").agg(
        avg_win_pct=("win_pct", "mean"),
        std_win_pct=("win_pct", "std"),
        total_matches=("matches", "sum"),
        total_wins=("wins", "sum"),
        seasons=("year", "nunique"),
    ).reset_index()
    consistency["std_win_pct"] = consistency["std_win_pct"].fillna(0).round(1)
    consistency["avg_win_pct"] = consistency["avg_win_pct"].round(1)
    # Consistency index: higher avg win% and lower std = better
    consistency["consistency_index"] = (
        consistency["avg_win_pct"] - 0.5 * consistency["std_win_pct"]
    ).round(1)
    return consistency.sort_values("consistency_index", ascending=False).reset_index(drop=True)


# ──────────────────────────────────────────────
# Season MVPs
# ──────────────────────────────────────────────

@st.cache_data
def compute_season_mvps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a custom MVP score per player per season.
    MVP Score = (Runs / 10) + (Wickets * 15) + (Catches * 5 proxy) + (Boundaries * 2)
    """
    bat = df.groupby(["year", "batter"]).agg(
        runs=("runs_batter", "sum"),
        boundaries=("is_boundary", "sum"),
    ).reset_index().rename(columns={"batter": "player"})

    bowl = df.groupby(["year", "bowler"]).agg(
        wickets=("bowler_wicket", "sum"),
    ).reset_index().rename(columns={"bowler": "player"})

    mvp = bat.merge(bowl, on=["year", "player"], how="outer").fillna(0)
    mvp["mvp_score"] = (
        mvp["runs"] / 10 + mvp["wickets"] * 15 + mvp["boundaries"] * 2
    ).round(1)

    # Top MVP per season
    top_mvps = mvp.loc[mvp.groupby("year")["mvp_score"].idxmax()].sort_values("year", ascending=False)
    return top_mvps.reset_index(drop=True)

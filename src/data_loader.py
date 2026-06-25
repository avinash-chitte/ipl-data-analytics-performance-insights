"""
data_loader.py — IPL Intelligence Hub
Handles loading real IPL data from CSV or generating realistic simulated data.
Uses Python logging and Streamlit caching for performance.
"""

import os
import logging
import pandas as pd
import numpy as np
import streamlit as st

from src.constants import (
    SIM_TEAMS, SIM_VENUES, SIM_BATTERS, SIM_BOWLERS,
)

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Simulated Data Generator
# ──────────────────────────────────────────────

def _generate_simulated_data() -> pd.DataFrame:
    """
    Generate a realistic simulated IPL ball-by-ball dataset.
    Used as a fallback when IPL.csv is not available.
    """
    logger.info("Generating simulated IPL dataset for demonstration...")
    np.random.seed(42)

    n_balls = 18000
    n_matches = 120

    # Build match-level metadata first
    match_ids = np.arange(100001, 100001 + n_matches)
    match_meta = {}
    dates = pd.date_range(start="2008-04-18", end="2025-05-28", periods=n_matches)

    for i, mid in enumerate(match_ids):
        teams = np.random.choice(SIM_TEAMS, size=2, replace=False)
        venue = np.random.choice(SIM_VENUES)
        city_map = {
            "Wankhede Stadium": "Mumbai",
            "M Chinnaswamy Stadium": "Bengaluru",
            "MA Chidambaram Stadium": "Chennai",
            "Eden Gardens": "Kolkata",
            "Rajiv Gandhi Intl Cricket Stadium": "Hyderabad",
            "Arun Jaitley Stadium": "Delhi",
            "Narendra Modi Stadium": "Ahmedabad",
            "IS Bindra Stadium": "Mohali",
            "Sawai Mansingh Stadium": "Jaipur",
        }
        toss_winner = np.random.choice(teams)
        toss_decision = np.random.choice(["field", "bat"], p=[0.65, 0.35])

        # Batting first / second determined by toss
        if toss_decision == "bat":
            batting_first, batting_second = toss_winner, [t for t in teams if t != toss_winner][0]
        else:
            batting_second, batting_first = toss_winner, [t for t in teams if t != toss_winner][0]

        match_won_by = np.random.choice(teams)
        target = np.random.randint(130, 220)

        match_meta[mid] = {
            "date": dates[i],
            "team1": batting_first,
            "team2": batting_second,
            "venue": venue,
            "city": city_map.get(venue, "Mumbai"),
            "toss_winner": toss_winner,
            "toss_decision": toss_decision,
            "match_won_by": match_won_by,
            "target": target,
            "player_of_match": np.random.choice(SIM_BATTERS + SIM_BOWLERS),
        }

    # Generate ball-by-ball data
    rows = []
    balls_per_match = n_balls // n_matches

    for mid in match_ids:
        meta = match_meta[mid]
        for innings in [1, 2]:
            batting_team = meta["team1"] if innings == 1 else meta["team2"]
            bowling_team = meta["team2"] if innings == 1 else meta["team1"]
            n_inn_balls = balls_per_match // 2

            for j in range(n_inn_balls):
                over = min(j // 6, 19)
                ball = (j % 6) + 1
                batter = np.random.choice(SIM_BATTERS)
                bowler = np.random.choice(SIM_BOWLERS)
                non_striker = np.random.choice([b for b in SIM_BATTERS if b != batter])
                runs_batter = np.random.choice([0, 1, 2, 4, 6], p=[0.36, 0.38, 0.09, 0.12, 0.05])
                runs_extras = np.random.choice([0, 1, 4], p=[0.94, 0.05, 0.01])
                runs_total = runs_batter + runs_extras
                wicket_kind = np.random.choice(
                    [None, "caught", "bowled", "lbw", "run out", "stumped"],
                    p=[0.95, 0.025, 0.01, 0.007, 0.005, 0.003],
                )
                bowler_wicket = 1 if wicket_kind in ("caught", "bowled", "lbw", "stumped") else 0

                rows.append({
                    "match_id": mid,
                    "date": meta["date"],
                    "innings": innings,
                    "batting_team": batting_team,
                    "bowling_team": bowling_team,
                    "over": over,
                    "ball": ball,
                    "valid_ball": 1,
                    "batter": batter,
                    "non_striker": non_striker,
                    "bat_pos": np.random.randint(1, 8),
                    "runs_batter": runs_batter,
                    "runs_extras": runs_extras,
                    "runs_total": runs_total,
                    "runs_bowler": runs_total,
                    "bowler": bowler,
                    "wicket_kind": wicket_kind,
                    "bowler_wicket": bowler_wicket,
                    "player_out": batter if wicket_kind else None,
                    "runs_target": float(meta["target"]) if innings == 2 else np.nan,
                    "toss_winner": meta["toss_winner"],
                    "toss_decision": meta["toss_decision"],
                    "venue": meta["venue"],
                    "city": meta["city"],
                    "match_won_by": meta["match_won_by"],
                    "player_of_match": meta["player_of_match"],
                })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["season"] = df["year"].astype(str)
    logger.info(f"Simulated dataset generated: {len(df):,} deliveries across {n_matches} matches.")
    return df


# ──────────────────────────────────────────────
# Real Data Loader
# ──────────────────────────────────────────────

def _load_csv_data() -> pd.DataFrame:
    """Attempt to load real IPL.csv from various paths."""
    paths = [
        "data/IPL.csv",
        "../data/IPL.csv",
        "IPL.csv",
        "/kaggle/input/ipl-dataset2008-2025/IPL.csv",
    ]
    for p in paths:
        if os.path.exists(p):
            logger.info(f"Loading IPL data from: {p}")
            df = pd.read_csv(p)
            df["date"] = pd.to_datetime(df["date"])
            df["year"] = df["date"].dt.year
            df["season"] = df["year"].astype(str)

            # Ensure bowling_team exists
            if "bowling_team" not in df.columns:
                # Derive bowling_team from match batting teams
                match_teams = df.groupby("match_id")["batting_team"].unique()
                def _get_bowling(row):
                    teams = match_teams.get(row["match_id"], [])
                    for t in teams:
                        if t != row["batting_team"]:
                            return t
                    return row["batting_team"]
                df["bowling_team"] = df.apply(_get_bowling, axis=1)

            # Ensure bowler_wicket exists
            if "bowler_wicket" not in df.columns:
                df["bowler_wicket"] = df["wicket_kind"].isin(
                    ["caught", "bowled", "lbw", "stumped", "caught and bowled", "hit wicket"]
                ).astype(int)

            # Ensure non_striker exists
            if "non_striker" not in df.columns:
                df["non_striker"] = "Unknown"

            return df
    return None


# ──────────────────────────────────────────────
# Public Interface (Cached)
# ──────────────────────────────────────────────

@st.cache_data(show_spinner="Loading IPL data…")
def load_data() -> pd.DataFrame:
    """
    Load IPL ball-by-ball data. Falls back to simulated data if CSV not found.
    Returns the raw DataFrame with date/year/season columns.
    """
    try:
        df = _load_csv_data()
        if df is not None:
            return df
        raise FileNotFoundError("IPL.csv not found in any expected location.")
    except Exception as e:
        logger.warning(f"Could not load real data: {e}. Falling back to simulated data.")
        return _generate_simulated_data()

import os
import pandas as pd
import numpy as np

def load_ipl_data(filepath='data/IPL.csv', kaggle_path='/kaggle/input/ipl-dataset2008-2025/IPL.csv'):
    """
    Loads the IPL ball-by-ball dataset.
    Falls back to Kaggle directory if local file is not found.
    """
    if os.path.exists(filepath):
        print(f"Loading data from local path: {filepath}")
        df = pd.read_csv(filepath)
    elif os.path.exists(kaggle_path):
        print(f"Loading data from Kaggle path: {kaggle_path}")
        df = pd.read_csv(kaggle_path)
    else:
        raise FileNotFoundError(
            f"Dataset not found! Please download 'IPL.csv' from Kaggle and place it in the '{os.path.dirname(filepath)}/' directory."
        )
    return df

def engineer_features(df):
    """
    Cleans the raw IPL dataset and engineers new columns for analysis.
    """
    print("Starting feature engineering...")
    
    # 1. Date & Temporal Features
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    df['month_name'] = df['date'].dt.month_name()
    df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
    df['year'] = df['date'].dt.year
    
    # Ensure correct sorting for cumulative metrics
    df = df.sort_values(by=['match_id', 'innings', 'over', 'ball']).reset_index(drop=True)
    
    # 2. Over-by-Over & Match Phases
    # Categorize match phases (Powerplay: overs 0-5, Middle: 6-14, Death: 15-19)
    # The 'over' column is 0-indexed (0 to 19)
    df['match_phase'] = pd.cut(
        df['over'], 
        bins=[-1, 5, 14, 20], 
        labels=['Powerplay', 'Middle Overs', 'Death Overs']
    )
    
    # 3. Boundaries & Dot Balls
    # Fours and Sixes are identified from runs_total and runs_extras
    df['is_four'] = (df['runs_total'] == 4) & (df['runs_extras'] == 0)
    df['is_six'] = (df['runs_total'] == 6) & (df['runs_extras'] == 0)
    df['is_boundary'] = df['is_four'] | df['is_six']
    df['is_dot'] = (df['runs_total'] == 0) & (df['valid_ball'] == 1)
    
    # 4. Wicket Features
    # Any non-null wicket_kind indicates a wicket
    # In cricket, some wickets are credited to the bowler, others (run out, retired hurt) are not.
    df['is_wicket'] = df['wicket_kind'].notna().astype(int)
    
    # 5. Cumulative Match Context
    # Cumulative runs and wickets for each innings in a match
    df['cumulative_runs'] = df.groupby(['match_id', 'innings', 'batting_team'])['runs_total'].cumsum()
    df['cumulative_wickets'] = df.groupby(['match_id', 'innings', 'batting_team'])['is_wicket'].cumsum()
    
    # Balls remaining in the 20-over innings
    # 120 balls total. Overs are 0 to 19, ball is 1 to 6.
    # Note: Extras (like wides/no balls) don't count as valid balls, but they do consume balls in some metrics.
    # We estimate valid balls remaining
    df['balls_remaining'] = 120 - (df['over'] * 6 + df['ball'].clip(upper=6))
    df['balls_remaining'] = df['balls_remaining'].clip(lower=0)
    
    # 6. Target chasing columns (only for 2nd innings)
    # Target runs is runs_target. Required run rate can be calculated.
    if 'runs_target' in df.columns:
        # Calculate runs needed
        df['runs_needed'] = df['runs_target'] - df['cumulative_runs']
        # If runs_needed < 0, they have already won (runs_needed should be clipped at 0 for win probabilities)
        df['runs_needed'] = df['runs_needed'].clip(lower=0)
        
        # Required run rate = (runs_needed) / (balls_remaining / 6)
        df['required_run_rate'] = np.where(
            df['balls_remaining'] > 0,
            (df['runs_needed'] * 6) / df['balls_remaining'],
            0
        )
        # Handle cases where required run rate explodes or is irrelevant (e.g. after match finishes)
        df.loc[df['innings'] != 2, 'runs_needed'] = np.nan
        df.loc[df['innings'] != 2, 'required_run_rate'] = np.nan
    
    print("Feature engineering complete!")
    return df

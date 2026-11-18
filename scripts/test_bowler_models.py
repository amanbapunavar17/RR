import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np

from src.analysis.data_loader import load_all_datasets
from src.analysis.data_cleaner import clean_data
from src.analysis.match_state import compute_match_states
from src.analysis.pressure_engine import compute_delivery_pressure

datasets = load_all_datasets()
df_clean, matches = clean_data(datasets)
df_state = compute_match_states(df_clean)
df = compute_delivery_pressure(df_state)

df_lb = df[df['is_legal_ball']].copy()
pop_bowl_press_econ = (df_lb[df_lb['is_high_bowling_pressure']]['bowler_runs'].sum() / df_lb[df_lb['is_high_bowling_pressure']]['is_legal_ball'].sum()) * 6.0
pop_bowl_norm_econ = (df_lb[~df_lb['is_high_bowling_pressure']]['bowler_runs'].sum() / df_lb[~df_lb['is_high_bowling_pressure']]['is_legal_ball'].sum()) * 6.0
pop_bowl_press_dot = (df_lb[df_lb['is_high_bowling_pressure']]['is_dot_ball_bowler'].sum() / df_lb[df_lb['is_high_bowling_pressure']]['is_legal_ball'].sum()) * 100
pop_bowl_press_sr = df_lb[df_lb['is_high_bowling_pressure']]['is_legal_ball'].sum() / max(1, df_lb[df_lb['is_high_bowling_pressure']]['is_bowler_wicket'].sum())

print(f"Population Bowler Pressure Econ: {pop_bowl_press_econ:.2f}, Normal Econ: {pop_bowl_norm_econ:.2f}")
print(f"Population Bowler Pressure Dot%: {pop_bowl_press_dot:.2f}%, Wicket SR: {pop_bowl_press_sr:.2f}")

bowl_stats = []
for (pid, pname), group in df_lb.groupby(['bowler_id', 'bowler_name']):
    press_grp = group[group['is_high_bowling_pressure']]
    norm_grp = group[~group['is_high_bowling_pressure']]
    
    p_balls = press_grp['is_legal_ball'].sum()
    n_balls = norm_grp['is_legal_ball'].sum()
    
    if p_balls < 200:  # Preliminary threshold (at least 33.2 overs under pressure)
        continue
        
    p_runs = press_grp['bowler_runs'].sum()
    p_wkts = press_grp['is_bowler_wicket'].sum()
    p_dots = press_grp['is_dot_ball_bowler'].sum()
    p_bnds = press_grp['is_boundary'].sum()
    p_matches = press_grp['match_id'].nunique()
    
    n_runs = norm_grp['bowler_runs'].sum()
    n_wkts = norm_grp['is_bowler_wicket'].sum()
    n_dots = norm_grp['is_dot_ball_bowler'].sum()
    n_bnds = norm_grp['is_boundary'].sum()
    
    p_econ = (p_runs / p_balls) * 6.0
    n_econ = (n_runs / n_balls * 6.0) if n_balls > 0 else pop_bowl_norm_econ
    
    # Delta econ: normal - pressure (positive means bowler got tighter under pressure!)
    delta_econ = n_econ - p_econ
    
    p_dot_pct = (p_dots / p_balls) * 100
    n_dot_pct = (n_dots / max(1, n_balls)) * 100
    delta_dot_pct = p_dot_pct - n_dot_pct
    
    p_bnd_pct = (p_bnds / p_balls) * 100
    n_bnd_pct = (n_bnds / max(1, n_balls)) * 100
    delta_bnd_pct = n_bnd_pct - p_bnd_pct  # positive means conceded fewer boundaries under pressure
    
    p_sr = (p_balls / max(1, p_wkts))
    p_w_rate = (p_wkts / p_balls) * 6.0  # wickets per 6 legal balls
    
    # Match consistency: proportion of matches with economy <= 8.5 or >= 1 wicket
    match_impacts = []
    for mid, mgrp in press_grp.groupby('match_id'):
        m_runs = mgrp['bowler_runs'].sum()
        m_balls = mgrp['is_legal_ball'].sum()
        m_wkts = mgrp['is_bowler_wicket'].sum()
        m_econ = (m_runs / m_balls) * 6.0 if m_balls > 0 else 8.0
        match_impacts.append(1 if (m_econ <= 8.5 or m_wkts >= 1) else 0)
    consistency = np.mean(match_impacts) if match_impacts else 0.5
    
    # Bayesian Shrinkage for Economy (K=60 balls)
    K_bowl = 60.0
    w_p = p_balls / (p_balls + K_bowl)
    shrunk_p_econ = w_p * p_econ + (1 - w_p) * pop_bowl_press_econ
    shrunk_delta_econ = w_p * delta_econ
    
    bowl_stats.append({
        'player_id': pid,
        'player_name': pname,
        'pressure_balls': p_balls,
        'pressure_runs': p_runs,
        'pressure_wickets': p_wkts,
        'pressure_econ': p_econ,
        'normal_econ': n_econ,
        'delta_econ': delta_econ,
        'shrunk_econ': shrunk_p_econ,
        'pressure_dot_pct': p_dot_pct,
        'delta_dot_pct': delta_dot_pct,
        'pressure_bnd_pct': p_bnd_pct,
        'pressure_sr': p_sr,
        'pressure_w_rate': p_w_rate,
        'pressure_matches': p_matches,
        'consistency': consistency
    })

bowl_df = pd.DataFrame(bowl_stats)
print(f"Total qualified bowlers (>= 200 balls): {len(bowl_df)}")

# Normalized composite score:
# Dimensions:
# 1. Shrunk Pressure Economy (-z because lower is better) (30%)
# 2. Economy Improvement vs baseline (Delta Econ) (25%)
# 3. Wicket Taking Rate under pressure (20%)
# 4. Dot-ball % under pressure (15%)
# 5. Match consistency (10%)
from scipy.stats import zscore
bowl_df['z_shrunk_econ'] = -zscore(bowl_df['shrunk_econ'])
bowl_df['z_delta_econ'] = zscore(bowl_df['delta_econ'])
bowl_df['z_w_rate'] = zscore(bowl_df['pressure_w_rate'])
bowl_df['z_dot'] = zscore(bowl_df['pressure_dot_pct'])
bowl_df['z_cons'] = zscore(bowl_df['consistency'])

bowl_df['raw_composite'] = (
    0.30 * bowl_df['z_shrunk_econ'] +
    0.25 * bowl_df['z_delta_econ'] +
    0.20 * bowl_df['z_w_rate'] +
    0.15 * bowl_df['z_dot'] +
    0.10 * bowl_df['z_cons']
)

min_s = bowl_df['raw_composite'].min()
max_s = bowl_df['raw_composite'].max()
bowl_df['pressure_score'] = 50.0 + (bowl_df['raw_composite'] / max(abs(min_s), abs(max_s))) * 45.0
bowl_df['pressure_score'] = bowl_df['pressure_score'].round(2)

print("\n--- TOP 20 BOWLERS UNDER PRESSURE ---")
print(bowl_df.sort_values(by='pressure_score', ascending=False)[
    ['player_id', 'player_name', 'pressure_score', 'pressure_balls', 'pressure_wickets', 'pressure_econ', 'normal_econ', 'delta_econ', 'pressure_dot_pct', 'consistency']
].head(20).to_string())


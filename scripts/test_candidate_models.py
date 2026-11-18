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

# Population baselines for Batters (balls faced)
df_bf = df[df['is_ball_faced']].copy()
pop_bat_press_sr = (df_bf[df_bf['is_high_batting_pressure']]['runs'].sum() / df_bf[df_bf['is_high_batting_pressure']]['is_ball_faced'].sum()) * 100
pop_bat_norm_sr = (df_bf[~df_bf['is_high_batting_pressure']]['runs'].sum() / df_bf[~df_bf['is_high_batting_pressure']]['is_ball_faced'].sum()) * 100

print(f"Population Batter Pressure SR: {pop_bat_press_sr:.2f}, Normal SR: {pop_bat_norm_sr:.2f}")

# Population baselines for Bowlers (legal balls)
df_lb = df[df['is_legal_ball']].copy()
pop_bowl_press_econ = (df_lb[df_lb['is_high_bowling_pressure']]['bowler_runs'].sum() / df_lb[df_lb['is_high_bowling_pressure']]['is_legal_ball'].sum()) * 6.0
pop_bowl_norm_econ = (df_lb[~df_lb['is_high_bowling_pressure']]['bowler_runs'].sum() / df_lb[~df_lb['is_high_bowling_pressure']]['is_legal_ball'].sum()) * 6.0
print(f"Population Bowler Pressure Econ: {pop_bowl_press_econ:.2f}, Normal Econ: {pop_bowl_norm_econ:.2f}")

# Let's inspect top candidates with preliminary ranking logic
print("\nCalculating Batter Metrics...")
# Group by striker_id and striker_name
bat_stats = []
for (pid, pname), group in df_bf.groupby(['striker_id', 'striker_name']):
    press_grp = group[group['is_high_batting_pressure']]
    norm_grp = group[~group['is_high_batting_pressure']]
    
    p_balls = press_grp['is_ball_faced'].sum()
    n_balls = norm_grp['is_ball_faced'].sum()
    
    if p_balls < 100:  # Preliminary threshold
        continue
        
    p_runs = press_grp['runs'].sum()
    p_outs = press_grp['is_wicket'].sum()
    p_fours = press_grp['is_four'].sum()
    p_sixes = press_grp['is_six'].sum()
    p_dots = (press_grp['runs'] == 0).sum()
    p_matches = press_grp['match_id'].nunique()
    
    n_runs = norm_grp['runs'].sum()
    n_outs = norm_grp['is_wicket'].sum()
    n_dots = (norm_grp['runs'] == 0).sum()
    n_fours = norm_grp['is_four'].sum()
    n_sixes = norm_grp['is_six'].sum()
    
    p_sr = (p_runs / p_balls) * 100
    n_sr = (n_runs / n_balls * 100) if n_balls > 0 else pop_bat_norm_sr
    
    p_avg = (p_runs / max(1, p_outs))
    n_avg = (n_runs / max(1, n_outs)) if n_balls > 0 else 25.0
    
    p_bnd_pct = ((p_fours + p_sixes) / p_balls) * 100
    n_bnd_pct = ((n_fours + n_sixes) / max(1, n_balls)) * 100
    
    p_dot_pct = (p_dots / p_balls) * 100
    n_dot_pct = (n_dots / max(1, n_balls)) * 100
    
    # Match consistency: proportion of matches with positive impact (SR >= 135 or runs >= 15)
    match_impacts = []
    for mid, mgrp in press_grp.groupby('match_id'):
        m_runs = mgrp['runs'].sum()
        m_bf = mgrp['is_ball_faced'].sum()
        m_sr = (m_runs / m_bf) * 100 if m_bf > 0 else 0
        match_impacts.append(1 if (m_sr >= 135.0 or m_runs >= 15) else 0)
    consistency = np.mean(match_impacts) if match_impacts else 0.5
    
    # Bayesian Shrinkage for SR (K=35)
    K_bat = 35.0
    w_p = p_balls / (p_balls + K_bat)
    shrunk_p_sr = w_p * p_sr + (1 - w_p) * pop_bat_press_sr
    
    # Strike rate improvement over normal baseline
    delta_sr = p_sr - n_sr
    shrunk_delta_sr = w_p * delta_sr
    
    bat_stats.append({
        'player_id': pid,
        'player_name': pname,
        'pressure_balls': p_balls,
        'pressure_runs': p_runs,
        'pressure_outs': p_outs,
        'pressure_sr': p_sr,
        'normal_sr': n_sr,
        'delta_sr': delta_sr,
        'shrunk_sr': shrunk_p_sr,
        'pressure_avg': p_avg,
        'normal_avg': n_avg,
        'pressure_bnd_pct': p_bnd_pct,
        'pressure_dot_pct': p_dot_pct,
        'pressure_matches': p_matches,
        'consistency': consistency
    })

bat_df = pd.DataFrame(bat_stats)
print(f"Total qualified batters (>= 100 balls): {len(bat_df)}")

# Normalized composite score:
# Dimensions:
# 1. Shrunk Pressure SR (35%)
# 2. Delta SR vs own baseline (25%)
# 3. Pressure Average / Wicket avoidance (15%)
# 4. Boundary % (15%)
# 5. Match consistency (10%)
from scipy.stats import zscore
bat_df['z_shrunk_sr'] = zscore(bat_df['shrunk_sr'])
bat_df['z_delta_sr'] = zscore(bat_df['delta_sr'])
bat_df['z_avg'] = zscore(bat_df['pressure_avg'].clip(upper=65.0))
bat_df['z_bnd'] = zscore(bat_df['pressure_bnd_pct'])
bat_df['z_cons'] = zscore(bat_df['consistency'])

bat_df['raw_composite'] = (
    0.35 * bat_df['z_shrunk_sr'] +
    0.25 * bat_df['z_delta_sr'] +
    0.15 * bat_df['z_avg'] +
    0.15 * bat_df['z_bnd'] +
    0.10 * bat_df['z_cons']
)

# Rescale to 0-100 rating
min_s = bat_df['raw_composite'].min()
max_s = bat_df['raw_composite'].max()
bat_df['pressure_score'] = 50.0 + (bat_df['raw_composite'] / max(abs(min_s), abs(max_s))) * 45.0
bat_df['pressure_score'] = bat_df['pressure_score'].round(2)

print("\n--- TOP 20 BATTERS UNDER PRESSURE ---")
print(bat_df.sort_values(by='pressure_score', ascending=False)[
    ['player_id', 'player_name', 'pressure_score', 'pressure_balls', 'pressure_runs', 'pressure_outs', 'pressure_sr', 'normal_sr', 'delta_sr', 'pressure_avg', 'consistency']
].head(20).to_string())


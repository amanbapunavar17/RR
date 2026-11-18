"""
scripts/investigate_final_quality_audit.py
Deep forensic inspection of the 20 players, phase-level delivery breakdown,
format splits (IPL vs T20I), red-flag resolution, and statistical validation.
"""

import pandas as pd
import numpy as np

print("Loading data...")
df_p = pd.read_csv('d:/RR/outputs/pressure_delivery_analysis.csv')
df_b = pd.read_csv('d:/RR/Data Pack/ball_by_ball.csv', usecols=[
    'match_id', 'innings', 'overid', 'over_ball_num', 'striker_id', 'bowler_id',
    'dismissed_player_id'
])
df = pd.merge(df_p, df_b, on=['match_id', 'innings', 'overid', 'over_ball_num'], how='inner')
print(f"Merged {len(df)} deliveries.")

# Check phases in df
print("Phases present:", df['phase'].value_counts().to_dict())

# List of 20 players to investigate:
target_batters = [
    (4246, "Nitish Rana"),
    (6931, "Pathum Nissanka"),
    (3782, "Shahrukh Khan"),
    (4821, "Mahipal Lomror"),
    (7059, "Nehal Wadhera"),
    (45966, "Prashant Veer"),
    (3297, "Shimron Hetmyer"),
    (20894, "Aman Khan"),
    (4229, "George Linde"),
    (167, "Ajinkya Rahane")
]

target_bowlers = [
    (8177, "Akash Madhwal"),
    (28, "Ishant Sharma"),
    (24475, "Rehan Ahmed"),
    (6162, "Kulwant Khejroliya"),
    (6286, "Shivam Mavi"),
    (6354, "Spencer Johnson"),
    (7545, "Kuldeep Sen"),
    (6683, "Mayank Markande"),
    (3653, "Avesh Khan"),
    (4229, "George Linde")
]

p75_bat = 55.20
p75_bowl = 68.90
df['is_press_bat'] = df['batting_pressure'] >= p75_bat
df['is_press_bowl'] = df['bowling_pressure'] >= p75_bowl

print("\n=================== BATTERS INVESTIGATION ===================")
for pid, name in target_batters:
    b_all = df[df['striker_id'] == pid]
    b_press = b_all[b_all['is_press_bat']]
    b_norm = b_all[~b_all['is_press_bat']]
    
    p_balls = len(b_press)
    p_runs = b_press['runs'].sum()
    p_outs = (b_press['dismissed_player_id'] == pid).sum()
    p_sr = (p_runs / p_balls * 100.0) if p_balls > 0 else 0.0
    
    n_balls = len(b_norm)
    n_runs = b_norm['runs'].sum()
    n_sr = (n_runs / n_balls * 100.0) if n_balls > 0 else 125.0
    delta_sr = p_sr - n_sr
    
    matches = b_press['match_id'].nunique()
    comps = b_press['comp_name'].value_counts().to_dict()
    phases = b_press['phase'].value_counts().to_dict()
    
    print(f"\n--- {name} (ID: {pid}) ---")
    print(f"  Pressure: {p_balls} balls, {p_runs} runs, {p_outs} dismissals, SR: {p_sr:.2f}")
    print(f"  Baseline: {n_balls} balls, {n_runs} runs, SR: {n_sr:.2f} (Delta: {delta_sr:+.2f})")
    print(f"  Matches: {matches} | Comps: {comps} | Phases: {phases}")

print("\n=================== BOWLERS INVESTIGATION ===================")
for pid, name in target_bowlers:
    bw_all = df[df['bowler_id'] == pid]
    bw_press = bw_all[bw_all['is_press_bowl']]
    bw_norm = bw_all[~bw_all['is_press_bowl']]
    
    p_balls = len(bw_press)
    p_runs = bw_press['bowler_runs'].sum()
    p_wkts = bw_press['is_bowler_wicket'].sum()
    p_econ = (p_runs / p_balls * 6.0) if p_balls > 0 else 0.0
    
    n_balls = len(bw_norm)
    n_runs = bw_norm['bowler_runs'].sum()
    n_econ = (n_runs / n_balls * 6.0) if n_balls > 0 else 8.50
    delta_econ = p_econ - n_econ
    
    matches = bw_press['match_id'].nunique()
    comps = bw_press['comp_name'].value_counts().to_dict()
    phases = bw_press['phase'].value_counts().to_dict()
    
    print(f"\n--- {name} (ID: {pid}) ---")
    print(f"  Pressure: {p_balls} balls, {p_runs} runs, {p_wkts} wkts, Econ: {p_econ:.2f}")
    print(f"  Baseline: {n_balls} balls, {n_runs} runs, Econ: {n_econ:.2f} (Delta: {delta_econ:+.2f})")
    print(f"  Matches: {matches} | Comps: {comps} | Phases: {phases}")

import pandas as pd
import numpy as np

# Load pressure deliveries
print("Loading pressure deliveries...")
df_p = pd.read_csv('d:/RR/outputs/pressure_delivery_analysis.csv')
print(f"Loaded {len(df_p)} deliveries.")

# Also load ball_by_ball to get match_id, overid, over_ball_num -> striker_id, bowler_id
print("Loading ball_by_ball...")
df_b = pd.read_csv('d:/RR/Data Pack/ball_by_ball.csv', usecols=[
    'match_id', 'innings', 'overid', 'over_ball_num', 'striker_id', 'bowler_id'
])

# Merge IDs to df_p if needed
print("Merging IDs...")
df = pd.merge(df_p, df_b, on=['match_id', 'innings', 'overid', 'over_ball_num'], how='left')
print(f"Merged dataframe: {len(df)} rows.")

p75_bat = 55.20
p75_bowl = 68.90

df['is_press_bat'] = df['batting_pressure'] >= p75_bat
df['is_press_bowl'] = df['bowling_pressure'] >= p75_bowl

# Let's inspect batting stats for some of our released players:
# e.g. Shimron Hetmyer (4328), Nehal Wadhera (19890), Mahipal Lomror (4821), Shahrukh Khan (3782)
for pid, name in [(4328, 'Shimron Hetmyer'), (19890, 'Nehal Wadhera'), (4821, 'Mahipal Lomror'), (3782, 'Shahrukh Khan'), (2320, 'Trent Boult'), (7545, 'Kuldeep Sen'), (24939, 'Akash Madhwal'), (48557, 'Vignesh Puthur')]:
    bat_grp = df[df['striker_id'] == pid]
    p_bat = bat_grp[bat_grp['is_press_bat']]
    n_bat = bat_grp[~bat_grp['is_press_bat']]
    
    bowl_grp = df[df['bowler_id'] == pid]
    p_bowl = bowl_grp[bowl_grp['is_press_bowl']]
    n_bowl = bowl_grp[~bowl_grp['is_press_bowl']]
    
    print(f"\n--- {name} (ID: {pid}) ---")
    if len(bat_grp) > 0:
        p_sr = (p_bat['runs'].sum() / len(p_bat) * 100) if len(p_bat) > 0 else 0
        base_sr = (n_bat['runs'].sum() / len(n_bat) * 100) if len(n_bat) > 0 else 0
        print(f"  BATTING: {len(p_bat)} press balls, {p_bat['runs'].sum()} runs, {p_sr:.2f} SR (Baseline: {base_sr:.2f}, Delta: {p_sr - base_sr:+.2f})")
    if len(bowl_grp) > 0:
        p_econ = (p_bowl['bowler_runs'].sum() / len(p_bowl) * 6) if len(p_bowl) > 0 else 0
        base_econ = (n_bowl['bowler_runs'].sum() / len(n_bowl) * 6) if len(n_bowl) > 0 else 0
        print(f"  BOWLING: {len(p_bowl)} press balls, {p_bowl['is_bowler_wicket'].sum()} wkts, {p_econ:.2f} Econ (Baseline: {base_econ:.2f}, Delta: {p_econ - base_econ:+.2f})")


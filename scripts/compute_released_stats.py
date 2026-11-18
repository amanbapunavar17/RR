import pandas as pd
import numpy as np

# Load resolved released players
rel_df = pd.read_csv('d:/RR/outputs/temp_resolved_released_players.csv')
pids = set(rel_df['player_id'].unique())
print(f"Tracking {len(pids)} unique released player IDs.")

# Load delivery pressure analysis
print("Loading pressure delivery analysis...")
df_p = pd.read_csv('d:/RR/outputs/pressure_delivery_analysis.csv')

# Load ball by ball IDs
print("Loading ball by ball IDs...")
df_b = pd.read_csv('d:/RR/Data Pack/ball_by_ball.csv', usecols=[
    'match_id', 'innings', 'overid', 'over_ball_num', 'striker_id', 'bowler_id', 'dismissed_player_id'
])

# Merge
df = pd.merge(df_p, df_b, on=['match_id', 'innings', 'overid', 'over_ball_num'], how='inner')
print(f"Merged {len(df)} deliveries.")

p75_bat = 55.20
p75_bowl = 68.90

df['is_press_bat'] = df['batting_pressure'] >= p75_bat
df['is_press_bowl'] = df['bowling_pressure'] >= p75_bowl

# Batting stats
bat_records = []
for pid in pids:
    p_info = rel_df[rel_df['player_id'] == pid].iloc[0]
    b_all = df[df['striker_id'] == pid]
    if len(b_all) == 0:
        continue
    
    b_press = b_all[b_all['is_press_bat']]
    b_norm = b_all[~b_all['is_press_bat']]
    
    press_balls = len(b_press)
    press_runs = b_press['runs'].sum()
    press_outs = (b_press['dismissed_player_id'] == pid).sum()
    press_sr = (press_runs / press_balls * 100.0) if press_balls > 0 else 0.0
    
    norm_balls = len(b_norm)
    norm_runs = b_norm['runs'].sum()
    norm_sr = (norm_runs / norm_balls * 100.0) if norm_balls > 0 else 125.0
    
    delta_sr = press_sr - norm_sr if press_balls > 0 else 0.0
    press_avg = (press_runs / press_outs) if press_outs > 0 else (press_runs * 1.5 if press_runs > 0 else 0.0)
    
    # Consistency across matches
    m_grp = b_press.groupby('match_id').size()
    match_count = len(m_grp)
    
    bat_records.append({
        'player_id': pid,
        'name': p_info['name'],
        'franchise': p_info['franchise'],
        'is_overseas': p_info['is_overseas'],
        'salary_lakhs': p_info['salary_lakhs'],
        'press_bat_balls': press_balls,
        'press_bat_runs': press_runs,
        'press_bat_outs': press_outs,
        'press_bat_sr': round(press_sr, 2),
        'norm_bat_sr': round(norm_sr, 2),
        'delta_bat_sr': round(delta_sr, 2),
        'press_bat_avg': round(press_avg, 2),
        'bat_match_count': match_count
    })

bat_df = pd.DataFrame(bat_records)
print(f"\nFound {len(bat_df)} released players who batted:")
print(bat_df.sort_values(by='press_bat_balls', ascending=False).head(15))

# Bowling stats
bowl_records = []
for pid in pids:
    p_info = rel_df[rel_df['player_id'] == pid].iloc[0]
    b_all = df[df['bowler_id'] == pid]
    if len(b_all) == 0:
        continue
    
    b_press = b_all[b_all['is_press_bowl']]
    b_norm = b_all[~b_all['is_press_bowl']]
    
    press_balls = len(b_press)
    press_runs = b_press['bowler_runs'].sum()
    press_wkts = b_press['is_bowler_wicket'].sum()
    press_econ = (press_runs / press_balls * 6.0) if press_balls > 0 else 0.0
    
    norm_balls = len(b_norm)
    norm_runs = b_norm['bowler_runs'].sum()
    norm_econ = (norm_runs / norm_balls * 6.0) if norm_balls > 0 else 8.50
    
    delta_econ = press_econ - norm_econ if press_balls > 0 else 0.0
    wkt_rate = (press_balls / press_wkts) if press_wkts > 0 else (press_balls * 2.0 if press_balls > 0 else 99.0)
    dot_pct = (b_press['bowler_runs'] == 0).sum() / press_balls * 100.0 if press_balls > 0 else 0.0
    
    m_grp = b_press.groupby('match_id').size()
    match_count = len(m_grp)
    
    bowl_records.append({
        'player_id': pid,
        'name': p_info['name'],
        'franchise': p_info['franchise'],
        'is_overseas': p_info['is_overseas'],
        'salary_lakhs': p_info['salary_lakhs'],
        'press_bowl_balls': press_balls,
        'press_bowl_runs': press_runs,
        'press_bowl_wkts': press_wkts,
        'press_bowl_econ': round(press_econ, 2),
        'norm_bowl_econ': round(norm_econ, 2),
        'delta_bowl_econ': round(delta_econ, 2),
        'press_bowl_dot_pct': round(dot_pct, 1),
        'bowl_match_count': match_count
    })

bowl_df = pd.DataFrame(bowl_records)
print(f"\nFound {len(bowl_df)} released players who bowled:")
print(bowl_df.sort_values(by='press_bowl_balls', ascending=False).head(15))


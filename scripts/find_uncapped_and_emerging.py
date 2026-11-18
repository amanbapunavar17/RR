"""
scripts/find_uncapped_and_emerging.py
Searches the full ball-by-ball dataset for players with lower ball samples
(e.g., 30 to 150 pressure balls) who exhibit extraordinary pressure performance,
focusing on uncapped Indians, state/regional/emerging stars, and undervalued specialists.
"""

import os
import pandas as pd
import numpy as np

# Load preprocessed pressure delivery data
df = pd.read_csv("outputs/pressure_delivery_analysis.csv")
pm = pd.read_csv("Data Pack/competition_team_player_mapping.csv")

p75_bat = 55.20
p75_bowl = 68.90

df['is_press_bat'] = df['batting_pressure'] >= p75_bat
df['is_press_bowl'] = df['bowling_pressure'] >= p75_bowl

# Mapping of players to teams
p_teams = pm.groupby('player_id')['team_name'].apply(lambda x: list(set(x))).to_dict()

# Flag Pakistani players
pak_pids = set([pid for pid, tnames in p_teams.items() if any('Pakistan' in t for t in tnames)])
# Flag Indian players (played for India or only in IPL/Indian domestic/Rising Stars)
india_pids = set([pid for pid, tnames in p_teams.items() if any('India' in t for t in tnames)])

# BATTERS: 30 to 200 pressure balls
bat_list = []
for (pid, pname), grp in df[df['is_ball_faced']].groupby(['striker_id', 'striker_name']):
    if pid in pak_pids:
        continue
    p_grp = grp[grp['is_press_bat']]
    n_grp = grp[~grp['is_press_bat']]
    p_balls = len(p_grp)
    if p_balls < 35:
        continue
    p_runs = p_grp['runs'].sum()
    p_outs = p_grp['is_dismissal'].sum()
    p_sr = (p_runs / p_balls) * 100.0
    n_sr = (n_grp['runs'].sum() / len(n_grp) * 100.0) if len(n_grp) > 0 else 125.0
    p_avg = (p_runs / p_outs) if p_outs > 0 else p_runs * 1.5
    
    # Check teams
    teams_played = p_teams.get(pid, [])
    is_capped = pid in india_pids
    ipl_balls = len(p_grp[p_grp['comp_name'].str.contains('IPL', case=False, na=False)])
    
    bat_list.append({
        'player_id': pid, 'player_name': pname,
        'pressure_balls': p_balls, 'pressure_runs': p_runs, 'pressure_sr': round(p_sr, 2),
        'normal_sr': round(n_sr, 2), 'delta_sr': round(p_sr - n_sr, 2),
        'pressure_avg': round(p_avg, 2), 'dismissals': p_outs,
        'ipl_balls': ipl_balls, 'is_capped_india': is_capped,
        'teams': ", ".join(teams_played)[:40]
    })

df_bats = pd.DataFrame(bat_list)
print("\n--- EMERGING / UNCAPPED / UNDERVALUED BATTERS (High Pressure SR & Lift, Balls >= 35) ---")
print(df_bats[(df_bats['pressure_sr'] >= 150) & (df_bats['pressure_balls'] >= 40)].sort_values(by='pressure_sr', ascending=False).head(30).to_string())

# BOWLERS: 40 to 240 pressure balls
bowl_list = []
for (pid, pname), grp in df[df['is_legal_ball']].groupby(['bowler_id', 'bowler_name']):
    if pid in pak_pids:
        continue
    p_grp = grp[grp['is_press_bowl']]
    n_grp = grp[~grp['is_press_bowl']]
    p_balls = len(p_grp)
    if p_balls < 40:
        continue
    p_runs = p_grp['bowler_runs'].sum()
    p_wkts = p_grp['is_bowler_wicket'].sum()
    p_econ = (p_runs / p_balls) * 6.0
    n_econ = (n_grp['bowler_runs'].sum() / len(n_grp) * 6.0) if len(n_grp) > 0 else 8.5
    
    teams_played = p_teams.get(pid, [])
    is_capped = pid in india_pids
    ipl_balls = len(p_grp[p_grp['comp_name'].str.contains('IPL', case=False, na=False)])
    
    bowl_list.append({
        'player_id': pid, 'player_name': pname,
        'pressure_balls': p_balls, 'pressure_runs': p_runs, 'pressure_econ': round(p_econ, 2),
        'normal_econ': round(n_econ, 2), 'delta_econ': round(n_econ - p_econ, 2),
        'pressure_wkts': p_wkts, 'wkt_rate': round(p_wkts / p_balls * 6.0, 3),
        'ipl_balls': ipl_balls, 'is_capped_india': is_capped,
        'teams': ", ".join(teams_played)[:40]
    })

df_bowls = pd.DataFrame(bowl_list)
print("\n--- EMERGING / UNCAPPED / UNDERVALUED BOWLERS (Pressure Econ <= 8.50, Balls >= 50) ---")
print(df_bowls[(df_bowls['pressure_econ'] <= 8.50) & (df_bowls['pressure_balls'] >= 50)].sort_values(by='pressure_econ', ascending=True).head(30).to_string())

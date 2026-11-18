"""
scripts/discover_hidden_gems.py
Identifies emerging, uncapped, and undervalued Indian and overseas talent
who demonstrate elite pressure metrics across flexible sample sizes (e.g. 40-120 balls).
"""

import os
import pandas as pd
import numpy as np

# Load bbb and metadata
bbb = pd.read_csv("Data Pack/ball_by_ball.csv")
matches = pd.read_csv("Data Pack/matches.csv")
comps = pd.read_csv("Data Pack/competitions.csv")
pm = pd.read_csv("Data Pack/competition_team_player_mapping.csv")

# Filter standard innings
df = bbb[bbb['innings'].isin([1, 2])].copy()

# Identify player teams
player_teams = pm.groupby('player_id')['team_name'].apply(lambda x: list(set(x))).to_dict()
player_comps = pm.groupby('player_id')['comp_name'].apply(lambda x: list(set(x))).to_dict()

# Flag Pakistani players
pak_players = set()
for pid, tnames in player_teams.items():
    if any('Pakistan' in t for t in tnames):
        pak_players.add(pid)

print(f"Total Pakistani players flagged: {len(pak_players)}")

# Load pressure scores computed in audit script
# Let's run a fast delivery-level calculation to get all players
from scipy.stats import zscore

# Read verified metrics if available, or compute on the fly
b_all = pd.read_csv("outputs/all_batter_metrics.csv")
bw_all = pd.read_csv("outputs/all_bowler_metrics.csv")

print("\n--- BATTERS IN ALL_METRICS (Non-Pakistani, High Impact) ---")
b_non_pak = b_all[~b_all['player_id'].isin(pak_players)].copy()
print(b_non_pak.sort_values(by='pressure_score', ascending=False)[
    ['player_name', 'player_id', 'pressure_score', 'pressure_sr', 'delta_sr', 'pressure_avg', 'pressure_balls', 'ipl_balls', 't20i_balls']
].head(25).to_string())

print("\n--- BOWLERS IN ALL_METRICS (Non-Pakistani, High Impact) ---")
bw_non_pak = bw_all[~bw_all['player_id'].isin(pak_players)].copy()
print(bw_non_pak.sort_values(by='pressure_score', ascending=False)[
    ['player_name', 'player_id', 'pressure_score', 'pressure_econ', 'delta_econ', 'pressure_wickets', 'pressure_balls', 'ipl_balls', 't20i_balls']
].head(25).to_string())


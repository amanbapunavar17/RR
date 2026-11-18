"""
scripts/explore_auction_candidates.py
Analyzes player pool in Data Pack, checking nationality, IPL teams,
competition presence (Emerging Asia Cup, IPL, T20Is), and identifies
the full landscape for IPL 2027 auction scouting.
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = "Data Pack"

teams = pd.read_csv(os.path.join(DATA_DIR, "teams.csv"))
player_map = pd.read_csv(os.path.join(DATA_DIR, "competition_team_player_mapping.csv"))
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))

print(f"Total player mappings: {len(player_map):,}")

# Join player_map with teams and comps
pm = player_map.merge(teams[['team_id', 'team_name']], on='team_id', how='left')
pm = pm.merge(comps[['comp_id', 'comp_name', 'match_format', 'season']], on='comp_id', how='left')

print("\nSample player mappings with teams and competitions:")
print(pm[['player_id', 'player_name', 'team_name', 'comp_name', 'season']].head(15).to_string())

# Check all teams in IPL
ipl_teams = pm[pm['comp_name'].str.contains('IPL', case=False, na=False)]['team_name'].unique()
print(f"\nIPL Teams in dataset ({len(ipl_teams)}):")
for t in sorted(ipl_teams):
    print(f"  - {t}")

# Check teams in Emerging Asia Cup / Rising Stars
emerging_teams = pm[pm['comp_name'].str.contains('Emerging|Rising', case=False, na=False)]['team_name'].unique()
print(f"\nEmerging / Rising Stars Teams ({len(emerging_teams)}):")
for t in sorted(emerging_teams):
    print(f"  - {t}")

# Look at all players in all_batter_metrics.csv and all_bowler_metrics.csv
b_all = pd.read_csv("outputs/all_batter_metrics.csv")
bw_all = pd.read_csv("outputs/all_bowler_metrics.csv")
print(f"\nTotal qualified batters in all_batter_metrics: {len(b_all)}")
print(f"Total qualified bowlers in all_bowler_metrics: {len(bw_all)}")



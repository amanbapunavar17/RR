"""
scripts/audit_player_discrepancies.py
Forensic investigation of player statistics, franchise history across IPL 2022-2026,
and exact root causes of any metric discrepancies.
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = "Data Pack"
pm = pd.read_csv(os.path.join(DATA_DIR, "competition_team_player_mapping.csv"))
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
bbb = pd.read_csv(os.path.join(DATA_DIR, "ball_by_ball.csv"))

# Inspect franchise history for specific players
players_to_check = [
    'Ashutosh Sharma', 'Shubham Dubey', 'Vignesh Puthur', 'Kuldeep Sen',
    'Tim David', 'Krunal Pandya', 'Ravichandran Ashwin', 'Mitchell Santner',
    'Prasidh Krishna', 'Trent Boult', 'Angkrish Raghuvanshi', 'Digvesh Rathi'
]

print("=== FRANCHISE HISTORY IN DATASET ===")
m = pm[pm['player_name'].isin(players_to_check)][['player_name', 'player_id', 'comp_name', 'team_name']].drop_duplicates()
print(m.sort_values(by=['player_name', 'comp_name']).to_string())

# Investigate Ashutosh Sharma delivery metrics
print("\n=== ASHUTOSH SHARMA DELIVERIES INVESTIGATION ===")
ash_balls = bbb[bbb['striker_id'] == 8101]
print(f"Total balls where Ashutosh is striker: {len(ash_balls)}")
print(f"Wides faced: {len(ash_balls[ash_balls['extras_type'] == 'wide'])}")
legal_faced = ash_balls[ash_balls['extras_type'] != 'wide']
print(f"Legal balls faced (balls faced): {len(legal_faced)}")
print(f"Total runs scored off bat: {legal_faced['runs'].sum()}")
print(f"Matches played in: {ash_balls['match_id'].nunique()}")

# Investigate Vignesh Puthur delivery metrics
print("\n=== VIGNESH PUTHUR BOWLING INVESTIGATION ===")
vp_balls = bbb[bbb['bowler_id'] == 48557]
print(f"Total balls bowled: {len(vp_balls)}")
print(f"Wides bowled: {len(vp_balls[vp_balls['extras_type'] == 'wide'])}")
vp_legal = vp_balls[~vp_balls['extras_type'].isin(['wide', 'Penalty'])]
print(f"Legal balls bowled: {len(vp_legal)}")
print(f"Total runs conceded off bat: {vp_balls['runs'].sum()}")
print(f"Wickets taken: {len(vp_balls[vp_balls['is_wicket'] == True])}")
print("Wicket kinds:")
print(vp_balls[vp_balls['is_wicket'] == True][['match_id', 'innings', 'overid', 'runs', 'dismissal_type']])


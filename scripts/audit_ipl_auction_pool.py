"""
scripts/audit_ipl_auction_pool.py
Audits the complete player pool for IPL 2027 auction feasibility.
Distinguishes Nationality (Indian vs Overseas vs Pakistani),
IPL status, Capped vs Uncapped, and evaluates Hidden Gems.
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = "Data Pack"
OUTPUT_DIR = "outputs"
REPORTS_DIR = "reports"

# Load mapping, matches, comps, teams
pm = pd.read_csv(os.path.join(DATA_DIR, "competition_team_player_mapping.csv"))
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
teams = pd.read_csv(os.path.join(DATA_DIR, "teams.csv"))
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))

print(f"Total rows in mapping: {len(pm)}")

# Map player nationality / international teams played for
intl_teams = [
    'India', 'Pakistan', 'Australia', 'England', 'South Africa', 'New Zealand',
    'West Indies', 'Sri Lanka', 'Bangladesh', 'Afghanistan', 'Ireland', 'Zimbabwe',
    'Netherlands', 'United Arab Emirates', 'Nepal', 'Japan'
]

# Identify national team appearances
player_nat = {}
for _, row in pm.iterrows():
    pid = row['player_id']
    tname = row['team_name']
    if tname in intl_teams:
        if pid not in player_nat:
            player_nat[pid] = set()
        player_nat[pid].add(tname)

# Identify IPL teams played for
ipl_team_names = [
    'Chennai Super Kings', 'Mumbai Indians', 'Rajasthan Royals', 'Punjab Kings',
    'Royal Challengers Bengaluru', 'Delhi Capitals', 'Kolkata Knight Riders',
    'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants'
]

player_ipl_teams = {}
for _, row in pm.iterrows():
    pid = row['player_id']
    tname = row['team_name']
    if tname in ipl_team_names:
        if pid not in player_ipl_teams:
            player_ipl_teams[pid] = set()
        player_ipl_teams[pid].add(tname)

print(f"Total players with national team mappings: {len(player_nat)}")
print(f"Total players with IPL team mappings: {len(player_ipl_teams)}")

# Check players in all_batter_metrics and all_bowler_metrics
b_all = pd.read_csv("outputs/all_batter_metrics.csv")
bw_all = pd.read_csv("outputs/all_bowler_metrics.csv")

print(f"\nTotal qualified batters: {len(b_all)}")
print(f"Total qualified bowlers: {len(bw_all)}")

# Let's inspect the top 30 batters and bowlers in all_batter_metrics / all_bowler_metrics
print("\n--- TOP 25 BATTERS IN HISTORICAL MODEL ---")
print(b_all.sort_values(by='pressure_score', ascending=False)[['player_name', 'player_id', 'pressure_score', 'pressure_sr', 'pressure_avg', 'pressure_balls', 'match_count', 'ipl_balls', 't20i_balls']].head(25).to_string())

print("\n--- TOP 25 BOWLERS IN HISTORICAL MODEL ---")
print(bw_all.sort_values(by='pressure_score', ascending=False)[['player_name', 'player_id', 'pressure_score', 'pressure_econ', 'pressure_wickets', 'pressure_balls', 'match_count', 'ipl_balls', 't20i_balls']].head(25).to_string())


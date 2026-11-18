"""
scripts/fix_player_metadata.py
Inspects player identities and builds an authoritative database of
Nationality, Current Status (Active / Retired / Retained),
and Capped / Uncapped status for realistic auction candidates.
"""

import pandas as pd
import numpy as np

# Load player mapping
pm = pd.read_csv("Data Pack/competition_team_player_mapping.csv")

# Let's inspect the names of all players who appeared in IPL teams
ipl_teams = [
    'Chennai Super Kings', 'Mumbai Indians', 'Rajasthan Royals', 'Punjab Kings',
    'Royal Challengers Bengaluru', 'Delhi Capitals', 'Kolkata Knight Riders',
    'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants'
]

ipl_players = pm[pm['team_name'].isin(ipl_teams)][['player_id', 'player_name', 'team_name']].drop_duplicates()
print(f"Total IPL player-team combinations: {len(ipl_players)}")
print(f"Unique IPL players: {ipl_players['player_id'].nunique()}")

# Let's see some sample player names
print(ipl_players.head(30).to_string())


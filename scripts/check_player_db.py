import pypdf
import pandas as pd
import numpy as np

# Load player mapping and ball by ball
mapping = pd.read_csv('d:/RR/Data Pack/competition_team_player_mapping.csv')
print("Mapping shape:", mapping.shape)
print("Unique players in mapping:", mapping['player_id'].nunique(), mapping['player_name'].nunique())

# Load all batter and bowler metrics
bat_df = pd.read_csv('d:/RR/outputs/all_batter_metrics.csv')
bowl_df = pd.read_csv('d:/RR/outputs/all_bowler_metrics.csv')
print("Batters:", len(bat_df), "Bowlers:", len(bowl_df))

# Let's inspect mapping sample
print(mapping[['player_id', 'player_name']].drop_duplicates().head(10))


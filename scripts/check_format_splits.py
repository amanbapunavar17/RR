import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np

from src.analysis.data_loader import load_all_datasets
from src.analysis.data_cleaner import clean_data
from src.analysis.match_state import compute_match_states
from src.analysis.pressure_engine import compute_delivery_pressure

datasets = load_all_datasets()
df_clean, matches = clean_data(datasets)
df_state = compute_match_states(df_clean)
df = compute_delivery_pressure(df_state)

print("--- FORMAT BREAKDOWN IN DATASET ---")
print(df.groupby('match_format')[['is_legal_ball', 'total_delivery_runs', 'is_bowler_wicket']].sum())

# Format in IPL vs non-IPL
df['format_group'] = np.where(df['is_ipl'], 'IPL', np.where(df['is_t20i'], 'T20I', 'Other_T20'))
print("\nDeliveries by format group:")
print(df['format_group'].value_counts())

# Check top batters format split
bat_press = df[df['is_high_batting_pressure'] & df['is_ball_faced']]
bat_split = bat_press.groupby(['striker_id', 'striker_name', 'format_group']).size().unstack(fill_value=0)
bat_split['total'] = bat_split.sum(axis=1)
print("\nTop 20 batters format split (pressure balls faced):")
print(bat_split.sort_values(by='total', ascending=False).head(20).to_string())

# Check top bowlers format split
bowl_press = df[df['is_high_bowling_pressure'] & df['is_legal_ball']]
bowl_split = bowl_press.groupby(['bowler_id', 'bowler_name', 'format_group']).size().unstack(fill_value=0)
bowl_split['total'] = bowl_split.sum(axis=1)
print("\nTop 20 bowlers format split (pressure legal balls bowled):")
print(bowl_split.sort_values(by='total', ascending=False).head(20).to_string())


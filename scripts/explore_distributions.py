import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np

from src.analysis.data_loader import load_all_datasets
from src.analysis.data_cleaner import clean_data
from src.analysis.match_state import compute_match_states
from src.analysis.pressure_engine import compute_delivery_pressure

print("Loading and preparing complete dataset...")
datasets = load_all_datasets()
df_clean, matches = clean_data(datasets)
df_state = compute_match_states(df_clean)
df = compute_delivery_pressure(df_state)

print(f"Total deliveries processed: {len(df):,}")
print(f"High batting pressure deliveries: {df['is_high_batting_pressure'].sum():,} ({df['is_high_batting_pressure'].mean()*100:.1f}%)")
print(f"High bowling pressure deliveries: {df['is_high_bowling_pressure'].sum():,} ({df['is_high_bowling_pressure'].mean()*100:.1f}%)")

# Let's inspect batter sample size distribution
bat_pressure_counts = df[df['is_high_batting_pressure'] & df['is_ball_faced']].groupby('striker_id').size()
print("\nBatter balls faced in pressure percentiles:")
print(bat_pressure_counts.describe(percentiles=[0.5, 0.75, 0.85, 0.9, 0.95, 0.98]))

# How many batters have >= 100, 120, 150 balls faced under pressure?
for thresh in [80, 100, 120, 150, 180, 200]:
    n_qual = (bat_pressure_counts >= thresh).sum()
    print(f"Batters with >= {thresh} pressure balls faced: {n_qual}")

# Bowler legal balls under pressure
bowl_pressure_counts = df[df['is_high_bowling_pressure'] & df['is_legal_ball']].groupby('bowler_id').size()
print("\nBowler legal balls in pressure percentiles:")
print(bowl_pressure_counts.describe(percentiles=[0.5, 0.75, 0.85, 0.9, 0.95, 0.98]))

for thresh in [180, 240, 300, 360, 400, 500]:
    n_qual = (bowl_pressure_counts >= thresh).sum()
    print(f"Bowlers with >= {thresh} pressure legal balls bowled: {n_qual}")


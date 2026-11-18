import pandas as pd
import numpy as np

print("Loading data for Match State calculation...")
matches = pd.read_csv('Data Pack/matches.csv')
bbb = pd.read_csv('Data Pack/ball_by_ball.csv')

# Exclude super overs
df = bbb[bbb['innings'].isin([1, 2])].copy()

# Sort deliveries chronologically within each match and innings
# Note: we need to ensure stable sorting by match_id, innings, overid, over_ball_num
df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

# Define legal deliveries
is_wide = df['extras_type'] == 'wide'
is_noball = df['extras_type'].isin(['Overstep', 'other'])
is_penalty = df['extras_type'] == 'Penalty'
df['is_legal_ball'] = ~(is_wide | is_noball | is_penalty)
df['is_ball_faced'] = ~(is_wide | is_penalty)

# Bowler runs conceded
# Wides: runs + extras1_runs + extras_2_runs
# No-balls: runs + extras1_runs
# Normal: runs
# Byes/legbyes/penalty: 0
df['bowler_runs'] = 0
mask_wide = df['extras_type'] == 'wide'
mask_nb = df['extras_type'].isin(['Overstep', 'other'])
mask_normal = df['extras_type'].isna()
df.loc[mask_wide, 'bowler_runs'] = df.loc[mask_wide, 'runs'] + df.loc[mask_wide, 'extras1_runs'] + df.loc[mask_wide, 'extras_2_runs']
df.loc[mask_nb, 'bowler_runs'] = df.loc[mask_nb, 'runs'] + df.loc[mask_nb, 'extras1_runs']
df.loc[mask_normal, 'bowler_runs'] = df.loc[mask_normal, 'runs']

# Total runs on delivery for team score
df['total_delivery_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']

# Bowler wicket: Caught, Bowled, LBW, Stump, Hit Wicket
df['is_bowler_wicket'] = df['dismissal_type'].isin(['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket'])

print(f"Total standard deliveries: {len(df):,}")
print(f"Total legal balls: {df['is_legal_ball'].sum():,}")
print(f"Total balls faced: {df['is_ball_faced'].sum():,}")
print(f"Total team runs: {df['total_delivery_runs'].sum():,}")
print(f"Total bowler runs: {df['bowler_runs'].sum():,}")
print(f"Total bowler wickets: {df['is_bowler_wicket'].sum():,}")


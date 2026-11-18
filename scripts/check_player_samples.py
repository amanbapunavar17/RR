import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np
from scripts.prototype_pressure_model import compute_match_states_and_pressure

df = compute_match_states_and_pressure()

# Check top batters by balls faced under high pressure (pressure >= 60)
df_bat_high = df[(df['batting_pressure'] >= 60) & df['is_ball_faced']]
top_batters = df_bat_high.groupby(['striker_id', 'striker_name']).agg(
    balls_faced=('is_ball_faced', 'sum'),
    runs=('runs', 'sum'),
    fours=('is_four', 'sum'),
    sixes=('is_six', 'sum'),
    outs=('is_wicket', 'sum')
).reset_index()
top_batters['sr'] = (top_batters['runs'] / top_batters['balls_faced']) * 100
print("Top 15 Batters by balls faced under pressure (>=60):")
print(top_batters.sort_values(by='balls_faced', ascending=False).head(15).to_string())

# Check top bowlers by legal balls bowled under high pressure (pressure >= 60)
df_bowl_high = df[(df['bowling_pressure'] >= 60) & df['is_legal_ball']]
top_bowlers = df_bowl_high.groupby(['bowler_id', 'bowler_name']).agg(
    legal_balls=('is_legal_ball', 'sum'),
    runs_conceded=('bowler_runs', 'sum'),
    wickets=('is_bowler_wicket', 'sum'),
    dots=('runs', lambda x: ((x == 0) & (df.loc[x.index, 'bowler_runs'] == 0)).sum())
).reset_index()
top_bowlers['econ'] = (top_bowlers['runs_conceded'] / top_bowlers['legal_balls']) * 6.0
print("\nTop 15 Bowlers by balls bowled under pressure (>=60):")
print(top_bowlers.sort_values(by='legal_balls', ascending=False).head(15).to_string())

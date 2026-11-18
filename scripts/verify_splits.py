import pandas as pd

b = pd.read_csv('outputs/all_batter_metrics.csv')
bw = pd.read_csv('outputs/all_bowler_metrics.csv')
t_b = pd.read_csv('outputs/top_10_batters.csv')
t_bw = pd.read_csv('outputs/top_10_bowlers.csv')

print('=== TOP 10 BATTERS SPLITS ===')
merged_b = t_b[['rank', 'player_id', 'player_name']].merge(b[['player_id', 'match_count', 'pressure_balls', 'ipl_balls', 't20i_balls']], on='player_id')
print(merged_b.to_string())

print('\n=== TOP 10 BOWLERS SPLITS ===')
merged_bw = t_bw[['rank', 'player_id', 'player_name']].merge(bw[['player_id', 'match_count', 'pressure_balls', 'ipl_balls', 't20i_balls']], on='player_id')
print(merged_bw.to_string())


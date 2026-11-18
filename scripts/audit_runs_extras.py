import pandas as pd
import numpy as np

bbb = pd.read_csv('Data Pack/ball_by_ball.csv')

print("--- EXTRAS AND RUNS INSPECTION ---")
# Check rows where extras_type is wide
print("\nSample WIDE deliveries:")
print(bbb[bbb['extras_type'] == 'wide'][['runs', 'extras_type', 'extras1_runs', 'extras_2_runs']].head(10))

# Check rows where extras_type is legbyes
print("\nSample LEGBYES deliveries:")
print(bbb[bbb['extras_type'] == 'legbyes'][['runs', 'extras_type', 'extras1_runs', 'extras_2_runs']].head(5))

# Check rows where extras_type is Overstep (no ball)
print("\nSample OVERSTEP deliveries:")
print(bbb[bbb['extras_type'] == 'Overstep'][['runs', 'extras_type', 'extras1_runs', 'extras_2_runs', 'is_four', 'is_six']].head(10))

# Check rows where extras_type is byes
print("\nSample BYES deliveries:")
print(bbb[bbb['extras_type'] == 'byes'][['runs', 'extras_type', 'extras1_runs', 'extras_2_runs']].head(5))

# Check rows where extras_type is other
print("\nSample OTHER deliveries:")
print(bbb[bbb['extras_type'] == 'other'][['runs', 'extras_type', 'extras1_runs', 'extras_2_runs']].head(5))

# Check rows where extras_2_runs > 0
print("\nSample extras_2_runs > 0:")
print(bbb[bbb['extras_2_runs'] > 0][['runs', 'extras_type', 'extras1_runs', 'extras_2_runs', 'is_four', 'is_six']].head(10))

# Let's inspect total runs on a delivery
# What is the score progression in an innings?
match_13511_inn1 = bbb[(bbb['match_id'] == 13511) & (bbb['innings'] == 1)]
print(f"\nMatch 13511 Innings 1 balls: {len(match_13511_inn1)}")
print(match_13511_inn1[['overid', 'over_ball_num', 'innings_ball_num', 'striker_name', 'bowler_name', 'runs', 'extras_type', 'extras1_runs', 'extras_2_runs', 'is_wicket']].head(15))

# Total sum of runs for this innings:
bat_runs = match_13511_inn1['runs'].sum()
ext1 = match_13511_inn1['extras1_runs'].sum()
ext2 = match_13511_inn1['extras_2_runs'].sum()
print(f"Match 13511 Inn 1: bat_runs={bat_runs}, ext1={ext1}, ext2={ext2}, total={bat_runs + ext1 + ext2}")

# Check legal ball definition
# Are wides and oversteps legal deliveries?
print("\nLegal balls check:")
print("over_ball_num for wide balls:")
print(bbb[bbb['extras_type'] == 'wide']['over_ball_num'].value_counts())
print("over_ball_num for Overstep balls:")
print(bbb[bbb['extras_type'] == 'Overstep']['over_ball_num'].value_counts())


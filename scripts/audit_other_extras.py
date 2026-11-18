import pandas as pd

bbb = pd.read_csv('Data Pack/ball_by_ball.csv')

print("--- INSPECTING 'other' EXTRAS_TYPE ---")
other_df = bbb[bbb['extras_type'] == 'other']
print("Runs off bat on 'other':", other_df['runs'].value_counts())
print("extras1_runs on 'other':", other_df['extras1_runs'].value_counts())
print("extras_2_runs on 'other':", other_df['extras_2_runs'].value_counts())
print("Sample 'other' rows:")
print(other_df[['match_id', 'innings', 'overid', 'over_ball_num', 'striker_name', 'bowler_name', 'runs', 'extras_type', 'extras1_runs', 'extras_2_runs', 'is_four', 'is_six']].head(10))

print("\n--- INSPECTING 'Penalty' EXTRAS_TYPE ---")
pen_df = bbb[bbb['extras_type'] == 'Penalty']
print(pen_df[['match_id', 'innings', 'overid', 'over_ball_num', 'runs', 'extras_type', 'extras1_runs', 'extras_2_runs']])

# Check how many balls in an over when there are no wides/overstep/other
print("\n--- BALLS IN OVER WHEN EXTRAS ARE NAN OR LEGBYES OR BYES ---")
# Count legal deliveries per over
# Let's see an example match and over where 'other' occurs
if len(other_df) > 0:
    sample_match = other_df.iloc[0]['match_id']
    sample_inn = other_df.iloc[0]['innings']
    sample_over = other_df.iloc[0]['overid']
    print(f"\nDeliveries in match {sample_match}, inn {sample_inn}, over {sample_over}:")
    print(bbb[(bbb['match_id'] == sample_match) & (bbb['innings'] == sample_inn) & (bbb['overid'] == sample_over)][['over_ball_num', 'innings_ball_num', 'runs', 'extras_type', 'extras1_runs', 'extras_2_runs']])


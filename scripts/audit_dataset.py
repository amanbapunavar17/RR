import pandas as pd
import numpy as np

print("Loading datasets...")
comps = pd.read_csv('Data Pack/competitions.csv')
teams = pd.read_csv('Data Pack/teams.csv')
matches = pd.read_csv('Data Pack/matches.csv')
p11 = pd.read_csv('Data Pack/playing_eleven.csv')
ctpm = pd.read_csv('Data Pack/competition_team_player_mapping.csv')
bbb = pd.read_csv('Data Pack/ball_by_ball.csv')

print("\n=== ROW COUNTS & SHAPES ===")
print(f"competitions: {comps.shape[0]:,} rows, {comps.shape[1]} cols")
print(f"teams: {teams.shape[0]:,} rows, {teams.shape[1]} cols")
print(f"matches: {matches.shape[0]:,} rows, {matches.shape[1]} cols")
print(f"playing_eleven: {p11.shape[0]:,} rows, {p11.shape[1]} cols")
print(f"competition_team_player_mapping: {ctpm.shape[0]:,} rows, {ctpm.shape[1]} cols")
print(f"ball_by_ball: {bbb.shape[0]:,} rows, {bbb.shape[1]} cols")

print("\n=== COMPETITIONS BREAKDOWN ===")
print(comps['match_format'].value_counts(dropna=False))
print("\nBy season and format:")
print(comps.groupby(['season', 'match_format']).size())

print("\nSample competition names:")
print(comps['comp_name'].value_counts().head(20))

print("\n=== MATCHES BREAKDOWN ===")
print(f"Unique match_ids: {matches['match_id'].nunique():,}")
print(f"Date range: {matches['match_date'].min()} to {matches['match_date'].max()}")
print("\nMissing values in matches:")
print(matches.isna().sum()[matches.isna().sum() > 0])

print("\nMatches with revised_target:")
print(matches[matches['revised_target'].notna()][['match_id', 'match_date', 'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target', 'result']].head(10))

print("\nMatches result distribution:")
print(matches['result'].value_counts().head(10))

print("\n=== BALL BY BALL BREAKDOWN ===")
print(f"Unique matches in BBB: {bbb['match_id'].nunique():,}")
print("Innings distribution:")
print(bbb['innings'].value_counts().sort_index())

print("\nOverid min and max:")
print(bbb.groupby('innings')['overid'].agg(['min', 'max']))

print("\nExtras types:")
print(bbb['extras_type'].value_counts(dropna=False))

print("\nExtras1_runs value counts:")
print(bbb['extras1_runs'].value_counts().head(10))

print("\nExtras_2_runs value counts:")
print(bbb['extras_2_runs'].value_counts().head(10))

print("\nRuns distribution:")
print(bbb['runs'].value_counts())

print("\nDismissal types:")
print(bbb['dismissal_type'].value_counts(dropna=False))

print("\nUnique strikers:", bbb['striker_id'].nunique())
print("Unique bowlers:", bbb['bowler_id'].nunique())

# Check match IDs overlap
match_diff = set(bbb['match_id']) - set(matches['match_id'])
print(f"BBB match_ids not in matches.csv: {len(match_diff)}")

matches_no_bbb = set(matches['match_id']) - set(bbb['match_id'])
print(f"matches.csv match_ids with no BBB data: {len(matches_no_bbb)}")
if matches_no_bbb:
    print("Sample matches without BBB data:")
    print(matches[matches['match_id'].isin(matches_no_bbb)][['match_id', 'match_date', 'home_team', 'away_team', 'result']].head(5))

# Check player ID overlap between bbb and ctpm / playing_eleven
bbb_players = set(bbb['striker_id']).union(set(bbb['bowler_id'])).union(set(bbb['non_striker_id']))
ctpm_players = set(ctpm['player_id'])
p11_players = set(p11['player_id'])
print(f"\nUnique players in BBB: {len(bbb_players)}")
print(f"BBB players missing from CTPM: {len(bbb_players - ctpm_players)}")
print(f"BBB players missing from P11: {len(bbb_players - p11_players)}")


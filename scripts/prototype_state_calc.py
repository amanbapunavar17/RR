import pandas as pd
import numpy as np

matches = pd.read_csv('Data Pack/matches.csv')
bbb = pd.read_csv('Data Pack/ball_by_ball.csv')

# Exclude super overs
df = bbb[bbb['innings'].isin([1, 2])].copy()
df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

# Flags
is_wide = df['extras_type'] == 'wide'
is_noball = df['extras_type'].isin(['Overstep', 'other'])
is_penalty = df['extras_type'] == 'Penalty'
df['is_legal_ball'] = ~(is_wide | is_noball | is_penalty)
df['is_ball_faced'] = ~(is_wide | is_penalty)
df['total_delivery_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']

# Groupby match_id and innings to compute cumulative metrics BEFORE the delivery
grouped = df.groupby(['match_id', 'innings'])
df['score_before'] = grouped['total_delivery_runs'].cumsum() - df['total_delivery_runs']
df['wickets_before'] = grouped['is_wicket'].cumsum() - df['is_wicket']
df['legal_balls_before'] = grouped['is_legal_ball'].cumsum() - df['is_legal_ball']
df['wickets_remaining'] = 10 - df['wickets_before']

# Merge match context (revised overs, revised target, inn1 total)
inn_totals = df.groupby(['match_id', 'innings'])['total_delivery_runs'].sum().unstack(level='innings')
inn1_actual = inn_totals[1].rename('inn1_actual_total')

matches_info = matches[['match_id', 'comp_id', 'match_date', 'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target']].copy()
matches_info = matches_info.merge(inn1_actual, on='match_id', how='left')

df = df.merge(matches_info, on='match_id', how='left')

# Determine total allocated balls for each innings
# If revised overs present (given in balls!), use it; else 120
df['total_balls_allocated'] = 120
df.loc[(df['innings'] == 1) & df['first_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['first_inn_revised_overs']
df.loc[(df['innings'] == 2) & df['second_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['second_inn_revised_overs']

df['balls_remaining'] = np.maximum(0, df['total_balls_allocated'] - df['legal_balls_before'])

# CRR (Current Run Rate)
# If legal_balls_before == 0, CRR is set to 0.0
df['crr'] = np.where(df['legal_balls_before'] > 0, (df['score_before'] / df['legal_balls_before']) * 6.0, 0.0)

# Target and Chase metrics for Innings 2
# Target is revised_target if present, else inn1_actual_total + 1
df['target'] = np.nan
df.loc[df['innings'] == 2, 'target'] = np.where(
    df.loc[df['innings'] == 2, 'revised_target'].notna(),
    df.loc[df['innings'] == 2, 'revised_target'],
    df.loc[df['innings'] == 2, 'inn1_actual_total'] + 1
)

df['runs_needed'] = np.nan
df.loc[df['innings'] == 2, 'runs_needed'] = np.maximum(0, df.loc[df['innings'] == 2, 'target'] - df.loc[df['innings'] == 2, 'score_before'])

# RRR (Required Run Rate)
# If balls_remaining == 0 and runs_needed > 0, set RRR very high (e.g. 36.0)
# If runs_needed == 0, RRR = 0.0
df['rrr'] = np.nan
cond_inn2 = df['innings'] == 2
df.loc[cond_inn2, 'rrr'] = np.where(
    df.loc[cond_inn2, 'balls_remaining'] > 0,
    (df.loc[cond_inn2, 'runs_needed'] / df.loc[cond_inn2, 'balls_remaining']) * 6.0,
    np.where(df.loc[cond_inn2, 'runs_needed'] > 0, 36.0, 0.0)
)

print("Sample innings 2 chase state:")
print(df[df['innings'] == 2][['match_id', 'overid', 'over_ball_num', 'score_before', 'wickets_before', 'balls_remaining', 'target', 'runs_needed', 'rrr']].head(15))


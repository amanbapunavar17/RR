import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load data
matches = pd.read_csv('Data Pack/matches.csv')
bbb = pd.read_csv('Data Pack/ball_by_ball.csv')
comps = pd.read_csv('Data Pack/competitions.csv')

# Exclude super overs
df = bbb[bbb['innings'].isin([1, 2])].copy()
df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

df['total_delivery_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
is_wide = df['extras_type'] == 'wide'
is_noball = df['extras_type'].isin(['Overstep', 'other'])
is_penalty = df['extras_type'] == 'Penalty'
df['is_legal_ball'] = ~(is_wide | is_noball | is_penalty)
df['is_dismissal'] = df['is_wicket'].fillna(False).astype(bool)

grouped = df.groupby(['match_id', 'innings'])
df['score_before'] = grouped['total_delivery_runs'].cumsum() - df['total_delivery_runs']
df['wickets_before'] = grouped['is_dismissal'].cumsum() - df['is_dismissal']
df['legal_balls_before'] = grouped['is_legal_ball'].cumsum() - df['is_legal_ball']
df['wickets_remaining'] = 10 - df['wickets_before']

# Match metadata
matches_info = matches[['match_id', 'comp_id', 'win_team_id', 'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target']].copy()
matches_info = matches_info.merge(comps[['comp_id', 'match_format', 'season', 'comp_name']], on='comp_id', how='left')

inn1_actual = df[df['innings'] == 1].groupby('match_id')['total_delivery_runs'].sum().rename('inn1_actual_total')
matches_info = matches_info.merge(inn1_actual, on='match_id', how='left')
df = df.merge(matches_info, on='match_id', how='left')

# Innings 2 deliveries
inn2 = df[df['innings'] == 2].copy()
inn2['total_balls_allocated'] = np.where(inn2['second_inn_revised_overs'].notna(), inn2['second_inn_revised_overs'], 120)
inn2['balls_remaining'] = np.maximum(0, inn2['total_balls_allocated'] - inn2['legal_balls_before'])
inn2['target'] = np.where(inn2['revised_target'].notna(), inn2['revised_target'], inn2['inn1_actual_total'] + 1)
inn2['runs_needed'] = np.maximum(0, inn2['target'] - inn2['score_before'])
inn2['rrr'] = np.where(inn2['balls_remaining'] > 0, (inn2['runs_needed'] / inn2['balls_remaining']) * 6.0, np.where(inn2['runs_needed'] > 0, 36.0, 0.0))

# Filter matches with decided winners
inn2 = inn2[inn2['win_team_id'].notna()].copy()
inn2['chase_won'] = (inn2['win_team_id'] == inn2['batting_team_id']).astype(int)

print(f"Total Innings 2 deliveries with known winner: {len(inn2):,}")
print(f"Total unique matches in Innings 2: {inn2['match_id'].nunique()}")
print(f"Overall chase win rate: {inn2['chase_won'].mean():.4f}")

# Model Investigation:
# Let's see: if we use runs_needed, balls_remaining, wickets_remaining WITHOUT rrr:
def sigmoid(z): return 1.0 / (1.0 + np.exp(-np.clip(z, -25, 25)))
def log_loss_fn(weights, X_mat, y_vec):
    p = np.clip(sigmoid(np.dot(X_mat, weights)), 1e-12, 1 - 1e-12)
    return -np.mean(y_vec * np.log(p) + (1 - y_vec) * np.log(1 - p))

# Feature Set 1: runs_needed, balls_remaining, wickets_remaining
f1 = ['runs_needed', 'balls_remaining', 'wickets_remaining']
X1 = inn2[f1].copy()
X1_mean, X1_std = X1.mean(), X1.std()
X1_norm = ((X1 - X1_mean) / X1_std).values
X1_mat = np.column_stack([np.ones(len(X1_norm)), X1_norm])
y = inn2['chase_won'].values

res1 = minimize(log_loss_fn, np.zeros(X1_mat.shape[1]), args=(X1_mat, y), method='BFGS')
w1 = res1.x

print("\n--- Model 1: runs_needed, balls_remaining, wickets_remaining (WITHOUT RRR ratio) ---")
print(f"Intercept: {w1[0]:.4f}")
for feat, coef in zip(f1, w1[1:]):
    print(f"  {feat}: {coef:.4f}")
brier1 = np.mean((y - sigmoid(np.dot(X1_mat, w1))) ** 2)
print(f"Brier score (in-sample): {brier1:.4f}")

# Notice: In Model 1, balls_remaining coefficient:
# Let's check w1[2]!


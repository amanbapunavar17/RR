import pandas as pd
import numpy as np
from scipy.optimize import minimize

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -25, 25)))

def log_loss_fn(weights, X_mat, y_vec):
    p = sigmoid(np.dot(X_mat, weights))
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -np.mean(y_vec * np.log(p) + (1 - y_vec) * np.log(1 - p))

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

# Total allocated balls
matches_info = matches[['match_id', 'comp_id', 'win_team_id', 'revised_target', 'second_inn_revised_overs']].copy()
matches_info = matches_info.merge(comps[['comp_id', 'match_format', 'season']], on='comp_id', how='left')

inn1_actual = df[df['innings'] == 1].groupby('match_id')['total_delivery_runs'].sum().rename('inn1_actual_total')
matches_info = matches_info.merge(inn1_actual, on='match_id', how='left')
df = df.merge(matches_info, on='match_id', how='left')

# Innings 2 metrics
inn2 = df[df['innings'] == 2].copy()
inn2['total_balls_allocated'] = np.where(inn2['second_inn_revised_overs'].notna(), inn2['second_inn_revised_overs'], 120)
inn2['balls_remaining'] = np.maximum(0, inn2['total_balls_allocated'] - inn2['legal_balls_before'])
inn2['target'] = np.where(inn2['revised_target'].notna(), inn2['revised_target'], inn2['inn1_actual_total'] + 1)
inn2['runs_needed'] = np.maximum(0, inn2['target'] - inn2['score_before'])
inn2['rrr'] = np.where(inn2['balls_remaining'] > 0, (inn2['runs_needed'] / inn2['balls_remaining']) * 6.0, np.where(inn2['runs_needed'] > 0, 36.0, 0.0))

# Target variable: did chasing team win?
inn2 = inn2[inn2['win_team_id'].notna()]
inn2['chase_won'] = (inn2['win_team_id'] == inn2['batting_team_id']).astype(int)

features = ['runs_needed', 'balls_remaining', 'wickets_remaining', 'rrr']
X = inn2[features].copy()
X['rrr'] = X['rrr'].clip(0, 36)
y = inn2['chase_won'].values

# Standardize features for stable optimization
X_mean = X.mean()
X_std = X.std()
X_norm = ((X - X_mean) / X_std).values
# Add intercept column
X_mat = np.column_stack([np.ones(len(X_norm)), X_norm])

init_weights = np.zeros(X_mat.shape[1])
res = minimize(log_loss_fn, init_weights, args=(X_mat, y), method='BFGS')
weights = res.x

inn2['wp'] = sigmoid(np.dot(X_mat, weights))

print("Innings 2 sample size:", len(inn2))
print("Chase won proportion:", inn2['chase_won'].mean())
print("\nLogistic Regression Weights (Normalized Features):")
print(f"  Intercept: {weights[0]:.4f}")
for feat, w in zip(features, weights[1:]):
    print(f"  {feat}: {w:.4f}")

brier = np.mean((y - inn2['wp']) ** 2)
print(f"Brier score: {brier:.4f}")

# Leverage Index: LI = 4 * WP * (1 - WP) [0 to 1 scale, max at WP=0.5]
inn2['leverage_index'] = 4.0 * inn2['wp'] * (1.0 - inn2['wp'])
print("\nLeverage Index Summary:")
print(inn2['leverage_index'].describe())

# Check sample deliveries across different situations:
print("\n--- SAMPLE CHASE SITUATIONS ---")
samples = [
    ("Tight Finish", (inn2['balls_remaining'] <= 18) & (inn2['runs_needed'] <= 25) & (inn2['runs_needed'] >= 10)),
    ("Blowout / Lost Cause", (inn2['balls_remaining'] <= 18) & (inn2['runs_needed'] >= 45)),
    ("Cruising Chase", (inn2['balls_remaining'] >= 30) & (inn2['runs_needed'] <= 15) & (inn2['wickets_remaining'] >= 7)),
    ("Middle Over Balance", (inn2['balls_remaining'] >= 45) & (inn2['balls_remaining'] <= 60) & (inn2['rrr'] >= 8) & (inn2['rrr'] <= 10))
]

for label, cond in samples:
    sub = inn2[cond]
    if len(sub) > 0:
        row = sub.iloc[0]
        print(f"\n{label} ({len(sub)} deliveries in dataset):")
        print(f"  Match: {row['match_id']}, Ball {row['overid']}.{row['over_ball_num']}")
        print(f"  Runs needed: {row['runs_needed']}, Balls left: {row['balls_remaining']}, Wkts left: {row['wickets_remaining']}, RRR: {row['rrr']:.2f}")
        print(f"  Win Prob (WP): {row['wp']:.3f}, Leverage Index (LI): {row['leverage_index']:.3f}")

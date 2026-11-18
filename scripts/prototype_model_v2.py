import pandas as pd
import numpy as np

# Load data
matches = pd.read_csv('Data Pack/matches.csv')
bbb = pd.read_csv('Data Pack/ball_by_ball.csv')
comps = pd.read_csv('Data Pack/competitions.csv')

# Exclude super overs
df = bbb[bbb['innings'].isin([1, 2])].copy()
df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

# Pre-delivery flags
df['total_delivery_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
is_wide = df['extras_type'] == 'wide'
is_noball = df['extras_type'].isin(['Overstep', 'other'])
is_penalty = df['extras_type'] == 'Penalty'
df['is_legal_ball'] = ~(is_wide | is_noball | is_penalty)
df['is_ball_faced'] = ~(is_wide | is_penalty)
df['is_dismissal'] = df['is_wicket'].fillna(False).astype(bool)

# Bowler runs
df['bowler_runs'] = 0
df.loc[is_wide, 'bowler_runs'] = df.loc[is_wide, 'runs'] + df.loc[is_wide, 'extras1_runs'] + df.loc[is_wide, 'extras_2_runs']
df.loc[is_noball, 'bowler_runs'] = df.loc[is_noball, 'runs'] + df.loc[is_noball, 'extras1_runs']
df.loc[df['extras_type'].isna(), 'bowler_runs'] = df.loc[df['extras_type'].isna(), 'runs']
df['is_bowler_wicket'] = df['dismissal_type'].isin(['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket'])

# Cumulative states strictly BEFORE delivery
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

# Innings allocated balls
df['total_balls_allocated'] = 120
df.loc[(df['innings'] == 1) & df['first_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['first_inn_revised_overs']
df.loc[(df['innings'] == 2) & df['second_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['second_inn_revised_overs']
df['balls_remaining'] = np.maximum(0, df['total_balls_allocated'] - df['legal_balls_before'])

# Innings 2 chase metrics
df['target'] = np.nan
cond_inn2 = df['innings'] == 2
df.loc[cond_inn2, 'target'] = np.where(
    df.loc[cond_inn2, 'revised_target'].notna(),
    df.loc[cond_inn2, 'revised_target'],
    df.loc[cond_inn2, 'inn1_actual_total'] + 1
)
df['runs_needed'] = np.nan
df.loc[cond_inn2, 'runs_needed'] = np.maximum(0, df.loc[cond_inn2, 'target'] - df.loc[cond_inn2, 'score_before'])
df['rrr'] = np.nan
df.loc[cond_inn2, 'rrr'] = np.where(
    df.loc[cond_inn2, 'balls_remaining'] > 0,
    (df.loc[cond_inn2, 'runs_needed'] / df.loc[cond_inn2, 'balls_remaining']) * 6.0,
    np.where(df.loc[cond_inn2, 'runs_needed'] > 0, 36.0, 0.0)
)
df['crr'] = np.where(df['legal_balls_before'] > 0, (df['score_before'] / df['legal_balls_before']) * 6.0, 8.0)

# =========================================================================
# REVISION 1: HISTORICALLY ESTIMATED EXPECTED SCORE MODEL (PAR SCORE)
# =========================================================================
def get_expected_inn1_total(row):
    comp = str(row['comp_name'])
    season = str(row['season'])
    fmt = str(row['match_format'])
    
    # IPL Season-Aware Expectations
    if 'IPL' in comp:
        if '2022' in season: return 171.1
        elif '2023' in season: return 182.7
        elif '2024' in season: return 189.6
        elif '2025' in season: return 190.1
        elif '2026' in season: return 193.4
        else: return 185.0
    # T20I Season-Aware Expectations
    elif fmt == 'T20I':
        if '2026' in season: return 181.8
        else: return 168.0
    # Other T20 (Emerging / Rising Stars)
    else:
        return 158.0

df['expected_inn1_total'] = df.apply(get_expected_inn1_total, axis=1)
df['par_run_rate'] = df['expected_inn1_total'] / 20.0  # Par RPO

print("--- EXPECTED SCORE MODEL CHECKS ---")
print(df.groupby(['match_format', 'season'])['expected_inn1_total'].mean().head(10))

# =========================================================================
# REVISION 5: EMPIRICAL WIN PROBABILITY & LEVERAGE INDEX MODEL (INNINGS 2)
# =========================================================================
# Fit Logistic Model on 2nd innings pre-delivery states
inn2_data = df[df['innings'] == 2].copy()
inn2_data = inn2_data[inn2_data['win_team_id'].notna()]
inn2_data['chase_won'] = (inn2_data['win_team_id'] == inn2_data['batting_team_id']).astype(int)

# Logistic regression using scipy
from scipy.optimize import minimize
def sigmoid(z): return 1.0 / (1.0 + np.exp(-np.clip(z, -25, 25)))
def log_loss_fn(weights, X_mat, y_vec):
    p = np.clip(sigmoid(np.dot(X_mat, weights)), 1e-12, 1 - 1e-12)
    return -np.mean(y_vec * np.log(p) + (1 - y_vec) * np.log(1 - p))

feat_cols = ['runs_needed', 'balls_remaining', 'wickets_remaining', 'rrr']
X = inn2_data[feat_cols].copy()
X['rrr'] = X['rrr'].clip(0, 36)
y = inn2_data['chase_won'].values
X_mean, X_std = X.mean(), X.std()
X_norm = ((X - X_mean) / X_std).values
X_mat = np.column_stack([np.ones(len(X_norm)), X_norm])

res = minimize(log_loss_fn, np.zeros(X_mat.shape[1]), args=(X_mat, y), method='BFGS')
weights = res.x

# Apply to all 2nd innings deliveries
X_all = df.loc[df['innings'] == 2, feat_cols].copy()
X_all['rrr'] = X_all['rrr'].clip(0, 36)
X_all_norm = ((X_all - X_mean) / X_std).values
X_all_mat = np.column_stack([np.ones(len(X_all_norm)), X_all_norm])
df['win_prob'] = np.nan
df.loc[df['innings'] == 2, 'win_prob'] = sigmoid(np.dot(X_all_mat, weights))

# Leverage Index: LI = 4 * WP * (1 - WP) [0 to 1 scale, max at WP=0.5]
df['leverage_index'] = np.nan
df.loc[df['innings'] == 2, 'leverage_index'] = 4.0 * df.loc[df['innings'] == 2, 'win_prob'] * (1.0 - df.loc[df['innings'] == 2, 'win_prob'])

print("\nWin Probability & Leverage Index fitted successfully!")
print("Leverage Index summary (Innings 2):")
print(df[df['innings'] == 2]['leverage_index'].describe())


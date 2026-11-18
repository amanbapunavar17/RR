import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np

# Load audited data
from scripts.audit_win_prob_model import df, inn2, sigmoid, res1, w1, f1, X1_mean, X1_std

# Compute pre-delivery Win Probability using the audited non-collinear model:
# P(chase_won) = sigmoid(w0 + w1*runs_needed_norm + w2*balls_rem_norm + w3*wkts_rem_norm)
X_all = df.loc[df['innings'] == 2, f1].copy()
X_all_norm = ((X_all - X1_mean) / X1_std).values
X_all_mat = np.column_stack([np.ones(len(X_all_norm)), X_all_norm])

df['win_prob'] = np.nan
df.loc[df['innings'] == 2, 'win_prob'] = sigmoid(np.dot(X_all_mat, w1))
df['leverage_index'] = np.nan
df.loc[df['innings'] == 2, 'leverage_index'] = 4.0 * df.loc[df['innings'] == 2, 'win_prob'] * (1.0 - df.loc[df['innings'] == 2, 'win_prob'])

# =========================================================================
# PRE-DELIVERY PRESSURE FORMULATION (STRICTLY CLIPPED TO [5.0, 100.0])
# =========================================================================
# Innings 1
b1 = df['legal_balls_before'].clip(0, 120)
w1 = df['wickets_before'].clip(0, 10)
w_rem1 = df['wickets_remaining'].clip(0, 10)
S1 = df['score_before']
S_exp1 = (b1 / 6.0) * df['par_run_rate']
sigma_S1 = 15.0 * np.sqrt(np.maximum(1, b1) / 60.0)

Z_S = (S_exp1 - S1) / sigma_S1
W_exp1 = 6.5 * np.power(b1 / 120.0, 0.85)
collapse_risk = (w1 - W_exp1) / np.sqrt(W_exp1 + 1.0)
tail_urgency = np.where(b1 >= 90, ((b1 - 90.0) / 30.0) * np.clip((5.0 - w_rem1) / 4.0, 0.0, 1.0), 0.0)
phase_bat1 = np.where(df['phase'] == 'Death', 25.0, np.where(df['phase'] == 'Middle', 15.0, 10.0))

inn1_bat = np.clip(25.0 + phase_bat1 + 12.0 * np.clip(Z_S, -1.5, 2.0) + 15.0 * np.clip(collapse_risk, -1.0, 2.5) + 18.0 * tail_urgency, 5.0, 100.0)

phase_bowl1 = np.where(df['phase'] == 'Death', 30.0, np.where(df['phase'] == 'Powerplay', 18.0, 12.0))
bat_dominance = np.clip((S1 - S_exp1) / sigma_S1, -1.0, 2.5)
wkts_in_hand = np.clip((W_exp1 - w1) / np.sqrt(W_exp1 + 1.0), 0.0, 2.0)

inn1_bowl = np.clip(20.0 + phase_bowl1 + 12.0 * bat_dominance + 15.0 * wkts_in_hand, 5.0, 100.0)

# Innings 2
rrr2 = df['rrr'].fillna(8.0).clip(0, 36)
w_rem2 = df['wickets_remaining'].clip(0, 10)
b_rem2 = df['balls_remaining'].clip(0, 120)
li2 = df['leverage_index'].fillna(0.5)

rate_index = np.clip((rrr2 - 4.0) / 10.0, 0.0, 2.0) * 50.0
w_scarcity = np.where(w_rem2 <= 2, 25.0, np.where(w_rem2 <= 4, 15.0, np.where(w_rem2 <= 6, 5.0, -5.0)))
D_bat = rate_index + w_scarcity
phase_death2 = np.where(df['phase'] == 'Death', 12.0, np.where(df['phase'] == 'Middle', 5.0, 0.0))

inn2_bat = np.clip(40.0 * li2 + 0.60 * D_bat + phase_death2, 5.0, 100.0)

# Continuous Reachable Tension
reachable_tension = 25.0 * np.exp(-((rrr2 - 9.5) ** 2) / (2.0 * (3.5 ** 2)))
opp_w_penalty = 15.0 * np.clip((w_rem2 - 3.0) / 5.0, 0.0, 1.0)
death_bonus = 15.0 * np.maximum(0, (30.0 - b_rem2) / 30.0) * np.exp(-((df['runs_needed'].fillna(0) - 25.0) ** 2) / (2.0 * (18.0 ** 2)))

inn2_bowl = np.clip(5.0 + 45.0 * li2 + reachable_tension + opp_w_penalty + death_bonus, 5.0, 100.0)

# Final assignment
df['batting_pressure_final'] = np.where(df['innings'] == 1, inn1_bat, inn2_bat).round(2)
df['bowling_pressure_final'] = np.where(df['innings'] == 1, inn1_bowl, inn2_bowl).round(2)

print("\n--- FINAL PRESSURE BOUNDS CHECK ---")
print("Batting Pressure Min:", df['batting_pressure_final'].min(), "Max:", df['batting_pressure_final'].max())
print("Bowling Pressure Min:", df['bowling_pressure_final'].min(), "Max:", df['bowling_pressure_final'].max())

print("\nBatting Pressure P75:", df['batting_pressure_final'].quantile(0.75))
print("Bowling Pressure P75:", df['bowling_pressure_final'].quantile(0.75))

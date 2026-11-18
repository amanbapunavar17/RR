import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np

# Load prototype data with WP and Leverage Index
from scripts.prototype_model_v2 import df

df['phase'] = 'Middle'
df.loc[df['legal_balls_before'] < 36, 'phase'] = 'Powerplay'
df.loc[df['legal_balls_before'] >= 90, 'phase'] = 'Death'

# =========================================================================
# REFINED INNINGS 1 PRESSURE FORMULA
# =========================================================================
b1 = df['legal_balls_before'].clip(0, 120)
w1 = df['wickets_before'].clip(0, 10)
w_rem1 = df['wickets_remaining'].clip(0, 10)
S1 = df['score_before']
S_exp1 = (b1 / 6.0) * df['par_run_rate']
sigma_S1 = 15.0 * np.sqrt(np.maximum(1, b1) / 60.0)

# 1. Z-score deficit vs par
Z_S = (S_exp1 - S1) / sigma_S1

# 2. Expected wickets lost
W_exp1 = 6.5 * np.power(b1 / 120.0, 0.85)

# 3. Collapse Risk
collapse_risk = (w1 - W_exp1) / np.sqrt(W_exp1 + 1.0)

# 4. Tail Urgency
tail_urgency = np.where(b1 >= 90, ((b1 - 90.0) / 30.0) * np.clip((5.0 - w_rem1) / 4.0, 0.0, 1.0), 0.0)

# 5. Phase Batting Demand
phase_bat1 = np.where(df['phase'] == 'Death', 25.0, np.where(df['phase'] == 'Middle', 15.0, 10.0))

inn1_bat_p = 25.0 + phase_bat1 + 12.0 * np.clip(Z_S, -1.5, 2.0) + 15.0 * np.clip(collapse_risk, -1.0, 2.5) + 18.0 * tail_urgency
inn1_bat_p = np.clip(inn1_bat_p, 5.0, 100.0)

# Bowler Innings 1
phase_bowl1 = np.where(df['phase'] == 'Death', 30.0, np.where(df['phase'] == 'Powerplay', 18.0, 12.0))
bat_dominance = np.clip((S1 - S_exp1) / sigma_S1, -1.0, 2.5)
wkts_in_hand = np.clip((W_exp1 - w1) / np.sqrt(W_exp1 + 1.0), 0.0, 2.0)

inn1_bowl_p = 20.0 + phase_bowl1 + 12.0 * bat_dominance + 15.0 * wkts_in_hand
inn1_bowl_p = np.clip(inn1_bowl_p, 5.0, 100.0)

# =========================================================================
# REFINED INNINGS 2 PRESSURE FORMULA (WITH LEVERAGE INDEX)
# =========================================================================
rrr2 = df['rrr'].fillna(8.0).clip(0, 36)
crr2 = df['crr'].fillna(8.0)
w_rem2 = df['wickets_remaining'].clip(0, 10)
b_rem2 = df['balls_remaining'].clip(0, 120)
li2 = df['leverage_index'].fillna(0.5)

# Execution demand
rate_index = np.clip((rrr2 - 4.0) / 10.0, 0.0, 2.0) * 50.0
w_scarcity = np.where(w_rem2 <= 2, 25.0, np.where(w_rem2 <= 4, 15.0, np.where(w_rem2 <= 6, 5.0, -5.0)))
D_bat = rate_index + w_scarcity

phase_death2 = np.where(df['phase'] == 'Death', 12.0, np.where(df['phase'] == 'Middle', 5.0, 0.0))

# Batting Pressure Innings 2: 40% Outcome Leverage + 60% Execution Demand + Phase
inn2_bat_p = 40.0 * li2 + 0.60 * D_bat + phase_death2
inn2_bat_p = np.clip(inn2_bat_p, 5.0, 100.0)

# Bowling Pressure Innings 2:
# High when LI is peaked, target is reachable (RRR 7-12), opponent has wickets in hand
reachable_tension = np.where((rrr2 >= 7.0) & (rrr2 <= 11.5), 25.0,
                    np.where((rrr2 > 11.5) & (rrr2 <= 15.0), 16.0,
                    np.where(rrr2 < 7.0, 20.0, 5.0)))
bowl_w_hand2 = np.where(w_rem2 >= 7, 15.0, np.where(w_rem2 >= 5, 8.0, 0.0))
bowl_death_bonus = np.where((b_rem2 <= 30) & (df['runs_needed'] > 0) & (df['runs_needed'] <= 50), 15.0, 0.0)

inn2_bowl_p = 45.0 * li2 + reachable_tension + bowl_w_hand2 + bowl_death_bonus
inn2_bowl_p = np.clip(inn2_bowl_p, 5.0, 100.0)

# Combined assignment
df['batting_pressure_v2'] = np.where(df['innings'] == 1, inn1_bat_p, inn2_bat_p).round(2)
df['bowling_pressure_v2'] = np.where(df['innings'] == 1, inn1_bowl_p, inn2_bowl_p).round(2)

print("\n=== REVISED PRESSURE V2 DISTRIBUTIONS ===")
print("Batting Pressure v2 Summary:")
print(df['batting_pressure_v2'].describe(percentiles=[0.25, 0.5, 0.7, 0.75, 0.8, 0.9]))

print("\nBowling Pressure v2 Summary:")
print(df['bowling_pressure_v2'].describe(percentiles=[0.25, 0.5, 0.7, 0.75, 0.8, 0.9]))

p75_bat = df['batting_pressure_v2'].quantile(0.75)
p75_bowl = df['bowling_pressure_v2'].quantile(0.75)
print(f"\nEmpirical P75 Cutoffs: Batting P75 = {p75_bat:.2f}, Bowling P75 = {p75_bowl:.2f}")

# Delivery Examples
print("\n--- ACTUAL DATASET DELIVERY EXAMPLES ---")
ex1 = df[(df['innings'] == 1) & (df['phase'] == 'Powerplay') & (df['wickets_before'] >= 3)].iloc[0]
print(f"Example 1: Innings 1 Powerplay Collapse (Match {ex1['match_id']}, Ball {ex1['overid']}.{ex1['over_ball_num']}):")
print(f"  Score: {ex1['score_before']}/{ex1['wickets_before']} in {ex1['legal_balls_before']} balls, Expected: {ex1['expected_inn1_total']:.1f}")
print(f"  Batting Pressure v2: {ex1['batting_pressure_v2']:.1f}, Bowling Pressure v2: {ex1['bowling_pressure_v2']:.1f}")

ex2 = df[(df['innings'] == 2) & (df['phase'] == 'Death') & (df['leverage_index'] >= 0.85)].iloc[0]
print(f"\nExample 2: Innings 2 Peaked Climax Leverage (Match {ex2['match_id']}, Ball {ex2['overid']}.{ex2['over_ball_num']}):")
print(f"  Runs needed: {ex2['runs_needed']}, Balls left: {ex2['balls_remaining']}, Wkts left: {ex2['wickets_remaining']}, RRR: {ex2['rrr']:.2f}")
print(f"  Win Prob: {ex2['win_prob']:.3f}, Leverage Index: {ex2['leverage_index']:.3f}")
print(f"  Batting Pressure v2: {ex2['batting_pressure_v2']:.1f}, Bowling Pressure v2: {ex2['bowling_pressure_v2']:.1f}")

ex3 = df[(df['innings'] == 2) & (df['balls_remaining'] <= 18) & (df['runs_needed'] >= 45)].iloc[0]
print(f"\nExample 3: Innings 2 Desperation Slogging / Lost Cause (Match {ex3['match_id']}, Ball {ex3['overid']}.{ex3['over_ball_num']}):")
print(f"  Runs needed: {ex3['runs_needed']}, Balls left: {ex3['balls_remaining']}, Wkts left: {ex3['wickets_remaining']}, RRR: {ex3['rrr']:.2f}")
print(f"  Win Prob: {ex3['win_prob']:.3f}, Leverage Index: {ex3['leverage_index']:.3f}")
print(f"  Batting Pressure v2: {ex3['batting_pressure_v2']:.1f}, Bowling Pressure v2: {ex3['bowling_pressure_v2']:.1f}")

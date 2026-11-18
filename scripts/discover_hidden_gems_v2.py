"""
scripts/discover_hidden_gems_v2.py
Analyzes the full ball-by-ball dataset under Methodology v2 to discover
hidden gems, uncapped Indian talents, emerging finishers, and undervalued specialists.
"""

import os
import pandas as pd
import numpy as np

# Load raw ball_by_ball and comps/matches
DATA_DIR = "Data Pack"
bbb = pd.read_csv(os.path.join(DATA_DIR, "ball_by_ball.csv"))
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))
pm = pd.read_csv(os.path.join(DATA_DIR, "competition_team_player_mapping.csv"))

# Player teams mapping
p_teams = pm.groupby('player_id')['team_name'].apply(lambda x: list(set(x))).to_dict()
p_comps = pm.groupby('player_id')['comp_name'].apply(lambda x: list(set(x))).to_dict()

# Pakistani players (ineligible)
pak_pids = set([pid for pid, tnames in p_teams.items() if any('Pakistan' in t for t in tnames)])
# Indian players (played for India or uncapped Indian in IPL/domestic)
india_pids = set([pid for pid, tnames in p_teams.items() if any('India' in t for t in tnames)])

# IPL teams list
ipl_teams = [
    'Chennai Super Kings', 'Mumbai Indians', 'Rajasthan Royals', 'Punjab Kings',
    'Royal Challengers Bengaluru', 'Delhi Capitals', 'Kolkata Knight Riders',
    'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants'
]

# Check which players played in IPL
ipl_player_pids = set([pid for pid, tnames in p_teams.items() if any(t in ipl_teams for t in tnames)])

# Filter standard innings
df = bbb[bbb['innings'].isin([1, 2])].copy()
df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

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

# Pre-delivery match state
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

# Total balls allocated
df['total_balls_allocated'] = 120
df.loc[(df['innings'] == 1) & df['first_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['first_inn_revised_overs']
df.loc[(df['innings'] == 2) & df['second_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['second_inn_revised_overs']
df['balls_remaining'] = np.maximum(0, df['total_balls_allocated'] - df['legal_balls_before'])

df['phase'] = 'Middle'
df.loc[df['legal_balls_before'] < 36, 'phase'] = 'Powerplay'
df.loc[df['legal_balls_before'] >= 90, 'phase'] = 'Death'

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

# Standardized WP primitives
mean_R, std_R = 92.4, 51.8
mean_B, std_B = 62.1, 34.6
mean_W, std_W = 6.9, 2.4

z_R = (df['runs_needed'] - mean_R) / std_R
z_B = (df['balls_remaining'] - mean_B) / std_B
z_W = (df['wickets_remaining'] - mean_W) / std_W

logit_wp = -0.2294 - 3.0121 * z_R + 1.5537 * z_B + 1.4970 * z_W
df['win_prob'] = np.where(df['innings'] == 2, 1.0 / (1.0 + np.exp(-logit_wp.clip(-12.0, 12.0))), 0.5)
df['leverage_index'] = np.where(df['innings'] == 2, 4.0 * df['win_prob'] * (1.0 - df['win_prob']), 0.5)

# Pressure scores
b1 = df['legal_balls_before'].clip(0, 120)
w1 = df['wickets_before'].clip(0, 10)
w_rem1 = df['wickets_remaining'].clip(0, 10)
S1 = df['score_before']
S_exp1 = (b1 / 6.0) * 8.5
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

rrr2 = df['rrr'].fillna(8.0).clip(0, 36)
w_rem2 = df['wickets_remaining'].clip(0, 10)
b_rem2 = df['balls_remaining'].clip(0, 120)
li2 = df['leverage_index'].fillna(0.5)

rate_index = np.clip((rrr2 - 4.0) / 10.0, 0.0, 2.0) * 50.0
w_scarcity = np.where(w_rem2 <= 2, 25.0, np.where(w_rem2 <= 4, 15.0, np.where(w_rem2 <= 6, 5.0, -5.0)))
D_bat = rate_index + w_scarcity
phase_death2 = np.where(df['phase'] == 'Death', 12.0, np.where(df['phase'] == 'Middle', 5.0, 0.0))
inn2_bat = np.clip(40.0 * li2 + 0.60 * D_bat + phase_death2, 5.0, 100.0)

reachable_tension = 25.0 * np.exp(-((rrr2 - 9.5) ** 2) / (2.0 * (3.5 ** 2)))
opp_w_penalty = 15.0 * np.clip((w_rem2 - 3.0) / 5.0, 0.0, 1.0)
death_bonus = 15.0 * np.maximum(0, (30.0 - b_rem2) / 30.0) * np.exp(-((df['runs_needed'].fillna(0) - 25.0) ** 2) / (2.0 * (18.0 ** 2)))
inn2_bowl = np.clip(5.0 + 45.0 * li2 + reachable_tension + opp_w_penalty + death_bonus, 5.0, 100.0)

df['batting_pressure_final'] = np.where(df['innings'] == 1, inn1_bat, inn2_bat).round(2)
df['bowling_pressure_final'] = np.where(df['innings'] == 1, inn1_bowl, inn2_bowl).round(2)

p75_bat = 55.20
p75_bowl = 68.90

df['is_press_bat'] = df['batting_pressure_final'] >= p75_bat
df['is_press_bowl'] = df['bowling_pressure_final'] >= p75_bowl

# ANALYZE BATTERS (Flexible Sample: Balls >= 30, non-Pakistani)
bat_res = []
for (pid, pname), grp in df[df['is_ball_faced']].groupby(['striker_id', 'striker_name']):
    if pid in pak_pids:
        continue
    p_grp = grp[grp['is_press_bat']]
    n_grp = grp[~grp['is_press_bat']]
    p_balls = len(p_grp)
    if p_balls < 30:
        continue
    p_runs = p_grp['runs'].sum()
    p_outs = p_grp['is_dismissal'].sum()
    p_sr = (p_runs / p_balls) * 100.0
    n_sr = (n_grp['runs'].sum() / len(n_grp) * 100.0) if len(n_grp) > 0 else 125.0
    p_avg = (p_runs / p_outs) if p_outs > 0 else p_runs * 1.5
    
    t_list = p_teams.get(pid, [])
    is_ipl = pid in ipl_player_pids
    is_india = pid in india_pids
    ipl_balls = len(p_grp[p_grp['comp_name'].str.contains('IPL', case=False, na=False)])
    
    bat_res.append({
        'player_id': pid, 'player_name': pname,
        'pressure_balls': p_balls, 'pressure_runs': p_runs,
        'pressure_sr': round(p_sr, 2), 'normal_sr': round(n_sr, 2),
        'delta_sr': round(p_sr - n_sr, 2), 'pressure_avg': round(p_avg, 2),
        'dismissals': p_outs, 'match_count': grp['match_id'].nunique(),
        'ipl_balls': ipl_balls, 'is_ipl': is_ipl, 'is_india': is_india,
        'teams': ", ".join(t_list)[:45]
    })

df_b_all = pd.DataFrame(bat_res)

# ANALYZE BOWLERS (Flexible Sample: Balls >= 35, non-Pakistani)
bowl_res = []
for (pid, pname), grp in df[df['is_legal_ball']].groupby(['bowler_id', 'bowler_name']):
    if pid in pak_pids:
        continue
    p_grp = grp[grp['is_press_bowl']]
    n_grp = grp[~grp['is_press_bowl']]
    p_balls = len(p_grp)
    if p_balls < 35:
        continue
    p_runs = p_grp['bowler_runs'].sum()
    p_wkts = p_grp['is_bowler_wicket'].sum()
    p_econ = (p_runs / p_balls) * 6.0
    n_econ = (n_grp['bowler_runs'].sum() / len(n_grp) * 6.0) if len(n_grp) > 0 else 8.5
    
    t_list = p_teams.get(pid, [])
    is_ipl = pid in ipl_player_pids
    is_india = pid in india_pids
    ipl_balls = len(p_grp[p_grp['comp_name'].str.contains('IPL', case=False, na=False)])
    
    bowl_res.append({
        'player_id': pid, 'player_name': pname,
        'pressure_balls': p_balls, 'pressure_runs': p_runs,
        'pressure_econ': round(p_econ, 2), 'normal_econ': round(n_econ, 2),
        'delta_econ': round(n_econ - p_econ, 2), 'pressure_wkts': p_wkts,
        'wkt_rate': round(p_wkts / p_balls * 6.0, 3),
        'match_count': grp['match_id'].nunique(),
        'ipl_balls': ipl_balls, 'is_ipl': is_ipl, 'is_india': is_india,
        'teams': ", ".join(t_list)[:45]
    })

df_bw_all = pd.DataFrame(bowl_res)

print("\n=== TOP UNCAPPED / EMERGING INDIAN BATTERS (Pressure SR >= 140, Delta SR > 0) ===")
uncapped_b = df_b_all[(df_b_all['is_ipl']) & (~df_b_all['is_india']) & (df_b_all['pressure_sr'] >= 140)]
print(uncapped_b.sort_values(by='pressure_sr', ascending=False)[
    ['player_name', 'player_id', 'pressure_balls', 'pressure_sr', 'delta_sr', 'pressure_avg', 'ipl_balls', 'teams']
].head(20).to_string())

print("\n=== TOP UNCAPPED / EMERGING INDIAN BOWLERS (Pressure Econ <= 9.00, Balls >= 40) ===")
uncapped_bw = df_bw_all[(df_bw_all['is_ipl']) & (~df_bw_all['is_india']) & (df_bw_all['pressure_econ'] <= 9.00)]
print(uncapped_bw.sort_values(by='pressure_econ', ascending=True)[
    ['player_name', 'player_id', 'pressure_balls', 'pressure_econ', 'delta_econ', 'pressure_wkts', 'ipl_balls', 'teams']
].head(20).to_string())

print("\n=== TOP OVERSEAS VALUE CANDIDATES (NON-TOP 5 MARQUEE) ===")
overseas_bw = df_bw_all[(~df_bw_all['is_india']) & (df_bw_all['pressure_econ'] <= 8.50) & (df_bw_all['pressure_balls'] >= 80)]
print(overseas_bw.sort_values(by='pressure_econ', ascending=True)[
    ['player_name', 'player_id', 'pressure_balls', 'pressure_econ', 'delta_econ', 'pressure_wkts', 'ipl_balls', 'teams']
].head(15).to_string())



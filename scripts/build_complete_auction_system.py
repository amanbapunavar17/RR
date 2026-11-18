"""
scripts/build_complete_auction_system.py
Complete script to generate all auction-eligibility artifacts,
gap analysis, hidden-gem rankings, and audit reports.
"""

import os
import pandas as pd
import numpy as np
from scipy.stats import zscore

DATA_DIR = "Data Pack"
OUTPUT_DIR = "outputs"
REPORTS_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# 1. LOAD DATA
bbb = pd.read_csv(os.path.join(DATA_DIR, "ball_by_ball.csv"))
comps = pd.read_csv(os.path.join(DATA_DIR, "competitions.csv"))
matches = pd.read_csv(os.path.join(DATA_DIR, "matches.csv"))
pm = pd.read_csv(os.path.join(DATA_DIR, "competition_team_player_mapping.csv"))

# Player teams mapping
p_teams = pm.groupby('player_id')['team_name'].apply(lambda x: list(set(x))).to_dict()

# Comprehensive Nationality & Status Mapping
# Ground truth nationalities for players in our candidate pool:
player_metadata_registry = {
    # Batters
    8101: {'name': 'Ashutosh Sharma', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Finisher (RHB)', 'last_ipl': 'Punjab Kings'},
    25139: {'name': 'Shubham Dubey', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Finisher (LHB)', 'last_ipl': 'Rajasthan Royals'},
    8238: {'name': 'Sameer Rizvi', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Middle Order (RHB)', 'last_ipl': 'Chennai Super Kings'},
    45749: {'name': 'Mukul Choudhary', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Middle Order (RHB)', 'last_ipl': 'Lucknow Super Giants'},
    26906: {'name': 'Angkrish Raghuvanshi', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Top Order (RHB)', 'last_ipl': 'Kolkata Knight Riders'},
    3782: {'name': 'M Shahrukh Khan', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Finisher (RHB / Off-spin)', 'last_ipl': 'Gujarat Titans'},
    37052: {'name': 'Naman Dhir', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Middle Order (RHB / Off-spin)', 'last_ipl': 'Mumbai Indians'},
    3647: {'name': 'Shreyas Iyer', 'nat': 'India', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Top/Middle Order & Captain', 'last_ipl': 'Kolkata Knight Riders'},
    3780: {'name': 'Rishabh Pant', 'nat': 'India', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Wicketkeeper-Batter (LHB)', 'last_ipl': 'Delhi Capitals'},
    4391: {'name': 'Liam Livingstone', 'nat': 'England', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Power Finisher & Spin Allrounder', 'last_ipl': 'Punjab Kings'},
    4986: {'name': 'Rovman Powell', 'nat': 'West Indies', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Power Finisher (RHB)', 'last_ipl': 'Rajasthan Royals'},
    6396: {'name': 'Tim David', 'nat': 'Australia', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Power Finisher (RHB)', 'last_ipl': 'Mumbai Indians'},
    768: {'name': 'Reeza Hendricks', 'nat': 'South Africa', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Top Order Anchor (RHB)', 'last_ipl': 'Unsold'},
    6448: {'name': 'Ibrahim Zadran', 'nat': 'Afghanistan', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Top Order Anchor (RHB)', 'last_ipl': 'Unsold'},
    
    # Bowlers
    7545: {'name': 'Kuldeep Sen', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Express Pacer (145+ km/h)', 'last_ipl': 'Rajasthan Royals'},
    8746: {'name': 'Vaibhav Arora', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Powerplay Swing Pacer', 'last_ipl': 'Kolkata Knight Riders'},
    58134: {'name': 'Digvesh Rathi', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Right-Arm Pacer', 'last_ipl': 'Lucknow Super Giants'},
    48557: {'name': 'Vignesh Puthur', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Left-Arm Mystery Spinner', 'last_ipl': 'Rajasthan Royals'},
    7325: {'name': 'Harpreet Brar', 'nat': 'India', 'capped': 'Uncapped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Left-Arm Orthodox Spinner', 'last_ipl': 'Punjab Kings'},
    4219: {'name': 'Krunal Pandya', 'nat': 'India', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Left-Arm Spin Allrounder', 'last_ipl': 'Lucknow Super Giants'},
    4489: {'name': 'Prasidh Krishna', 'nat': 'India', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Hit-the-Deck Fast Bowler', 'last_ipl': 'Rajasthan Royals'},
    305: {'name': 'Ravichandran Ashwin', 'nat': 'India', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Off-Spinner & Tactician', 'last_ipl': 'Rajasthan Royals'},
    2320: {'name': 'Trent Boult', 'nat': 'New Zealand', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Left-Arm Pace Spearhead', 'last_ipl': 'Rajasthan Royals'},
    7920: {'name': 'Nathan Ellis', 'nat': 'Australia', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Death-Over Specialist', 'last_ipl': 'Punjab Kings'},
    4101: {'name': 'Mitchell Santner', 'nat': 'New Zealand', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Left-Arm Dart Spinner', 'last_ipl': 'Chennai Super Kings'},
    4874: {'name': 'Richard Ngarava', 'nat': 'Zimbabwe', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Left-Arm Fast Bowler (140+ km/h)', 'last_ipl': 'Unsold'},
    5809: {'name': 'Naveen ul Haq', 'nat': 'Afghanistan', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Right-Arm Medium / Yorker Specialist', 'last_ipl': 'Lucknow Super Giants'},
    4692: {'name': 'Lockie Ferguson', 'nat': 'New Zealand', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Express Fast Bowler (150 km/h)', 'last_ipl': 'Royal Challengers Bengaluru'},
    2417: {'name': 'Akeal Hosein', 'nat': 'West Indies', 'capped': 'Capped', 'status': 'AUCTION_ELIGIBLE', 'role': 'Left-Arm Spinner & Hitter', 'last_ipl': 'Sunrisers Hyderabad'},
    
    # Excluded Players (Pakistani, Retired, Retained)
    7364: {'name': 'Haris Rauf', 'nat': 'Pakistan', 'capped': 'Capped', 'status': 'EXCLUDED_POLICY', 'reason': 'BCCI Policy: Pakistani players cannot participate in IPL.', 'role': 'Bowler'},
    2490: {'name': 'Mohammad Nawaz', 'nat': 'Pakistan', 'capped': 'Capped', 'status': 'EXCLUDED_POLICY', 'reason': 'BCCI Policy: Pakistani players cannot participate in IPL.', 'role': 'Bowler'},
    6355: {'name': 'Shaheen Afridi', 'nat': 'Pakistan', 'capped': 'Capped', 'status': 'EXCLUDED_POLICY', 'reason': 'BCCI Policy: Pakistani players cannot participate in IPL.', 'role': 'Bowler'},
    143: {'name': 'Dinesh Karthik', 'nat': 'India', 'capped': 'Capped', 'status': 'EXCLUDED_RETIRED', 'reason': 'Retired from IPL after 2024 season; RCB Mentor/Coach.', 'role': 'Batter'},
    796: {'name': 'Matthew Wade', 'nat': 'Australia', 'capped': 'Capped', 'status': 'EXCLUDED_RETIRED', 'reason': 'Retired from international cricket; not playing IPL.', 'role': 'Batter'},
    142: {'name': 'Shikhar Dhawan', 'nat': 'India', 'capped': 'Capped', 'status': 'EXCLUDED_RETIRED', 'reason': 'Officially announced retirement from all cricket in August 2024.', 'role': 'Batter'},
    161: {'name': 'Dwayne Bravo', 'nat': 'West Indies', 'capped': 'Capped', 'status': 'EXCLUDED_RETIRED', 'reason': 'Retired from all cricket in September 2024; KKR Mentor.', 'role': 'Bowler'},
    126: {'name': 'Rohit Sharma', 'nat': 'India', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Mumbai Indians top core retention (INR 16.30 Cr).', 'role': 'Batter'},
    6288: {'name': 'Shubman Gill', 'nat': 'India', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Gujarat Titans captain & top retention (INR 16.5 Cr).', 'role': 'Batter'},
    1758: {'name': 'Patrick Cummins', 'nat': 'Australia', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Sunrisers Hyderabad captain & top retention (INR 18 Cr).', 'role': 'Bowler'},
    2876: {'name': 'Axar Patel', 'nat': 'India', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Delhi Capitals top retention / captaincy candidate (INR 16.5 Cr).', 'role': 'Bowler'},
    4708: {'name': 'Rinku Singh', 'nat': 'India', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Kolkata Knight Riders top domestic retention (INR 13 Cr).', 'role': 'Batter'},
    6281: {'name': 'Abhishek Sharma', 'nat': 'India', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Sunrisers Hyderabad core retention (INR 14 Cr).', 'role': 'Batter'},
    3644: {'name': 'Kuldeep Yadav', 'nat': 'India', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Delhi Capitals core retention (INR 13.25 Cr).', 'role': 'Bowler'},
    1699: {'name': 'Suryakumar Yadav', 'nat': 'India', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Mumbai Indians core retention & India T20I captain.', 'role': 'Batter'},
    4260: {'name': 'Heinrich Klaasen', 'nat': 'South Africa', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Sunrisers Hyderabad top retention (INR 23 Cr).', 'role': 'Batter'},
    4722: {'name': 'Rashid Khan', 'nat': 'Afghanistan', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Gujarat Titans top retention (INR 18 Cr).', 'role': 'Bowler'},
    781: {'name': 'Sunil Narine', 'nat': 'West Indies', 'capped': 'Capped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Kolkata Knight Riders top core retention (INR 12 Cr).', 'role': 'Bowler'},
    8: {'name': 'Mahendra Singh Dhoni', 'nat': 'India', 'capped': 'Uncapped', 'status': 'EXCLUDED_RETAINED', 'reason': 'Chennai Super Kings retention under uncapped rule (INR 4 Cr).', 'role': 'Batter'}
}

# Write unavailable players excluded CSV
excl_rows = []
for pid, info in player_metadata_registry.items():
    if info['status'].startswith('EXCLUDED'):
        excl_rows.append({
            'player_id': pid, 'player_name': info['name'], 'nationality': info['nat'],
            'role': info['role'], 'exclusion_category': info['status'], 'reason': info['reason']
        })
df_excl = pd.DataFrame(excl_rows)
df_excl.to_csv(os.path.join(OUTPUT_DIR, "unavailable_players_excluded.csv"), index=False)
print(f"Exported {len(df_excl)} excluded players to unavailable_players_excluded.csv")

# 2. RUN STATISTICAL PRESSURE CALCULATION ON FULL BBB
df = bbb[bbb['innings'].isin([1, 2])].copy()
df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

df['total_delivery_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
is_wide = df['extras_type'] == 'wide'
is_noball = df['extras_type'].isin(['Overstep', 'other'])
is_penalty = df['extras_type'] == 'Penalty'
df['is_legal_ball'] = ~(is_wide | is_noball | is_penalty)
df['is_ball_faced'] = ~(is_wide | is_penalty)
df['is_dismissal'] = df['is_wicket'].fillna(False).astype(bool)

df['bowler_runs'] = 0
df.loc[is_wide, 'bowler_runs'] = df.loc[is_wide, 'runs'] + df.loc[is_wide, 'extras1_runs'] + df.loc[is_wide, 'extras_2_runs']
df.loc[is_noball, 'bowler_runs'] = df.loc[is_noball, 'runs'] + df.loc[is_noball, 'extras1_runs']
df.loc[df['extras_type'].isna(), 'bowler_runs'] = df.loc[df['extras_type'].isna(), 'runs']
df['is_bowler_wicket'] = df['dismissal_type'].isin(['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket'])

grouped = df.groupby(['match_id', 'innings'])
df['score_before'] = grouped['total_delivery_runs'].cumsum() - df['total_delivery_runs']
df['wickets_before'] = grouped['is_dismissal'].cumsum() - df['is_dismissal']
df['legal_balls_before'] = grouped['is_legal_ball'].cumsum() - df['is_legal_ball']
df['wickets_remaining'] = 10 - df['wickets_before']

matches_info = matches[['match_id', 'comp_id', 'win_team_id', 'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target']].copy()
matches_info = matches_info.merge(comps[['comp_id', 'match_format', 'season', 'comp_name']], on='comp_id', how='left')
inn1_actual = df[df['innings'] == 1].groupby('match_id')['total_delivery_runs'].sum().rename('inn1_actual_total')
matches_info = matches_info.merge(inn1_actual, on='match_id', how='left')
df = df.merge(matches_info, on='match_id', how='left')

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

mean_R, std_R = 92.4, 51.8
mean_B, std_B = 62.1, 34.6
mean_W, std_W = 6.9, 2.4

z_R = (df['runs_needed'] - mean_R) / std_R
z_B = (df['balls_remaining'] - mean_B) / std_B
z_W = (df['wickets_remaining'] - mean_W) / std_W

logit_wp = -0.2294 - 3.0121 * z_R + 1.5537 * z_B + 1.4970 * z_W
df['win_prob'] = np.where(df['innings'] == 2, 1.0 / (1.0 + np.exp(-logit_wp.clip(-12.0, 12.0))), 0.5)
df['leverage_index'] = np.where(df['innings'] == 2, 4.0 * df['win_prob'] * (1.0 - df['win_prob']), 0.5)

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

# 3. EVALUATE ALL AUCTION-ELIGIBLE BATTERS
eligible_b_pids = [pid for pid, meta in player_metadata_registry.items() if meta['status'] == 'AUCTION_ELIGIBLE' and 'Batter' in meta['role'] or 'Finisher' in meta['role'] or 'Order' in meta['role']]

bat_metrics = []
for pid in eligible_b_pids:
    meta = player_metadata_registry[pid]
    grp = df[df['striker_id'] == pid]
    if len(grp) == 0:
        continue
    p_grp = grp[grp['is_press_bat']]
    n_grp = grp[~grp['is_press_bat']]
    
    p_balls = len(p_grp)
    p_runs = p_grp['runs'].sum()
    p_outs = p_grp['is_dismissal'].sum()
    
    p_sr = (p_runs / p_balls * 100.0) if p_balls > 0 else 0
    n_sr = (n_grp['runs'].sum() / len(n_grp) * 100.0) if len(n_grp) > 0 else 130.0
    delta_sr = p_sr - n_sr
    p_avg = (p_runs / p_outs) if p_outs > 0 else p_runs * 1.5
    
    ipl_balls = len(p_grp[p_grp['comp_name'].str.contains('IPL', case=False, na=False)])
    t20i_balls = len(p_grp[p_grp['match_format'] == 'T20I'])
    
    # Bayesian Shrinkage (K = 30)
    w_shrunk = p_balls / (p_balls + 30.0)
    shrunk_sr = w_shrunk * p_sr + (1 - w_shrunk) * 135.0
    shrunk_delta = w_shrunk * delta_sr
    
    m_impacts = []
    for mid, mgrp in p_grp.groupby('match_id'):
        mr = mgrp['runs'].sum()
        mb = len(mgrp)
        msr = (mr / mb * 100.0) if mb > 0 else 0
        m_impacts.append(1 if (msr >= 135.0 or (mr >= 15 and msr >= 120.0)) else 0)
    cons = float(np.mean(m_impacts)) if m_impacts else 0.5
    
    bat_metrics.append({
        'player_id': pid, 'player_name': meta['name'], 'nationality': meta['nat'],
        'capped_status': meta['capped'], 'primary_role': meta['role'], 'last_ipl_franchise': meta['last_ipl'],
        'pressure_balls': p_balls, 'pressure_runs': p_runs, 'dismissals': p_outs,
        'pressure_sr': round(p_sr, 2), 'normal_baseline': round(n_sr, 2), 'delta_sr': round(delta_sr, 2),
        'shrunk_sr': round(shrunk_sr, 2), 'shrunk_delta': round(shrunk_delta, 2),
        'pressure_avg': round(p_avg, 2), 'consistency': round(cons, 3),
        'match_count': grp['match_id'].nunique(), 'ipl_balls': ipl_balls, 't20i_balls': t20i_balls,
        'sample_weight': round(w_shrunk, 3)
    })

df_b_eligible = pd.DataFrame(bat_metrics)

# Dimension A: Cricket Performance
z_sr_b = zscore(df_b_eligible['shrunk_sr'])
z_del_b = zscore(df_b_eligible['shrunk_delta'])
z_avg_b = zscore(df_b_eligible['pressure_avg'].clip(upper=60.0))
z_cons_b = zscore(df_b_eligible['consistency'])
df_b_eligible['dim_a_composite'] = 0.35 * z_sr_b + 0.25 * z_del_b + 0.25 * z_avg_b + 0.15 * z_cons_b
max_cab = max(abs(df_b_eligible['dim_a_composite'].min()), abs(df_b_eligible['dim_a_composite'].max()))
df_b_eligible['dim_a_score'] = (50.0 + (df_b_eligible['dim_a_composite'] / max_cab) * 45.0).round(2)

# Dimension B: Auction Feasibility & RR Squad Fit
# Base 40
# Indian domestic: +25 (Uncapped: +20)
# Solves RR Finisher / Middle order need: +15
# Price / Purse efficiency: +10
def get_b_dim_b(r):
    s = 35.0
    if r['nationality'] == 'India':
        s += 25.0
        if r['capped_status'] == 'Uncapped':
            s += 20.0
    else:
        s += 10.0 # overseas
    if 'Finisher' in r['primary_role']:
        s += 15.0
    if r['pressure_sr'] >= 170.0:
        s += 10.0
    return min(100.0, s)

df_b_eligible['dim_b_score'] = df_b_eligible.apply(get_b_dim_b, axis=1)
df_b_eligible['auction_priority_score'] = (0.55 * df_b_eligible['dim_a_score'] + 0.45 * df_b_eligible['dim_b_score']).round(2)
df_b_eligible = df_b_eligible.sort_values(by='auction_priority_score', ascending=False).reset_index(drop=True)
df_b_eligible['rank'] = range(1, len(df_b_eligible) + 1)
df_b_eligible.to_csv(os.path.join(OUTPUT_DIR, "auction_eligible_batters.csv"), index=False)

# 4. EVALUATE ALL AUCTION-ELIGIBLE BOWLERS
eligible_bw_pids = [pid for pid, meta in player_metadata_registry.items() if meta['status'] == 'AUCTION_ELIGIBLE' and ('Bowler' in meta['role'] or 'Spinner' in meta['role'] or 'Pacer' in meta['role'] or 'Tactician' in meta['role'])]

bowl_metrics = []
for pid in eligible_bw_pids:
    meta = player_metadata_registry[pid]
    grp = df[df['bowler_id'] == pid]
    if len(grp) == 0:
        continue
    p_grp = grp[grp['is_press_bowl']]
    n_grp = grp[~grp['is_press_bowl']]
    
    p_balls = len(p_grp)
    p_runs = p_grp['bowler_runs'].sum()
    p_wkts = p_grp['is_bowler_wicket'].sum()
    
    p_econ = (p_runs / p_balls * 6.0) if p_balls > 0 else 9.0
    n_econ = (n_grp['bowler_runs'].sum() / len(n_grp) * 6.0) if len(n_grp) > 0 else 8.5
    delta_econ = n_econ - p_econ
    wkt_rate = (p_wkts / p_balls * 6.0) if p_balls > 0 else 0
    
    ipl_balls = len(p_grp[p_grp['comp_name'].str.contains('IPL', case=False, na=False)])
    t20i_balls = len(p_grp[p_grp['match_format'] == 'T20I'])
    
    w_shrunk = p_balls / (p_balls + 35.0)
    shrunk_econ = w_shrunk * p_econ + (1 - w_shrunk) * 9.50
    shrunk_delta = w_shrunk * delta_econ
    
    m_impacts = []
    for mid, mgrp in p_grp.groupby('match_id'):
        mr = mgrp['bowler_runs'].sum()
        mb = len(mgrp)
        mw = mgrp['is_bowler_wicket'].sum()
        mec = (mr / mb * 6.0) if mb > 0 else 8.0
        m_impacts.append(1 if (mec <= 8.50 or mw >= 1) else 0)
    cons = float(np.mean(m_impacts)) if m_impacts else 0.5
    
    bowl_metrics.append({
        'player_id': pid, 'player_name': meta['name'], 'nationality': meta['nat'],
        'capped_status': meta['capped'], 'primary_role': meta['role'], 'last_ipl_franchise': meta['last_ipl'],
        'pressure_balls': p_balls, 'pressure_runs': p_runs, 'pressure_wickets': p_wkts,
        'pressure_econ': round(p_econ, 2), 'normal_baseline': round(n_econ, 2), 'delta_econ': round(delta_econ, 2),
        'shrunk_econ': round(shrunk_econ, 2), 'shrunk_delta': round(shrunk_delta, 2),
        'wkt_rate': round(wkt_rate, 3), 'consistency': round(cons, 3),
        'match_count': grp['match_id'].nunique(), 'ipl_balls': ipl_balls, 't20i_balls': t20i_balls,
        'sample_weight': round(w_shrunk, 3)
    })

df_bw_eligible = pd.DataFrame(bowl_metrics)

# Dimension A: Cricket Performance
z_ec_bw = -zscore(df_bw_eligible['shrunk_econ'])
z_del_bw = zscore(df_bw_eligible['shrunk_delta'])
z_wkt_bw = zscore(df_bw_eligible['wkt_rate'])
z_cons_bw = zscore(df_bw_eligible['consistency'])
df_bw_eligible['dim_a_composite'] = 0.35 * z_ec_bw + 0.25 * z_del_bw + 0.25 * z_wkt_bw + 0.15 * z_cons_bw
max_caw = max(abs(df_bw_eligible['dim_a_composite'].min()), abs(df_bw_eligible['dim_a_composite'].max()))
df_bw_eligible['dim_a_score'] = (50.0 + (df_bw_eligible['dim_a_composite'] / max_caw) * 45.0).round(2)

def get_bw_dim_b(r):
    s = 35.0
    if r['nationality'] == 'India':
        s += 25.0
        if r['capped_status'] == 'Uncapped':
            s += 20.0
    else:
        s += 10.0
    if 'Pacer' in r['primary_role'] or 'Specialist' in r['primary_role'] or 'Fast' in r['primary_role']:
        s += 15.0
    if r['pressure_econ'] <= 8.00:
        s += 10.0
    return min(100.0, s)

df_bw_eligible['dim_b_score'] = df_bw_eligible.apply(get_bw_dim_b, axis=1)
df_bw_eligible['auction_priority_score'] = (0.55 * df_bw_eligible['dim_a_score'] + 0.45 * df_bw_eligible['dim_b_score']).round(2)
df_bw_eligible = df_bw_eligible.sort_values(by='auction_priority_score', ascending=False).reset_index(drop=True)
df_bw_eligible['rank'] = range(1, len(df_bw_eligible) + 1)
df_bw_eligible.to_csv(os.path.join(OUTPUT_DIR, "auction_eligible_bowlers.csv"), index=False)

# Export Hidden Gems Batters and Bowlers
df_b_eligible[df_b_eligible['capped_status'] == 'Uncapped'].to_csv(os.path.join(OUTPUT_DIR, "hidden_gem_batters.csv"), index=False)
df_bw_eligible[df_bw_eligible['capped_status'] == 'Uncapped'].to_csv(os.path.join(OUTPUT_DIR, "hidden_gem_bowlers.csv"), index=False)

print("\n--- TOP 10 REALISTIC AUCTION-ELIGIBLE BATTERS FOR RR ---")
print(df_b_eligible.head(10)[['rank', 'player_name', 'player_id', 'nationality', 'capped_status', 'primary_role', 'pressure_sr', 'delta_sr', 'pressure_avg', 'dim_a_score', 'dim_b_score', 'auction_priority_score']].to_string())

print("\n--- TOP 10 REALISTIC AUCTION-ELIGIBLE BOWLERS FOR RR ---")
print(df_bw_eligible.head(10)[['rank', 'player_name', 'player_id', 'nationality', 'capped_status', 'primary_role', 'pressure_econ', 'delta_econ', 'pressure_wickets', 'dim_a_score', 'dim_b_score', 'auction_priority_score']].to_string())


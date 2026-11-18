import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd
import numpy as np
from scipy.stats import zscore, spearmanr

# Load the evaluated deliveries from test_pressure_v2_calc
from scripts.test_pressure_v2_calc import df

# Define candidate thresholds:
# Batting thresholds: P70 (52.0), P75 (55.0), P80 (58.0)
# Bowling thresholds: P70 (64.0), P75 (68.0), P80 (73.0)

print("\n=== SENSITIVITY TESTING OF REFINED v2 MODEL ===")

def evaluate_batters_v2(df_in, bat_thresh, min_balls=120, weights=(0.35, 0.25, 0.25, 0.15)):
    w_sr, w_delta, w_avg, w_cons = weights
    df_bf = df_in[df_in['is_ball_faced']].copy()
    df_bf['is_press'] = df_bf['batting_pressure_v2'] >= bat_thresh
    
    pop_press_sr = (df_bf[df_bf['is_press']]['runs'].sum() / df_bf[df_bf['is_press']]['is_ball_faced'].sum()) * 100.0
    pop_norm_sr = (df_bf[~df_bf['is_press']]['runs'].sum() / df_bf[~df_bf['is_press']]['is_ball_faced'].sum()) * 100.0
    
    records = []
    for (pid, pname), grp in df_bf.groupby(['striker_id', 'striker_name']):
        p_grp = grp[grp['is_press']]
        n_grp = grp[~grp['is_press']]
        
        p_balls = p_grp['is_ball_faced'].sum()
        p_matches = p_grp['match_id'].nunique()
        if p_balls < min_balls or p_matches < 10:
            continue
            
        n_balls = n_grp['is_ball_faced'].sum()
        p_runs = p_grp['runs'].sum()
        p_outs = p_grp['is_wicket'].sum()
        
        n_runs = n_grp['runs'].sum()
        n_outs = n_grp['is_wicket'].sum()
        
        p_sr = (p_runs / p_balls) * 100.0
        n_sr = (n_runs / n_balls * 100.0) if n_balls > 0 else pop_norm_sr
        delta_sr = p_sr - n_sr
        p_avg = p_runs / max(1, p_outs)
        
        # Empirical Bayes shrinkage (K=40)
        K = 40.0
        w = p_balls / (p_balls + K)
        shrunk_sr = w * p_sr + (1 - w) * pop_press_sr
        shrunk_delta_sr = w * delta_sr
        
        # Match consistency
        m_impacts = []
        for mid, mgrp in p_grp.groupby('match_id'):
            mr = mgrp['runs'].sum()
            mb = mgrp['is_ball_faced'].sum()
            msr = (mr / mb * 100.0) if mb > 0 else 0
            m_impacts.append(1 if (msr >= 135.0 or (mr >= 15 and msr >= 120.0)) else 0)
        cons = np.mean(m_impacts) if m_impacts else 0.5
        
        records.append({
            'player_id': pid, 'player_name': pname,
            'balls': p_balls, 'runs': p_runs, 'outs': p_outs,
            'sr': p_sr, 'normal_sr': n_sr, 'delta_sr': delta_sr,
            'shrunk_sr': shrunk_sr, 'shrunk_delta_sr': shrunk_delta_sr,
            'avg': p_avg, 'consistency': cons
        })
        
    bdf = pd.DataFrame(records)
    if len(bdf) == 0: return bdf
    
    # Orthogonal 4-pillar composite score:
    # 1. Shrunk SR (Velocity)
    # 2. Shrunk Delta SR (Clutch lift over personal baseline)
    # 3. Pressure Avg (Dismissal resistance)
    # 4. Consistency (Match-to-match reliability)
    bdf['z_sr'] = zscore(bdf['shrunk_sr'])
    bdf['z_delta'] = zscore(bdf['shrunk_delta_sr'])
    bdf['z_avg'] = zscore(bdf['avg'].clip(upper=60.0))
    bdf['z_cons'] = zscore(bdf['consistency'])
    
    bdf['composite'] = w_sr * bdf['z_sr'] + w_delta * bdf['z_delta'] + w_avg * bdf['z_avg'] + w_cons * bdf['z_cons']
    max_c = max(abs(bdf['composite'].min()), abs(bdf['composite'].max()))
    bdf['pressure_score'] = 50.0 + (bdf['composite'] / max_c) * 45.0
    return bdf.sort_values(by='pressure_score', ascending=False).reset_index(drop=True)

def evaluate_bowlers_v2(df_in, bowl_thresh, min_balls=240, weights=(0.35, 0.25, 0.25, 0.15)):
    w_econ, w_delta, w_wkt, w_cons = weights
    df_lb = df_in[df_in['is_legal_ball']].copy()
    df_lb['is_press'] = df_lb['bowling_pressure_v2'] >= bowl_thresh
    
    pop_press_econ = (df_lb[df_lb['is_press']]['bowler_runs'].sum() / df_lb[df_lb['is_press']]['is_legal_ball'].sum()) * 6.0
    pop_norm_econ = (df_lb[~df_lb['is_press']]['bowler_runs'].sum() / df_lb[~df_lb['is_press']]['is_legal_ball'].sum()) * 6.0
    
    records = []
    for (pid, pname), grp in df_lb.groupby(['bowler_id', 'bowler_name']):
        p_grp = grp[grp['is_press']]
        n_grp = grp[~grp['is_press']]
        
        p_balls = p_grp['is_legal_ball'].sum()
        p_matches = p_grp['match_id'].nunique()
        if p_balls < min_balls or p_matches < 15:
            continue
            
        n_balls = n_grp['is_legal_ball'].sum()
        p_runs = p_grp['bowler_runs'].sum()
        p_wkts = p_grp['is_bowler_wicket'].sum()
        
        n_runs = n_grp['bowler_runs'].sum()
        n_wkts = n_grp['is_bowler_wicket'].sum()
        
        p_econ = (p_runs / p_balls) * 6.0
        n_econ = (n_runs / n_balls * 6.0) if n_balls > 0 else pop_norm_econ
        delta_econ = n_econ - p_econ  # positive is better (tighter)
        
        # Empirical Bayes shrinkage (K=60)
        K = 60.0
        w = p_balls / (p_balls + K)
        shrunk_econ = w * p_econ + (1 - w) * pop_press_econ
        shrunk_delta_econ = w * delta_econ
        
        wkt_rate = (p_wkts / p_balls) * 6.0  # wickets per 6 legal balls
        
        # Match consistency: econ <= 8.5 or >= 1 wicket
        m_impacts = []
        for mid, mgrp in p_grp.groupby('match_id'):
            mr = mgrp['bowler_runs'].sum()
            mb = mgrp['is_legal_ball'].sum()
            mw = mgrp['is_bowler_wicket'].sum()
            mec = (mr / mb * 6.0) if mb > 0 else 8.0
            m_impacts.append(1 if (mec <= 8.50 or mw >= 1) else 0)
        cons = np.mean(m_impacts) if m_impacts else 0.5
        
        records.append({
            'player_id': pid, 'player_name': pname,
            'balls': p_balls, 'runs': p_runs, 'wkts': p_wkts,
            'econ': p_econ, 'normal_econ': n_econ, 'delta_econ': delta_econ,
            'shrunk_econ': shrunk_econ, 'shrunk_delta_econ': shrunk_delta_econ,
            'wkt_rate': wkt_rate, 'consistency': cons
        })
        
    bdf = pd.DataFrame(records)
    if len(bdf) == 0: return bdf
    
    # Orthogonal 4-pillar composite score:
    # 1. Shrunk Econ (Run suppression, lower is better -> negate Z)
    # 2. Shrunk Delta Econ (Clutch tightening vs own baseline)
    # 3. Wicket taking rate (Threat per over)
    # 4. Consistency (Match containment rate)
    bdf['z_econ'] = -zscore(bdf['shrunk_econ'])
    bdf['z_delta'] = zscore(bdf['shrunk_delta_econ'])
    bdf['z_wkt'] = zscore(bdf['wkt_rate'])
    bdf['z_cons'] = zscore(bdf['consistency'])
    
    bdf['composite'] = w_econ * bdf['z_econ'] + w_delta * bdf['z_delta'] + w_wkt * bdf['z_wkt'] + w_cons * bdf['z_cons']
    max_c = max(abs(bdf['composite'].min()), abs(bdf['composite'].max()))
    bdf['pressure_score'] = 50.0 + (bdf['composite'] / max_c) * 45.0
    return bdf.sort_values(by='pressure_score', ascending=False).reset_index(drop=True)

# Run Threshold Comparisons
bat_p70 = evaluate_batters_v2(df, 52.0)
bat_p75 = evaluate_batters_v2(df, 55.0)
bat_p80 = evaluate_batters_v2(df, 58.0)

bowl_p70 = evaluate_bowlers_v2(df, 64.0)
bowl_p75 = evaluate_bowlers_v2(df, 68.0)
bowl_p80 = evaluate_bowlers_v2(df, 73.0)

print(f"Qualified Batters count at P75: {len(bat_p75)}")
print(f"Qualified Bowlers count at P75: {len(bowl_p75)}")

print("\nTop 10 Batters at P75 Cutoff (55.0):")
print(bat_p75[['player_id', 'player_name', 'pressure_score', 'balls', 'runs', 'outs', 'sr', 'normal_sr', 'delta_sr', 'avg', 'consistency']].head(10).to_string())

print("\nTop 10 Bowlers at P75 Cutoff (68.0):")
print(bowl_p75[['player_id', 'player_name', 'pressure_score', 'balls', 'wkts', 'econ', 'normal_econ', 'delta_econ', 'wkt_rate', 'consistency']].head(10).to_string())

# Rank Correlation between P70, P75, and P80
common_bat = set(bat_p70['player_id']).intersection(set(bat_p75['player_id'])).intersection(set(bat_p80['player_id']))
r70_b = bat_p70.set_index('player_id').loc[list(common_bat)]['pressure_score']
r75_b = bat_p75.set_index('player_id').loc[list(common_bat)]['pressure_score']
r80_b = bat_p80.set_index('player_id').loc[list(common_bat)]['pressure_score']
print("\nBatter Rank Correlation (P70 vs P75):", spearmanr(r70_b, r75_b).statistic)
print("Batter Rank Correlation (P75 vs P80):", spearmanr(r75_b, r80_b).statistic)

common_bowl = set(bowl_p70['player_id']).intersection(set(bowl_p75['player_id'])).intersection(set(bowl_p80['player_id']))
r70_bw = bowl_p70.set_index('player_id').loc[list(common_bowl)]['pressure_score']
r75_bw = bowl_p75.set_index('player_id').loc[list(common_bowl)]['pressure_score']
r80_bw = bowl_p80.set_index('player_id').loc[list(common_bowl)]['pressure_score']
print("Bowler Rank Correlation (P70 vs P75):", spearmanr(r70_bw, r75_bw).statistic)
print("Bowler Rank Correlation (P75 vs P80):", spearmanr(r75_bw, r80_bw).statistic)


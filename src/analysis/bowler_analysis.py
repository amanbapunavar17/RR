"""
Bowler Analysis Module for SupeRR Selector Season 2
Computes individual bowler metrics under pressure and normal conditions.
Accurately attributes extras (wides/no-balls included, byes/leg-byes excluded, run-outs excluded).
Evaluates economy rates, wicket rates, dot and boundary percentages, format splits, and match consistency.
"""

import numpy as np
import pandas as pd
from scipy.stats import zscore

def analyze_bowlers(df, min_pressure_balls=240, min_matches=15):
    """
    Computes comprehensive bowling metrics comparing pressure performance to normal baselines.
    Applies Empirical Bayes shrinkage and format weighting.
    """
    df_lb = df[df['is_legal_ball']].copy()
    
    # Population benchmarks
    press_df = df_lb[df_lb['is_high_bowling_pressure']]
    norm_df = df_lb[~df_lb['is_high_bowling_pressure']]
    
    pop_press_econ = (press_df['bowler_runs'].sum() / press_df['is_legal_ball'].sum()) * 6.0
    pop_norm_econ = (norm_df['bowler_runs'].sum() / norm_df['is_legal_ball'].sum()) * 6.0
    pop_press_dot = (press_df['is_dot_ball_bowler'].sum() / press_df['is_legal_ball'].sum()) * 100.0
    pop_press_bnd = (press_df['is_boundary'].sum() / press_df['is_legal_ball'].sum()) * 100.0
    pop_press_sr = press_df['is_legal_ball'].sum() / max(1, press_df['is_bowler_wicket'].sum())

    bowl_records = []
    
    for (pid, pname), group in df_lb.groupby(['bowler_id', 'bowler_name']):
        p_grp = group[group['is_high_bowling_pressure']]
        n_grp = group[~group['is_high_bowling_pressure']]
        
        p_balls = int(p_grp['is_legal_ball'].sum())
        p_matches = int(p_grp['match_id'].nunique())
        
        # Eligibility filter
        if p_balls < min_pressure_balls or p_matches < min_matches:
            continue
            
        n_balls = int(n_grp['is_legal_ball'].sum())
        tot_matches = int(group['match_id'].nunique())
        
        p_runs = int(p_grp['bowler_runs'].sum())
        p_wkts = int(p_grp['is_bowler_wicket'].sum())
        p_dots = int(p_grp['is_dot_ball_bowler'].sum())
        p_bnds = int(p_grp['is_boundary'].sum())
        
        n_runs = int(n_grp['bowler_runs'].sum())
        n_wkts = int(n_grp['is_bowler_wicket'].sum())
        n_dots = int(n_grp['is_dot_ball_bowler'].sum())
        n_bnds = int(n_grp['is_boundary'].sum())
        
        p_econ = (p_runs / p_balls) * 6.0
        n_econ = (n_runs / n_balls * 6.0) if n_balls > 0 else pop_norm_econ
        # Positive delta_econ means the bowler improved (lowered their economy) under pressure
        delta_econ = n_econ - p_econ
        
        p_dot_pct = (p_dots / p_balls) * 100.0
        n_dot_pct = (n_dots / max(1, n_balls)) * 100.0
        delta_dot_pct = p_dot_pct - n_dot_pct
        
        p_bnd_pct = (p_bnds / p_balls) * 100.0
        n_bnd_pct = (n_bnds / max(1, n_balls)) * 100.0
        # Positive delta_bnd_pct means bowler conceded FEWER boundaries under pressure
        delta_bnd_pct = n_bnd_pct - p_bnd_pct
        
        p_sr = (p_balls / max(1, p_wkts))
        n_sr = (n_balls / max(1, n_wkts)) if n_balls > 0 else 24.0
        p_w_rate = (p_wkts / p_balls) * 6.0  # wickets per 6 legal balls
        
        # Phase performance under pressure
        death_p = p_grp[p_grp['phase'] == 'Death']
        mid_p = p_grp[p_grp['phase'] == 'Middle']
        pp_p = p_grp[p_grp['phase'] == 'Powerplay']
        
        death_econ = (death_p['bowler_runs'].sum() / death_p['is_legal_ball'].sum() * 6.0) if len(death_p) > 0 else p_econ
        mid_econ = (mid_p['bowler_runs'].sum() / mid_p['is_legal_ball'].sum() * 6.0) if len(mid_p) > 0 else p_econ
        pp_econ = (pp_p['bowler_runs'].sum() / pp_p['is_legal_ball'].sum() * 6.0) if len(pp_p) > 0 else p_econ
        
        # Format splits
        ipl_p = p_grp[p_grp['is_ipl']]
        t20i_p = p_grp[p_grp['is_t20i']]
        
        ipl_balls = int(ipl_p['is_legal_ball'].sum())
        ipl_runs = int(ipl_p['bowler_runs'].sum())
        ipl_wkts = int(ipl_p['is_bowler_wicket'].sum())
        ipl_econ = (ipl_runs / ipl_balls * 6.0) if ipl_balls > 0 else np.nan
        
        t20i_balls = int(t20i_p['is_legal_ball'].sum())
        t20i_runs = int(t20i_p['bowler_runs'].sum())
        t20i_wkts = int(t20i_p['is_bowler_wicket'].sum())
        t20i_econ = (t20i_runs / t20i_balls * 6.0) if t20i_balls > 0 else np.nan
        
        # Match-to-match consistency:
        # Proportion of pressure matches where economy was <= 8.50 OR bowler took >= 1 wicket
        match_impacts = []
        for mid, mgrp in p_grp.groupby('match_id'):
            m_r = mgrp['bowler_runs'].sum()
            m_lb = mgrp['is_legal_ball'].sum()
            m_w = mgrp['is_bowler_wicket'].sum()
            m_ec = (m_r / m_lb * 6.0) if m_lb > 0 else 8.0
            match_impacts.append(1 if (m_ec <= 8.50 or m_w >= 1) else 0)
        consistency = float(np.mean(match_impacts)) if match_impacts else 0.5
        
        # Empirical Bayes Shrinkage for pressure economy (K = 60 balls = 10 overs)
        K_bowl = 60.0
        shrinkage_weight = p_balls / (p_balls + K_bowl)
        shrunk_econ = shrinkage_weight * p_econ + (1.0 - shrinkage_weight) * pop_press_econ
        shrunk_delta_econ = shrinkage_weight * delta_econ
        
        bowl_records.append({
            'player_id': pid,
            'player_name': pname,
            'pressure_balls': p_balls,
            'pressure_runs': p_runs,
            'pressure_wickets': p_wkts,
            'pressure_econ': round(p_econ, 2),
            'normal_econ': round(n_econ, 2),
            'delta_econ': round(delta_econ, 2),
            'shrunk_econ': round(shrunk_econ, 2),
            'shrunk_delta_econ': round(shrunk_delta_econ, 2),
            'pressure_dot_pct': round(p_dot_pct, 2),
            'normal_dot_pct': round(n_dot_pct, 2),
            'delta_dot_pct': round(delta_dot_pct, 2),
            'pressure_bnd_pct': round(p_bnd_pct, 2),
            'normal_bnd_pct': round(n_bnd_pct, 2),
            'delta_bnd_pct': round(delta_bnd_pct, 2),
            'pressure_sr': round(p_sr, 2),
            'normal_sr': round(n_sr, 2),
            'pressure_w_rate': round(p_w_rate, 3),
            'death_econ': round(death_econ, 2),
            'middle_econ': round(mid_econ, 2),
            'powerplay_econ': round(pp_econ, 2),
            'ipl_balls': ipl_balls,
            'ipl_runs': ipl_runs,
            'ipl_wkts': ipl_wkts,
            'ipl_econ': round(ipl_econ, 2) if not np.isnan(ipl_econ) else np.nan,
            't20i_balls': t20i_balls,
            't20i_runs': t20i_runs,
            't20i_wkts': t20i_wkts,
            't20i_econ': round(t20i_econ, 2) if not np.isnan(t20i_econ) else np.nan,
            'pressure_matches': p_matches,
            'total_matches': tot_matches,
            'consistency': round(consistency, 3),
            'sample_reliability': round(shrinkage_weight, 3)
        })

    bowl_df = pd.DataFrame(bowl_records)
    
    # Composite Reliability Rating Calculation
    # Dimensions:
    # 1. Shrunk Pressure Economy (-z because lower economy is better) (25%)
    # 2. Economy Improvement vs own normal baseline (Delta Econ) (25%)
    # 3. Wicket taking rate under pressure (20%)
    # 4. Dot-ball % under pressure (15%)
    # 5. Match-to-match consistency (10%)
    # 6. Sample size reliability weight (5%)
    z_shrunk_econ = -zscore(bowl_df['shrunk_econ'])
    z_delta_econ = zscore(bowl_df['shrunk_delta_econ'])
    z_w_rate = zscore(bowl_df['pressure_w_rate'])
    z_dot = zscore(bowl_df['pressure_dot_pct'])
    z_cons = zscore(bowl_df['consistency'])
    z_rel = zscore(bowl_df['sample_reliability'])
    
    raw_score = (
        0.25 * z_shrunk_econ +
        0.25 * z_delta_econ +
        0.20 * z_w_rate +
        0.15 * z_dot +
        0.10 * z_cons +
        0.05 * z_rel
    )
    
    min_s, max_s = raw_score.min(), raw_score.max()
    bowl_df['pressure_score'] = (50.0 + (raw_score / max(abs(min_s), abs(max_s))) * 45.0).round(2)
    bowl_df['normal_baseline'] = bowl_df['normal_econ']
    
    return bowl_df.sort_values(by='pressure_score', ascending=False).reset_index(drop=True)


"""
Batter Analysis Module for SupeRR Selector Season 2
Computes individual batter metrics under pressure and normal conditions.
Evaluates strike rates, averages, boundary and dot percentages, format splits, and match consistency.
"""

import numpy as np
import pandas as pd
from scipy.stats import zscore

def analyze_batters(df, min_pressure_balls=120, min_matches=10):
    """
    Computes comprehensive batting metrics comparing pressure performance to normal baselines.
    Applies Empirical Bayes shrinkage and format weighting.
    """
    df_bf = df[df['is_ball_faced']].copy()
    
    # Population benchmarks
    press_df = df_bf[df_bf['is_high_batting_pressure']]
    norm_df = df_bf[~df_bf['is_high_batting_pressure']]
    
    pop_press_sr = (press_df['runs'].sum() / press_df['is_ball_faced'].sum()) * 100.0
    pop_norm_sr = (norm_df['runs'].sum() / norm_df['is_ball_faced'].sum()) * 100.0
    pop_press_avg = press_df['runs'].sum() / max(1, press_df['is_wicket'].sum())
    pop_press_bnd = ((press_df['is_four'].sum() + press_df['is_six'].sum()) / press_df['is_ball_faced'].sum()) * 100.0
    pop_press_dot = ((press_df['runs'] == 0).sum() / press_df['is_ball_faced'].sum()) * 100.0

    bat_records = []
    
    for (pid, pname), group in df_bf.groupby(['striker_id', 'striker_name']):
        p_grp = group[group['is_high_batting_pressure']]
        n_grp = group[~group['is_high_batting_pressure']]
        
        p_balls = int(p_grp['is_ball_faced'].sum())
        p_matches = int(p_grp['match_id'].nunique())
        
        # Eligibility filter
        if p_balls < min_pressure_balls or p_matches < min_matches:
            continue
            
        n_balls = int(n_grp['is_ball_faced'].sum())
        tot_matches = int(group['match_id'].nunique())
        
        p_runs = int(p_grp['runs'].sum())
        p_outs = int(p_grp['is_wicket'].sum())
        p_fours = int(p_grp['is_four'].sum())
        p_sixes = int(p_grp['is_six'].sum())
        p_dots = int((p_grp['runs'] == 0).sum())
        
        n_runs = int(n_grp['runs'].sum())
        n_outs = int(n_grp['is_wicket'].sum())
        n_fours = int(n_grp['is_four'].sum())
        n_sixes = int(n_grp['is_six'].sum())
        n_dots = int((n_grp['runs'] == 0).sum())
        
        p_sr = (p_runs / p_balls) * 100.0
        n_sr = (n_runs / n_balls * 100.0) if n_balls > 0 else pop_norm_sr
        delta_sr = p_sr - n_sr
        
        p_avg = (p_runs / max(1, p_outs))
        n_avg = (n_runs / max(1, n_outs)) if n_balls > 0 else 25.0
        delta_avg = p_avg - n_avg
        
        p_bnd_pct = ((p_fours + p_sixes) / p_balls) * 100.0
        n_bnd_pct = ((n_fours + n_sixes) / max(1, n_balls)) * 100.0
        
        p_dot_pct = (p_dots / p_balls) * 100.0
        n_dot_pct = (n_dots / max(1, n_balls)) * 100.0
        
        p_rpb = p_runs / p_balls
        n_rpb = (n_runs / n_balls) if n_balls > 0 else (pop_norm_sr / 100.0)
        
        # Phase performance under pressure
        death_p = p_grp[p_grp['phase'] == 'Death']
        mid_p = p_grp[p_grp['phase'] == 'Middle']
        pp_p = p_grp[p_grp['phase'] == 'Powerplay']
        
        death_sr = (death_p['runs'].sum() / death_p['is_ball_faced'].sum() * 100.0) if len(death_p) > 0 else p_sr
        mid_sr = (mid_p['runs'].sum() / mid_p['is_ball_faced'].sum() * 100.0) if len(mid_p) > 0 else p_sr
        pp_sr = (pp_p['runs'].sum() / pp_p['is_ball_faced'].sum() * 100.0) if len(pp_p) > 0 else p_sr
        
        # Format splits
        ipl_p = p_grp[p_grp['is_ipl']]
        t20i_p = p_grp[p_grp['is_t20i']]
        
        ipl_balls = int(ipl_p['is_ball_faced'].sum())
        ipl_runs = int(ipl_p['runs'].sum())
        ipl_sr = (ipl_runs / ipl_balls * 100.0) if ipl_balls > 0 else np.nan
        
        t20i_balls = int(t20i_p['is_ball_faced'].sum())
        t20i_runs = int(t20i_p['runs'].sum())
        t20i_sr = (t20i_runs / t20i_balls * 100.0) if t20i_balls > 0 else np.nan
        
        # Match-to-match consistency:
        # Proportion of pressure innings where batter made a positive impact (SR >= 135 or runs >= 15 with SR >= 120)
        match_impacts = []
        for mid, mgrp in p_grp.groupby('match_id'):
            m_r = mgrp['runs'].sum()
            m_bf = mgrp['is_ball_faced'].sum()
            m_sr = (m_r / m_bf * 100.0) if m_bf > 0 else 0.0
            match_impacts.append(1 if (m_sr >= 135.0 or (m_r >= 15 and m_sr >= 120.0)) else 0)
        consistency = float(np.mean(match_impacts)) if match_impacts else 0.5
        
        # Empirical Bayes Shrinkage for pressure SR (K = 40 balls)
        K_bat = 40.0
        shrinkage_weight = p_balls / (p_balls + K_bat)
        shrunk_sr = shrinkage_weight * p_sr + (1.0 - shrinkage_weight) * pop_press_sr
        shrunk_delta_sr = shrinkage_weight * delta_sr
        
        bat_records.append({
            'player_id': pid,
            'player_name': pname,
            'pressure_balls': p_balls,
            'pressure_runs': p_runs,
            'pressure_outs': p_outs,
            'pressure_sr': round(p_sr, 2),
            'normal_sr': round(n_sr, 2),
            'delta_sr': round(delta_sr, 2),
            'shrunk_sr': round(shrunk_sr, 2),
            'shrunk_delta_sr': round(shrunk_delta_sr, 2),
            'pressure_avg': round(p_avg, 2),
            'normal_avg': round(n_avg, 2),
            'delta_avg': round(delta_avg, 2),
            'pressure_bnd_pct': round(p_bnd_pct, 2),
            'normal_bnd_pct': round(n_bnd_pct, 2),
            'pressure_dot_pct': round(p_dot_pct, 2),
            'normal_dot_pct': round(n_dot_pct, 2),
            'pressure_rpb': round(p_rpb, 3),
            'normal_rpb': round(n_rpb, 3),
            'death_sr': round(death_sr, 2),
            'middle_sr': round(mid_sr, 2),
            'powerplay_sr': round(pp_sr, 2),
            'ipl_balls': ipl_balls,
            'ipl_runs': ipl_runs,
            'ipl_sr': round(ipl_sr, 2) if not np.isnan(ipl_sr) else np.nan,
            't20i_balls': t20i_balls,
            't20i_runs': t20i_runs,
            't20i_sr': round(t20i_sr, 2) if not np.isnan(t20i_sr) else np.nan,
            'pressure_matches': p_matches,
            'total_matches': tot_matches,
            'consistency': round(consistency, 3),
            'sample_reliability': round(shrinkage_weight, 3)
        })

    bat_df = pd.DataFrame(bat_records)
    
    # Composite Reliability Rating Calculation
    # Dimensions:
    # 1. Shrunk Pressure Strike Rate (30%)
    # 2. Strike Rate Improvement over own normal baseline (25%)
    # 3. Wicket avoidance / Pressure Average (15%)
    # 4. Boundary scoring percentage (15%)
    # 5. Match-to-match consistency (10%)
    # 6. Sample size reliability weight (5%)
    z_shrunk_sr = zscore(bat_df['shrunk_sr'])
    z_delta_sr = zscore(bat_df['shrunk_delta_sr'])
    z_avg = zscore(bat_df['pressure_avg'].clip(upper=60.0))
    z_bnd = zscore(bat_df['pressure_bnd_pct'])
    z_cons = zscore(bat_df['consistency'])
    z_rel = zscore(bat_df['sample_reliability'])
    
    raw_score = (
        0.30 * z_shrunk_sr +
        0.25 * z_delta_sr +
        0.15 * z_avg +
        0.15 * z_bnd +
        0.10 * z_cons +
        0.05 * z_rel
    )
    
    # Scale to 0-100 rating
    min_s, max_s = raw_score.min(), raw_score.max()
    bat_df['pressure_score'] = (50.0 + (raw_score / max(abs(min_s), abs(max_s))) * 45.0).round(2)
    bat_df['normal_baseline'] = bat_df['normal_sr']
    
    return bat_df.sort_values(by='pressure_score', ascending=False).reset_index(drop=True)


"""
Pressure Engine Module for SupeRR Selector Season 2
Implements delivery-level statistical pressure models (0-100) for batting and bowling.
Integrates innings phase, wickets remaining, chase dynamics (RRR, runs needed), and match leverage.
"""

import numpy as np
import pandas as pd

def compute_delivery_pressure(df):
    """
    Computes delivery-level batting_pressure and bowling_pressure scores (0-100).
    Adds pressure columns and high-pressure flags to df.
    """
    b_done = df['legal_balls_before'].clip(0, 120)
    w_lost = df['wickets_before'].clip(0, 10)
    w_rem = df['wickets_remaining'].clip(0, 10)
    b_rem = df['balls_remaining'].clip(0, 120)
    phase = df['phase']
    
    # =========================================================================
    # 1. INNINGS 1: TARGET-SETTING PRESSURE
    # Par Score benchmark = 168 runs (~8.40 RPO across T20/IPL)
    # Expected score by ball b: exp_score = (b / 6) * 8.4
    # Expected wickets lost by ball b: exp_w = (b / 120) * 6.5
    # =========================================================================
    exp_score1 = (b_done / 6.0) * 8.40
    exp_w1 = (b_done / 120.0) * 6.5
    
    # A. Batting Collapse & Resource Risk [-15, +35]
    # Wickets lost ahead of expected schedule
    collapse_risk_bat = np.clip((w_lost - exp_w1) / 2.5, -1.0, 2.5) * 15.0
    
    # B. Score Deficit vs Expected Par [-15, +25]
    deficit_bat = np.clip((exp_score1 - df['score_before']) / 18.0, -1.2, 2.0) * 12.0
    
    # C. Phase Acceleration Demand [10, 30]
    phase_bat1 = np.where(phase == 'Death', 28.0, np.where(phase == 'Middle', 14.0, 10.0))
    
    # D. Late Inning Wicket Scarcity Urgency [0, 20]
    tail_urgency_bat = np.where((b_rem <= 36) & (w_rem <= 4), 18.0, 
                       np.where((b_rem <= 24) & (w_rem <= 5), 10.0, 0.0))

    inn1_bat = 22.0 + collapse_risk_bat + deficit_bat + phase_bat1 + tail_urgency_bat
    inn1_bat = np.clip(inn1_bat, 5.0, 95.0)

    # Bowler Pressure in Innings 1:
    # High when batters are accelerating in death overs, or batting team has wickets in hand
    phase_bowl1 = np.where(phase == 'Death', 32.0, np.where(phase == 'Powerplay', 18.0, 14.0))
    bat_accelerating = np.clip((df['score_before'] - exp_score1) / 18.0, -1.0, 2.0) * 12.0
    bowl_wickets_in_hand = np.clip((w_rem - 5) / 5.0, 0.0, 1.0) * 15.0 # Batters have luxury of swinging freely

    inn1_bowl = 18.0 + phase_bowl1 + bat_accelerating + bowl_wickets_in_hand
    inn1_bowl = np.clip(inn1_bowl, 5.0, 95.0)

    # =========================================================================
    # 2. INNINGS 2: CHASE PRESSURE
    # Driven by RRR, differential (RRR - CRR), balls remaining, wickets in hand, and closeness
    # =========================================================================
    rrr = df['rrr'].fillna(8.0)
    crr = df['crr'].fillna(8.0)
    runs_nd = df['runs_needed'].fillna(0.0)
    
    # A. Rate Demand Factor for Batters
    # Base rate index: RRR <= 6.0 is calm (~15 pts), 9.0 is par (~45 pts), 13.0 is steep (~75 pts), 16+ is extreme (~90 pts)
    rrr_factor_bat = np.clip((rrr - 4.0) / 9.0, 0.0, 1.8) * 45.0
    # Differential pressure: RRR pulling away from CRR
    diff_rate_bat = np.clip((rrr - crr) / 3.0, -1.0, 2.0) * 10.0
    
    # B. Wicket Scarcity for Batters
    # Wickets remaining impact
    w_factor_bat = np.where(w_rem <= 2, 25.0,
                   np.where(w_rem <= 4, 15.0,
                   np.where(w_rem <= 6, 6.0, -4.0)))

    # C. Climax Leverage (Time running out in a close finish)
    climax_bat = np.where(phase == 'Death', 15.0, np.where(phase == 'Middle', 6.0, 2.0))

    # D. Blowout Dampener (Garbage time filter)
    # Impossible chase (e.g. > 45 needed off 10 balls) or Stroll chase (e.g. < 10 needed off 35 balls with 8 wkts)
    is_chase_lost = (runs_nd > 40) & (b_rem <= 12)
    is_chase_won = (runs_nd <= 8) & (b_rem >= 24) & (w_rem >= 6)

    inn2_bat = rrr_factor_bat + diff_rate_bat + w_factor_bat + climax_bat + 8.0
    inn2_bat = np.where(is_chase_lost, 45.0, np.where(is_chase_won, 15.0, inn2_bat))
    inn2_bat = np.clip(inn2_bat, 5.0, 100.0)

    # Bowler Pressure in Innings 2:
    # Bowler is under MAXIMUM pressure when:
    # Opponent is chasing a tight target, balls remaining are few (death overs), and RRR is reachable (6.5 - 12.0)
    # One mistake (boundary or wide) can lose the match!
    # If RRR is 25+ (game already won), bowler has massive cushion -> low pressure.
    death_closeness_bowl = np.where((b_rem <= 30) & (runs_nd > 0) & (runs_nd <= 55), 35.0,
                           np.where((b_rem <= 60) & (runs_nd > 0) & (runs_nd <= 90), 20.0, 10.0))

    # Reachable rate pressure: bowler is tested when rate is tight
    rate_tension_bowl = np.where((rrr >= 7.0) & (rrr <= 11.5), 28.0,
                        np.where((rrr > 11.5) & (rrr <= 15.0), 18.0,
                        np.where(rrr < 7.0, 22.0, 8.0)))

    # Opponent wickets in hand: set batters with wickets in hand put maximum heat on bowler
    opp_wkts_bowl = np.where(w_rem >= 7, 15.0, np.where(w_rem >= 5, 8.0, -8.0))

    inn2_bowl = death_closeness_bowl + rate_tension_bowl + opp_wkts_bowl + 12.0
    inn2_bowl = np.where(is_chase_lost, 20.0, np.where(is_chase_won, 15.0, inn2_bowl))
    inn2_bowl = np.clip(inn2_bowl, 5.0, 100.0)

    # Final combined assignment
    is_inn1 = df['innings'] == 1
    df['batting_pressure'] = np.where(is_inn1, inn1_bat, inn2_bat).round(2)
    df['bowling_pressure'] = np.where(is_inn1, inn1_bowl, inn2_bowl).round(2)

    # Primary High Pressure Flag (threshold >= 60.0)
    df['is_high_batting_pressure'] = df['batting_pressure'] >= 60.0
    df['is_high_bowling_pressure'] = df['bowling_pressure'] >= 60.0

    return df


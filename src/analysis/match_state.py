"""
Match State Module for SupeRR Selector Season 2
Computes delivery-level cumulative game states prior to each ball bowled.
Handles innings progression, allocated overs, revised targets, CRR, RRR, and match phases.
"""

import pandas as pd
import numpy as np

def compute_match_states(df):
    """
    Computes exact pre-delivery match states for every delivery in df.
    """
    df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

    # Group by match and innings for cumulative tracking
    grouped = df.groupby(['match_id', 'innings'])
    
    # Cumulative states strictly BEFORE current delivery
    df['score_before'] = grouped['total_delivery_runs'].cumsum() - df['total_delivery_runs']
    df['wickets_before'] = grouped['is_dismissal'].cumsum() - df['is_dismissal']
    df['legal_balls_before'] = grouped['is_legal_ball'].cumsum() - df['is_legal_ball']
    df['wickets_remaining'] = 10 - df['wickets_before']

    # Total balls allocated per innings
    # Matches may have revised overs in balls (e.g. 90, 48, 30); default is 120 balls (20 overs)
    df['total_balls_allocated'] = 120
    df.loc[(df['innings'] == 1) & df['first_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['first_inn_revised_overs']
    df.loc[(df['innings'] == 2) & df['second_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['second_inn_revised_overs']

    # Balls remaining in innings
    df['balls_remaining'] = np.maximum(0, df['total_balls_allocated'] - df['legal_balls_before'])

    # Innings Phase (standard T20 / adjusted for shortened):
    # Standard: Powerplay (overs 1-6: < 36 balls), Middle (overs 7-15: 36-89 balls), Death (overs 16-20: >= 90 balls)
    df['phase'] = 'Middle'
    df.loc[df['legal_balls_before'] < 36, 'phase'] = 'Powerplay'
    df.loc[df['legal_balls_before'] >= 90, 'phase'] = 'Death'

    # Current Run Rate (CRR)
    df['crr'] = np.where(
        df['legal_balls_before'] > 0,
        (df['score_before'] / df['legal_balls_before']) * 6.0,
        8.0  # prior default par rate before first legal delivery
    )

    # Innings 2 Chase Target & RRR
    # Target = revised_target if present, else inn1_actual_total + 1
    df['target'] = np.nan
    cond_inn2 = df['innings'] == 2
    df.loc[cond_inn2, 'target'] = np.where(
        df.loc[cond_inn2, 'revised_target'].notna(),
        df.loc[cond_inn2, 'revised_target'],
        df.loc[cond_inn2, 'inn1_actual_total'] + 1
    )

    df['runs_needed'] = np.nan
    df.loc[cond_inn2, 'runs_needed'] = np.maximum(0, df.loc[cond_inn2, 'target'] - df.loc[cond_inn2, 'score_before'])

    # Required Run Rate (RRR)
    df['rrr'] = np.nan
    df.loc[cond_inn2, 'rrr'] = np.where(
        df.loc[cond_inn2, 'balls_remaining'] > 0,
        (df.loc[cond_inn2, 'runs_needed'] / df.loc[cond_inn2, 'balls_remaining']) * 6.0,
        np.where(df.loc[cond_inn2, 'runs_needed'] > 0, 36.0, 0.0)
    )

    return df


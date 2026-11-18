"""
Data Cleaner Module for SupeRR Selector Season 2
Cleans, normalizes, and filters raw ball-by-ball and match records.
Excludes super overs, computes legal delivery flags, formats bowler runs and bowler wickets.
"""

import pandas as pd
import numpy as np

def clean_data(datasets):
    """
    Cleans datasets and prepares delivery-level DataFrame.
    """
    matches = datasets['matches'].copy()
    bbb = datasets['bbb'].copy()
    comps = datasets['competitions'].copy()
    ctpm = datasets['ctpm'].copy()

    # 1. Exclude super overs (innings >= 3)
    df = bbb[bbb['innings'].isin([1, 2])].copy()
    df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

    # 2. Delivery type classification
    is_wide = df['extras_type'] == 'wide'
    is_noball = df['extras_type'].isin(['Overstep', 'other'])
    is_penalty = df['extras_type'] == 'Penalty'
    
    df['is_legal_ball'] = ~(is_wide | is_noball | is_penalty)
    df['is_ball_faced'] = ~(is_wide | is_penalty)
    
    # 3. Runs definitions
    # Batter runs: runs directly off bat
    df['batter_runs'] = df['runs']
    # Total runs for team score:
    df['total_delivery_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']
    
    # Bowler runs conceded:
    # Wides: runs + extras1_runs + extras_2_runs
    # No-balls: runs + extras1_runs (extras_2_runs are byes/leg-byes on no-ball)
    # Normal: runs
    # Byes / Leg-byes / Penalty: 0
    df['bowler_runs'] = 0
    df.loc[is_wide, 'bowler_runs'] = df.loc[is_wide, 'runs'] + df.loc[is_wide, 'extras1_runs'] + df.loc[is_wide, 'extras_2_runs']
    df.loc[is_noball, 'bowler_runs'] = df.loc[is_noball, 'runs'] + df.loc[is_noball, 'extras1_runs']
    df.loc[df['extras_type'].isna(), 'bowler_runs'] = df.loc[df['extras_type'].isna(), 'runs']

    # 4. Wicket classification:
    # Bowler-credited wickets: Caught, Bowled, LBW, Stump, Hit Wicket
    # Non-bowler: RunOut, Retire Out, Obstructing the field
    df['is_bowler_wicket'] = df['dismissal_type'].isin(['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket'])
    df['is_dismissal'] = df['is_wicket'].fillna(False).astype(bool)

    # 5. Dot balls & Boundaries
    df['is_dot_ball_batter'] = df['is_ball_faced'] & (df['batter_runs'] == 0)
    df['is_dot_ball_bowler'] = df['is_legal_ball'] & (df['bowler_runs'] == 0)
    df['is_boundary'] = df['is_four'] | df['is_six']

    # 6. Merge competition and match context
    comp_map = comps[['comp_id', 'comp_name', 'match_format', 'season']].copy()
    matches = matches.merge(comp_map, on='comp_id', how='left')
    
    # Calculate Innings 1 actual total runs
    inn1_totals = df[df['innings'] == 1].groupby('match_id')['total_delivery_runs'].sum().rename('inn1_actual_total')
    matches = matches.merge(inn1_totals, on='match_id', how='left')

    # Merge match info into delivery DataFrame
    match_cols = [
        'match_id', 'comp_id', 'comp_name', 'match_format', 'season', 'match_date',
        'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target',
        'home_team_id', 'away_team_id', 'win_team_id', 'inn1_actual_total'
    ]
    df = df.merge(matches[match_cols], on='match_id', how='left')

    # Standardize competition grouping: IPL vs T20I vs Other T20
    df['is_ipl'] = df['comp_name'].str.contains('IPL', case=False, na=False)
    df['is_t20i'] = df['match_format'] == 'T20I'

    return df, matches


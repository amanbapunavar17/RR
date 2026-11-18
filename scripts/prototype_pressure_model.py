import pandas as pd
import numpy as np

def compute_match_states_and_pressure(bbb_path='Data Pack/ball_by_ball.csv', matches_path='Data Pack/matches.csv'):
    matches = pd.read_csv(matches_path)
    bbb = pd.read_csv(bbb_path)

    # Exclude super overs
    df = bbb[bbb['innings'].isin([1, 2])].copy()
    df = df.sort_values(by=['match_id', 'innings', 'overid', 'over_ball_num']).reset_index(drop=True)

    # Delivery flags
    is_wide = df['extras_type'] == 'wide'
    is_noball = df['extras_type'].isin(['Overstep', 'other'])
    is_penalty = df['extras_type'] == 'Penalty'
    df['is_legal_ball'] = ~(is_wide | is_noball | is_penalty)
    df['is_ball_faced'] = ~(is_wide | is_penalty)
    df['total_delivery_runs'] = df['runs'] + df['extras1_runs'] + df['extras_2_runs']

    # Bowler runs
    df['bowler_runs'] = 0
    mask_wide = is_wide
    mask_nb = is_noball
    mask_normal = df['extras_type'].isna()
    df.loc[mask_wide, 'bowler_runs'] = df.loc[mask_wide, 'runs'] + df.loc[mask_wide, 'extras1_runs'] + df.loc[mask_wide, 'extras_2_runs']
    df.loc[mask_nb, 'bowler_runs'] = df.loc[mask_nb, 'runs'] + df.loc[mask_nb, 'extras1_runs']
    df.loc[mask_normal, 'bowler_runs'] = df.loc[mask_normal, 'runs']

    # Bowler wicket: Caught, Bowled, LBW, Stump, Hit Wicket
    df['is_bowler_wicket'] = df['dismissal_type'].isin(['Caught', 'Bowled', 'LBW', 'Stump', 'Hit Wicket'])

    # Cumulative match state BEFORE delivery
    grouped = df.groupby(['match_id', 'innings'])
    df['score_before'] = grouped['total_delivery_runs'].cumsum() - df['total_delivery_runs']
    df['wickets_before'] = grouped['is_wicket'].cumsum() - df['is_wicket']
    df['legal_balls_before'] = grouped['is_legal_ball'].cumsum() - df['is_legal_ball']
    df['wickets_remaining'] = 10 - df['wickets_before']

    # Innings totals
    inn_totals = df.groupby(['match_id', 'innings'])['total_delivery_runs'].sum().unstack(level='innings')
    inn1_actual = inn_totals[1].rename('inn1_actual_total')

    matches_info = matches[['match_id', 'comp_id', 'match_date', 'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target', 'win_team_id']].copy()
    matches_info = matches_info.merge(inn1_actual, on='match_id', how='left')

    df = df.merge(matches_info, on='match_id', how='left')

    # Total balls allocated
    df['total_balls_allocated'] = 120
    df.loc[(df['innings'] == 1) & df['first_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['first_inn_revised_overs']
    df.loc[(df['innings'] == 2) & df['second_inn_revised_overs'].notna(), 'total_balls_allocated'] = df['second_inn_revised_overs']

    df['balls_remaining'] = np.maximum(0, df['total_balls_allocated'] - df['legal_balls_before'])

    # Innings phase:
    # Powerplay: legal_balls_before < 36 (overs 1-6)
    # Middle: 36 <= legal_balls_before < 90 (overs 7-15)
    # Death: legal_balls_before >= 90 (overs 16-20)
    df['phase'] = 'Middle'
    df.loc[df['legal_balls_before'] < 36, 'phase'] = 'Powerplay'
    df.loc[df['legal_balls_before'] >= 90, 'phase'] = 'Death'

    # Current run rate
    df['crr'] = np.where(df['legal_balls_before'] > 0, (df['score_before'] / df['legal_balls_before']) * 6.0, 8.0)

    # Innings 2 Target & RRR
    df['target'] = np.nan
    df.loc[df['innings'] == 2, 'target'] = np.where(
        df.loc[df['innings'] == 2, 'revised_target'].notna(),
        df.loc[df['innings'] == 2, 'revised_target'],
        df.loc[df['innings'] == 2, 'inn1_actual_total'] + 1
    )

    df['runs_needed'] = np.nan
    df.loc[df['innings'] == 2, 'runs_needed'] = np.maximum(0, df.loc[df['innings'] == 2, 'target'] - df.loc[df['innings'] == 2, 'score_before'])

    df['rrr'] = np.nan
    cond_inn2 = df['innings'] == 2
    df.loc[cond_inn2, 'rrr'] = np.where(
        df.loc[cond_inn2, 'balls_remaining'] > 0,
        (df.loc[cond_inn2, 'runs_needed'] / df.loc[cond_inn2, 'balls_remaining']) * 6.0,
        np.where(df.loc[cond_inn2, 'runs_needed'] > 0, 36.0, 0.0)
    )

    # ==========================================
    # PRESSURE ENGINE CALCULATION (0 - 100)
    # ==========================================
    # We compute separate batting_pressure and bowling_pressure
    
    # 1. INNINGS 1 (Setting a target)
    # Par score baseline ~ 168 (8.4 rpo)
    # Expected runs by ball b: exp_runs = (b / 120) * 168
    # If score_before < exp_runs, batting team is under pressure
    # Wickets lost factor: loss of wickets accelerates pressure
    b1 = df['legal_balls_before'].clip(0, 120)
    w_lost1 = df['wickets_before'].clip(0, 10)
    b_rem1 = df['balls_remaining'].clip(0, 120)

    # Batting pressure in Innings 1:
    # Components:
    # A. Collapse risk: wickets lost relative to balls completed
    # If 3 down in powerplay (b <= 36) -> high collapse pressure
    exp_w = (b1 / 120.0) * 7.0  # expected wickets lost
    w_pressure = np.clip((w_lost1 - exp_w) / 3.0, -1.0, 2.0) * 20.0  # [-20, 40]
    
    # B. Phase pressure: death overs demand boundary acceleration
    phase_p_bat = np.where(df['phase'] == 'Death', 30.0, np.where(df['phase'] == 'Middle', 15.0, 10.0))
    
    # C. Score deficit vs par: par rate 8.4
    exp_score = (b1 / 6.0) * 8.4
    run_deficit = np.clip((exp_score - df['score_before']) / 20.0, -1.5, 2.0) * 15.0 # [-22.5, 30]

    # D. Late innings urgency if low wickets remaining:
    late_wicket_urgency = np.where((b_rem1 <= 30) & (df['wickets_remaining'] <= 4), 20.0, 0.0)

    inn1_bat_pressure = 25.0 + phase_p_bat + w_pressure + run_deficit + late_wicket_urgency
    inn1_bat_pressure = np.clip(inn1_bat_pressure, 5.0, 95.0)

    # Bowling pressure in Innings 1:
    # Bowlers face high pressure when:
    # A. Death overs against batters (runs flow fast): phase_p_bowl
    phase_p_bowl = np.where(df['phase'] == 'Death', 35.0, np.where(df['phase'] == 'Powerplay', 20.0, 15.0))
    # B. Batting team is ahead of par with wickets in hand (batters dominant)
    bat_dominance = np.clip((df['score_before'] - exp_score) / 20.0, -1.0, 2.0) * 15.0
    w_hand_bonus = np.clip((df['wickets_remaining'] - 6) / 4.0, 0.0, 1.0) * 15.0 # more wickets in hand = harder for bowler
    
    inn1_bowl_pressure = 20.0 + phase_p_bowl + bat_dominance + w_hand_bonus
    inn1_bowl_pressure = np.clip(inn1_bowl_pressure, 5.0, 95.0)

    # 2. INNINGS 2 (The Chase)
    # Batting pressure in Innings 2:
    # Dominant factors: RRR, Wickets in hand, Closeness / Balls remaining, Blowout discount
    rrr = df['rrr'].fillna(8.0)
    runs_nd = df['runs_needed'].fillna(0.0)
    b_rem2 = df['balls_remaining'].clip(0, 120)
    w_rem2 = df['wickets_remaining'].clip(0, 10)

    # Base RRR pressure:
    # 6.0 rpo -> 15 pts, 9.0 rpo -> 45 pts, 12.0 rpo -> 75 pts, 15.0+ rpo -> 95 pts
    rrr_score = np.clip((rrr - 4.0) / 10.0, 0.0, 1.8) * 50.0  # up to 90

    # Wickets remaining pressure multiplier:
    # Fewer wickets = much more pressure
    w_mult = np.where(w_rem2 <= 2, 25.0, np.where(w_rem2 <= 4, 15.0, np.where(w_rem2 <= 6, 5.0, -5.0)))

    # Leverage / Closeness factor:
    # When balls are running out and match is tight, every ball matters
    # If blowout (e.g. 60 needed off 6 balls, win prob ~ 0.001) or (3 needed off 30 balls, win prob ~ 0.999), pressure normalizes
    is_blowout_loss = (runs_nd > 36) & (b_rem2 <= 12)
    is_blowout_win = (runs_nd <= 10) & (b_rem2 >= 30) & (w_rem2 >= 6)

    inn2_bat_pressure = rrr_score + w_mult + np.where(df['phase'] == 'Death', 15.0, 5.0)
    inn2_bat_pressure = np.where(is_blowout_loss, 45.0, np.where(is_blowout_win, 15.0, inn2_bat_pressure))
    inn2_bat_pressure = np.clip(inn2_bat_pressure, 5.0, 100.0)

    # Bowling pressure in Innings 2:
    # Bowlers face extreme pressure when:
    # Opponent is chasing a reachable target in the death overs or tight contest (RRR 7 - 11, close finish)
    # Bowlers have zero margin for error!
    # But if RRR is 25+ (batters hopeless), bowling pressure is LOW.
    # If RRR is 3 (batters walking it), match is lost, pressure is moderate/low.
    # Peak bowling pressure: Death overs (balls_rem <= 30), tight target (runs_nd between 10 and 50, RRR between 6 and 13)
    bowl_death_leverage = np.where((b_rem2 <= 30) & (runs_nd > 0) & (runs_nd <= 55), 35.0, 
                          np.where((b_rem2 <= 60) & (runs_nd > 0) & (runs_nd <= 90), 20.0, 10.0))
    
    # Margin of error pressure: if RRR is between 7 and 12, bowler is under heavy gun
    margin_pressure = np.where((rrr >= 7.0) & (rrr <= 12.0), 30.0,
                      np.where((rrr > 12.0) & (rrr <= 16.0), 20.0,
                      np.where(rrr < 7.0, 25.0, 10.0)))

    # Opponent wickets in hand:
    bowl_w_hand = np.where(w_rem2 >= 6, 15.0, np.where(w_rem2 >= 4, 5.0, -10.0))

    inn2_bowl_pressure = bowl_death_leverage + margin_pressure + bowl_w_hand + 10.0
    inn2_bowl_pressure = np.where(is_blowout_loss, 20.0, np.where(is_blowout_win, 15.0, inn2_bowl_pressure))
    inn2_bowl_pressure = np.clip(inn2_bowl_pressure, 5.0, 100.0)

    # Assign combined pressure scores
    df['batting_pressure'] = np.where(df['innings'] == 1, inn1_bat_pressure, inn2_bat_pressure)
    df['bowling_pressure'] = np.where(df['innings'] == 1, inn1_bowl_pressure, inn2_bowl_pressure)

    return df

print("Testing pressure computation...")
df_test = compute_match_states_and_pressure()
print("Batting Pressure Summary:")
print(df_test['batting_pressure'].describe())
print("\nBowling Pressure Summary:")
print(df_test['bowling_pressure'].describe())

print("\nBatting Pressure by Phase:")
print(df_test.groupby('phase')['batting_pressure'].mean())

print("\nBowling Pressure by Phase:")
print(df_test.groupby('phase')['bowling_pressure'].mean())

print("\nBatting Pressure by Innings:")
print(df_test.groupby('innings')['batting_pressure'].mean())

print("\nBowling Pressure by Innings:")
print(df_test.groupby('innings')['bowling_pressure'].mean())

# Distribution across pressure bands
print("\nBatting deliveries by pressure tier:")
print(pd.cut(df_test['batting_pressure'], bins=[0, 40, 60, 75, 100], labels=['Low (<40)', 'Moderate (40-60)', 'High (60-75)', 'Extreme (75+)']).value_counts(normalize=True))

print("\nBowling deliveries by pressure tier:")
print(pd.cut(df_test['bowling_pressure'], bins=[0, 40, 60, 75, 100], labels=['Low (<40)', 'Moderate (40-60)', 'High (60-75)', 'Extreme (75+)']).value_counts(normalize=True))


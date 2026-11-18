import pandas as pd

df_p = pd.read_csv('d:/RR/outputs/pressure_delivery_analysis.csv')
df_b = pd.read_csv('d:/RR/Data Pack/ball_by_ball.csv', usecols=['match_id', 'innings', 'overid', 'over_ball_num', 'bowler_id'])
df = pd.merge(df_p, df_b, on=['match_id', 'innings', 'overid', 'over_ball_num'], how='inner')

pat = df[df['bowler_name'].str.contains('Pathirana', case=False, na=False)]
print("Pathirana in dataset:")
print(pat[['bowler_id', 'bowler_name']].drop_duplicates())

if not pat.empty:
    pid = pat['bowler_id'].iloc[0]
    pname = pat['bowler_name'].iloc[0]
    print(f"\nTotal deliveries in dataset for {pname} (ID {pid}): {len(pat)}")

    p75_bowl = 68.90
    pat_press = pat[pat['bowling_pressure'] >= p75_bowl]
    pat_norm = pat[pat['bowling_pressure'] < p75_bowl]

    p_balls = len(pat_press)
    n_balls = len(pat_norm)
    p_runs = pat_press['bowler_runs'].sum()
    n_runs = pat_norm['bowler_runs'].sum()
    p_wkts = pat_press['is_bowler_wicket'].sum()
    n_wkts = pat_norm['is_bowler_wicket'].sum()

    p_econ = (p_runs / p_balls * 6.0) if p_balls > 0 else 0.0
    n_econ = (n_runs / n_balls * 6.0) if n_balls > 0 else 0.0
    delta_econ = p_econ - n_econ

    print(f"Pressure deliveries (P >= 68.90): {p_balls}")
    print(f"Pressure runs: {p_runs}, wickets: {p_wkts}, economy: {p_econ:.2f}")
    print(f"Baseline deliveries: {n_balls}, runs: {n_runs}, wickets: {n_wkts}, economy: {n_econ:.2f}")
    print(f"Delta Economy: {delta_econ:+.2f}")
    print(f"Unique matches (pressure): {pat_press['match_id'].nunique()}")
    print("\nCompetitions breakdown (pressure):")
    print(pat_press['comp_name'].value_counts())
    print("\nPhase breakdown (pressure):")
    print(pat_press['phase'].value_counts())
    print("\nOverall deliveries phase breakdown:")
    print(pat['phase'].value_counts())

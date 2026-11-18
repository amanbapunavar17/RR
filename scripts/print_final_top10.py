import pandas as pd

df_b = pd.read_csv('d:/RR/Data Pack/ball_by_ball.csv')
df_p = pd.read_csv('d:/RR/outputs/pressure_delivery_analysis.csv')
df = pd.merge(df_p, df_b[['match_id', 'innings', 'overid', 'over_ball_num', 'striker_id', 'bowler_id', 'extras_type']], 
              on=['match_id', 'innings', 'overid', 'over_ball_num'], how='inner')

is_wide = df['extras_type'] == 'wide'
is_nb = df['extras_type'].isin(['Overstep', 'other'])
df['is_legal_ball'] = ~(is_wide | is_nb)

p75_bat = 55.20
p75_bowl = 68.90

df_ppr = pd.read_csv('d:/RR/outputs/final_pressure_performance_ranking.csv')

def get_matches(pid, disc):
    if disc == 'Batting':
        sub = df[(df['striker_id'] == pid) & (df['batting_pressure'] >= p75_bat)]
    else:
        sub = df[(df['bowler_id'] == pid) & (df['bowling_pressure'] >= p75_bowl)]
    return sub['match_id'].nunique()

df_ppr['matches'] = [get_matches(r['player_id'], r['discipline']) for _, r in df_ppr.iterrows()]

print("=== TOP 10 OVERALL BATTERS (PURE PPR) ===")
top_bat = df_ppr[df_ppr['discipline'] == 'Batting'].sort_values(by=['ppr_score', 'sample_balls'], ascending=[False, False]).head(10)
for idx, (_, r) in enumerate(top_bat.iterrows(), 1):
    print(f"{idx} | {r['player_name']} | {r['player_id']} | {r['capped_status']} | {int(r['runs_or_wkts'])} | {int(r['sample_balls'])} | {r['pressure_sr_or_econ']:.2f} | {r['baseline_sr_or_econ']:.2f} | {r['delta_lift']:+.2f} | {r['matches']} | {r['ppr_score']:.2f}")

print("\n=== TOP 10 OVERALL BOWLERS (PURE PPR) ===")
top_bowl = df_ppr[df_ppr['discipline'] == 'Bowling'].sort_values(by=['ppr_score', 'sample_balls'], ascending=[False, False]).head(10)
for idx, (_, r) in enumerate(top_bowl.iterrows(), 1):
    print(f"{idx} | {r['player_name']} | {r['player_id']} | {r['capped_status']} | {int(r['runs_or_wkts'])} | {int(r['sample_balls'])} | {r['pressure_sr_or_econ']:.2f} | {r['baseline_sr_or_econ']:.2f} | {r['delta_lift']:+.2f} | {r['matches']} | {r['ppr_score']:.2f}")

print("\n=== TOP 10 INDIAN BATTERS (PURE PPR) ===")
ind_bat = df_ppr[(df_ppr['discipline'] == 'Batting') & (df_ppr['classification'] == 'Indian')].sort_values(by=['ppr_score', 'sample_balls'], ascending=[False, False]).head(10)
for idx, (_, r) in enumerate(ind_bat.iterrows(), 1):
    print(f"{idx} | {r['player_name']} | {r['player_id']} | {r['capped_status']} | {int(r['runs_or_wkts'])} | {int(r['sample_balls'])} | {r['pressure_sr_or_econ']:.2f} | {r['baseline_sr_or_econ']:.2f} | {r['delta_lift']:+.2f} | {r['matches']} | {r['ppr_score']:.2f}")

print("\n=== TOP INDIAN BOWLERS (PURE PPR) ===")
ind_bowl = df_ppr[(df_ppr['discipline'] == 'Bowling') & (df_ppr['classification'] == 'Indian')].sort_values(by=['ppr_score', 'sample_balls'], ascending=[False, False])
for idx, (_, r) in enumerate(ind_bowl.iterrows(), 1):
    print(f"{idx} | {r['player_name']} | {r['player_id']} | {r['capped_status']} | {int(r['runs_or_wkts'])} | {int(r['sample_balls'])} | {r['pressure_sr_or_econ']:.2f} | {r['baseline_sr_or_econ']:.2f} | {r['delta_lift']:+.2f} | {r['matches']} | {r['ppr_score']:.2f}")

# Also print Top 10 Specialist Batters (excluding primary_role == Bowler)
print("\n=== TOP 10 SPECIALIST BATTERS & ALL-ROUNDERS (EXCLUDING PRIMARY BOWLERS) ===")
spec_bat = df_ppr[(df_ppr['discipline'] == 'Batting') & (df_ppr['primary_role'] != 'Bowler')].sort_values(by=['ppr_score', 'sample_balls'], ascending=[False, False]).head(10)
for idx, (_, r) in enumerate(spec_bat.iterrows(), 1):
    print(f"{idx} | {r['player_name']} | {r['player_id']} | {r['capped_status']} | {int(r['runs_or_wkts'])} | {int(r['sample_balls'])} | {r['pressure_sr_or_econ']:.2f} | {r['baseline_sr_or_econ']:.2f} | {r['delta_lift']:+.2f} | {r['matches']} | {r['ppr_score']:.2f}")

print("\n=== TOP 10 INDIAN SPECIALIST BATTERS & ALL-ROUNDERS (EXCLUDING PRIMARY BOWLERS) ===")
ind_spec_bat = df_ppr[(df_ppr['discipline'] == 'Batting') & (df_ppr['classification'] == 'Indian') & (df_ppr['primary_role'] != 'Bowler')].sort_values(by=['ppr_score', 'sample_balls'], ascending=[False, False]).head(10)
for idx, (_, r) in enumerate(ind_spec_bat.iterrows(), 1):
    print(f"{idx} | {r['player_name']} | {r['player_id']} | {r['capped_status']} | {int(r['runs_or_wkts'])} | {int(r['sample_balls'])} | {r['pressure_sr_or_econ']:.2f} | {r['baseline_sr_or_econ']:.2f} | {r['delta_lift']:+.2f} | {r['matches']} | {r['ppr_score']:.2f}")


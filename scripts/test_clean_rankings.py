import pandas as pd
pool = pd.read_csv('d:/RR/outputs/official_ipl_2027_released_player_pool.csv')
active = pool[pool['active_status'] == 'Active'].copy()

# Batters:
batters = active[
    (active['primary_role'].isin(['Batter', 'Wicketkeeper-Batter'])) |
    ((active['primary_role'] == 'All-Rounder') & (active['press_bat_balls'] > 0))
].sort_values(by=['caps', 'pps'], ascending=False).head(10)

# Bowlers:
bowlers = active[
    (active['primary_role'] == 'Bowler') |
    ((active['primary_role'] == 'All-Rounder') & (active['press_bowl_balls'] > 0))
].sort_values(by=['caps', 'pps'], ascending=False).head(10)

print('--- REFINED TOP 10 BATTERS ---')
for idx, r in batters.reset_index(drop=True).iterrows():
    print(f"{idx+1}. {r['player_name']} ({r['classification']}, {r['capped_status']}) - {r['last_franchise']} | Press SR: {r['press_bat_sr']} | Delta: {r['delta_bat_sr']:+0.2f} | PPS: {r['pps']} | AOS: {r['aos']} | CAPS: {r['caps']}")

print('\n--- REFINED TOP 10 BOWLERS ---')
for idx, r in bowlers.reset_index(drop=True).iterrows():
    print(f"{idx+1}. {r['player_name']} ({r['classification']}, {r['capped_status']}) - {r['last_franchise']} | Press Econ: {r['press_bowl_econ']} | Delta: {r['delta_bowl_econ']:+0.2f} | PPS: {r['pps']} | AOS: {r['aos']} | CAPS: {r['caps']}")


import pandas as pd
import numpy as np

# Load pool
pool = pd.read_csv('d:/RR/outputs/official_ipl_2027_released_player_pool.csv')
active = pool[pool['active_status'] == 'Active'].copy()

# Inspect all bowlers sorted purely by pure PPS_bowl
print("--- ALL BOWLERS SORTED BY PURE PPS_BOWL ---")
bowlers = active[active['press_bowl_balls'] >= 15].sort_values(by='pps_bowl', ascending=False)
for idx, r in bowlers.reset_index(drop=True).iterrows():
    print(f"{idx+1}. {r['player_name']} ({r['classification']}, {r['capped_status']}) | {r['last_franchise']} | {r['press_bowl_balls']} balls, {r['press_bowl_wkts']} wkts, {r['press_bowl_econ']} Econ (Delta: {r['delta_bowl_econ']:+0.2f}) | PPS: {r['pps_bowl']:.2f} | AOS: {r['aos']:.2f}")

print("\n--- ALL BATTERS SORTED BY PURE PPS_BAT ---")
batters = active[active['press_bat_balls'] >= 25].sort_values(by='pps_bat', ascending=False)
for idx, r in batters.reset_index(drop=True).iterrows():
    print(f"{idx+1}. {r['player_name']} ({r['classification']}, {r['capped_status']}) | {r['last_franchise']} | {r['press_bat_balls']} balls, {r['press_bat_runs']} runs, {r['press_bat_sr']} SR (Delta: {r['delta_bat_sr']:+0.2f}) | PPS: {r['pps_bat']:.2f} | AOS: {r['aos']:.2f}")


import pandas as pd
hgb = pd.read_csv('d:/RR/outputs/rr_hidden_gem_batters.csv')
hgbowl = pd.read_csv('d:/RR/outputs/rr_hidden_gem_bowlers.csv')

print("HG BATTERS:")
for idx, r in hgb.head(5).iterrows():
    print(f"| **{r['rank']}** | **{r['player_name']}** | `{r['player_id']}` | {r['last_franchise']} | {r['press_bat_balls']} balls | {r['press_bat_sr']:.2f} SR | {r['delta_bat_sr']:+.2f} | {r['pps']:.2f} | {r['aos']:.2f} | **{r['caps']:.2f}** |")

print("\nHG BOWLERS:")
for idx, r in hgbowl.head(5).iterrows():
    print(f"| **{r['rank']}** | **{r['player_name']}** | `{r['player_id']}` | {r['last_franchise']} | {r['press_bowl_balls']} balls | {r['press_bowl_econ']:.2f} Econ | {r['delta_bowl_econ']:+.2f} | {r['pps']:.2f} | {r['aos']:.2f} | **{r['caps']:.2f}** |")


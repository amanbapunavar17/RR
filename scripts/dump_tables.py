import pandas as pd
bat = pd.read_csv('d:/RR/outputs/rr_auction_eligible_batters.csv')
bowl = pd.read_csv('d:/RR/outputs/rr_auction_eligible_bowlers.csv')
short = pd.read_csv('d:/RR/outputs/rr_final_auction_shortlist.csv')

print("BATTERS:")
for idx, r in bat.iterrows():
    print(f"| **{r['rank']}** | **{r['player_name']}** | `{r['player_id']}` | {r['classification']} ({r['capped_status']}) | {r['last_franchise']} | {r['press_bat_sr']:.2f} | {r['delta_bat_sr']:+.2f} | {r['pps']:.2f} | {r['aos']:.2f} | **{r['caps']:.2f}** |")

print("\nBOWLERS:")
for idx, r in bowl.iterrows():
    print(f"| **{r['rank']}** | **{r['player_name']}** | `{r['player_id']}` | {r['classification']} ({r['capped_status']}) | {r['last_franchise']} | {r['press_bowl_econ']:.2f} | {r['delta_bowl_econ']:+.2f} | {r['pps']:.2f} | {r['aos']:.2f} | **{r['caps']:.2f}** |")


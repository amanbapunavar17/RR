import pandas as pd
df = pd.read_csv('d:/RR/outputs/final_rr_strategic_shortlist.csv')
for idx, r in df.iterrows():
    print(f"| **{r['strategic_rank']}** | **{r['player_name']}** | `{r['player_id']}` | {r['classification']} ({r['capped_status']}) | {r['last_franchise']} | {r['ppr_raw']:.2f} | {r['ppr_norm']:.2f} | {r['aor']:.2f} | **{r['srr']:.2f}** | {r['rr_priority_alignment']} |")


import pandas as pd
hg = pd.read_csv('d:/RR/outputs/final_hidden_gems.csv')
print("=== FINAL HIDDEN GEMS ===")
for idx, r in hg.iterrows():
    print(f"| **{r['gem_rank']}** | **{r['player_name']}** | `{r['player_id']}` | {r['classification']} | {r['capped_status']} | Raw PPR: {r['ppr_raw']:.2f} | Norm PPR: {r['ppr_norm']:.2f} | AOR: {r['aor']:.2f} | **SRR: {r['srr']:.2f}** |")


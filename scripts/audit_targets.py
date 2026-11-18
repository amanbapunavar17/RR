import pandas as pd
import numpy as np

matches = pd.read_csv('Data Pack/matches.csv')
bbb = pd.read_csv('Data Pack/ball_by_ball.csv')

# Look at revised target matches
dls_matches = matches[matches['revised_target'].notna()]
print(f"Number of matches with revised_target: {len(dls_matches)}")
print(dls_matches[['match_id', 'match_date', 'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target', 'result']].head(15))

# Check 1st innings total vs 2nd innings target
inn_totals = bbb[bbb['innings'] <= 2].groupby(['match_id', 'innings'])[['runs', 'extras1_runs', 'extras_2_runs']].sum()
inn_totals['total_runs'] = inn_totals['runs'] + inn_totals['extras1_runs'] + inn_totals['extras_2_runs']
print("\nSample innings totals:")
print(inn_totals.head(10))

# Check matches where 2nd innings exists
inn1_totals = inn_totals.xs(1, level='innings')['total_runs']
# Merge with matches
m_merged = matches.set_index('match_id').join(inn1_totals.rename('inn1_actual_total'))
print("\nSample comparison of inn1_actual_total vs revised_target:")
print(m_merged[m_merged['revised_target'].notna()][['match_date', 'inn1_actual_total', 'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target', 'result']].head(10))


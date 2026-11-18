"""
scripts/inspect_vignesh_puthur.py
Analyzes every delivery bowled by Vignesh Puthur (player_id: 48557),
separating total IPL balls/wickets from high-pressure deliveries/wickets.
"""

import os
import pandas as pd
import numpy as np

# Load bbb and run the approved pressure engine
import sys
sys.path.append(".")
from scripts.generate_final_verification_dossier import df, p75_bowl

vp = df[df['bowler_id'] == 48557].copy()
print(f"Total deliveries bowled by Vignesh Puthur: {len(vp)}")
vp_legal = vp[vp['is_legal_ball']]
print(f"Total legal balls: {len(vp_legal)}")
print(f"Total runs conceded: {vp['bowler_runs'].sum()}")
print(f"Total wickets taken: {vp['is_bowler_wicket'].sum()}")
print(f"Total overall economy: {(vp['bowler_runs'].sum() / len(vp_legal)) * 6.0:.2f}")

vp_press = vp[vp['bowling_pressure_final'] >= p75_bowl]
print(f"\n--- PRESSURE DELIVERIES (Pressure >= {p75_bowl:.2f}) ---")
print(f"Total pressure balls: {len(vp_press)}")
print(f"Pressure legal balls: {len(vp_press[vp_press['is_legal_ball']])}")
print(f"Pressure runs conceded: {vp_press['bowler_runs'].sum()}")
print(f"Pressure wickets: {vp_press['is_bowler_wicket'].sum()}")
if len(vp_press[vp_press['is_legal_ball']]) > 0:
    print(f"Pressure economy: {(vp_press['bowler_runs'].sum() / len(vp_press[vp_press['is_legal_ball']])) * 6.0:.2f}")

print("\nDetail of all Vignesh Puthur pressure deliveries:")
print(vp_press[['match_id', 'innings', 'overid', 'over_ball_num', 'score_before', 'runs_needed', 'rrr', 'bowling_pressure_final', 'bowler_runs', 'is_bowler_wicket', 'dismissal_type']].to_string())


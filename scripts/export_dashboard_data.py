"""
scripts/export_dashboard_data.py
Exports all certified, frozen analytics datasets into JSON format
for the live interactive Rajasthan Royals IPL 2027 Dashboard.
"""

import os
import json
import pandas as pd
import numpy as np

OUTPUTS_DIR = 'd:/RR/outputs'
DATA_DIR = 'd:/RR/dashboard/public/data'
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Load data
pool = pd.read_csv(f'{OUTPUTS_DIR}/official_ipl_2027_released_player_pool.csv')
ppr = pd.read_csv(f'{OUTPUTS_DIR}/final_pressure_performance_ranking.csv')
aor = pd.read_csv(f'{OUTPUTS_DIR}/final_auction_opportunity_ranking.csv')
srr = pd.read_csv(f'{OUTPUTS_DIR}/final_rr_strategic_shortlist.csv')
hg = pd.read_csv(f'{OUTPUTS_DIR}/final_hidden_gems.csv')
scen = pd.read_csv(f'{OUTPUTS_DIR}/final_six_player_scenarios.csv')

# Load match-level delivery stats for match counts
df_b = pd.read_csv('d:/RR/Data Pack/ball_by_ball.csv')
df_p = pd.read_csv('d:/RR/outputs/pressure_delivery_analysis.csv')
df = pd.merge(df_p, df_b[['match_id', 'innings', 'overid', 'over_ball_num', 'striker_id', 'bowler_id', 'extras_type']], 
              on=['match_id', 'innings', 'overid', 'over_ball_num'], how='inner')

is_wide = df['extras_type'] == 'wide'
is_nb = df['extras_type'].isin(['Overstep', 'other'])
df['is_legal_ball'] = ~(is_wide | is_nb)

p75_bat = 55.20
p75_bowl = 68.90

def get_matches(pid, disc):
    if disc == 'Batting':
        sub = df[(df['striker_id'] == pid) & (df['batting_pressure'] >= p75_bat)]
    else:
        sub = df[(df['bowler_id'] == pid) & (df['bowling_pressure'] >= p75_bowl)]
    return int(sub['match_id'].nunique())

ppr['matches'] = [get_matches(r['player_id'], r['discipline']) for _, r in ppr.iterrows()]

# Batters & Bowlers
batters = ppr[ppr['discipline'] == 'Batting'].sort_values(by=['ppr_score', 'sample_balls'], ascending=[False, False]).to_dict(orient='records')
bowlers = ppr[ppr['discipline'] == 'Bowling'].sort_values(by=['ppr_score', 'sample_balls'], ascending=[False, False]).to_dict(orient='records')

# 2. RR Retained Squad
retained_squad = [
    {"name": "Riyan Parag", "role": "Captain & Middle Batter", "nationality": "Indian", "type": "Retained", "category": "Core"},
    {"name": "Yashasvi Jaiswal", "role": "Top-Order Opener", "nationality": "Indian", "type": "Retained", "category": "Core"},
    {"name": "Vaibhav Sooryavanshi", "role": "Top-Order Batter", "nationality": "Indian", "type": "Retained", "category": "Emerging"},
    {"name": "Dhruv Jurel", "role": "Wicketkeeper-Batter", "nationality": "Indian", "type": "Retained", "category": "Core"},
    {"name": "Ravindra Jadeja", "role": "All-Rounder (LA Spin)", "nationality": "Indian", "type": "Retained", "category": "Core"},
    {"name": "Jofra Archer", "role": "Fast Bowler", "nationality": "Overseas", "type": "Retained", "category": "Pace"},
    {"name": "Mohammed Shami", "role": "Fast-Medium Bowler", "nationality": "Indian", "type": "Traded in from LSG", "category": "Pace"},
    {"name": "Sandeep Sharma", "role": "Pace Bowler / Death Specialist", "nationality": "Indian", "type": "Retained", "category": "Pace"},
    {"name": "Ravi Bishnoi", "role": "Leg-Spin Bowler", "nationality": "Indian", "type": "Retained", "category": "Spin"},
    {"name": "Manimaran Siddharth", "role": "Left-Arm Orthodox Spinner", "nationality": "Indian", "type": "Traded in from LSG", "category": "Spin"},
    {"name": "Nandre Burger", "role": "Left-Arm Fast Bowler", "nationality": "Overseas", "type": "Retained", "category": "Pace"},
    {"name": "Dasun Shanaka", "role": "Pace-Bowling All-Rounder", "nationality": "Overseas", "type": "Retained", "category": "All-Rounder"},
    {"name": "Donovan Ferreira", "role": "Power Finisher / WK", "nationality": "Overseas", "type": "Retained", "category": "Finisher"},
    {"name": "Lhuan-dre Pretorius", "role": "Top-Order WK-Batter", "nationality": "Overseas", "type": "Retained", "category": "Emerging"},
    {"name": "Shubham Dubey", "role": "Lower-Order Finisher", "nationality": "Indian", "type": "Retained", "category": "Finisher"},
    {"name": "Brijesh Sharma", "role": "Batter", "nationality": "Indian", "type": "Retained", "category": "Bench"},
    {"name": "Aman Rao Perala", "role": "Batter", "nationality": "Indian", "type": "Retained", "category": "Bench"},
    {"name": "Sushant Mishra", "role": "Fast Bowler", "nationality": "Indian", "type": "Retained", "category": "Pace Bench"},
    {"name": "Yash Raj Punja", "role": "Pacer", "nationality": "Indian", "type": "Retained", "category": "Pace Bench"}
]

# 3. Pathirana Forensic Data
pathirana_data = {
    "player_id": 8661,
    "name": "Matheesha Pathirana",
    "role": "Marquee Overseas Death Specialist",
    "release_franchise": "Kolkata Knight Riders",
    "previous_salary_cr": 18.0,
    "total_career_deliveries": 1279,
    "pressure_deliveries": 281,
    "pressure_legal_balls": 248,
    "pressure_runs": 415,
    "pressure_wickets": 20,
    "pressure_economy": 10.04,
    "baseline_economy": 8.49,
    "delta_economy": 1.55,
    "extras_breakdown": {
        "legal_dots_and_bat_runs": 238,
        "wides": 32,
        "other_noballs": 1,
        "overstep_noballs": 0,
        "legbyes": 8,
        "byes": 2
    },
    "death_phase_pressure": {
        "deliveries": 190,
        "legal_balls": 168,
        "wides": 21,
        "noballs": 1,
        "runs": 301,
        "wickets": 15,
        "death_economy": 10.75,
        "population_benchmark_death_economy": 11.15,
        "economy_advantage": -0.40,
        "strike_rate_balls_per_wicket": 11.2
    },
    "competition_split": {
        "ipl_balls": 181,
        "t20i_balls": 100,
        "unique_matches": 26
    },
    "pps_score": 59.27,
    "ppr_percentile": 91.95
}

# 4. Summary metrics
summary_metrics = {
    "retained_count": 19,
    "retained_indian": 14,
    "retained_overseas": 5,
    "remaining_purse_cr": 27.05,
    "available_slots": 6,
    "max_overseas_slots": 3,
    "released_pool_count": 89,
    "active_eligible_candidates": 87,
    "ineligible_retired_count": 2,
    "qualified_discipline_entries": len(ppr),
    "qualified_unique_players": ppr['player_id'].nunique(),
    "top_strategic_target": srr.iloc[0]['player_name'],
    "top_strategic_srr": float(srr.iloc[0]['srr_pct']),
    "recommended_scenario": "Scenario B2: Specialist Diversification Strategy",
    "recommended_spend_cr": 16.75,
    "recommended_buffer_cr": 10.30
}

# Save all JSONs
with open(f'{DATA_DIR}/summary.json', 'w') as f:
    json.dump(summary_metrics, f, indent=2)

with open(f'{DATA_DIR}/retained_squad.json', 'w') as f:
    json.dump(retained_squad, f, indent=2)

with open(f'{DATA_DIR}/strategic_shortlist.json', 'w') as f:
    json.dump(srr.to_dict(orient='records'), f, indent=2)

with open(f'{DATA_DIR}/top_batters.json', 'w') as f:
    json.dump(batters, f, indent=2)

with open(f'{DATA_DIR}/top_bowlers.json', 'w') as f:
    json.dump(bowlers, f, indent=2)

with open(f'{DATA_DIR}/hidden_gems.json', 'w') as f:
    json.dump(hg.to_dict(orient='records'), f, indent=2)

with open(f'{DATA_DIR}/scenarios.json', 'w') as f:
    json.dump(scen.to_dict(orient='records'), f, indent=2)

with open(f'{DATA_DIR}/active_pool.json', 'w') as f:
    json.dump(pool[pool['active_status'] == 'Active'].to_dict(orient='records'), f, indent=2)

with open(f'{DATA_DIR}/pathirana_audit.json', 'w') as f:
    json.dump(pathirana_data, f, indent=2)

print("All dashboard data successfully exported to dashboard/public/data/!")


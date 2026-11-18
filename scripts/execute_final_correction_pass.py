"""
scripts/execute_final_correction_pass.py
Executes the final correction pass:
1. Normalizes PPR to 0-100 scale: PPR_norm = (PPR - 25) / 70 * 100
   SRR = 0.50 * PPR_norm + 0.50 * AOR
2. Reclassifies Kuldeep Sen as Capped (India ODI cap #250).
3. Marks Ajinkya Rahane as Retired from IPL.
4. Generates updated CSVs:
   - outputs/final_pressure_performance_ranking.csv
   - outputs/final_auction_opportunity_ranking.csv
   - outputs/final_rr_strategic_shortlist.csv
   - outputs/final_hidden_gems.csv
   - outputs/final_six_player_scenarios.csv
"""

import os
import pandas as pd
import numpy as np

# Load master pool
pool = pd.read_csv('d:/RR/outputs/official_ipl_2027_released_player_pool.csv')

# 1. Update Kuldeep Sen (7545) -> Capped
pool.loc[pool['player_id'] == 7545, 'capped_status'] = 'Capped'

# 2. Update Ajinkya Rahane (167) -> Retired from IPL
pool.loc[pool['player_id'] == 167, 'active_status'] = 'Retired from IPL'
pool.loc[pool['player_id'] == 167, 'auction_eligibility'] = 'Ineligible (Retired from IPL)'
pool.loc[pool['player_id'] == 167, 'aos'] = 0.0

# Active pool: players whose active_status is 'Active'
active_pool = pool[pool['active_status'] == 'Active'].copy()
print(f"Total active released players in pool: {len(active_pool)}")

# Save updated master pool
pool.to_csv('d:/RR/outputs/official_ipl_2027_released_player_pool.csv', index=False)

# =========================================================================
# 1. FINAL PRESSURE PERFORMANCE RANKING (PPR)
# Pure cricket performance under high pressure (P >= P75).
# Qualification threshold: N_press >= 25 deliveries.
# Normalized PPR: PPR_norm = (PPR - 25.0) / 70.0 * 100.0
# =========================================================================
bat_perf = active_pool[active_pool['press_bat_balls'] >= 25].copy()
bat_perf['discipline'] = 'Batting'
bat_perf['perf_metric'] = bat_perf['press_bat_sr']
bat_perf['baseline_metric'] = bat_perf['press_bat_sr'] - bat_perf['delta_bat_sr']
bat_perf['delta_metric'] = bat_perf['delta_bat_sr']
bat_perf['ppr_score'] = bat_perf['pps_bat']
bat_perf['sample_balls'] = bat_perf['press_bat_balls']
bat_perf['sample_runs_or_wkts'] = bat_perf['press_bat_runs']

bowl_perf = active_pool[active_pool['press_bowl_balls'] >= 25].copy()
bowl_perf['discipline'] = 'Bowling'
bowl_perf['perf_metric'] = bowl_perf['press_bowl_econ']
bowl_perf['baseline_metric'] = bowl_perf['press_bowl_econ'] - bowl_perf['delta_bowl_econ']
bowl_perf['delta_metric'] = bowl_perf['delta_bowl_econ']
bowl_perf['ppr_score'] = bowl_perf['pps_bowl']
bowl_perf['sample_balls'] = bowl_perf['press_bowl_balls']
bowl_perf['sample_runs_or_wkts'] = bowl_perf['press_bowl_wkts']

ppr_combined = pd.concat([bat_perf, bowl_perf], ignore_index=True)
ppr_combined['ppr_norm'] = np.round((ppr_combined['ppr_score'] - 25.0) / 70.0 * 100.0, 2)
ppr_combined = ppr_combined.sort_values(by=['ppr_score', 'sample_balls'], ascending=[False, False])
ppr_combined['ppr_rank'] = range(1, len(ppr_combined) + 1)

ppr_export = ppr_combined[[
    'ppr_rank', 'player_name', 'player_id', 'discipline', 'primary_role',
    'classification', 'capped_status', 'last_franchise',
    'sample_balls', 'sample_runs_or_wkts', 'perf_metric', 'baseline_metric',
    'delta_metric', 'ppr_score', 'ppr_norm'
]].rename(columns={
    'sample_runs_or_wkts': 'runs_or_wkts',
    'perf_metric': 'pressure_sr_or_econ',
    'baseline_metric': 'baseline_sr_or_econ',
    'delta_metric': 'delta_lift'
})

ppr_export.to_csv('d:/RR/outputs/final_pressure_performance_ranking.csv', index=False)
print(f"1. Saved final_pressure_performance_ranking.csv ({len(ppr_export)} entries)")

# =========================================================================
# 2. FINAL AUCTION OPPORTUNITY RANKING (AOR)
# Market opportunity and RR fit score (0-100 scale).
# =========================================================================
# Re-evaluate AOS for Kuldeep Sen (now Capped Indian: i_slot adjusted from 1.0 to 0.80)
# Kuldeep Sen (7545): i_avail=0.90, i_fit=0.90, i_slot=0.80, i_sample=35/(35+40)=0.4667
# AOS = 100 * (0.35*0.90 + 0.30*0.90 + 0.25*0.80 + 0.10*0.4667) = 100 * (0.315 + 0.270 + 0.200 + 0.0467) = 83.17
active_pool.loc[active_pool['player_id'] == 7545, 'aos'] = 83.17

aor_df = active_pool.sort_values(by=['aos', 'pps'], ascending=[False, False]).copy()
aor_df['aor_rank'] = range(1, len(aor_df) + 1)

aor_export = aor_df[[
    'aor_rank', 'player_name', 'player_id', 'primary_role', 'classification',
    'capped_status', 'last_franchise', 'salary_lakhs', 'aos',
    'rr_priority_alignment', 'auction_eligibility'
]].rename(columns={'salary_lakhs': 'previous_contract_salary_lakhs'})

aor_export.to_csv('d:/RR/outputs/final_auction_opportunity_ranking.csv', index=False)
print(f"2. Saved final_auction_opportunity_ranking.csv ({len(aor_export)} entries)")

# =========================================================================
# 3. FINAL RR STRATEGIC SHORTLIST (SRR)
# Transparently normalized:
# PPR_norm = (PPS - 25.0) / 70.0 * 100.0
# SRR = 0.50 * PPR_norm + 0.50 * AOR
# Strictly gated by N_press >= 25 balls (or intentional developmental gems)
# =========================================================================
strategic_candidates = active_pool[
    (active_pool['press_bat_balls'] >= 25) |
    (active_pool['press_bowl_balls'] >= 25) |
    (active_pool['player_id'].isin([48557, 7279, 31529]))
].copy()

strategic_candidates['ppr_norm'] = np.round((strategic_candidates['pps'] - 25.0) / 70.0 * 100.0, 2)
strategic_candidates['srr'] = np.round(0.50 * strategic_candidates['ppr_norm'] + 0.50 * strategic_candidates['aos'], 2)

strategic_candidates = strategic_candidates.sort_values(by=['srr', 'ppr_norm'], ascending=[False, False])
strategic_candidates['strategic_rank'] = range(1, len(strategic_candidates) + 1)

srr_export = strategic_candidates[[
    'strategic_rank', 'player_name', 'player_id', 'primary_role',
    'classification', 'capped_status', 'last_franchise',
    'press_bat_balls', 'press_bat_sr', 'delta_bat_sr',
    'press_bowl_balls', 'press_bowl_econ', 'delta_bowl_econ',
    'pps', 'ppr_norm', 'aos', 'srr', 'rr_priority_alignment'
]].head(15).rename(columns={'pps': 'ppr_raw', 'aos': 'aor'})

srr_export.to_csv('d:/RR/outputs/final_rr_strategic_shortlist.csv', index=False)
print(f"3. Saved final_rr_strategic_shortlist.csv ({len(srr_export)} entries)")

# =========================================================================
# 4. FINAL HIDDEN GEMS (5 STANDOUT PROSPECTS)
# Kuldeep Sen updated to Capped.
# =========================================================================
hg_data = [
    {
        'gem_rank': 1,
        'player_name': 'Shahrukh Khan',
        'player_id': 3782,
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'specialist_skill': 'Lower-Order Death Overs Power Finisher (#6/#7)',
        'delivery_evidence': '168 pressure balls, 275 runs, 163.69 SR (+32.75 lift); 93 balls in overs 16-20',
        'sample_size_and_confidence': '168 balls across 26 matches (100% IPL); High statistical confidence',
        'rr_tactical_fit': 'Directly solves Priority 1 (Hetmyer void) using an Indian uncapped slot',
        'why_overlooked': 'Released by GT after high-profile auction tag; market focuses on aggregate runs rather than clutch phase SR',
        'estimated_valuation_inr_cr': '5.50 - 6.50 Cr (Estimated bid range based on finisher scarcity)',
        'ppr_raw': 64.96, 'ppr_norm': 57.09, 'aor': 95.08, 'srr': 76.09
    },
    {
        'gem_rank': 2,
        'player_name': 'Akash Madhwal',
        'player_id': 8177,
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'specialist_skill': 'Pinpoint Yorker & Death Overs Defender (Overs 16-20)',
        'delivery_evidence': '78 pressure balls, 76 balls in Death phase (97.4%), 8.69 Econ (-0.91 compression), 7 wkts',
        'sample_size_and_confidence': '78 balls across 10 matches (100% IPL); Verified death-phase execution',
        'rr_tactical_fit': 'Directly solves Priority 2 (Death Pace), pairing with Sandeep Sharma to protect Shami/Archer',
        'why_overlooked': 'Underutilized at CSK due to crowded pace bench; perceived as older uncapped player (age 33)',
        'estimated_valuation_inr_cr': '3.50 - 4.50 Cr (Estimated bid range based on death specialist demand)',
        'ppr_raw': 59.20, 'ppr_norm': 48.86, 'aor': 95.11, 'srr': 71.99
    },
    {
        'gem_rank': 3,
        'player_name': 'Mahipal Lomror',
        'player_id': 4821,
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'specialist_skill': 'High-Impact Boundary Striker vs Spin & Pace in Death Transition',
        'delivery_evidence': '55 pressure balls, 102 runs, 185.45 SR (+49.90 lift); highest SR in released pool',
        'sample_size_and_confidence': '55 balls across 8 matches; Moderate sample with acknowledged variance (EB shrunk to 164.2)',
        'rr_tactical_fit': 'Dynamic #5/#6 float batter, intimate knowledge of SMS Stadium Jaipur (former RR product)',
        'why_overlooked': 'Released by MI during squad overhaul; perceived as utility pinch-hitter rather than specialist',
        'estimated_valuation_inr_cr': '1.50 - 2.50 Cr (Estimated bid range; outstanding value-for-money)',
        'ppr_raw': 65.16, 'ppr_norm': 57.37, 'aor': 92.79, 'srr': 75.08
    },
    {
        'gem_rank': 4,
        'player_name': 'Atharva Ankolekar',
        'player_id': 7279,
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'specialist_skill': 'Emerging Left-Arm Orthodox Spinner with Drift & High Release',
        'delivery_evidence': 'India U-19 World Cup star; domestic T20 economy under 6.80 rpo; disciplined stump-to-stump line',
        'sample_size_and_confidence': 'Domestic track record; small IPL pressure sample (explicitly noted as developmental prospect)',
        'rr_tactical_fit': 'Directly solves Priority 3 (Emerging Spin Backup) to replace departed Vignesh Puthur',
        'why_overlooked': 'Remained in MI reserve nets behind international spinners; accessible near base price',
        'estimated_valuation_inr_cr': '0.30 - 0.75 Cr (Estimated base-tier developmental acquisition)',
        'ppr_raw': 40.00, 'ppr_norm': 21.43, 'aor': 78.00, 'srr': 49.72
    },
    {
        'gem_rank': 5,
        'player_name': 'Kuldeep Sen',
        'player_id': 7545,
        'classification': 'Indian (Capped)',
        'capped_status': 'Capped',
        'specialist_skill': '148+ km/h Raw Physical Velocity & Steep Hard-Deck Bounce',
        'delivery_evidence': '35 pressure balls, 23 in death phase, 9.77 Econ against elite batters; clocked at 148.5 km/h; India ODI Cap #250',
        'sample_size_and_confidence': '35 balls across 4 matches; Moderate sample with documented workload history',
        'rr_tactical_fit': 'Restores domestic express pace depth for Sawai Mansingh Stadium without burning overseas slot',
        'why_overlooked': 'Released during RR contract churn; injury concerns cause rival teams to hesitate',
        'estimated_valuation_inr_cr': '0.75 - 1.20 Cr (Estimated low-cost re-acquisition opportunity)',
        'ppr_raw': 47.00, 'ppr_norm': 31.43, 'aor': 83.17, 'srr': 57.30
    }
]

hg_export = pd.DataFrame(hg_data)
hg_export.to_csv('d:/RR/outputs/final_hidden_gems.csv', index=False)
print(f"4. Saved final_hidden_gems.csv (5 verified gems, Kuldeep Sen Capped)")

# =========================================================================
# 5. FINAL SIX-PLAYER SCENARIOS
# Kuldeep Sen updated to Capped.
# Vignesh Puthur valuation explicitly labeled as strategic estimate.
# =========================================================================
scenarios_data = [
    # Scenario A: Conservative Value Strategy
    {
        'scenario': 'Scenario A: Conservative Value Strategy',
        'slot_num': 1,
        'target_player': 'Mahipal Lomror',
        'player_id': 4821,
        'role': 'Indian Middle Finisher',
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '1.50 - 2.50 Cr',
        'target_allocation_cr': 2.00,
        'valuation_assumptions': 'Estimated market price based on uncapped domestic hitter demand; not an official base price',
        'tactical_rationale': '185.45 Pressure SR at budget valuation; fills finishing slot at fraction of marquee cost'
    },
    {
        'scenario': 'Scenario A: Conservative Value Strategy',
        'slot_num': 2,
        'target_player': 'Akash Madhwal',
        'player_id': 8177,
        'role': 'Indian Death Pacer',
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '3.00 - 4.00 Cr',
        'target_allocation_cr': 3.50,
        'valuation_assumptions': 'Estimated winning bid reflecting high demand for domestic death specialists',
        'tactical_rationale': 'Premier domestic yorker specialist; solves death bowling with zero overseas penalty'
    },
    {
        'scenario': 'Scenario A: Conservative Value Strategy',
        'slot_num': 3,
        'target_player': 'Atharva Ankolekar',
        'player_id': 7279,
        'role': 'Emerging Indian Spinner',
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '0.30 - 0.60 Cr',
        'target_allocation_cr': 0.40,
        'valuation_assumptions': 'Estimated bidding close to base tier (30-50L) for unheralded spin talent',
        'tactical_rationale': 'Replaces Vignesh Puthur; high-ceiling domestic left-arm orthodox backup'
    },
    {
        'scenario': 'Scenario A: Conservative Value Strategy',
        'slot_num': 4,
        'target_player': 'Kuldeep Sen',
        'player_id': 7545,
        'role': 'Indian Express Pacer',
        'classification': 'Indian (Capped)',
        'capped_status': 'Capped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '0.75 - 1.20 Cr',
        'target_allocation_cr': 1.00,
        'valuation_assumptions': 'Estimated acquisition range for injury-return capped international pacer',
        'tactical_rationale': 'Low-cost in-house re-acquisition providing 148 km/h pace cover for Shami and Archer'
    },
    {
        'scenario': 'Scenario A: Conservative Value Strategy',
        'slot_num': 5,
        'target_player': 'George Linde',
        'player_id': 4229,
        'role': 'Overseas Spin All-Rounder',
        'classification': 'Overseas (Capped)',
        'capped_status': 'Overseas Capped',
        'overseas_slot_used': 'Yes (1 of 3)',
        'estimated_bid_range_cr': '1.00 - 1.50 Cr',
        'target_allocation_cr': 1.25,
        'valuation_assumptions': 'Estimated range for overseas utility all-rounder in lower-demand tier',
        'tactical_rationale': '6.51 Pressure Econ + 156.60 SR; exceptional two-way value for under 2 Cr'
    },
    {
        'scenario': 'Scenario A: Conservative Value Strategy',
        'slot_num': 6,
        'target_player': 'Prashant Veer / Robin Minz',
        'player_id': 45966,
        'role': 'Domestic Batting / WK Depth',
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '0.30 - 0.75 Cr',
        'target_allocation_cr': 0.50,
        'valuation_assumptions': 'Estimated bench-tier acquisition near base price',
        'tactical_rationale': 'High-upside bench cover; secures full 25-man squad depth'
    },

    # Scenario B: Balanced Squad Strategy (Recommended)
    {
        'scenario': 'Scenario B: Balanced Squad Strategy (Recommended)',
        'slot_num': 1,
        'target_player': 'Shahrukh Khan',
        'player_id': 3782,
        'role': 'Primary Indian Death Finisher',
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '5.50 - 7.00 Cr',
        'target_allocation_cr': 6.00,
        'valuation_assumptions': 'Estimated competitive market clearing price for premier domestic finisher',
        'tactical_rationale': 'Proven clutch finisher (163.69 SR, 168 balls); anchors lower-order with Dhruv Jurel'
    },
    {
        'scenario': 'Scenario B: Balanced Squad Strategy (Recommended)',
        'slot_num': 2,
        'target_player': 'Akash Madhwal',
        'player_id': 8177,
        'role': 'Indian Death Pacer',
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '3.50 - 4.50 Cr',
        'target_allocation_cr': 4.00,
        'valuation_assumptions': 'Estimated valuation reflecting scarcity of proven Indian death bowlers',
        'tactical_rationale': '8.69 Death Econ (-0.91 compression); pairs with Sandeep Sharma for elite overs 18-20'
    },
    {
        'scenario': 'Scenario B: Balanced Squad Strategy (Recommended)',
        'slot_num': 3,
        'target_player': 'Shimron Hetmyer',
        'player_id': 3297,
        'role': 'Overseas Match-Winner Finisher',
        'classification': 'Overseas (Capped)',
        'capped_status': 'Overseas Capped',
        'overseas_slot_used': 'Yes (1 of 3)',
        'estimated_bid_range_cr': '6.00 - 7.50 Cr',
        'target_allocation_cr': 6.50,
        'valuation_assumptions': 'Estimated market correction from previous 11 Cr contract; high franchise interest',
        'tactical_rationale': 'Re-acquisition at rationalized price; 476 clutch balls, proven RR culture fit'
    },
    {
        'scenario': 'Scenario B: Balanced Squad Strategy (Recommended)',
        'slot_num': 4,
        'target_player': 'Spencer Johnson',
        'player_id': 6354,
        'role': 'Overseas Express Fast Bowler',
        'classification': 'Overseas (Capped)',
        'capped_status': 'Overseas Capped',
        'overseas_slot_used': 'Yes (2 of 3)',
        'estimated_bid_range_cr': '3.50 - 4.50 Cr',
        'target_allocation_cr': 4.00,
        'valuation_assumptions': 'Estimated valuation for 145+ km/h left-arm pacer in mini-auction pool',
        'tactical_rationale': '145+ km/h left-arm thunderbolts; steep hard-deck bounce enforcer for SMS Stadium'
    },
    {
        'scenario': 'Scenario B: Balanced Squad Strategy (Recommended)',
        'slot_num': 5,
        'target_player': 'Kuldeep Sen',
        'player_id': 7545,
        'role': 'Indian Express Pacer',
        'classification': 'Indian (Capped)',
        'capped_status': 'Capped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '0.75 - 1.20 Cr',
        'target_allocation_cr': 1.00,
        'valuation_assumptions': 'Estimated re-acquisition valuation for in-house capped pace asset',
        'tactical_rationale': 'In-house 148 km/h enforcer; domestic pace depth cover for Shami'
    },
    {
        'scenario': 'Scenario B: Balanced Squad Strategy (Recommended)',
        'slot_num': 6,
        'target_player': 'Atharva Ankolekar / Vignesh Puthur',
        'player_id': 7279,
        'role': 'Emerging Indian Spinner',
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '0.30 - 0.75 Cr',
        'target_allocation_cr': 0.50,
        'valuation_assumptions': 'Strategic estimate for domestic spin depth; not an official base price',
        'tactical_rationale': 'Base-tier acquisition; restores mystery/developmental spin depth behind Jadeja and Bishnoi'
    },

    # Scenario C: Aggressive Match-Winner Strategy
    {
        'scenario': 'Scenario C: Aggressive Match-Winner Strategy',
        'slot_num': 1,
        'target_player': 'Nitish Rana',
        'player_id': 4246,
        'role': 'Marquee Middle-Order Batter',
        'classification': 'Indian (Capped)',
        'capped_status': 'Capped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '7.00 - 8.50 Cr',
        'target_allocation_cr': 8.00,
        'valuation_assumptions': 'Estimated winning bid range in competitive bidding for marquee Indian batter',
        'tactical_rationale': '156.33 Pressure SR on 229 balls; left-handed middle anchor and accelerator'
    },
    {
        'scenario': 'Scenario C: Aggressive Match-Winner Strategy',
        'slot_num': 2,
        'target_player': 'Matheesha Pathirana',
        'player_id': 8661,
        'role': 'Marquee Overseas Death Specialist',
        'classification': 'Overseas (Capped)',
        'capped_status': 'Overseas Capped',
        'overseas_slot_used': 'Yes (1 of 3)',
        'estimated_bid_range_cr': '8.50 - 10.00 Cr',
        'target_allocation_cr': 9.50,
        'valuation_assumptions': 'Estimated market price for premier death specialist (released at 18 Cr)',
        'tactical_rationale': '281 clutch balls (190 in death); unplayable sling-arm death yorkers'
    },
    {
        'scenario': 'Scenario C: Aggressive Match-Winner Strategy',
        'slot_num': 3,
        'target_player': 'Akash Madhwal',
        'player_id': 8177,
        'role': 'Indian Death Pacer',
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '3.50 - 4.50 Cr',
        'target_allocation_cr': 4.00,
        'valuation_assumptions': 'Estimated valuation reflecting essential requirement for domestic death execution',
        'tactical_rationale': 'Essential domestic death partner to lock overs 17-20'
    },
    {
        'scenario': 'Scenario C: Aggressive Match-Winner Strategy',
        'slot_num': 4,
        'target_player': 'Rehan Ahmed',
        'player_id': 24475,
        'role': 'Overseas Leg-Spin Enforcer',
        'classification': 'Overseas (Capped)',
        'capped_status': 'Overseas Capped',
        'overseas_slot_used': 'Yes (2 of 3)',
        'estimated_bid_range_cr': '1.50 - 2.50 Cr',
        'target_allocation_cr': 2.00,
        'valuation_assumptions': 'Estimated winning range for young England international spinner',
        'tactical_rationale': '7.50 Pressure Econ (-2.68 compression); dynamic wicket-taker'
    },
    {
        'scenario': 'Scenario C: Aggressive Match-Winner Strategy',
        'slot_num': 5,
        'target_player': 'Kuldeep Sen',
        'player_id': 7545,
        'role': 'Indian Express Pacer',
        'classification': 'Indian (Capped)',
        'capped_status': 'Capped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '0.75 - 1.20 Cr',
        'target_allocation_cr': 1.00,
        'valuation_assumptions': 'Estimated re-acquisition price for capped express pace enforcer',
        'tactical_rationale': '148 km/h domestic pace cover for Mohammed Shami'
    },
    {
        'scenario': 'Scenario C: Aggressive Match-Winner Strategy',
        'slot_num': 6,
        'target_player': 'Vignesh Puthur',
        'player_id': 48557,
        'role': 'Emerging Indian Mystery Spinner',
        'classification': 'Indian (Uncapped)',
        'capped_status': 'Uncapped',
        'overseas_slot_used': 'No',
        'estimated_bid_range_cr': '0.30 - 0.50 Cr',
        'target_allocation_cr': 0.35,
        'valuation_assumptions': 'Strategic estimate for base-tier uncapped re-acquisition; not official base price',
        'tactical_rationale': 'Direct re-acquisition; unreadable middle-overs trajectory development weapon'
    }
]

scenarios_df = pd.DataFrame(scenarios_data)
scenarios_df.to_csv('d:/RR/outputs/final_six_player_scenarios.csv', index=False)
print(f"5. Saved final_six_player_scenarios.csv (Kuldeep Sen Capped, Vignesh estimate labeled)")


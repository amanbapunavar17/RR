"""
Ranking Engine Module for SupeRR Selector Season 2
Generates official Top 10 Batters and Top 10 Bowlers under pressure.
Outputs all required CSV files with complete traceability to ball-by-ball records.
"""

import os
import pandas as pd
import numpy as np

def generate_official_rankings(bat_df, bowl_df, output_dir="outputs"):
    """
    Finalizes and exports the Top 10 Batters and Top 10 Bowlers under pressure.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. TOP 10 BATTERS
    # -------------------------------------------------------------
    top_batters = bat_df.head(10).copy()
    top_batters['rank'] = range(1, 11)
    
    # Determine confidence indicator
    top_batters['confidence_indicator'] = np.where(
        top_batters['pressure_balls'] >= 250, 'Very High (Elite Sample)',
        np.where(top_batters['pressure_balls'] >= 180, 'High (Substantial Sample)', 'Solid (Qualified Sample)')
    )
    
    # Statistical Justifications
    justifications_bat = []
    for _, row in top_batters.iterrows():
        name = row['player_name']
        sr_diff = row['delta_sr']
        diff_str = f"+{sr_diff:.1f}" if sr_diff > 0 else f"{sr_diff:.1f}"
        just = (
            f"{name} achieves a remarkable pressure strike rate of {row['pressure_sr']:.1f} ({diff_str} over normal baseline of {row['normal_sr']:.1f}) "
            f"across {row['pressure_balls']} pressure balls with {row['pressure_runs']} runs and an average of {row['pressure_avg']:.1f}. "
            f"Demonstrates {row['consistency']*100:.1f}% match-level positive impact consistency and {row['pressure_bnd_pct']:.1f}% boundary scoring."
        )
        justifications_bat.append(just)
        
    top_batters['statistical_justification'] = justifications_bat
    
    # Required Top 10 Batters Schema:
    # Rank, Player Name, Player ID, Pressure Score, Normal Baseline, Pressure Strike Rate,
    # Runs Scored Under Pressure, Balls Faced Under Pressure, Dismissals, Pressure Sample Size,
    # Match Count, Confidence or Reliability Indicator, Short Statistical Justification.
    cols_bat_export = [
        'rank', 'player_name', 'player_id', 'pressure_score', 'normal_baseline',
        'pressure_sr', 'pressure_runs', 'pressure_balls', 'pressure_outs',
        'sample_reliability', 'pressure_matches', 'confidence_indicator',
        'statistical_justification'
    ]
    
    top_bat_export = top_batters[cols_bat_export].rename(columns={
        'pressure_runs': 'runs_under_pressure',
        'pressure_balls': 'balls_faced_under_pressure',
        'pressure_outs': 'dismissals',
        'sample_reliability': 'pressure_sample_reliability',
        'pressure_matches': 'match_count'
    })
    
    top_bat_path = os.path.join(output_dir, "top_10_batters.csv")
    top_bat_export.to_csv(top_bat_path, index=False)
    print(f"Exported Top 10 Batters to {top_bat_path}")

    # -------------------------------------------------------------
    # 2. TOP 10 BOWLERS
    # -------------------------------------------------------------
    top_bowlers = bowl_df.head(10).copy()
    top_bowlers['rank'] = range(1, 11)
    
    top_bowlers['confidence_indicator'] = np.where(
        top_bowlers['pressure_balls'] >= 450, 'Very High (Elite Sample)',
        np.where(top_bowlers['pressure_balls'] >= 300, 'High (Substantial Sample)', 'Solid (Qualified Sample)')
    )
    
    justifications_bowl = []
    for _, row in top_bowlers.iterrows():
        name = row['player_name']
        ec_diff = row['delta_econ']
        diff_str = f"-{ec_diff:.2f} rpo" if ec_diff > 0 else f"+{abs(ec_diff):.2f} rpo"
        just = (
            f"{name} delivers elite economy of {row['pressure_econ']:.2f} under pressure ({diff_str} suppression vs normal {row['normal_econ']:.2f}) "
            f"over {row['pressure_balls']} pressure legal balls ({row['pressure_balls']//6} ov), capturing {row['pressure_wickets']} wickets with "
            f"{row['pressure_dot_pct']:.1f}% dot-ball rate and {row['consistency']*100:.1f}% match-level containment consistency."
        )
        justifications_bowl.append(just)
        
    top_bowlers['statistical_justification'] = justifications_bowl
    
    # Required Top 10 Bowlers Schema:
    # Rank, Player Name, Player ID, Pressure Score, Normal Baseline, Pressure Economy,
    # Pressure Wickets, Pressure Dot-Ball Percentage, Pressure Sample Size, Match Count,
    # Confidence or Reliability Indicator, Short Statistical Justification.
    cols_bowl_export = [
        'rank', 'player_name', 'player_id', 'pressure_score', 'normal_baseline',
        'pressure_econ', 'pressure_wickets', 'pressure_dot_pct',
        'sample_reliability', 'pressure_matches', 'confidence_indicator',
        'statistical_justification'
    ]
    
    top_bowl_export = top_bowlers[cols_bowl_export].rename(columns={
        'sample_reliability': 'pressure_sample_reliability',
        'pressure_matches': 'match_count'
    })
    
    top_bowl_path = os.path.join(output_dir, "top_10_bowlers.csv")
    top_bowl_export.to_csv(top_bowl_path, index=False)
    print(f"Exported Top 10 Bowlers to {top_bowl_path}")
    
    # Export full metrics
    all_bat_path = os.path.join(output_dir, "all_batter_metrics.csv")
    bat_df.to_csv(all_bat_path, index=False)
    
    all_bowl_path = os.path.join(output_dir, "all_bowler_metrics.csv")
    bowl_df.to_csv(all_bowl_path, index=False)
    print(f"Exported full player metrics to {all_bat_path} and {all_bowl_path}")
    
    return top_batters, top_bowlers


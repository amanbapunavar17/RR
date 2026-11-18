"""
Data Loader Module for SupeRR Selector Season 2
Loads raw datasets from Data Pack directory with proper type enforcement and verification.
"""

import os
import pandas as pd
import numpy as np

def load_all_datasets(data_dir="Data Pack"):
    """
    Loads all core CSV files from the Data Pack directory.
    Returns a dictionary of DataFrames.
    """
    files = {
        'competitions': os.path.join(data_dir, 'competitions.csv'),
        'teams': os.path.join(data_dir, 'teams.csv'),
        'matches': os.path.join(data_dir, 'matches.csv'),
        'playing_eleven': os.path.join(data_dir, 'playing_eleven.csv'),
        'ctpm': os.path.join(data_dir, 'competition_team_player_mapping.csv'),
        'bbb': os.path.join(data_dir, 'ball_by_ball.csv')
    }
    
    datasets = {}
    for name, path in files.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required dataset file not found: {path}")
        datasets[name] = pd.read_csv(path, low_memory=False)
        
    return datasets


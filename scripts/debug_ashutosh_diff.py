"""
scripts/debug_ashutosh_diff.py
Compares the delivery-level pressure scores and classifications
for Ashutosh Sharma between generate_final_verification_dossier.py
and build_complete_auction_system.py.
"""

import pandas as pd
import numpy as np

# Let's inspect the pressure formulas in both files!
# In generate_final_verification_dossier.py:
# def get_expected_inn1_total(row):
#   comp = str(row['comp_name'])
#   season = str(row['season'])
#   fmt = str(row['match_format'])
#   if 'IPL' in comp:
#       if '2022' in season: return 171.1
#       elif '2023' in season: return 182.7
#       elif '2024' in season: return 189.6
#       elif '2025' in season: return 190.1
#       elif '2026' in season: return 193.4
#       else: return 185.0
#   elif fmt == 'T20I':
#       return 181.8 if '2026' in season else 168.0
#   else: return 158.0
#
# But look at build_complete_auction_system.py line 125:
# S_exp1 = (b1 / 6.0) * 8.5
# Notice that build_complete_auction_system used a static 8.5 par rate instead of the dynamic par total
# from Methodology v2!
# Let's verify this!


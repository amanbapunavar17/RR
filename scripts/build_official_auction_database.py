"""
scripts/build_official_auction_database.py
Generates the complete official IPL 2027 released-player pool and RR auction strategy artifacts
with strict role segregation and tactical alignment.
"""

import os
import pandas as pd
import numpy as np

os.makedirs('d:/RR/outputs', exist_ok=True)
os.makedirs('d:/RR/reports', exist_ok=True)

# Load delivery pressure data
print("Loading pressure deliveries...")
df_p = pd.read_csv('d:/RR/outputs/pressure_delivery_analysis.csv')
df_b = pd.read_csv('d:/RR/Data Pack/ball_by_ball.csv', usecols=[
    'match_id', 'innings', 'overid', 'over_ball_num', 'striker_id', 'bowler_id', 'dismissed_player_id'
])
df = pd.merge(df_p, df_b, on=['match_id', 'innings', 'overid', 'over_ball_num'], how='inner')
print(f"Merged {len(df)} deliveries.")

p75_bat = 55.20
p75_bowl = 68.90
df['is_press_bat'] = df['batting_pressure'] >= p75_bat
df['is_press_bowl'] = df['bowling_pressure'] >= p75_bowl

# Complete metadata for all 89 players
players_meta = [
    # CSK (11)
    ("Akash Madhwal", False, 30, "Chennai Super Kings", 8177, "Bowler", "India", "Uncapped", 33, "Active"),
    ("Aman Khan", False, 40, "Chennai Super Kings", 20894, "All-Rounder", "India", "Uncapped", 29, "Active"),
    ("Dian Forrester", True, 75, "Chennai Super Kings", 46929, "All-Rounder", "South Africa", "Overseas Uncapped", 25, "Active"),
    ("Kuldip Yadav", False, 30, "Chennai Super Kings", 20693, "Bowler", "India", "Uncapped", 29, "Active"),
    ("Macneil Noronha", False, 30, "Chennai Super Kings", 33095, "All-Rounder", "India", "Uncapped", 23, "Active"),
    ("Matt Henry", True, 200, "Chennai Super Kings", 3174, "Bowler", "New Zealand", "Overseas Capped", 34, "Active"),
    ("Matthew Short", True, 150, "Chennai Super Kings", 3727, "Batter", "Australia", "Overseas Capped", 31, "Active"),
    ("MS Dhoni", False, 400, "Chennai Super Kings", 8, "Wicketkeeper-Batter", "India", "Retired / Mentor", 45, "Retired (Mentor)"),
    ("Prashant Veer", False, 1420, "Chennai Super Kings", 45966, "All-Rounder", "India", "Uncapped", 21, "Active"),
    ("Spencer Johnson", True, 150, "Chennai Super Kings", 6354, "Bowler", "Australia", "Overseas Capped", 30, "Active"),
    ("Zak Foulkes", True, 75, "Chennai Super Kings", 29066, "All-Rounder", "New Zealand", "Overseas Capped", 24, "Active"),
    
    # DC (9)
    ("Abhishek Porel", False, 400, "Delhi Capitals", 19714, "Wicketkeeper-Batter", "India", "Uncapped", 24, "Active"),
    ("Ajay Mandal", False, 30, "Delhi Capitals", 7553, "All-Rounder", "India", "Uncapped", 30, "Active"),
    ("Dushmantha Chameera", True, 75, "Delhi Capitals", 2399, "Bowler", "Sri Lanka", "Overseas Capped", 34, "Active"),
    ("Karun Nair", False, 50, "Delhi Capitals", 930, "Batter", "India", "Capped", 34, "Active"),
    ("Mitchell Starc", True, 1175, "Delhi Capitals", 829, "Bowler", "Australia", "Overseas Capped", 36, "Active"),
    ("Nitish Rana", False, 420, "Delhi Capitals", 4246, "Batter", "India", "Capped", 32, "Active"),
    ("Pathum Nissanka", True, 400, "Delhi Capitals", 6931, "Batter", "Sri Lanka", "Overseas Capped", 28, "Active"),
    ("Rehan Ahmed", True, 75, "Delhi Capitals", 24475, "Bowler", "England", "Overseas Capped", 22, "Active"),
    ("Sahil Parakh", False, 30, "Delhi Capitals", 48575, "Batter", "India", "Uncapped", 19, "Active"),
    
    # GT (6)
    ("Connor Esterhuizen", True, 75, "Gujarat Titans", 28970, "Batter", "South Africa", "Overseas Uncapped", 25, "Active"),
    ("Luke Wood", True, 75, "Gujarat Titans", 3660, "Bowler", "England", "Overseas Capped", 31, "Active"),
    ("Ishant Sharma", False, 75, "Gujarat Titans", 28, "Bowler", "India", "Capped", 38, "Active"),
    ("Kulwant Khejroliya", False, 30, "Gujarat Titans", 6162, "Bowler", "India", "Uncapped", 34, "Active"),
    ("Prithviraj Yarra", False, 30, "Gujarat Titans", 6351, "Bowler", "India", "Uncapped", 28, "Active"),
    ("Shahrukh Khan", False, 400, "Gujarat Titans", 3782, "All-Rounder", "India", "Uncapped", 31, "Active"),
    
    # KKR (12)
    ("Ajinkya Rahane", False, 150, "Kolkata Knight Riders", 167, "Batter", "India", "Capped", 38, "Active"),
    ("Akash Deep", False, 100, "Kolkata Knight Riders", 7473, "Bowler", "India", "Capped", 29, "Active"),
    ("Blessing Muzarabani", True, 150, "Kolkata Knight Riders", 6523, "Bowler", "Zimbabwe", "Overseas Capped", 30, "Active"),
    ("Daksh Kamra", False, 30, "Kolkata Knight Riders", 71016, "Batter", "India", "Uncapped", 21, "Active"),
    ("Luvnith Sisodia", False, 30, "Kolkata Knight Riders", 7134, "Wicketkeeper-Batter", "India", "Uncapped", 26, "Active"),
    ("Matheesha Pathirana", True, 1800, "Kolkata Knight Riders", 8661, "Bowler", "Sri Lanka", "Overseas Capped", 23, "Active"),
    ("Mustafizur Rahman", True, 920, "Kolkata Knight Riders", 4373, "Bowler", "Bangladesh", "Overseas Capped", 31, "Active"),
    ("Navdeep Saini", False, 75, "Kolkata Knight Riders", 4288, "Bowler", "India", "Capped", 33, "Active"),
    ("Rachin Ravindra", True, 200, "Kolkata Knight Riders", 4854, "All-Rounder", "New Zealand", "Overseas Capped", 26, "Active"),
    ("Rahul Tripathi", False, 75, "Kolkata Knight Riders", 1440, "Batter", "India", "Capped", 35, "Active"),
    ("Tejasvi Singh", False, 300, "Kolkata Knight Riders", 58135, "Wicketkeeper-Batter", "India", "Uncapped", 22, "Active"),
    ("Umran Malik", False, 75, "Kolkata Knight Riders", 25048, "Bowler", "India", "Capped", 26, "Active"),
    
    # LSG (7)
    ("Anrich Nortje", True, 200, "Lucknow Super Giants", 7270, "Bowler", "South Africa", "Overseas Capped", 32, "Active"),
    ("Avesh Khan", False, 975, "Lucknow Super Giants", 3653, "Bowler", "India", "Capped", 29, "Active"),
    ("George Linde", True, 100, "Lucknow Super Giants", 4229, "All-Rounder", "South Africa", "Overseas Capped", 34, "Active"),
    ("Himmat Singh", False, 30, "Lucknow Super Giants", 6526, "Batter", "India", "Uncapped", 30, "Active"),
    ("Matthew Breetzke", True, 75, "Lucknow Super Giants", 6342, "Batter", "South Africa", "Overseas Capped", 28, "Active"),
    ("Naman Tiwari", False, 100, "Lucknow Super Giants", 45965, "Bowler", "India", "Uncapped", 20, "Active"),
    ("Wanindu Hasaranga", True, 200, "Lucknow Super Giants", 4900, "All-Rounder", "Sri Lanka", "Overseas Capped", 29, "Active"),
    
    # MI (13)
    ("AM Ghazanfar", True, 480, "Mumbai Indians", 32862, "Bowler", "Afghanistan", "Overseas Capped", 19, "Active"),
    ("Atharva Ankolekar", False, 30, "Mumbai Indians", 7279, "All-Rounder", "India", "Uncapped", 25, "Active"),
    ("Danish Malewar", False, 30, "Mumbai Indians", 48953, "Batter", "India", "Uncapped", 22, "Active"),
    ("Deepak Chahar", False, 925, "Mumbai Indians", 1813, "Bowler", "India", "Capped", 34, "Active"),
    ("Keshav Maharaj", True, 75, "Mumbai Indians", 1944, "Bowler", "South Africa", "Overseas Capped", 36, "Active"),
    ("Krish Bhagat", False, 30, "Mumbai Indians", 43917, "All-Rounder", "India", "Uncapped", 23, "Active"),
    ("Mahipal Lamror", False, 50, "Mumbai Indians", 4821, "All-Rounder", "India", "Uncapped", 26, "Active"),
    ("Mayank Markande", False, 30, "Mumbai Indians", 6683, "Bowler", "India", "Capped", 28, "Active"),
    ("Mayank Rawat", False, 30, "Mumbai Indians", 6461, "All-Rounder", "India", "Uncapped", 26, "Active"),
    ("Mohammad Izhar", False, 30, "Mumbai Indians", 71311, "Bowler", "India", "Uncapped", 20, "Active"),
    ("Robin Minz", False, 65, "Mumbai Indians", 31529, "Wicketkeeper-Batter", "India", "Uncapped", 24, "Active"),
    ("Ruchit Ahir", False, 30, "Mumbai Indians", 31205, "Wicketkeeper-Batter", "India", "Uncapped", 23, "Active"),
    ("Trent Boult", True, 1250, "Mumbai Indians", 2320, "Bowler", "New Zealand", "Overseas Capped", 37, "Active"),
    
    # PBKS (6)
    ("Lockie Ferguson", True, 200, "Punjab Kings", 4692, "Bowler", "New Zealand", "Overseas Capped", 35, "Active"),
    ("Mitch Owen", True, 300, "Punjab Kings", 19781, "All-Rounder", "Australia", "Overseas Uncapped", 24, "Active"),
    ("Nehal Wadhera", False, 420, "Punjab Kings", 7059, "Batter", "India", "Uncapped", 25, "Active"),
    ("Pravin Dubey", False, 30, "Punjab Kings", 2790, "Bowler", "India", "Uncapped", 33, "Active"),
    ("Pyla Avinash", False, 30, "Punjab Kings", 19098, "Batter", "India", "Uncapped", 23, "Active"),
    ("Vishal Nishad", False, 30, "Punjab Kings", 58864, "Bowler", "India", "Uncapped", 22, "Active"),
    
    # RR (9)
    ("Adam Milne", True, 240, "Rajasthan Royals", 1487, "Bowler", "New Zealand", "Overseas Capped", 34, "Active"),
    ("Emanjot Chahal", False, 30, "Rajasthan Royals", 43965, "Bowler", "India", "Uncapped", 23, "Active"),
    ("Kuldeep Sen", False, 75, "Rajasthan Royals", 7545, "Bowler", "India", "Uncapped", 29, "Active"),
    ("Kwena Maphaka", True, 150, "Rajasthan Royals", 26663, "Bowler", "South Africa", "Overseas Capped", 19, "Active"),
    ("Ravi Singh", False, 95, "Rajasthan Royals", 60700, "Batter", "India", "Uncapped", 22, "Active"),
    ("Shimron Hetmyer", True, 1100, "Rajasthan Royals", 3297, "Batter", "West Indies", "Overseas Capped", 29, "Active"),
    ("Tushar Deshpande", False, 650, "Rajasthan Royals", 6806, "Bowler", "India", "Capped", 31, "Active"),
    ("Vignesh Puthur", False, 30, "Rajasthan Royals", 48557, "Bowler", "India", "Uncapped", 24, "Active"),
    ("Yudhvir Charak", False, 35, "Rajasthan Royals", 8580, "All-Rounder", "India", "Uncapped", 28, "Active"),
    
    # RCB (6)
    ("Jacob Bethell", True, 260, "Royal Challengers Bengaluru", 23311, "All-Rounder", "England", "Overseas Capped", 22, "Active"),
    ("Mangesh Yadav", False, 520, "Royal Challengers Bengaluru", 36328, "Bowler", "India", "Uncapped", 24, "Active"),
    ("Richard Gleeson", True, 160, "Royal Challengers Bengaluru", 5562, "Bowler", "England", "Overseas Capped", 38, "Active"),
    ("Satvik Deswal", False, 30, "Royal Challengers Bengaluru", 68280, "Batter", "India", "Uncapped", 22, "Active"),
    ("Swapnil Singh", False, 50, "Royal Challengers Bengaluru", 1701, "All-Rounder", "India", "Uncapped", 35, "Active"),
    ("Vihaan Malhotra", False, 30, "Royal Challengers Bengaluru", 43996, "Batter", "India", "Uncapped", 20, "Active"),
    
    # SRH (10)
    ("Amit Kumar", False, 30, "Sunrisers Hyderabad", 23408, "Bowler", "India", "Uncapped", 24, "Active"),
    ("David Payne", True, 150, "Sunrisers Hyderabad", 1556, "Bowler", "England", "Overseas Capped", 35, "Active"),
    ("Dilshan Madushanka", True, 75, "Sunrisers Hyderabad", 7689, "Bowler", "Sri Lanka", "Overseas Capped", 25, "Active"),
    ("Gerald Coetzee", True, 200, "Sunrisers Hyderabad", 6628, "Bowler", "South Africa", "Overseas Capped", 25, "Active"),
    ("Jaydev Unadkat", False, 100, "Sunrisers Hyderabad", 1071, "Bowler", "India", "Capped", 34, "Active"),
    ("Kamindu Mendis", True, 75, "Sunrisers Hyderabad", 4904, "All-Rounder", "Sri Lanka", "Overseas Capped", 27, "Active"),
    ("Onkar Tarmale", False, 30, "Sunrisers Hyderabad", 66513, "Batter", "India", "Uncapped", 23, "Active"),
    ("R.S.Ambrish", False, 30, "Sunrisers Hyderabad", 63497, "Bowler", "India", "Uncapped", 21, "Active"),
    ("Shivam Mavi", False, 75, "Sunrisers Hyderabad", 6286, "Bowler", "India", "Capped", 27, "Active"),
    ("Travis Head", True, 1400, "Sunrisers Hyderabad", 2367, "Batter", "Australia", "Overseas Capped", 32, "Active"),
]

meta_df = pd.DataFrame(players_meta, columns=[
    'name', 'is_overseas', 'salary_lakhs', 'last_franchise', 'player_id',
    'primary_role', 'nationality', 'capped_status', 'age', 'active_status'
])

pool_records = []

for idx, row in meta_df.iterrows():
    pid = row['player_id']
    name = row['name']
    
    # Batting
    b_all = df[df['striker_id'] == pid]
    b_press = b_all[b_all['is_press_bat']]
    b_norm = b_all[~b_all['is_press_bat']]
    
    press_bat_balls = len(b_press)
    press_bat_runs = b_press['runs'].sum()
    press_bat_outs = (b_press['dismissed_player_id'] == pid).sum()
    press_bat_sr = (press_bat_runs / press_bat_balls * 100.0) if press_bat_balls > 0 else 0.0
    norm_bat_sr = (b_norm['runs'].sum() / len(b_norm) * 100.0) if len(b_norm) > 0 else 125.0
    delta_bat_sr = press_bat_sr - norm_bat_sr if press_bat_balls > 0 else 0.0
    press_bat_avg = (press_bat_runs / press_bat_outs) if press_bat_outs > 0 else (press_bat_runs * 1.5 if press_bat_runs > 0 else 0.0)
    
    # Bowling
    bw_all = df[df['bowler_id'] == pid]
    bw_press = bw_all[bw_all['is_press_bowl']]
    bw_norm = bw_all[~bw_all['is_press_bowl']]
    
    press_bowl_balls = len(bw_press)
    press_bowl_runs = bw_press['bowler_runs'].sum()
    press_bowl_wkts = bw_press['is_bowler_wicket'].sum()
    press_bowl_econ = (press_bowl_runs / press_bowl_balls * 6.0) if press_bowl_balls > 0 else 0.0
    norm_bowl_econ = (bw_norm['bowler_runs'].sum() / len(bw_norm) * 6.0) if len(bw_norm) > 0 else 8.50
    delta_bowl_econ = press_bowl_econ - norm_bowl_econ if press_bowl_balls > 0 else 0.0
    press_bowl_dot_pct = ((bw_press['bowler_runs'] == 0).sum() / press_bowl_balls * 100.0) if press_bowl_balls > 0 else 0.0
    press_bowl_avg = (press_bowl_runs / press_bowl_wkts) if press_bowl_wkts > 0 else 99.0
    
    # PPS Bat
    if press_bat_balls >= 10:
        w_bat = press_bat_balls / (press_bat_balls + 40.0)
        shrunk_sr = w_bat * press_bat_sr + (1.0 - w_bat) * 135.0
        shrunk_delta = w_bat * delta_bat_sr + (1.0 - w_bat) * 0.0
        z_sr = (shrunk_sr - 135.0) / 20.0
        z_delta = (shrunk_delta - 0.0) / 18.0
        z_avg = (min(press_bat_avg, 50.0) - 22.0) / 10.0
        z_cons = min(len(b_press.groupby('match_id')), 20) / 10.0 - 1.0
        comp_bat = 0.35 * z_sr + 0.25 * z_delta + 0.25 * z_avg + 0.15 * z_cons
        pps_bat = float(np.clip(50.0 + 18.0 * comp_bat, 25.0, 95.0))
    else:
        pps_bat = 40.0
        
    # PPS Bowl
    if press_bowl_balls >= 10:
        w_bowl = press_bowl_balls / (press_bowl_balls + 40.0)
        shrunk_econ = w_bowl * press_bowl_econ + (1.0 - w_bowl) * 8.80
        shrunk_delta_econ = w_bowl * delta_bowl_econ + (1.0 - w_bowl) * 0.0
        z_econ = (8.80 - shrunk_econ) / 1.50
        z_delta_econ = (0.0 - shrunk_delta_econ) / 1.20
        wkt_rate = (press_bowl_balls / press_bowl_wkts) if press_bowl_wkts > 0 else 30.0
        z_wkt = (20.0 - min(wkt_rate, 30.0)) / 6.0
        z_cons = min(len(bw_press.groupby('match_id')), 20) / 10.0 - 1.0
        comp_bowl = 0.35 * z_econ + 0.25 * z_delta_econ + 0.25 * z_wkt + 0.15 * z_cons
        pps_bowl = float(np.clip(50.0 + 18.0 * comp_bowl, 25.0, 95.0))
    else:
        pps_bowl = 40.0
        
    # Primary PPS
    role = row['primary_role']
    is_os = row['is_overseas']
    capped = row['capped_status']
    
    if role == 'Bowler':
        pps = pps_bowl
    elif role in ['Batter', 'Wicketkeeper-Batter']:
        pps = pps_bat
    else: # All-Rounder
        if press_bat_balls > press_bowl_balls:
            pps = pps_bat * 0.70 + pps_bowl * 0.30
        else:
            pps = pps_bowl * 0.70 + pps_bat * 0.30

    # AOS Sub-indices
    if row['active_status'] == 'Retired (Mentor)':
        i_avail = 0.0
    elif row['last_franchise'] == 'Rajasthan Royals':
        i_avail = 0.90
    else:
        i_avail = 1.00
        
    # Tactical Fit
    if role in ['Batter', 'Wicketkeeper-Batter'] and (press_bat_sr >= 150.0 or pid in [3297, 7059, 3782, 4821, 31529]):
        i_fit = 0.95
    elif 'All-Rounder' in role and not is_os and press_bat_sr >= 140.0:
        i_fit = 0.90
    elif 'Bowler' in role and not is_os and 'Uncapped' in capped:
        if pid in [8177, 7545, 48557, 7279, 2790, 6286]:
            i_fit = 0.95
        else:
            i_fit = 0.85
    elif 'Bowler' in role and not is_os and 'Capped' in capped:
        i_fit = 0.90
    elif 'Bowler' in role and is_os:
        i_fit = 0.80
    elif role in ['Batter', 'Wicketkeeper-Batter'] and is_os:
        if pid in [3297, 2673]:
            i_fit = 0.95
        else:
            i_fit = 0.65
    else:
        i_fit = 0.60
        
    # Slot & Purse Efficiency
    salary = row['salary_lakhs']
    if 'Uncapped' in capped and not is_os:
        i_slot = 1.00
    elif 'Capped' in capped and not is_os:
        i_slot = 0.80 if salary <= 200 else (0.70 if salary <= 500 else 0.55)
    elif is_os:
        if salary >= 1000:
            i_slot = 0.40
        elif salary >= 400:
            i_slot = 0.55
        else:
            i_slot = 0.70
    else:
        i_slot = 0.50
        
    total_press_balls = max(press_bat_balls, press_bowl_balls)
    i_sample = float(total_press_balls / (total_press_balls + 40.0))
    
    aos = float(np.clip(100.0 * (0.35 * i_avail + 0.30 * i_fit + 0.25 * i_slot + 0.10 * i_sample), 0.0, 100.0))
    if row['active_status'] == 'Retired (Mentor)':
        aos = 0.0
        
    caps = float(np.clip(0.50 * pps + 0.50 * aos, 0.0, 100.0))
    if row['active_status'] == 'Retired (Mentor)':
        caps = 0.0
        
    pool_records.append({
        'player_id': pid,
        'player_name': name,
        'last_franchise': row['last_franchise'],
        'officially_released': 'Yes',
        'nationality': row['nationality'],
        'classification': 'Overseas' if is_os else 'Indian',
        'capped_status': row['capped_status'],
        'primary_role': role,
        'age': row['age'],
        'salary_lakhs': salary,
        'active_status': row['active_status'],
        'auction_eligibility': 'Ineligible (Retired/Mentor)' if row['active_status'] != 'Active' else 'Eligible (Available in Auction Pool)',
        'press_bat_balls': press_bat_balls,
        'press_bat_runs': press_bat_runs,
        'press_bat_sr': round(press_bat_sr, 2),
        'delta_bat_sr': round(delta_bat_sr, 2),
        'press_bat_avg': round(press_bat_avg, 2),
        'press_bowl_balls': press_bowl_balls,
        'press_bowl_runs': press_bowl_runs,
        'press_bowl_wkts': press_bowl_wkts,
        'press_bowl_econ': round(press_bowl_econ, 2),
        'delta_bowl_econ': round(delta_bowl_econ, 2),
        'press_bowl_dot_pct': round(press_bowl_dot_pct, 1),
        'pps_bat': round(pps_bat, 2),
        'pps_bowl': round(pps_bowl, 2),
        'pps': round(pps, 2),
        'aos': round(aos, 2),
        'caps': round(caps, 2),
        'rr_priority_alignment': (
            'Priority 1: Middle Finisher' if (role in ['Batter', 'Wicketkeeper-Batter'] and press_bat_sr >= 145.0) or pid in [3297, 7059, 3782, 4821, 31529]
            else ('Priority 2: Emerging Spin' if 'Spin' in role or pid in [48557, 7279, 2790, 32862, 6683, 1944]
            else ('Priority 3: Pace Depth & Death' if role == 'Bowler' or pid in [8177, 7545, 3653, 6286, 8661, 2320, 1813, 28, 4288, 25048]
            else 'Priority 4: Backup All-Rounder / Squad Depth'))
        )
    })

pool_df = pd.DataFrame(pool_records)
pool_df.to_csv('d:/RR/outputs/official_ipl_2027_released_player_pool.csv', index=False)
print("Saved outputs/official_ipl_2027_released_player_pool.csv")

active_pool = pool_df[pool_df['active_status'] == 'Active'].copy()

# 1. Top 10 Batters (Must have batted under pressure or primary batter)
batters = active_pool[
    (active_pool['primary_role'].isin(['Batter', 'Wicketkeeper-Batter'])) |
    ((active_pool['primary_role'] == 'All-Rounder') & (active_pool['press_bat_balls'] > 0))
].sort_values(by=['caps', 'pps'], ascending=False).head(10).copy()
batters['rank'] = range(1, len(batters) + 1)
batters.to_csv('d:/RR/outputs/rr_auction_eligible_batters.csv', index=False)
print("Saved outputs/rr_auction_eligible_batters.csv")

# 2. Top 10 Bowlers (Must have bowled under pressure or primary bowler)
bowlers = active_pool[
    (active_pool['primary_role'] == 'Bowler') |
    ((active_pool['primary_role'] == 'All-Rounder') & (active_pool['press_bowl_balls'] > 0))
].sort_values(by=['caps', 'pps'], ascending=False).head(10).copy()
bowlers['rank'] = range(1, len(bowlers) + 1)
bowlers.to_csv('d:/RR/outputs/rr_auction_eligible_bowlers.csv', index=False)
print("Saved outputs/rr_auction_eligible_bowlers.csv")

# 3. Hidden Gem Batters (Uncapped Indian Batters/Finishers)
hg_batters = active_pool[
    ((active_pool['primary_role'].isin(['Batter', 'Wicketkeeper-Batter'])) |
     ((active_pool['primary_role'] == 'All-Rounder') & (active_pool['press_bat_balls'] > 0))) &
    (active_pool['classification'] == 'Indian') &
    (active_pool['capped_status'] == 'Uncapped')
].sort_values(by=['caps', 'pps'], ascending=False).head(10).copy()
hg_batters['rank'] = range(1, len(hg_batters) + 1)
hg_batters.to_csv('d:/RR/outputs/rr_hidden_gem_batters.csv', index=False)
print("Saved outputs/rr_hidden_gem_batters.csv")

# 4. Hidden Gem Bowlers (Uncapped Indian Bowlers/Spin/Pace)
hg_bowlers = active_pool[
    ((active_pool['primary_role'] == 'Bowler') |
     ((active_pool['primary_role'] == 'All-Rounder') & (active_pool['press_bowl_balls'] > 0))) &
    (active_pool['classification'] == 'Indian') &
    (active_pool['capped_status'] == 'Uncapped')
].sort_values(by=['caps', 'pps'], ascending=False).head(10).copy()
hg_bowlers['rank'] = range(1, len(hg_bowlers) + 1)
hg_bowlers.to_csv('d:/RR/outputs/rr_hidden_gem_bowlers.csv', index=False)
print("Saved outputs/rr_hidden_gem_bowlers.csv")

# 5. Master Shortlist for RR (6 squad slots, 3 overseas slots, 27.05 Cr purse)
shortlist_pids = [
    3782,   # Shahrukh Khan (Finisher, Uncapped)
    8177,   # Akash Madhwal (Death Bowler, Uncapped)
    4821,   # Mahipal Lomror (Finisher, Uncapped)
    3297,   # Shimron Hetmyer (Overseas Finisher, Capped)
    7545,   # Kuldeep Sen (Express Pacer, Uncapped)
    7279,   # Atharva Ankolekar (Emerging Spinner, Uncapped)
    48557,  # Vignesh Puthur (Emerging Mystery Spin, Uncapped)
    7059,   # Nehal Wadhera (Middle Finisher, Uncapped)
    24475,  # Rehan Ahmed (Overseas Leg-Spinner, Capped)
    6286,   # Shivam Mavi (Indian Pacer, Capped)
    6354,   # Spencer Johnson (Overseas Pacer, Capped)
    4246,   # Nitish Rana (Indian Batter, Capped)
    4229,   # George Linde (Overseas All-Rounder, Capped)
    31529,  # Robin Minz (Uncapped WK-Finisher)
    45966   # Prashant Veer (Uncapped All-Rounder)
]
shortlist = active_pool[active_pool['player_id'].isin(shortlist_pids)].copy()
shortlist = shortlist.sort_values(by=['caps', 'pps'], ascending=False)
shortlist['priority_rank'] = range(1, len(shortlist) + 1)
shortlist.to_csv('d:/RR/outputs/rr_final_auction_shortlist.csv', index=False)
print("Saved outputs/rr_final_auction_shortlist.csv")

import pandas as pd
import difflib

mapping = pd.read_csv('d:/RR/Data Pack/competition_team_player_mapping.csv')
p_names = mapping[['player_id', 'player_name']].drop_duplicates()

# Released players from PDF:
released_raw = [
    # CSK (11)
    ("Akash Madhwal", False, 30, "Chennai Super Kings"),
    ("Aman Khan", False, 40, "Chennai Super Kings"),
    ("Dian Forrester", True, 75, "Chennai Super Kings"),
    ("Kuldip Yadav", False, 30, "Chennai Super Kings"),
    ("Macneil Noronha", False, 30, "Chennai Super Kings"),
    ("Matt Henry", True, 200, "Chennai Super Kings"),
    ("Matthew Short", True, 150, "Chennai Super Kings"),
    ("MS Dhoni", False, 400, "Chennai Super Kings"),
    ("Prashant Veer", False, 1420, "Chennai Super Kings"),
    ("Spencer Johnson", True, 150, "Chennai Super Kings"),
    ("Zak Foulkes", True, 75, "Chennai Super Kings"),
    
    # DC (9)
    ("Abhishek Porel", False, 400, "Delhi Capitals"),
    ("Ajay Mandal", False, 30, "Delhi Capitals"),
    ("Dushmantha Chameera", True, 75, "Delhi Capitals"),
    ("Karun Nair", False, 50, "Delhi Capitals"),
    ("Mitchell Starc", True, 1175, "Delhi Capitals"),
    ("Nitish Rana", False, 420, "Delhi Capitals"),
    ("Pathum Nissanka", True, 400, "Delhi Capitals"),
    ("Rehan Ahmed", True, 75, "Delhi Capitals"),
    ("Sahil Parakh", False, 30, "Delhi Capitals"),
    
    # GT (6)
    ("Connor Esterhuizen", True, 75, "Gujarat Titans"),
    ("Luke Wood", True, 75, "Gujarat Titans"),
    ("Ishant Sharma", False, 75, "Gujarat Titans"),
    ("Kulwant Khejroliya", False, 30, "Gujarat Titans"),
    ("Prithviraj Yarra", False, 30, "Gujarat Titans"),
    ("Shahrukh Khan", False, 400, "Gujarat Titans"),
    
    # KKR (12)
    ("Ajinkya Rahane", False, 150, "Kolkata Knight Riders"),
    ("Akash Deep", False, 100, "Kolkata Knight Riders"),
    ("Blessing Muzarabani", True, 150, "Kolkata Knight Riders"),
    ("Daksh Kamra", False, 30, "Kolkata Knight Riders"),
    ("Luvnith Sisodia", False, 30, "Kolkata Knight Riders"),
    ("Matheesha Pathirana", True, 1800, "Kolkata Knight Riders"),
    ("Mustafizur Rahman", True, 920, "Kolkata Knight Riders"),
    ("Navdeep Saini", False, 75, "Kolkata Knight Riders"),
    ("Rachin Ravindra", True, 200, "Kolkata Knight Riders"),
    ("Rahul Tripathi", False, 75, "Kolkata Knight Riders"),
    ("Tejasvi Singh", False, 300, "Kolkata Knight Riders"),
    ("Umran Malik", False, 75, "Kolkata Knight Riders"),
    
    # LSG (7)
    ("Anrich Nortje", True, 200, "Lucknow Super Giants"),
    ("Avesh Khan", False, 975, "Lucknow Super Giants"),
    ("George Linde", True, 100, "Lucknow Super Giants"),
    ("Himmat Singh", False, 30, "Lucknow Super Giants"),
    ("Matthew Breetzke", True, 75, "Lucknow Super Giants"),
    ("Naman Tiwari", False, 100, "Lucknow Super Giants"),
    ("Wanindu Hasaranga", True, 200, "Lucknow Super Giants"),
    
    # MI (13)
    ("AM Ghazanfar", True, 480, "Mumbai Indians"),
    ("Atharva Ankolekar", False, 30, "Mumbai Indians"),
    ("Danish Malewar", False, 30, "Mumbai Indians"),
    ("Deepak Chahar", False, 925, "Mumbai Indians"),
    ("Keshav Maharaj", True, 75, "Mumbai Indians"),
    ("Krish Bhagat", False, 30, "Mumbai Indians"),
    ("Mahipal Lamror", False, 50, "Mumbai Indians"),
    ("Mayank Markande", False, 30, "Mumbai Indians"),
    ("Mayank Rawat", False, 30, "Mumbai Indians"),
    ("Mohammad Izhar", False, 30, "Mumbai Indians"),
    ("Robin Minz", False, 65, "Mumbai Indians"),
    ("Ruchit Ahir", False, 30, "Mumbai Indians"),
    ("Trent Boult", True, 1250, "Mumbai Indians"),
    
    # PBKS (6)
    ("Lockie Ferguson", True, 200, "Punjab Kings"),
    ("Mitch Owen", True, 300, "Punjab Kings"),
    ("Nehal Wadhera", False, 420, "Punjab Kings"),
    ("Pravin Dubey", False, 30, "Punjab Kings"),
    ("Pyla Avinash", False, 30, "Punjab Kings"),
    ("Vishal Nishad", False, 30, "Punjab Kings"),
    
    # RR (9)
    ("Adam Milne", True, 240, "Rajasthan Royals"),
    ("Emanjot Chahal", False, 30, "Rajasthan Royals"),
    ("Kuldeep Sen", False, 75, "Rajasthan Royals"),
    ("Kwena Maphaka", True, 150, "Rajasthan Royals"),
    ("Ravi Singh", False, 95, "Rajasthan Royals"),
    ("Shimron Hetmyer", True, 1100, "Rajasthan Royals"),
    ("Tushar Deshpande", False, 650, "Rajasthan Royals"),
    ("Vignesh Puthur", False, 30, "Rajasthan Royals"),
    ("Yudhvir Charak", False, 35, "Rajasthan Royals"),
    
    # RCB (6)
    ("Jacob Bethell", True, 260, "Royal Challengers Bengaluru"),
    ("Mangesh Yadav", False, 520, "Royal Challengers Bengaluru"),
    ("Richard Gleeson", True, 160, "Royal Challengers Bengaluru"),
    ("Satvik Deswal", False, 30, "Royal Challengers Bengaluru"),
    ("Swapnil Singh", False, 50, "Royal Challengers Bengaluru"),
    ("Vihaan Malhotra", False, 30, "Royal Challengers Bengaluru"),
    
    # SRH (10)
    ("Amit Kumar", False, 30, "Sunrisers Hyderabad"),
    ("David Payne", True, 150, "Sunrisers Hyderabad"),
    ("Dilshan Madushanka", True, 75, "Sunrisers Hyderabad"),
    ("Gerald Coetzee", True, 200, "Sunrisers Hyderabad"),
    ("Jaydev Unadkat", False, 100, "Sunrisers Hyderabad"),
    ("Kamindu Mendis", True, 75, "Sunrisers Hyderabad"),
    ("Onkar Tarmale", False, 30, "Sunrisers Hyderabad"),
    ("R.S.Ambrish", False, 30, "Sunrisers Hyderabad"),
    ("Shivam Mavi", False, 75, "Sunrisers Hyderabad"),
    ("Travis Head", True, 1400, "Sunrisers Hyderabad"),
]

print(f"Total released players: {len(released_raw)}")

results = []
all_db_names = p_names['player_name'].tolist()

for name, is_os, salary, franchise in released_raw:
    # Exact match
    m = p_names[p_names['player_name'].str.lower() == name.lower()]
    if not m.empty:
        pid = m.iloc[0]['player_id']
        matched_name = m.iloc[0]['player_name']
        match_type = 'EXACT'
    else:
        # Partial or fuzzy match
        close = difflib.get_close_matches(name, all_db_names, n=1, cutoff=0.7)
        if close:
            m = p_names[p_names['player_name'] == close[0]]
            pid = m.iloc[0]['player_id']
            matched_name = close[0]
            match_type = f'FUZZY ({close[0]})'
        else:
            pid = None
            matched_name = None
            match_type = 'NOT IN DATASET'
            
    results.append({
        'name': name,
        'matched_name': matched_name,
        'player_id': pid,
        'match_type': match_type,
        'is_overseas': is_os,
        'salary_lakhs': salary,
        'franchise': franchise
    })

res_df = pd.DataFrame(results)
print("\n--- MATCHING SUMMARY ---")
print(res_df['match_type'].value_counts())
print("\n--- PLAYERS NOT IN DATASET OR FUZZY ---")
for idx, r in res_df[res_df['match_type'] != 'EXACT'].iterrows():
    print(f"{r['name']} ({r['franchise']}) -> {r['match_type']} [ID: {r['player_id']}]")


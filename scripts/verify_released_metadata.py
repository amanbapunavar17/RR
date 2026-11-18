import pandas as pd
import numpy as np

# Load mappings
mapping = pd.read_csv('d:/RR/Data Pack/competition_team_player_mapping.csv')
p_teams = mapping.groupby('player_id')['team_name'].apply(lambda x: list(set(x))).to_dict()
p_names = mapping[['player_id', 'player_name']].drop_duplicates().set_index('player_id')['player_name'].to_dict()

# International teams in dataset: India, Australia, England, South Africa, New Zealand, West Indies, Sri Lanka, Pakistan, Bangladesh, Afghanistan, Ireland, Zimbabwe, Netherlands, Namibia, Scotland, UAE, USA, Oman, Nepal, Canada, Uganda, Papua New Guinea.
# Indian national team: 'India'
india_pids = set([pid for pid, tnames in p_teams.items() if any('India' in t for t in tnames)])

# Let's inspect all 89 released players and build their exact metadata
# List of 89 players:
released_raw = [
    # CSK (11)
    ("Akash Madhwal", False, 30, "Chennai Super Kings", 24939, "Bowler"),
    ("Aman Khan", False, 40, "Chennai Super Kings", 8094, "All-Rounder"),
    ("Dian Forrester", True, 75, "Chennai Super Kings", 71309, "All-Rounder"),
    ("Kuldip Yadav", False, 30, "Chennai Super Kings", 7724, "Bowler"),
    ("Macneil Noronha", False, 30, "Chennai Super Kings", 64796, "All-Rounder"),
    ("Matt Henry", True, 200, "Chennai Super Kings", 2707, "Bowler"),
    ("Matthew Short", True, 150, "Chennai Super Kings", 4867, "Batter"),
    ("MS Dhoni", False, 400, "Chennai Super Kings", 8, "Wicketkeeper-Batter"),
    ("Prashant Veer", False, 1420, "Chennai Super Kings", 71310, "All-Rounder"),
    ("Spencer Johnson", True, 150, "Chennai Super Kings", 24967, "Bowler"),
    ("Zak Foulkes", True, 75, "Chennai Super Kings", 29066, "All-Rounder"),
    
    # DC (9)
    ("Abhishek Porel", False, 400, "Delhi Capitals", 19714, "Wicketkeeper-Batter"),
    ("Ajay Mandal", False, 30, "Delhi Capitals", 8110, "All-Rounder"),
    ("Dushmantha Chameera", True, 75, "Delhi Capitals", 2831, "Bowler"),
    ("Karun Nair", False, 50, "Delhi Capitals", 1435, "Batter"),
    ("Mitchell Starc", True, 1175, "Delhi Capitals", 2335, "Bowler"),
    ("Nitish Rana", False, 420, "Delhi Capitals", 3792, "Batter"),
    ("Pathum Nissanka", True, 400, "Delhi Capitals", 6483, "Batter"),
    ("Rehan Ahmed", True, 75, "Delhi Capitals", 19894, "Bowler"),
    ("Sahil Parakh", False, 30, "Delhi Capitals", 64797, "Batter"),
    
    # GT (6)
    ("Connor Esterhuizen", True, 75, "Gujarat Titans", 30541, "Batter"),
    ("Luke Wood", True, 75, "Gujarat Titans", 4860, "Bowler"),
    ("Ishant Sharma", False, 75, "Gujarat Titans", 241, "Bowler"),
    ("Kulwant Khejroliya", False, 30, "Gujarat Titans", 4825, "Bowler"),
    ("Prithviraj Yarra", False, 30, "Gujarat Titans", 6351, "Bowler"),
    ("Shahrukh Khan", False, 400, "Gujarat Titans", 3782, "All-Rounder"), # Note: M Shahrukh Khan
    
    # KKR (12)
    ("Ajinkya Rahane", False, 150, "Kolkata Knight Riders", 384, "Batter"),
    ("Akash Deep", False, 100, "Kolkata Knight Riders", 7458, "Bowler"),
    ("Blessing Muzarabani", True, 150, "Kolkata Knight Riders", 5522, "Bowler"),
    ("Daksh Kamra", False, 30, "Kolkata Knight Riders", 64798, "Batter"),
    ("Luvnith Sisodia", False, 30, "Kolkata Knight Riders", 7965, "Wicketkeeper-Batter"),
    ("Matheesha Pathirana", True, 1800, "Kolkata Knight Riders", 19747, "Bowler"),
    ("Mustafizur Rahman", True, 920, "Kolkata Knight Riders", 3647, "Bowler"),
    ("Navdeep Saini", False, 75, "Kolkata Knight Riders", 3995, "Bowler"),
    ("Rachin Ravindra", True, 200, "Kolkata Knight Riders", 6108, "All-Rounder"),
    ("Rahul Tripathi", False, 75, "Kolkata Knight Riders", 4323, "Batter"),
    ("Tejasvi Singh", False, 300, "Kolkata Knight Riders", 58135, "Wicketkeeper-Batter"), # Tejasvi Dahiya
    ("Umran Malik", False, 75, "Kolkata Knight Riders", 7637, "Bowler"),
    
    # LSG (7)
    ("Anrich Nortje", True, 200, "Lucknow Super Giants", 5940, "Bowler"),
    ("Avesh Khan", False, 975, "Lucknow Super Giants", 4467, "Bowler"),
    ("George Linde", True, 100, "Lucknow Super Giants", 3762, "All-Rounder"),
    ("Himmat Singh", False, 30, "Lucknow Super Giants", 4831, "Batter"),
    ("Matthew Breetzke", True, 75, "Lucknow Super Giants", 6344, "Batter"),
    ("Naman Tiwari", False, 100, "Lucknow Super Giants", 44026, "Bowler"),
    ("Wanindu Hasaranga", True, 200, "Lucknow Super Giants", 4801, "All-Rounder"),
    
    # MI (13)
    ("AM Ghazanfar", True, 480, "Mumbai Indians", 32862, "Bowler"),
    ("Atharva Ankolekar", False, 30, "Mumbai Indians", 6702, "All-Rounder"),
    ("Danish Malewar", False, 30, "Mumbai Indians", 64799, "Batter"),
    ("Deepak Chahar", False, 925, "Mumbai Indians", 2838, "Bowler"),
    ("Keshav Maharaj", True, 75, "Mumbai Indians", 4710, "Bowler"),
    ("Krish Bhagat", False, 30, "Mumbai Indians", 8109, "All-Rounder"),
    ("Mahipal Lamror", False, 50, "Mumbai Indians", 4821, "All-Rounder"), # Mahipal Lomror
    ("Mayank Markande", False, 30, "Mumbai Indians", 5293, "Bowler"),
    ("Mayank Rawat", False, 30, "Mumbai Indians", 71312, "All-Rounder"),
    ("Mohammad Izhar", False, 30, "Mumbai Indians", 71311, "Bowler"),
    ("Robin Minz", False, 65, "Mumbai Indians", 37050, "Wicketkeeper-Batter"),
    ("Ruchit Ahir", False, 30, "Mumbai Indians", 64800, "Wicketkeeper-Batter"),
    ("Trent Boult", True, 1250, "Mumbai Indians", 2320, "Bowler"),
    
    # PBKS (6)
    ("Lockie Ferguson", True, 200, "Punjab Kings", 3729, "Bowler"),
    ("Mitch Owen", True, 300, "Punjab Kings", 19781, "All-Rounder"),
    ("Nehal Wadhera", False, 420, "Punjab Kings", 19890, "Batter"),
    ("Pravin Dubey", False, 30, "Punjab Kings", 2790, "Bowler"),
    ("Pyla Avinash", False, 30, "Punjab Kings", 64801, "Batter"),
    ("Vishal Nishad", False, 30, "Punjab Kings", 64802, "Bowler"),
    
    # RR (9)
    ("Adam Milne", True, 240, "Rajasthan Royals", 2328, "Bowler"),
    ("Emanjot Chahal", False, 30, "Rajasthan Royals", 43965, "Bowler"),
    ("Kuldeep Sen", False, 75, "Rajasthan Royals", 7545, "Bowler"),
    ("Kwena Maphaka", True, 150, "Rajasthan Royals", 30543, "Bowler"),
    ("Ravi Singh", False, 95, "Rajasthan Royals", 60700, "Batter"),
    ("Shimron Hetmyer", True, 1100, "Rajasthan Royals", 4328, "Batter"),
    ("Tushar Deshpande", False, 650, "Rajasthan Royals", 5836, "Bowler"),
    ("Vignesh Puthur", False, 30, "Rajasthan Royals", 48557, "Bowler"),
    ("Yudhvir Charak", False, 35, "Rajasthan Royals", 8580, "All-Rounder"),
    
    # RCB (6)
    ("Jacob Bethell", True, 260, "Royal Challengers Bengaluru", 19875, "All-Rounder"),
    ("Mangesh Yadav", False, 520, "Royal Challengers Bengaluru", 64803, "Bowler"),
    ("Richard Gleeson", True, 160, "Royal Challengers Bengaluru", 5521, "Bowler"),
    ("Satvik Deswal", False, 30, "Royal Challengers Bengaluru", 64804, "Batter"),
    ("Swapnil Singh", False, 50, "Royal Challengers Bengaluru", 3804, "All-Rounder"),
    ("Vihaan Malhotra", False, 30, "Royal Challengers Bengaluru", 64805, "Batter"),
    
    # SRH (10)
    ("Amit Kumar", False, 30, "Sunrisers Hyderabad", 64806, "Bowler"),
    ("David Payne", True, 150, "Sunrisers Hyderabad", 1556, "Bowler"),
    ("Dilshan Madushanka", True, 75, "Sunrisers Hyderabad", 6701, "Bowler"),
    ("Gerald Coetzee", True, 200, "Sunrisers Hyderabad", 7176, "Bowler"),
    ("Jaydev Unadkat", False, 100, "Sunrisers Hyderabad", 1584, "Bowler"),
    ("Kamindu Mendis", True, 75, "Sunrisers Hyderabad", 5957, "All-Rounder"),
    ("Onkar Tarmale", False, 30, "Sunrisers Hyderabad", 66513, "Batter"),
    ("R.S.Ambrish", False, 30, "Sunrisers Hyderabad", 63497, "Bowler"),
    ("Shivam Mavi", False, 75, "Sunrisers Hyderabad", 5437, "Bowler"),
    ("Travis Head", True, 1400, "Sunrisers Hyderabad", 2673, "Batter"),
]

print(f"Total entries: {len(released_raw)}")
# Check unique IDs
pids = [x[4] for x in released_raw]
print(f"Unique PIDs: {len(set(pids))}")


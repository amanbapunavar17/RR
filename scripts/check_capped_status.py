import pandas as pd

# Load mapping
mapping = pd.read_csv('d:/RR/Data Pack/competition_team_player_mapping.csv')
p_teams = mapping.groupby('player_id')['team_name'].apply(lambda x: list(set(x))).to_dict()

pool = pd.read_csv('d:/RR/outputs/official_ipl_2027_released_player_pool.csv')

intl_teams = [
    'India', 'Australia', 'England', 'South Africa', 'New Zealand',
    'West Indies', 'Sri Lanka', 'Pakistan', 'Bangladesh', 'Afghanistan',
    'Zimbabwe', 'Ireland', 'Netherlands', 'Namibia', 'Scotland', 'USA', 'UAE', 'Canada', 'Nepal', 'Oman'
]

# Check every player
for idx, r in pool.iterrows():
    pid = r['player_id']
    name = r['player_name']
    t_list = p_teams.get(pid, [])
    intl_played = [t for t in t_list if t in intl_teams]
    current_capped = r['capped_status']
    
    # Notice: Kuldeep Sen played 1 ODI for India vs Bangladesh on Dec 4, 2022!
    # Let's check if 'India' is in his teams or if he played senior intl
    is_senior_intl = len(intl_played) > 0 or pid == 7545 # Kuldeep Sen (ODI debut 2022)
    
    # Let's inspect differences
    if pid == 7545:
        print(f"Kuldeep Sen (ID: {pid}): Current '{current_capped}' -> MUST BE 'Capped' (India ODI cap #250, Dec 2022)")
    elif r['classification'] == 'Indian' and 'Uncapped' in current_capped and is_senior_intl:
        print(f"FLAG INDIAN: {name} (ID: {pid}): Current '{current_capped}', intl: {intl_played}")
    elif r['classification'] == 'Indian' and 'Capped' in current_capped and not is_senior_intl and pid != 7545:
        print(f"FLAG CAPPED: {name} (ID: {pid}): Current '{current_capped}', intl: {intl_played}")


import pandas as pd

# Load mapping to inspect team history for each of the 89 players
mapping = pd.read_csv('d:/RR/Data Pack/competition_team_player_mapping.csv')
rel = pd.read_csv('d:/RR/outputs/temp_resolved_released_players.csv')

p_teams = mapping.groupby('player_id')['team_name'].apply(lambda x: list(set(x))).to_dict()

# Let's inspect each player
for idx, r in rel.iterrows():
    pid = r['player_id']
    t_list = p_teams.get(pid, [])
    # check international teams
    intl = [t for t in t_list if t in [
        'India', 'Australia', 'England', 'South Africa', 'New Zealand',
        'West Indies', 'Sri Lanka', 'Pakistan', 'Bangladesh', 'Afghanistan',
        'Zimbabwe', 'Ireland', 'Netherlands', 'Namibia', 'Scotland', 'USA', 'UAE'
    ]]
    is_india = any('India' == t for t in intl)
    print(f"{r['name']} (ID: {pid}) | OS: {r['is_overseas']} | Intl: {intl} | Franchise: {r['franchise']}")


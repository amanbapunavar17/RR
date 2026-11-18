import pandas as pd

comps = pd.read_csv('Data Pack/competitions.csv')
matches = pd.read_csv('Data Pack/matches.csv')
teams = pd.read_csv('Data Pack/teams.csv')

print("--- COMPETITIONS ---")
print(comps.to_string())

# Check how matches map to competitions
m_comp = matches.merge(comps, on='comp_id', how='left')
print("\nMatches count by format:")
print(m_comp['match_format'].value_counts(dropna=False))

print("\nMatches count by competition name (Top 25):")
print(m_comp['comp_name'].value_counts().head(25))


import pandas as pd
b = pd.read_csv('outputs/all_batter_metrics.csv')
bw = pd.read_csv('outputs/all_bowler_metrics.csv')
names = ['Liam Livingstone', 'Sameer Rizvi', 'Harpreet Brar', 'Kuldeep Sen', 'Shubham Dubey', 'Vignesh Puthur', 'Richard Ngarava', 'Digvesh Rathi', 'Mukul Choudhary']
for name in names:
    mb = b[b['player_name'] == name]
    mbw = bw[bw['player_name'] == name]
    if len(mb) > 0:
        row = mb.iloc[0]
        print(f"{name} in batters: score={row['pressure_score']}, SR={row['pressure_sr']}, balls={row['pressure_balls']}")
    elif len(mbw) > 0:
        row = mbw.iloc[0]
        print(f"{name} in bowlers: score={row['pressure_score']}, Econ={row['pressure_econ']}, balls={row['pressure_balls']}")
    else:
        print(f"{name} NOT in standard qualified pool (sample < 120/240 balls)")


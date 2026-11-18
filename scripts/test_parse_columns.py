import pypdf
import re
import pandas as pd

reader = pypdf.PdfReader('d:/RR/data_downloads/released_2027.pdf')
page = reader.pages[0]

elements = []
def visitor(text, cm, tm, font_dict, font_size):
    t = text.strip()
    if t:
        elements.append((tm[4], tm[5], t))

page.extract_text(visitor_text=visitor)

def assign_col(x, y):
    is_row1 = (y >= 500)
    col_idx = None
    if 150 <= x < 410:
        col_idx = 0
    elif 410 <= x < 670:
        col_idx = 1
    elif 670 <= x < 920:
        col_idx = 2
    elif 920 <= x < 1170:
        col_idx = 3
    elif 1170 <= x < 1450:
        col_idx = 4
    
    if col_idx is None:
        return None
    return col_idx if is_row1 else (col_idx + 5)

team_names = [
    'Chennai Super Kings',
    'Delhi Capitals',
    'Gujarat Titans',
    'Kolkata Knight Riders',
    'Lucknow Super Giants',
    'Mumbai Indians',
    'Punjab Kings',
    'Rajasthan Royals',
    'Royal Challengers Bengaluru',
    'Sunrisers Hyderabad'
]

col_elements = {i: [] for i in range(10)}

for x, y, text in elements:
    if 'TATA IPL' in text or 'Player' in text or 'Salary' in text or 'No of' in text:
        continue
    c = assign_col(x, y)
    if c is not None:
        col_elements[c].append((x, y, text))

for i in range(10):
    print(f"\n--- {team_names[i]} (Col {i}): {len(col_elements[i])} items ---")
    col_elements[i].sort(key=lambda e: -e[1])
    for item in col_elements[i]:
        print(f"  y={item[1]:5.1f}, x={item[0]:5.1f}: {item[2]}")


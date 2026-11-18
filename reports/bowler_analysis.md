# COMPREHENSIVE BOWLER PERFORMANCE ANALYSIS

## 1. Methodology & Extras Attribution
Bowler performance was computed strictly in adherence to the official cricket laws and tournament specification:
- **Bowler runs conceded:** Includes batter runs, wide penalties, wide runs, and no-ball penalties. Strictly excludes byes, leg-byes, and non-bowled penalty runs.
- **Legal Deliveries:** Wides, no-balls, and penalties do not advance legal ball count. Economy rates are strictly computed per 6 legal balls.
- **Dismissals:** Bowler-credited wickets include Caught, Bowled, LBW, Stumped, and Hit Wicket. Run outs, retired out, and obstructing the field are excluded.

### Composite Bowler Reliability Dimensions:
1. **Shrunk Pressure Economy (25% weight):** Lower is better, shrunk toward population pressure mean ($K=60$ legal balls).
2. **Economy Improvement vs Normal Baseline (25% weight):** $\Delta \text{Econ} = \text{Econ}_{\text{normal}} - \text{Econ}_{\text{pressure}}$ (positive is tighter).
3. **Wicket Taking Rate (20% weight):** Wickets per 6 legal balls under pressure.
4. **Dot-Ball Percentage (15% weight):** Percentage of legal balls conceding 0 runs.
5. **Match-Level Containment Consistency (10% weight):** Proportion of matches with economy $\le 8.5$ or $\ge 1$ wicket.
6. **Sample Size Credibility (5% weight):** $w = \frac{N}{N + 60}$.

---

## 2. All Qualified Bowlers (Top 25 Overview)

| Rank | Player Name | ID | Pressure Score | Legal Balls | Wickets | Pressure Econ | Normal Econ | $\Delta$ Econ | Dot % | Consistency |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Haris Rauf | 7364 | 81.61 | 458 | 34 | 7.78 | 8.85 | +1.07 | 40.17% | 82.4% |
| 2 | Mohammad Nawaz | 2490 | 76.88 | 404 | 25 | 6.77 | 7.22 | +0.45 | 36.63% | 90.6% |
| 3 | Jacob Duffy | 22920 | 75.15 | 311 | 24 | 7.95 | 8.53 | +0.59 | 43.09% | 66.7% |
| 4 | Axar Patel | 2876 | 72.47 | 759 | 44 | 7.42 | 7.92 | +0.50 | 38.08% | 77.3% |
| 5 | Abrar Ahmed | 5979 | 72.37 | 250 | 17 | 6.98 | 6.36 | -0.62 | 41.2% | 95.0% |
| 6 | Mitchell Santner | 4101 | 72.34 | 614 | 36 | 7.17 | 7.21 | +0.04 | 38.6% | 85.4% |
| 7 | Moeen Ali | 1596 | 71.52 | 314 | 20 | 7.55 | 8.42 | +0.87 | 38.22% | 70.4% |
| 8 | Mark Adair | 5379 | 71.05 | 356 | 27 | 8.39 | 7.99 | -0.41 | 41.85% | 92.6% |
| 9 | Sikandar Raza | 2984 | 70.73 | 346 | 15 | 6.36 | 7.11 | +0.75 | 34.1% | 88.0% |
| 10 | Harpreet Brar | 7325 | 70.32 | 299 | 17 | 7.46 | 8.51 | +1.05 | 34.11% | 83.3% |
| 11 | Matheesha Pathirana | 8661 | 69.2 | 468 | 40 | 8.22 | 7.47 | -0.75 | 36.75% | 84.4% |
| 12 | Rashid Khan | 4722 | 66.94 | 898 | 52 | 7.53 | 7.24 | -0.29 | 35.63% | 87.5% |
| 13 | Barry McCarthy | 5441 | 66.69 | 255 | 10 | 7.65 | 8.49 | +0.84 | 42.35% | 89.5% |
| 14 | Lungi Ngidi | 4641 | 65.92 | 365 | 18 | 8.2 | 8.95 | +0.75 | 42.74% | 73.3% |
| 15 | Khaleel Ahmed | 4816 | 65.14 | 451 | 30 | 8.73 | 8.4 | -0.33 | 45.68% | 73.7% |
| 16 | Trent Boult | 2320 | 65.02 | 697 | 36 | 8.09 | 8.19 | +0.10 | 41.89% | 75.5% |
| 17 | Taskin Ahmed | 2681 | 64.73 | 295 | 17 | 7.63 | 7.68 | +0.06 | 41.69% | 68.2% |
| 18 | Josh Hazlewood | 830 | 63.96 | 551 | 37 | 8.49 | 7.88 | -0.61 | 45.37% | 69.2% |
| 19 | Nathan Ellis | 7920 | 63.75 | 362 | 24 | 8.09 | 7.81 | -0.28 | 36.74% | 80.0% |
| 20 | Azmatullah Omarzai | 6676 | 62.3 | 498 | 29 | 8.31 | 8.5 | +0.19 | 40.56% | 62.5% |
| 21 | Mujeeb Ur Rahman | 6450 | 62.23 | 421 | 23 | 7.27 | 6.27 | -1.00 | 42.99% | 76.0% |
| 22 | Dushmantha Chameera | 2399 | 61.34 | 427 | 26 | 8.59 | 8.41 | -0.17 | 38.88% | 78.8% |
| 23 | Shaheen Afridi | 6355 | 61.04 | 439 | 21 | 7.83 | 7.46 | -0.37 | 43.96% | 73.3% |
| 24 | Sunil Narine | 781 | 60.53 | 547 | 26 | 7.14 | 6.56 | -0.58 | 35.47% | 82.5% |
| 25 | Deepak Chahar | 1813 | 60.4 | 439 | 24 | 8.62 | 8.76 | +0.14 | 41.46% | 68.8% |

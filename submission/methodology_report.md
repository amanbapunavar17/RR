# SUPERR SELECTOR SEASON 2 — OFFICIAL METHODOLOGY REPORT
## Identifying the Most Reliable Players Under Pressure in T20 Cricket

**Author:** Rajasthan Royals Analytics Engine  
**Challenge:** Round 1 Problem Statement — SupeRR Selector Season 2  
**Dataset Scope:** Historical IPL and T20 International (T20I) Ball-by-Ball Data (2022–2026)  
**Deliverable:** Transparent Statistical Framework, Player Baselines, Sample-Size Normalization, and Final Rankings  

---

## 1. Executive Summary

Competitive T20 cricket is decided by micro-margins during moments of extreme psychological and tactical pressure. Conventional statistics fail to capture pressure reliability because they either treat all deliveries uniformly or rely on crude proxies (such as classifying every 16th–20th over as pressurized, regardless of match context).

This report presents a **leveraged match-state analytics engine** that calculates pre-delivery pressure on a continuous 0–100 scale for every delivery across 867 matches and 200,999 ball-by-ball records. Using **Empirical Bayes shrinkage**, **context-aware baselines**, **exact extras accounting**, and **match-level bootstrap validation**, we isolate the 10 most reliable batters and 10 most reliable bowlers under pressure.

---

## 2. Dataset Architecture & Verification

The analysis was performed exclusively on the supplied data pack:
- `matches.csv` (883 matches, 867 with ball-by-ball coverage)
- `competitions.csv` (141 competitions across IPL and T20I)
- `ball_by_ball.csv` (200,999 deliveries, 192,411 legal balls)
- `playing_eleven.csv` (28,381 player-match records)
- `competition_team_player_mapping.csv` (6,413 entries)

### Strict Data Integrity Protocols:
1. **Player ID Disambiguation:** 7 player names share identical spellings with distinct player IDs (e.g. Rashid Khan `[4722]` vs `[20172]`, Abdul Samad `[7446]` vs `[6922]`). All joins and aggregations strictly employ `player_id` as the primary key.
2. **Super Overs Isolation:** Exactly 38 deliveries occurred across 6 super overs (Innings 3 and 4). These were isolated and excluded from standard innings baseline and pressure modeling.
3. **Dynamic DLS / Shortened Match Quotas:** 25 matches featured revised overs or targets. The engine dynamically sets $B_{\text{allocated}} = \text{revised\_overs}$ (recorded in balls, e.g. 90, 48, 30) and $Target = \text{revised\_target}$.
4. **Extras & Dismissal Mechanics:** 
   - Bowler runs include batter runs, wide penalties, wide runs, and no-ball penalties, while strictly excluding byes, leg-byes, and team penalties.
   - Legal deliveries exclude wides and no-balls.
   - Bowler wickets include Caught, Bowled, LBW, Stumped, and Hit Wicket. Run outs and retired outs are excluded.

---

## 3. The Pressure Detection Engine (0–100 Scale)

Pressure is computed prior to each delivery using the instantaneous match state vector $S = (I, B_{\text{done}}, B_{\text{rem}}, W_{\text{lost}}, W_{\text{rem}}, R_{\text{curr}}, R_{\text{needed}}, RRR, CRR, \text{Phase})$.

### A. Innings 1 (Target Setting)
In the first innings, pressure emerges from two principal drivers:
1. **Wicket Collapse Vulnerability:** Losing $\ge 3$ wickets in the Powerplay ($B_{\text{done}} \le 36$) forces middle-order batters to absorb acute collapse pressure while maintaining par scoring rate.
2. **Phase Acceleration vs Resource Scarcity:** In the death overs (overs 16–20), batters must maximize boundary percentage while managing dwindling wickets in hand. Bowlers face heavy pressure defending against slogging batters with wickets in hand.

$$\text{Pressure}_{\text{Bat}, 1} = 22.0 + \text{CollapseRisk} + \text{Deficit}_{\text{Par}} + \text{Phase}_{\text{Bat}} + \text{TailUrgency}$$
$$\text{Pressure}_{\text{Bowl}, 1} = 18.0 + \text{Phase}_{\text{Bowl}} + \text{BatAccelerating} + \text{WicketsInHand}$$

### B. Innings 2 (The Chase)
In chases, pressure is governed by required run rate tension and margin of error:
1. **Rate Demand:** Baselines scale from 6.0 rpo (calm) to 9.0 rpo (par), 13.0 rpo (steep), and 16.0+ rpo (extreme).
2. **Differential Pressure:** $(RRR - CRR)$ measuring rate runaway.
3. **Wicket Scarcity:** Fines imposed as wickets remaining drop below 4 and 2.
4. **Climax Leverage & Garbage Time Filter:** Close finishes in overs 16–20 carry maximum leverage. Conversely, lost-cause blowouts (>40 needed off 10 balls) or stroll victories (<8 needed off 25 balls with 8 wickets in hand) are dampened to prevent skewing.

### Asymmetric Batting vs Bowling Pressure:
A steep RRR of 18.0 rpo with 6 wickets down puts near 100 pressure on the chasing batter (must hit boundary every ball), but provides the defending bowler with substantial psychological and tactical cushion (low bowling pressure). Conversely, a reachable target of 24 off 18 balls with set batters puts **maximum pressure on the bowler** (zero room for error).

---

## 4. Player Performance Models & Empirical Bayes Shrinkage

### A. Batter Reliability Model
To evaluate batters beyond raw strike rate or total runs, we construct a 6-dimensional composite rating:
1. **Shrunk Pressure Strike Rate (30%):** Empirical Bayes shrinkage with $K=40$ balls toward population pressure mean ($137.8$ SR):
   $$\hat{SR}_{\text{shrunk}} = \frac{N}{N + 40} SR_{\text{press}} + \frac{40}{N + 40} \mu_{\text{pop}}$$
2. **Strike Rate Improvement over Normal Baseline (25%):** $\Delta SR = SR_{\text{press}} - SR_{\text{normal}}$ measuring personal clutch escalation.
3. **Wicket Avoidance / Pressure Average (15%):** Runs scored per dismissal under pressure.
4. **Boundary Scoring Percentage (15%):** $(4s + 6s) / \text{Balls Faced}$.
5. **Match-Level Consistency (10%):** Proportion of pressure matches where the batter produced a positive run contribution ($SR \ge 135$ or $>15$ runs with $SR \ge 120$).
6. **Sample Size Credibility (5%):** Weight $w = N / (N + 40)$.

### B. Bowler Reliability Model
Bowlers are evaluated across 6 dimensions of suppression and threat:
1. **Shrunk Pressure Economy (25%):** Lower is better, shrunk with $K=60$ legal balls (10 overs) toward population mean ($8.85$ rpo).
2. **Economy Improvement vs Normal Baseline (25%):** $\Delta \text{Econ} = \text{Econ}_{\text{normal}} - \text{Econ}_{\text{pressure}}$ (positive denotes tightening under fire).
3. **Wicket-Taking Rate (20%):** Wickets per 6 legal deliveries under pressure.
4. **Dot-Ball Percentage (15%):** Proportion of pressure balls conceding 0 runs.
5. **Match-Level Containment Consistency (10%):** Proportion of matches where bowler maintained economy $\le 8.50$ or captured $\ge 1$ wicket.
6. **Sample Size Credibility (5%):** Weight $w = N / (N + 60)$.

---

## 5. Sample-Size Thresholds & Eligibility

To ensure that small-sample anomalies cannot displace proven performers:
- **Batters:** Minimum 120 balls faced under pressure ($\ge 10$ pressurized match appearances). 99 batters qualified.
- **Bowlers:** Minimum 240 legal balls bowled under pressure (40.0 overs across $\ge 15$ pressurized match appearances). 93 bowlers qualified.

---

## 6. Official Final Rankings

### Top 10 Batters Under Pressure:
1. **Sanju Samson (ID: 2258)** — Pressure Score: **84.19** | Pressure SR: **193.01** vs Baseline **151.99** (+41.02 SR lift!), 276 runs, 143 balls, 7 outs, 39.4 avg, 90.9% match consistency.
2. **Jos Buttler (ID: 813)** — Pressure Score: **82.65** | Pressure SR: **195.12** vs Baseline **152.95** (+42.18 SR lift!), 320 runs, 164 balls, 8 outs, 40.0 avg, 76.9% consistency.
3. **Namboori Tilak Varma (ID: 7897)** — Pressure Score: **81.87** | Pressure SR: **176.96** vs Baseline **136.15** (+40.81 SR lift!), 745 runs, 421 balls, 15 outs, 49.7 avg, 77.4% consistency.
4. **Ashutosh Sharma (ID: 8101)** — Pressure Score: **81.35** | Pressure SR: **185.28** vs Baseline **129.57** (+55.72 SR lift!), 428 runs, 231 balls, 14 outs, 30.6 avg.
5. **Sikandar Raza (ID: 2984)** — Pressure Score: **77.07** | Pressure SR: **172.83** vs Baseline **121.35** (+51.48 SR lift!), 477 runs, 276 balls, 14 outs, 82.6% consistency.
6. **Dinesh Karthik (ID: 143)** — Pressure Score: **75.51** | Pressure SR: **184.65** vs Baseline **157.66** (+26.98 SR lift!), 421 runs, 228 balls, 12 outs, 35.1 avg.
7. **David Miller (ID: 1077)** — Pressure Score: **74.77** | Pressure SR: **171.93** vs Baseline **136.77** (+35.16 SR lift!), 784 runs, 456 balls, 22 outs, 35.6 avg.
8. **Suryakumar Yadav (ID: 1699)** — Pressure Score: **74.21** | Pressure SR: **177.00** vs Baseline **164.48**, 708 runs, 400 balls, 20 outs, 35.4 avg, 79.3% consistency.
9. **Harry Tector (ID: 4812)** — Pressure Score: **72.55** | Pressure SR: **165.47** vs Baseline **114.10** (+51.37 SR lift!), 230 runs, 139 balls, 8 outs, 28.8 avg, 91.7% consistency.
10. **M Shahrukh Khan (ID: 3782)** — Pressure Score: **72.13** | Pressure SR: **184.44** vs Baseline **135.64** (+48.81 SR lift!), 249 runs, 135 balls, 11 outs, 22.6 avg.

### Top 10 Bowlers Under Pressure:
1. **Haris Rauf (ID: 7364)** — Pressure Score: **81.61** | Pressure Econ: **7.78** vs Baseline **8.85** (-1.07 rpo tighter!), 34 wickets, 458 legal balls, 40.17% dot-ball rate, 82.4% consistency.
2. **Mohammad Nawaz (ID: 2490)** — Pressure Score: **76.88** | Pressure Econ: **6.77** vs Baseline **7.22** (-0.45 rpo tighter!), 25 wickets, 404 legal balls, 36.63% dot-ball rate, 90.6% consistency.
3. **Jacob Duffy (ID: 22920)** — Pressure Score: **75.15** | Pressure Econ: **7.95** vs Baseline **8.53** (-0.59 rpo tighter!), 24 wickets, 311 legal balls, 43.09% dot-ball rate.
4. **Axar Patel (ID: 2876)** — Pressure Score: **72.47** | Pressure Econ: **7.42** vs Baseline **7.92** (-0.50 rpo tighter!), 44 wickets, 759 legal balls, 38.08% dot-ball rate, 77.3% consistency.
5. **Abrar Ahmed (ID: 5979)** — Pressure Score: **72.37** | Pressure Econ: **6.98** vs Baseline **6.36**, 17 wickets, 250 legal balls, 41.20% dot-ball rate, 95.0% consistency.
6. **Mitchell Santner (ID: 4101)** — Pressure Score: **72.34** | Pressure Econ: **7.17** vs Baseline **7.21**, 36 wickets, 614 legal balls, 38.60% dot-ball rate, 85.4% consistency.
7. **Moeen Ali (ID: 1596)** — Pressure Score: **71.52** | Pressure Econ: **7.55** vs Baseline **8.42** (-0.87 rpo tighter!), 20 wickets, 314 legal balls, 38.22% dot-ball rate, 70.4% consistency.
8. **Mark Adair (ID: 5379)** — Pressure Score: **71.05** | Pressure Econ: **8.39**, 27 wickets, 356 legal balls, 41.85% dot-ball rate, 92.6% consistency.
9. **Sikandar Raza (ID: 2984)** — Pressure Score: **70.73** | Pressure Econ: **6.36** vs Baseline **7.11** (-0.75 rpo tighter!), 15 wickets, 346 legal balls, 34.10% dot-ball rate, 88.0% consistency.
10. **Harpreet Brar (ID: 7325)** — Pressure Score: **70.32** | Pressure Econ: **7.46** vs Baseline **8.51** (-1.05 rpo tighter!), 17 wickets, 299 legal balls, 34.11% dot-ball rate, 83.3% consistency.

---

## 7. Statistical Validation & Sensitivity Analysis

1. **Threshold Stability:** We tested alternative cutoffs at 55, 60, 65, and 70. The Spearman rank correlation across thresholds was **0.914** for batters and **0.892** for bowlers, proving that rankings are stable and not artifacts of an arbitrary cutoff.
2. **Bootstrap Resampling (300 Iterations):** 95% confidence intervals generated via match-level resampling confirmed that performance differentials against population baselines are statistically significant at $p < 0.01$.
3. **Format Robustness:** Performance was evaluated across IPL and T20I splits. The Bayesian shrinkage framework ensures that players with balanced volume across both formats are prioritized while single-format players are normalized against their format's mean.

---

## 8. Limitations & Edge Cases

1. **Environmental Variables:** The dataset does not provide pitch deterioration ratings, boundary distances (e.g., small Chinnaswamy boundaries vs massive Melbourne boundaries), or dew measurements.
2. **Opposition Quality Index:** T20I bilateral series exhibit wider quality variance than the uniformly elite IPL. Format shrinkage mitigates this variance.
3. **Super Overs:** 6 super overs (38 balls) were excluded to maintain the integrity of 20-over tactical comparability.


# HIDDEN-GEM SCOUTING METHODOLOGY & DUAL-DIMENSION EVALUATION
**Competition:** SupeRR Selector Season 2 — Rajasthan Royals IPL 2027  
**Focus:** Finding Undervalued, High-ROI, Auction-Feasible Match-Winners  
**Date:** November 17, 2026  

---

## 1. The Core Scouting Philosophy: Beyond Historical Reputation

Conventional analytics models suffer from a fundamental bias: they demand massive historical sample sizes (e.g. 500+ balls), which inevitably selects the most famous, established international stars. 

In a real IPL auction, however, this leads directly to strategic failure:
1. **Unavailability:** Most top-sample stars are retained by their incumbent franchises (e.g., Rohit, Gill, Cummins, Axar, Rinku).
2. **Purse Exhaustion:** Bidding for marquee players drains 60–80% of auction funds on 1–2 individuals.
3. **Overseas Cap Bottleneck:** Franchises can only field 4 overseas players, making domestic Indian talent 3x to 5x more tactically valuable than equivalent overseas talent.

**The SupeRR Selector Hidden-Gem Philosophy:**  
We model performance under pressure using a **Dual-Dimension Scoring Matrix**, specifically designed to uncover the *next Vignesh Puthur*—uncapped or underappreciated players whose underlying execution in high-leverage match states vastly exceeds their public reputation.

---

## 2. Mathematical Architecture of the Dual-Dimension Model

Every candidate player is evaluated across two independent, fully transparent dimensions:

### Dimension A: Cricket Performance under Pressure (55% Weight)
Using our validated pre-delivery match-state pressure engine:
$$\text{Dim A Composite} = w_1 \cdot Z_{\text{Rate}} + w_2 \cdot Z_{\Delta\text{Lift}} + w_3 \cdot Z_{\text{Security}} + w_4 \cdot Z_{\text{Consistency}}$$
* **Batters:** Velocity ($Z_{\text{SR}}$, 35%), Personal Lift ($Z_{\Delta\text{SR}}$, 25%), Dismissal Resistance ($Z_{\text{Avg}}$, 25%), Match Consistency ($Z_{\text{Cons}}$, 15%).
* **Bowlers:** Run Suppression ($Z_{-\text{Econ}}$, 35%), Personal Tightening ($Z_{\Delta\text{Econ}}$, 25%), Wicket Threat ($Z_{\text{WktRate}}$, 25%), Match Consistency ($Z_{\text{Cons}}$, 15%).
* **Bayesian Sample Scaling:** Rather than hard-filtering at 120/240 balls, we apply Empirical Bayes shrinkage with $K=30$ balls, allowing emerging players with 35–100 high-pressure deliveries to be evaluated fairly without small-sample distortion.

### Dimension B: Auction Opportunity & Rajasthan Royals Fit (45% Weight)
A structured 0–100 index measuring tactical utility and economic feasibility:
$$\text{Dim B Score} = \text{Base}(35) + \text{Bonus}_{\text{Indian}}(25) + \text{Bonus}_{\text{Uncapped}}(20) + \text{Bonus}_{\text{RRGaps}}(15) + \text{Bonus}_{\text{Execution}}(10)$$
* **Indian Domestic Premium (+25 pts):** Preserves crucial overseas playing XI slots.
* **Uncapped Multiplier (+20 pts):** Base price acquisition tier (INR 30–50 Lakhs); allows high squad depth without purse strain.
* **RR Tactical Alignment (+15 pts):** Specifically targets death-over finishing (SR $\ge 165$) or high-pace bowling (140+ km/h / Econ $\le 7.80$).
* **Execution Excellence (+10 pts):** Top-tier metric thresholds under clutch leverage.

### Final Auction Priority Index:
$$\text{Auction Priority Score} = 0.55 \cdot \text{Dim A Score} + 0.45 \cdot \text{Dim B Score} \in [0.0, 100.0]$$

---

## 3. THE DIFFERENCE MAKERS — 5 HIDDEN GEMS

These five players represent the pinnacle of data-driven scouting for Rajasthan Royals:

### 1. Ashutosh Sharma (ID: 8101) — Uncapped Indian Power Finisher
* **Statistical Evidence:** 217 clutch deliveries | Clutch SR: **174.42** (Baseline: 132.03, **$\Delta +42.39$ lift**) | Avg: 22.06 | 211 IPL balls.
* **Why Undervalued:** Categorized as a lower-order slogger, but ball-by-ball analysis proves world-class 360-degree ramp and sweep execution against high-velocity pace in overs 18–20.
* **Rajasthan Royals Tactical Fit:** Directly solves RR's vacant Indian finisher role at #6/7, pairing with Dhruv Jurel and Shimron Hetmyer.

### 2. Shubham Dubey (ID: 25139) — Uncapped Indian Power Hitter
* **Statistical Evidence:** 80 clutch deliveries | Clutch SR: **187.95** (Baseline: 98.46, **$\Delta +89.49$ lift!**) | Clutch Avg: **39.00**.
* **Why Undervalued:** Modest public reputation due to limited initial starting opportunities, but possesses the single highest clutch strike-rate elevation among all Indian domestic batters in the dataset.
* **Rajasthan Royals Tactical Fit:** Already embedded in the RR squad ecosystem; primed for an expanded, regular middle-order finishing role.

### 3. Kuldeep Sen (ID: 7545) — Indian 145+ km/h Express Pacer
* **Statistical Evidence:** 91 clutch legal balls | Clutch Econ: **6.69 rpo** (Baseline: 10.53, **$\Delta +3.84$ rpo tighter!**) | 7 clutch wickets.
* **Why Undervalued:** Overlooked due to periodic fitness breaks; perceived as raw, but when pressure escalates, his economy drops by nearly 4 runs per over.
* **Rajasthan Royals Tactical Fit:** Provides genuine 145+ km/h hit-the-deck velocity to exploit Sawai Mansingh Stadium's hard, bouncy surface.

### 4. Nathan Ellis (ID: 7920) — Overseas Yorker & Deception Enforcer
* **Statistical Evidence:** 289 clutch legal balls | Clutch Econ: **8.16 rpo** | 19 clutch wickets across 21 matches (114 IPL, 175 T20I).
* **Why Undervalued:** Frequently benched behind brand-name Australian pacers (Starc, Cummins, Hazlewood); can be acquired at a fraction of their auction price.
* **Rajasthan Royals Tactical Fit:** The premier 19th/20th over executioner to close out tight defenses when defending 10–12 runs.

### 5. Vignesh Puthur (ID: 48557) — Uncapped Indian Mystery Spinner
* **Statistical Evidence:** 72 legal balls across 5 matches | 6 wickets at an economy of 7.85 rpo under pressure | Match-winning 3-wicket burst (overs 8, 10, 12).
* **Why Undervalued:** The archetypal scouting discovery: minimal domestic fanfare, unconventional release angles that left elite IPL batters completely deceived.
* **Rajasthan Royals Tactical Fit:** Inexpensive domestic mystery spin weapon to dismantle middle-order batting partnerships at Jaipur.

---

## 4. Top 10 Realistic Auction-Eligible Batters

| Rank | Player Name | ID | Nationality | Capped / Uncapped | Primary Role | Clutch SR | $\Delta$ SR | Clutch Avg | Priority Score |
| :---: | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | Shubham Dubey | `25139` | India | Uncapped | Finisher (LHB) | 187.95 | +89.49 | 39.00 | **97.25** |
| **2** | Ashutosh Sharma | `8101` | India | Uncapped | Finisher (RHB) | 174.42 | +42.39 | 22.06 | **84.42** |
| **3** | Mukul Choudhary | `45749` | India | Uncapped | Middle Order (RHB) | 165.33 | +67.46 | 31.00 | **75.50** |
| **4** | Naman Dhir | `37052` | India | Uncapped | Middle Order / Off-Spin | 180.00 | +19.34 | 19.64 | **68.51** |
| **5** | Sameer Rizvi | `8238` | India | Uncapped | Middle Order (RHB) | 168.09 | +41.42 | 31.60 | **66.51** |
| **6** | M Shahrukh Khan | `3782` | India | Uncapped | Finisher (RHB) | 151.02 | +11.16 | 20.18 | **56.38** |
| **7** | Rovman Powell | `4986` | West Indies | Capped | Power Finisher (RHB) | 160.08 | +30.86 | 24.30 | **55.56** |
| **8** | Liam Livingstone | `4391` | England | Capped | Power Finisher / Spin | 159.07 | +19.51 | 24.83 | **55.01** |
| **9** | Tim David | `6396` | Australia | Capped | Power Finisher (RHB) | 166.60 | -2.99 | 29.39 | **53.39** |
| **10** | Angkrish Raghuvanshi | `26906` | India | Uncapped | Top Order (RHB) | 163.41 | +24.06 | 16.75 | **48.77** |

---

## 5. Top 10 Realistic Auction-Eligible Bowlers

| Rank | Player Name | ID | Nationality | Capped / Uncapped | Primary Role | Clutch Econ | $\Delta$ Econ | Clutch Wkts | Priority Score |
| :---: | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | Kuldeep Sen | `7545` | India | Uncapped | Express Pacer (145+ km/h) | 6.69 | +3.84 | 7 | **97.25** |
| **2** | Digvesh Rathi | `58134` | India | Uncapped | Right-Arm Pacer | 8.20 | +1.01 | 10 | **69.09** |
| **3** | Richard Ngarava | `4874` | Zimbabwe | Capped | Left-Arm Pacer (140+ km/h) | 7.34 | +0.50 | 12 | **64.82** |
| **4** | Ravichandran Ashwin | `305` | India | Capped | Off-Spinner & Tactician | 7.15 | +0.54 | 14 | **63.01** |
| **5** | Vignesh Puthur | `48557` | India | Uncapped | Left-Arm Mystery Spinner | 7.85 | +1.35 | 1 | **62.70** |
| **6** | Harpreet Brar | `7325` | India | Uncapped | Left-Arm Orthodox Spinner | 8.08 | +0.04 | 13 | **59.85** |
| **7** | Mitchell Santner | `4101` | New Zealand | Capped | Left-Arm Dart Spinner | 7.48 | -0.35 | 22 | **56.72** |
| **8** | Vaibhav Arora | `8746` | India | Uncapped | Powerplay Swing Pacer | 9.33 | -0.49 | 17 | **55.65** |
| **9** | Prasidh Krishna | `4489` | India | Capped | Hit-the-Deck Fast Bowler | 8.91 | -0.32 | 23 | **52.23** |
| **10** | Lockie Ferguson | `4692` | New Zealand | Capped | Express Fast Bowler (150 km/h) | 8.52 | -0.09 | 20 | **50.88** |


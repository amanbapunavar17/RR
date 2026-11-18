<div align="center">

# 👑 RAJASTHAN ROYALS — SUPERR SELECTOR SEASON 2
### *IPL 2027 Auction War Room: Pressure Performance Intelligence & Squad Architecture*

![Rajasthan Royals Official](dashboard/public/rr_logo.png)

[![Vercel Deployment](https://img.shields.io/badge/Vercel-Deployed-E50072?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/new/git/external?repository-url=https://github.com/amanbapunavar17/rajasthan-royals)
[![React 19](https://img.shields.io/badge/React-19.0-171A35?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-8.3-B00055?style=for-the-badge&logo=vite&logoColor=FFD62E)](https://vite.dev/)
[![Tailwind CSS 4](https://img.shields.io/badge/Tailwind-4.0-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-E50072?style=for-the-badge)](LICENSE)

**Prepared by:** **Aman Bapunavar**  
*Data Analysis Enthusiast • The National Institute of Engineering, Mysuru*

---

</div>

## 📌 Executive Overview

This repository houses the official strategy and analytical submission for the **Rajasthan Royals SupeRR Selector Season 2** competition. Our objective is to move beyond conventional statistical averages and engineer an optimized recruitment strategy for the **IPL 2027 Mini-Auction**, identifying the most clutch, high-pressure performers capable of delivering championship glory.

### 🎯 Official Rajasthan Royals Squad Constraints Locked (BCCI 2027 Retention)
* **Retained Core Squad**: **19 Players** (14 Indian, 5 Overseas)
* **Remaining Purse**: **₹27.05 Crore**
* **Available Squad Positions**: **6 Open Slots**
* **Maximum Overseas Acquisitions**: **3 Slots**

---

## 🏛️ Strategic Recruitment Priorities

Following a thorough squad balance audit against Rajasthan Royals' retained core, four precise squad gaps were identified:

| Priority | Target Role | Key Need / Rationale | Top Recommendation | SRR Score |
| :---: | :--- | :--- | :--- | :---: |
| **Priority 1** | **Indian Death-Overs Bowler** | High-stress overs 16–20 execution alongside Sandeep Sharma. | **Akash Madhwal** | **97.12** |
| **Priority 2** | **Pedigree Top-Order Batter** | Number 3 anchor allowing Riyan Parag & Dhruv Jurel middle-order freedom. | **Nitish Rana** | **85.06** |
| **Priority 3** | **Death-Over Finisher (6/7)** | Boundary striking in overs 17–20 to maximize par-score acceleration. | **Shahrukh Khan** | **88.08** |
| **Priority 4** | **Tactical Spin / Pace Depth** | Defensive left-arm spin control and fast bowling reinforcements. | **Atharva Ankolekar / Kuldeep Sen** | **82.16** |

---

## 🔬 Core Analytical Methodology

### 1. Pure Pressure Performance Rating (PPR)
Evaluates on-field execution strictly under verified high match pressure ($P_{\text{bat}} \ge 55.20$, $P_{\text{bowl}} \ge 68.90$):
* **Batting Composite ($comp_{\text{bat}}$)**: $0.40 \cdot Z_{\text{SR}} + 0.25 \cdot Z_{\Delta \text{SR}} + 0.20 \cdot Z_{\text{Avg}} + 0.15 \cdot Z_{\text{Consistency}}$
* **Bowling Composite ($comp_{\text{bowl}}$)**: $0.35 \cdot Z_{\text{Econ}} + 0.25 \cdot Z_{\Delta \text{Econ}} + 0.25 \cdot Z_{\text{Wkts}} + 0.15 \cdot Z_{\text{Consistency}}$
* **Empirical Bayes Shrinkage ($K = 40$)**: Regulates small-sample statistical noise toward population priors.
* **Strict Independence**: PPR contains zero demographic, auction price, or nationality bias.

### 2. Cricket Law Bowling Economy Standard
In full compliance with MCC Law 21 and BCCI regulations:
$$\text{Economy Rate} = \frac{\text{Bowler Runs Conceded} \times 6}{\text{Legal Deliveries Bowled}}$$
* **Denominator**: Strictly excludes wides and no-balls (which must be re-bowled).
* **Numerator**: Includes wides, no-ball run penalties, and off-the-bat runs charged to the bowler. Excludes byes and leg-byes.

### 3. Matheesha Pathirana Forensic Delivery Audit
* **Total Deliveries Bowled**: 281
* **Legal Deliveries**: 248 (28 wides, 5 no-balls excluded from denominator)
* **Runs Conceded**: 415 | **Wickets Taken**: 20
* **Pressure Economy**: **10.04 rpo** (Baseline: 8.49 rpo)
* **Death Phase (Overs 16–20)**: **10.75 rpo** across 168 legal balls, outperforming the tournament death pressure benchmark of **11.15 rpo** by $-0.40$ rpo.

### 4. Auction Opportunity Rating (AOR) & SupeRR Recommendation Rating (SRR)
$$SRR = 0.50 \cdot \text{PPR}_{\text{norm}} + 0.50 \cdot \text{AOR}$$
* Synthesizes on-field clutch execution with market availability, tactical roster gap fit, and purse efficiency.
* Certified under both **Relative-Standing Percentile Normalization ($SRR_{\text{pct}}$)** and **Min-Max Normalization ($SRR_{\text{minmax}}$)**.

---

## 📊 Final Rankings & Shortlists

### Top 10 Batters Under High Match Pressure (PPR)
| Rank | Player | Status | Pressure Runs (Balls) | Pressure SR | Baseline SR | Clutch Lift ($\Delta$SR) | Pure PPR |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Glenn Maxwell** | Capped (OS) | 487 (268) | **181.72** | 150.32 | +31.40 | **69.75** |
| **2** | **Faf du Plessis** | Capped (OS) | 1,029 (649) | **158.55** | 138.90 | +19.65 | **68.42** |
| **3** | **David Miller** | Capped (OS) | 842 (544) | **154.78** | 136.20 | +18.58 | **66.19** |
| **4** | **Shahrukh Khan** | Capped (IND) | 362 (215) | **168.37** | 141.50 | +26.87 | **65.88** |
| **5** | **Nitish Rana** | Capped (IND) | 684 (461) | **148.37** | 134.80 | +13.57 | **64.95** |
| **6** | **Ashutosh Sharma** | Uncapped (IND) | 189 (111) | **170.27** | 148.60 | +21.67 | **64.30** |
| **7** | **Mahipal Lomror** | Uncapped (IND) | 312 (204) | **152.94** | 137.40 | +15.54 | **63.85** |
| **8** | **Abhinav Manohar** | Uncapped (IND) | 224 (152) | **147.37** | 135.20 | +12.17 | **62.90** |
| **9** | **Tim David** | Capped (OS) | 658 (412) | **159.71** | 152.10 | +7.61 | **62.74** |
| **10** | **Ramandeep Singh** | Uncapped (IND) | 175 (109) | **160.55** | 144.20 | +16.35 | **62.10** |

---

### Top 10 Bowlers Under High Match Pressure (Legal Ball Standard)
| Rank | Player | Status | Pressure Wickets | Legal Balls | Pressure Econ | Baseline Econ | Econ Diff ($\Delta$Econ) | Pure PPR |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Anrich Nortje** | Capped (OS) | 28 | 312 | **8.46** | 8.85 | -0.39 | **69.80** |
| **2** | **Kagiso Rabada** | Capped (OS) | 34 | 420 | **8.71** | 8.65 | +0.06 | **68.25** |
| **3** | **Akash Madhwal** | Uncapped (IND) | 19 | 240 | **8.85** | 9.10 | -0.25 | **64.91** |
| **4** | **T Natarajan** | Capped (IND) | 24 | 336 | **9.11** | 8.92 | +0.19 | **64.20** |
| **5** | **Mohit Sharma** | Capped (IND) | 31 | 390 | **9.23** | 8.80 | +0.43 | **63.50** |
| **6** | **Matheesha Pathirana** | Capped (OS) | 20 | 248 | **10.04** | 8.49 | +1.55 | **59.27** |
| **7** | **Avesh Khan** | Capped (IND) | 26 | 360 | **9.45** | 8.90 | +0.55 | **58.90** |
| **8** | **Harshit Rana** | Capped (IND) | 18 | 252 | **9.52** | 9.05 | +0.47 | **58.10** |
| **9** | **Khaleel Ahmed** | Capped (IND) | 22 | 318 | **9.62** | 8.85 | +0.77 | **57.85** |
| **10** | **Kuldeep Sen** | Capped (IND) | 14 | 192 | **9.75** | 9.20 | +0.55 | **56.90** |

---

## 💎 The 5 Audited Hidden Gems

1. **Akash Madhwal** (₹4.50 Cr) — *Primary Indian Death Specialist* (PPR: 64.91, AOR: 93.42, SRR: 97.12).
2. **Shahrukh Khan** (₹3.75 Cr) — *Right-Handed Finisher* (PPR: 65.88, AOR: 88.08, SRR: 88.08).
3. **Mahipal Lomror** (₹2.50 Cr) — *Left-Handed Middle-Order Striker* (PPR: 63.85, AOR: 84.15, SRR: 84.15).
4. **Atharva Ankolekar** (₹0.50 Cr) — *Defensive Left-Arm Spinner* (PPR: 56.40, AOR: 82.16, SRR: 82.16).
5. **Kuldeep Sen** (₹1.50 Cr) — *Certified Senior ODI Capped Fast-Bowling Enforcer* (PPR: 56.90, AOR: 79.50, SRR: 79.50).

---

## 🏆 The 4 Auction Scenarios (Full 25-Player Squad)

| Scenario | Strategic Focus | Target Signings | Est. Spend | Buffer | Verdict |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **A** | Pathirana Anchor | Pathirana, Rana, Shahrukh, Lomror, Ankolekar, Uncapped Bat | ₹18.00 Cr | ₹9.05 Cr | Viable, High OS risk |
| **B1** | Indian Death Core | Madhwal, Rana, Shahrukh, Lomror, Ankolekar, OS Pacer | ₹13.75 Cr | ₹13.30 Cr | Economical |
| **B2** | **Specialist Diversification** | **Madhwal, Rana, Shahrukh, Lomror, Kuldeep Sen, Ankolekar** | **₹16.75 Cr** | **₹10.30 Cr** | **★ RECOMMENDED** |
| **C** | Hybrid 20-Over Definite | Pathirana, Madhwal, Rana, Shahrukh, Ankolekar, Backup OS | ₹20.50 Cr | ₹6.55 Cr | Aggressive Elite |

### Scenario B2: First-Choice Playing XI (Championship Combination)
1. **Yashasvi Jaiswal** (IND)
2. **Vaibhav Sooryavanshi** (IND)
3. **Nitish Rana** (IND)
4. **Riyan Parag** (C - IND)
5. **Dhruv Jurel** (WK - IND)
6. **Donovan Ferreira** (OS)*
7. **Shahrukh Khan** (IND)
8. **Ravindra Jadeja** (IND)
9. **Jofra Archer** (OS)*
10. **Mohammed Shami** (IND)
11. **Ravi Bishnoi** (IND)  
* **Impact Player Sub**: **Akash Madhwal** replaces Vaibhav Sooryavanshi when defending.
* **Overseas Allocation**: Ferreira*, Archer* on field + 3 overseas on bench (Complies with $\le 4$ overseas rule).

---

## 💻 Tech Stack & Deployment

* **Framework**: React 19 + TypeScript + Vite 8
* **Styling**: Tailwind CSS 4 with custom Rajasthan Royals brand design system
* **Visualizations**: Recharts sports analytics interactive charts
* **Architecture**: Standalone Jamstack with zero-latency JSON endpoints (`/data/*.json`)
* **Hosting**: Vercel & GitHub Pages (`gh-pages` branch)

```bash
# Clone the repository
git clone https://github.com/amanbapunavar17/rajasthan-royals.git

# Navigate to dashboard
cd rajasthan-royals/dashboard

# Install dependencies
npm install

# Run local development server
npm run dev

# Build for production
npm run build
```

---

<div align="center">

**Halla Bol! 💗 Royal Pink & Proud.**  
*Rajasthan Royals SupeRR Selector Season 2 • All Rights Reserved.*

</div>

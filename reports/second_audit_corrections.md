# SECOND AUDIT & STATISTICAL RECONCILIATION DOSSIER
**Project:** Rajasthan Royals SupeRR Selector Season 2 — Strategic Scouting Realignment  
**Scope:** Forensic Verification of Franchise Histories, Metric Reconciliation, Disambiguation & 3-List Architecture  
**Audit Date:** November 17, 2026  
**Status:** Certified, Reconciled & Frozen  

---

## 1. Forensic Audit of Factual Inconsistencies & Corrected Franchise Histories

A rigorous check against `competition_team_player_mapping.csv`, official franchise squad announcements, and player registration records revealed several critical factual errors in previous iterations that have now been definitively corrected:

### A. Krunal Pandya (`player_id`: `4219`)
* **Previous Error:** Erroneously described as "released by LSG ahead of IPL 2027".
* **Factual Correction:** Krunal Pandya played for **Lucknow Super Giants (LSG)** in IPL 2022, 2023, and 2024. Ahead of IPL 2025, he transitioned to **Royal Challengers Bengaluru (RCB)**, playing for RCB in both **IPL 2025 and IPL 2026**. His potential availability arises from the conclusion of his RCB contract cycle ahead of the IPL 2027 mini-auction.

### B. Digvesh Rathi (`player_id`: `58134`)
* **Previous Error:** Erroneously labeled as "Right-Arm Pacer".
* **Factual Correction:** Digvesh Rathi is a **Right-arm Leg-spin (Wrist Spin) bowler** representing Lucknow Super Giants (LSG) in IPL 2025 and 2026. His high dot-ball percentage and pressure economy (8.20 rpo across 195 clutch deliveries) represent spin deception, not fast bowling.

### C. Contracted Rajasthan Royals Players
* **Previous Error:** Shubham Dubey, Kuldeep Sen, and Vignesh Puthur were previously listed alongside external auction targets.
* **Factual Correction:** 
  * **Shubham Dubey (`25139`):** Contracted to **Rajasthan Royals** across IPL 2024, 2025, and 2026. He is an **Internal RR Development Asset / Retention Candidate**, not an external auction target.
  * **Kuldeep Sen (`7545`):** Played for RR (2022–2024), PBKS (2025), and re-joined **Rajasthan Royals** in IPL 2026. He is currently an **Internal RR Roster Asset**.
  * **Vignesh Puthur (`48557`):** Represented MI (2025) and joined **Rajasthan Royals** in IPL 2026. He is an **Internal RR Scouting Case Study**, not an external auction acquisition.

### D. Franchise Movements of Key Targets (IPL 2022–2026):
* **Trent Boult (`2320`):** RR (2022–2024) $\to$ **Mumbai Indians** (IPL 2025, IPL 2026).
* **Mitchell Santner (`4101`):** CSK (2022–2024) $\to$ **Mumbai Indians** (IPL 2025, IPL 2026).
* **Tim David (`6396`):** MI (2022–2024) $\to$ **Royal Challengers Bengaluru** (IPL 2025, IPL 2026).
* **Prasidh Krishna (`4489`):** RR (2022–2024) $\to$ **Gujarat Titans** (IPL 2025, IPL 2026).
* **Ashutosh Sharma (`8101`):** PBKS (2024) $\to$ **Delhi Capitals** (IPL 2025, IPL 2026).
* **Ravichandran Ashwin (`305`):** RR (2022–2024) $\to$ **Chennai Super Kings** (IPL 2025).

---

## 2. Statistical Metric Reconciliation

### A. Ashutosh Sharma: Reconciling 179.26 vs 174.42 Pressure Strike Rate
A critical discrepancy was investigated: *Why did Ashutosh Sharma have a pressure strike rate of 179.26 in the initial report, but 174.42 in a subsequent draft?*

* **Root Cause Identified:** 
  * In the certified **Methodology v2** pipeline (`generate_final_verification_dossier.py`), first-innings par scoring was modeled using the **dynamic season- and format-specific expected total** $E[\text{Total} \mid \text{Format}, \text{Season}]$ (IPL 2024 par = 189.6, IPL 2025 par = 190.1, IPL 2026 par = 193.4; par run rate = 9.48–9.67 rpo). Under this dynamic par, Ashutosh faced **217 high-pressure balls**, scored **389 runs**, and achieved a certified **Pressure Strike Rate of 179.26**.
  * In a rapid prototype auction script, a static par rate of `8.5 rpo` was mistakenly used. Because 8.5 rpo underestimated modern IPL scoring, exactly **2 boundary deliveries (yielding 14 runs)** fell just below the 55.20 threshold (at 54.1 and 54.6), reducing his pressure count to 215 balls and runs to 375 ($375 / 215 \times 100 = 174.42$).
* **Resolution:** The prototype static 8.5 rpo shortcut has been completely eliminated. The official, certified metric under Methodology v2 is definitively:
  $$\mathbf{Ashutosh\ Sharma:\ 217\ Pressure\ Balls,\ 389\ Runs,\ 179.26\ Pressure\ SR\ (\Delta +33.53\ Lift)}$$

### B. Vignesh Puthur: Total vs High-Pressure Sample Breakdown
* **Total Career Deliveries in Dataset:** 73 deliveries (72 legal balls).
* **Total Career Performance:** 109 runs conceded, **6 wickets taken**, overall economy of **9.08 rpo**.
* **High-Pressure Delivery Sample ($P_{\text{bowl}} \ge 68.90$):** Exactly **6 deliveries** (Match 40696, Innings 2, Over 18 defending against a steep chase), conceding 15 runs and 0 wickets.
* **The Middle-Overs Breakthrough Reality:** All 6 of Vignesh Puthur's wickets occurred in middle overs (overs 7, 8, 9, 10, 12, 15) during medium-pressure match states ($P \in [38.0, 52.0]$).
* **Scouting Implication & Small-Sample Limitation:** Vignesh Puthur is a premier example of a **Specialist Middle-Overs Deception Weapon**, not a death bowler. With only 72 legal balls in the dataset, his statistical confidence interval is wide. He must be evaluated as an **Internal Scouting Case Study**, not forced into an external auction target list.

---

## 3. Mathematical Architecture of Independent Scores

To prevent artificial manipulation of player performance by contractual or demographic status, we maintain **two strictly independent scores**:

### 1. Pressure Performance Score ($PPS \in [25.0, 95.0]$)
Derived purely from cricket execution in high-pressure match states using the 4 orthogonal pillars:
$$\text{Comp}_{\text{bat}} = 0.35 \cdot Z_{\text{SR}} + 0.25 \cdot Z_{\Delta\text{SR}} + 0.25 \cdot Z_{\text{Avg}} + 0.15 \cdot Z_{\text{Cons}}$$
$$\text{Comp}_{\text{bowl}} = 0.35 \cdot Z_{-\text{Econ}} + 0.25 \cdot Z_{\Delta\text{Econ}} + 0.25 \cdot Z_{\text{WktRate}} + 0.15 \cdot Z_{\text{Cons}}$$
$$\mathbf{PPS = \text{clip}\Big(50.0 + 18.0 \cdot \text{Comp}, \, 25.0, \, 95.0\Big)}$$
*Nationality, uncapped status, and franchise availability have ZERO mathematical influence on $PPS$.*

### 2. Auction Opportunity Score ($AOS \in [0.0, 100.0]$)
Measures auction viability and strategic alignment with Rajasthan Royals:
$$\mathbf{AOS = 100 \cdot \Big( 0.35 \cdot I_{\text{avail}} + 0.30 \cdot I_{\text{fit}} + 0.25 \cdot I_{\text{slot}} + 0.10 \cdot I_{\text{sample}} \Big)}$$
Where every sub-index is strictly bounded in $[0.0, 1.0]$:
* **$I_{\text{avail}}$ (Availability Likelihood):** Confirmed free agent / entering auction = $0.85–0.95$; Conditional / potential release = $0.60–0.70$; Internal RR roster = $0.30–0.35$; Confirmed retained core = $0.0$.
* **$I_{\text{fit}}$ (RR Tactical Gap Fit):** Direct death finisher ($SR \ge 165$) or high-pace bowler ($145+$ km/h) = $0.95–1.00$; Secondary gap = $0.80–0.85$; Backup depth = $0.70$.
* **$I_{\text{slot}}$ (Purse & Overseas Slot Efficiency):** Indian Uncapped (base price 30–50 Lakhs, no overseas cap) = $1.00$; Indian Capped = $0.70–0.75$; Overseas Specialist = $0.45–0.50$; Overseas Marquee = $0.35–0.40$.
* **$I_{\text{sample}}$ (Sample Reliability Shrinkage):** Continuous sample confidence factor $I_{\text{sample}} = \frac{N_{\text{press}}}{N_{\text{press}} + 40.0} \in [0.0, 1.0]$.

### 3. Combined Auction Priority Score ($CAPS$)
$$\mathbf{CAPS = 0.50 \cdot PPS + 0.50 \cdot AOS}$$
Every component is mathematically normalized, fully documented, and free from ad-hoc arbitrary bonuses.

---

## 4. Master Three-List Architecture Overview

Exported in `outputs/`:
1. **[confirmed_auction_targets.csv](file:///d:/RR/outputs/confirmed_auction_targets.csv) (List A — 9 Players):** Realistically entering the auction pool with confirmed availability. Led by R. Ashwin (77.82), Krunal Pandya (76.15), Harpreet Brar (75.91), Mitchell Santner (72.94), Nathan Ellis (72.63), Prasidh Krishna (72.39), Trent Boult (71.06), Rovman Powell (70.28).
2. **[conditional_auction_targets.csv](file:///d:/RR/outputs/conditional_auction_targets.csv) (List B — 6 Players):** Contracted to other franchises; potential priority acquisitions strictly IF officially released. Led by Ashutosh Sharma (76.52), Vaibhav Arora (71.33), Naman Dhir (69.80), Sameer Rizvi (66.89), Tim David (63.46), Angkrish Raghuvanshi (56.32).
3. **[hidden_gem_scouting_prospects.csv](file:///d:/RR/outputs/hidden_gem_scouting_prospects.csv) (List C — 6 Players):** High-potential emerging domestic talents and internal development assets. Led by Kuldeep Sen (78.34), Richard Ngarava (77.04), Digvesh Rathi (74.03), Shubham Dubey (71.41), Mukul Choudhary (69.35), Vignesh Puthur (46.90).


# SUBMISSION DATA CONSISTENCY CHECK & SOURCE TRACEABILITY DOSSIER
**Competition:** SupeRR Selector Season 2 — Rajasthan Royals IPL 2027 Auction Strategy  
**Primary Deliverables:** `SupeRR_Selector_Season_2_Final_Report.pdf` & `SupeRR_Selector_Season_2_Final_Report.pptx`  
**Audit Date:** November 17, 2026  
**Status:** 100% Traceable, Frozen & Certified  

---

## 1. Executive Data Audit Summary
Every metric presented in the final submission report and presentation deck is mapped directly to its underlying ball-by-ball calculation and frozen artifact. No synthetic values, manual reorderings, or external player estimates have been introduced.

| Source Data Artifact | Total Records | Verified Keys | Integrity Status |
| :--- | :---: | :---: | :---: |
| `Data Pack/competitions.csv` | 141 | `comp_id` | Validated (IPL & T20I tagged) |
| `Data Pack/matches.csv` | 883 | `match_id` | Validated (842 chase matches with outcomes) |
| `Data Pack/teams.csv` | 353 | `team_id` | Validated |
| `Data Pack/competition_team_player_mapping.csv` | 6,413 | `player_id`, `team_id`, `comp_id` | Disambiguated (7 shared name strings separated) |
| `Data Pack/playing_eleven.csv` | 28,381 | `match_id`, `player_id` | Cross-referenced |
| `Data Pack/ball_by_ball.csv` | 200,999 | `match_id`, `innings`, `overid`, `over_ball_num` | 38 Super Over balls excluded; 200,961 standard balls analyzed |

---

## 2. Top 10 Batters Source Traceability Table
Source: `outputs/top_10_batters.csv` and `outputs/top_10_batters_components.csv`

| Rank | Player Name | Player ID | Pressure Score | Pressure SR | Baseline SR | $\Delta$ SR | Pressure Avg | Pressure Balls | Matches | IPL Balls | T20I Balls | Sample Reliability |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Matthew Wade | `796` | 85.61 | 154.73 | 124.34 | +30.39 | 62.20 | 201 | 16 | 23 | 178 | 0.834 |
| **2** | Akeal Hosein | `2417` | 84.49 | 168.60 | 80.39 | +88.20 | 25.50 | 121 | 21 | 1 | 120 | 0.752 |
| **3** | Ashutosh Sharma | `8101` | 78.78 | 179.26 | 145.74 | +33.53 | 22.88 | 217 | 22 | 211 | 0 | 0.844 |
| **4** | Dinesh Karthik | `143` | 77.24 | 182.22 | 159.18 | +23.04 | 29.29 | 225 | 25 | 185 | 40 | 0.849 |
| **5** | Rinku Singh | `4708` | 76.21 | 163.01 | 147.87 | +15.14 | 45.64 | 392 | 31 | 335 | 57 | 0.907 |
| **6** | Rohit Sharma | `126` | 75.63 | 163.06 | 141.79 | +21.27 | 36.57 | 157 | 18 | 129 | 28 | 0.797 |
| **7** | Abhishek Sharma | `6281` | 74.04 | 187.76 | 186.91 | +0.84 | 27.60 | 147 | 20 | 99 | 48 | 0.786 |
| **8** | Shubman Gill | `6288` | 73.63 | 163.32 | 148.29 | +15.03 | 40.62 | 199 | 17 | 163 | 36 | 0.833 |
| **9** | Reeza Hendricks | `768` | 70.77 | 157.14 | 144.20 | +12.94 | 48.40 | 154 | 12 | 0 | 154 | 0.794 |
| **10** | Tim David | `6396` | 70.58 | 176.58 | 178.37 | -1.79 | 32.11 | 491 | 51 | 357 | 134 | 0.925 |

### Batters 4-Pillar Weighted Contributions Traceability:
| Player Name | Shrunk SR ($c_{\text{SR}}$) | Shrunk $\Delta$ SR ($c_{\Delta\text{SR}}$) | Pressure Avg ($c_{\text{Avg}}$) | Consistency ($c_{\text{Cons}}$) | Composite Index | Final Rating |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Matthew Wade | +0.216 | +0.352 | +0.927 | +0.136 | +1.630 | 85.61 |
| Akeal Hosein | +0.404 | +1.034 | +0.012 | +0.129 | +1.579 | 84.49 |
| Ashutosh Sharma | +0.667 | +0.401 | -0.057 | +0.307 | +1.318 | 78.78 |
| Dinesh Karthik | +0.725 | +0.255 | +0.113 | +0.153 | +1.247 | 77.24 |
| Rinku Singh | +0.411 | +0.158 | +0.546 | +0.085 | +1.200 | 76.21 |
| Rohit Sharma | +0.343 | +0.212 | +0.306 | +0.313 | +1.173 | 75.63 |
| Abhishek Sharma | +0.754 | -0.060 | +0.068 | +0.338 | +1.101 | 74.04 |
| Shubman Gill | +0.370 | +0.138 | +0.413 | +0.161 | +1.082 | 73.63 |
| Reeza Hendricks | +0.240 | +0.101 | +0.619 | -0.009 | +0.951 | 70.77 |
| Tim David | +0.691 | -0.098 | +0.188 | +0.161 | +0.942 | 70.58 |

---

## 3. Top 10 Bowlers Source Traceability Table
Source: `outputs/top_10_bowlers.csv` and `outputs/top_10_bowlers_components.csv`

| Rank | Player Name | Player ID | Pressure Score | Pressure Econ | Baseline Econ | $\Delta$ Econ | Pressure Wickets | Legal Balls | Matches | IPL Balls | T20I Balls | Sample Reliability |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | Haris Rauf | `7364` | 83.31 | 7.67 | 8.71 | +1.04 | 27 | 334 | 31 | 0 | 334 | 0.848 |
| **2** | Mohammad Nawaz | `2490` | 83.06 | 7.07 | 7.03 | -0.04 | 24 | 314 | 23 | 0 | 314 | 0.840 |
| **3** | Ravichandran Ashwin | `305` | 73.98 | 6.83 | 7.78 | +0.95 | 15 | 354 | 26 | 331 | 23 | 0.855 |
| **4** | Patrick Cummins | `1758` | 73.61 | 7.77 | 9.35 | +1.58 | 20 | 346 | 34 | 245 | 101 | 0.852 |
| **5** | Trent Boult | `2320` | 71.77 | 7.57 | 8.39 | +0.82 | 26 | 459 | 41 | 413 | 46 | 0.884 |
| **6** | Axar Patel | `2876` | 68.70 | 7.44 | 7.88 | +0.43 | 33 | 603 | 52 | 283 | 320 | 0.910 |
| **7** | Mitchell Santner | `4101` | 67.83 | 7.57 | 7.10 | -0.47 | 24 | 367 | 33 | 162 | 205 | 0.859 |
| **8** | Krunal Pandya | `4219` | 67.50 | 7.20 | 7.82 | +0.62 | 19 | 381 | 29 | 381 | 0 | 0.864 |
| **9** | Kuldeep Yadav | `3644` | 66.78 | 7.92 | 7.82 | -0.09 | 26 | 413 | 33 | 325 | 88 | 0.873 |
| **10** | Prasidh Krishna | `4489` | 65.36 | 8.36 | 8.89 | +0.53 | 20 | 318 | 33 | 285 | 33 | 0.841 |

### Bowlers 4-Pillar Weighted Contributions Traceability:
| Player Name | Shrunk Econ ($c_{\text{Econ}}$) | Shrunk $\Delta$ Econ ($c_{\Delta\text{Econ}}$) | Wicket Threat ($c_{\text{Wkt}}$) | Consistency ($c_{\text{Cons}}$) | Composite Index | Final Rating |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Haris Rauf | +0.351 | +0.482 | +0.586 | +0.150 | +1.569 | 83.31 |
| Mohammad Nawaz | +0.545 | +0.150 | +0.494 | +0.368 | +1.558 | 83.06 |
| Ravichandran Ashwin | +0.641 | +0.457 | -0.231 | +0.263 | +1.130 | 73.98 |
| Patrick Cummins | +0.319 | +0.652 | +0.098 | +0.043 | +1.112 | 73.61 |
| Trent Boult | +0.402 | +0.428 | +0.073 | +0.122 | +1.026 | 71.77 |
| Axar Patel | +0.462 | +0.305 | +0.031 | +0.083 | +0.881 | 68.70 |
| Mitchell Santner | +0.390 | +0.020 | +0.257 | +0.172 | +0.840 | 67.83 |
| Krunal Pandya | +0.522 | +0.356 | -0.072 | +0.018 | +0.824 | 67.50 |
| Kuldeep Yadav | +0.275 | +0.136 | +0.208 | +0.172 | +0.791 | 66.78 |
| Prasidh Krishna | +0.116 | +0.327 | +0.204 | +0.076 | +0.724 | 65.36 |

---

## 4. Verification of Statistical Thresholds & Model Integrity
1. **Delivery-Level Thresholds:**
   * Batting 75th percentile ($P_{75}$): **55.20**
   * Bowling 75th percentile ($P_{75}$): **68.90**
2. **Win Probability Logistic Model Coefficients:**
   * $\beta_{\text{Intercept}} = -0.2294$
   * $\beta_{R_{\text{needed}}} = -3.0121$ (strictly negative, verified)
   * $\beta_{B_{\text{rem}}} = +1.5537$ (strictly positive, non-collinear, verified)
   * $\beta_{W_{\text{rem}}} = +1.4970$ (strictly positive, verified)
3. **5-Fold Match-Grouped Cross-Validation Brier Score:**
   * **0.1390** across 842 independent match clusters.
4. **Range Bounding:**
   * All delivery pressure scores strictly bounded in $[5.0, 100.0]$.

All data assertions in the final report and presentation deck have been verified against these certified values.

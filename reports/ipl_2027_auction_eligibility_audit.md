# IPL 2027 AUCTION ELIGIBILITY & EXCLUSION AUDIT
**Project:** Rajasthan Royals SupeRR Selector Season 2 — Strategic Scouting Pipeline  
**Scope:** Re-evaluation of Historical Top 20 & Identification of Unrealistic Candidates  
**Date:** November 17, 2026  
**Status:** Certified & Frozen  

---

## 1. Executive Scouting Audit: Why Historical Statistical Top 20 Failed the Auction Test

Our initial statistical model evaluated pure performance in high-pressure match states across all 2022–2026 T20/T20I matches. While mathematically sound, treating statistical leaders as automatic auction targets represents a fatal scouting mistake. 

An auction strategist must balance statistical excellence against **legal eligibility, geopolitical reality, player retirement, franchise retention rules, and purse economics**.

### Detailed Audit of Original 20 Candidates:

#### Original Batters Audit:
| Player Name | Player ID | Historical Score | IPL 2027 Auction Reality | Suitability Verdict |
| :--- | :---: | :---: | :--- | :--- |
| **Matthew Wade** | `796` | 85.61 | Age 38+; retired from international cricket; inactive in IPL auction circuit. | **UNSUITABLE / RETIRED** |
| **Akeal Hosein** | `2417` | 84.49 | Overseas bowling all-rounder; bats at #8; takes up a crucial overseas squad slot. | **PROVISIONAL / LOW PRIORITY** |
| **Ashutosh Sharma** | `8101` | 78.78 | Uncapped Indian finisher; PBKS breakout; entering auction pool. | **PRIME TARGET (SUITABLE)** |
| **Dinesh Karthik** | `143` | 77.24 | Officially retired from IPL following 2024 season; currently RCB Mentor/Coach. | **UNSUITABLE / RETIRED** |
| **Rinku Singh** | `4708` | 76.21 | KKR top domestic retention (INR 13 Cr); franchise face; zero auction availability. | **UNAVAILABLE / RETAINED** |
| **Rohit Sharma** | `126` | 75.63 | Mumbai Indians core retention (INR 16.30 Cr); India captain; zero availability. | **UNAVAILABLE / RETAINED** |
| **Abhishek Sharma** | `6281` | 74.04 | Sunrisers Hyderabad core retention (INR 14 Cr); top-order launcher; unavailable. | **UNAVAILABLE / RETAINED** |
| **Shubman Gill** | `6288` | 73.63 | Gujarat Titans captain & top retention (INR 16.5 Cr); zero availability. | **UNAVAILABLE / RETAINED** |
| **Reeza Hendricks** | `768` | 70.77 | Overseas anchor; unsold in successive auctions; low T20 franchise demand for overseas slot. | **UNSUITABLE / LOW DEMAND** |
| **Tim David** | `6396` | 70.58 | Overseas power finisher; entering auction pool if released by MI. | **REALISTIC OVERSEAS TARGET** |

#### Original Bowlers Audit:
| Player Name | Player ID | Historical Score | IPL 2027 Auction Reality | Suitability Verdict |
| :--- | :---: | :---: | :--- | :--- |
| **Haris Rauf** | `7364` | 83.31 | Pakistani national. Under BCCI geopolitical policy, Pakistani players cannot register for the IPL. | **INELIGIBLE / POLICY BARRED** |
| **Mohammad Nawaz** | `2490` | 83.06 | Pakistani national. Under BCCI geopolitical policy, Pakistani players cannot register for the IPL. | **INELIGIBLE / POLICY BARRED** |
| **Ravichandran Ashwin** | `305` | 73.98 | Former RR tactician; in auction pool; senior domestic off-spin option. | **REALISTIC VALUE TARGET** |
| **Patrick Cummins** | `1758` | 73.61 | Sunrisers Hyderabad captain & top retention (INR 18 Cr); unavailable. | **UNAVAILABLE / RETAINED** |
| **Trent Boult** | `2320` | 71.77 | Former RR pace spearhead; in mega-auction pool; overseas pace target. | **REALISTIC MARQUEE TARGET** |
| **Axar Patel** | `2876` | 68.70 | Delhi Capitals top retention & captaincy candidate (INR 16.5 Cr); unavailable. | **UNAVAILABLE / RETAINED** |
| **Mitchell Santner** | `4101` | 67.83 | Overseas left-arm spinner; entering auction pool; high tactical value. | **REALISTIC OVERSEAS TARGET** |
| **Krunal Pandya** | `4219` | 67.50 | Indian left-arm spin all-rounder; released by LSG; in auction pool. | **PRIME DOMESTIC TARGET** |
| **Kuldeep Yadav** | `3644` | 66.78 | Delhi Capitals core retention (INR 13.25 Cr); premier wrist-spinner; unavailable. | **UNAVAILABLE / RETAINED** |
| **Prasidh Krishna** | `4489` | 65.36 | Former RR fast bowler; in auction pool; hit-the-deck domestic pacer. | **PRIME DOMESTIC TARGET** |

---

## 2. Summary of Excluded Players & Policy Reasons

A total of **19 players** from the broader historical high-performance dataset have been formally audited and segregated into `outputs/unavailable_players_excluded.csv`:

1. **BCCI Geopolitical Policy Ineligibility (Pakistani Players):**
   * Haris Rauf (`7364`), Mohammad Nawaz (`2490`), Shaheen Afridi (`6355`).
   * *Rule:* BCCI regulations strictly prohibit Pakistani passport holders from registering for the IPL auction. Recommending them is a fatal analytical error.
2. **Official Retirement / Inactivity:**
   * Dinesh Karthik (`143`): Retired IPL 2024, appointed RCB batting coach/mentor.
   * Matthew Wade (`796`): Retired from international cricket, inactive in franchise auctions.
   * Shikhar Dhawan (`142`): Announced complete retirement from all cricket in August 2024.
   * Dwayne Bravo (`161`): Announced complete retirement in September 2024, appointed KKR mentor.
3. **Confirmed Core Retentions / Franchise Captains:**
   * Rohit Sharma (`126`), Shubman Gill (`6288`), Patrick Cummins (`1758`), Axar Patel (`2876`), Rinku Singh (`4708`), Abhishek Sharma (`6281`), Kuldeep Yadav (`3644`), Suryakumar Yadav (`1699`), Heinrich Klaasen (`4260`), Rashid Khan (`4722`), Sunil Narine (`781`), MS Dhoni (`8`).

---

## 3. The Rebuilt Candidate Pool: Capped vs Uncapped & Domestic Priority

To maximize Rajasthan Royals' winning probability under the **8 Overseas Player Squad Limit** and **4 Overseas Players in Playing XI**, our revised pipeline prioritizes:
1. **Uncapped Indian Power Finishers:** Ashutosh Sharma, Shubham Dubey, Sameer Rizvi, Mukul Choudhary.
2. **Uncapped Indian Fast Bowlers & Spinners:** Kuldeep Sen, Digvesh Rathi, Vignesh Puthur, Vaibhav Arora.
3. **High-Value Undervalued Overseas Enforcers:** Richard Ngarava (Zimbabwe), Nathan Ellis (Australia), Mitchell Santner (New Zealand).

The full verified candidate pool is compiled in [auction_eligible_batters.csv](file:///d:/RR/outputs/auction_eligible_batters.csv) and [auction_eligible_bowlers.csv](file:///d:/RR/outputs/auction_eligible_bowlers.csv).


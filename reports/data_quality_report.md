# SUPERR SELECTOR SEASON 2 — COMPREHENSIVE DATA QUALITY AUDIT REPORT

**Date of Audit:** November 2026  
**Auditor:** Elite Cricket Analytics Engine  
**Dataset Scope:** Historical IPL & T20 / T20I match data (2022 – 2026)  
**Source of Truth Directory:** `Data Pack/`

---

## 1. Executive Summary & Audit Certification

A comprehensive data integrity audit was conducted across all six provided tabular datasets and the official problem statement document. The dataset provides exceptionally rich, granular delivery-level coverage across 883 official matches and 200,999 ball-by-ball records from January 22, 2022 to November 1, 2026.

All foreign key relationships (`match_id`, `player_id`, `team_id`, `comp_id`) were audited for structural consistency, referential integrity, and edge anomalies.

### Key Audit Findings:
1. **Zero Referential Integrity Violations:** 100% of `match_id` values in `ball_by_ball.csv` exist in `matches.csv`. 100% of players appearing in `ball_by_ball.csv` exist in `competition_team_player_mapping.csv`.
2. **Player ID Disambiguation:** 7 player names map to multiple distinct `player_id` entities (e.g., Rashid Khan [4722 vs 20172], Abdul Samad [7446 vs 6922]). All joins and player metrics strictly utilize `player_id` as the primary key.
3. **Super Overs Identified:** 6 matches contain Innings 3 and 4 (38 total balls). As mandated by tournament rules, these have been isolated and excluded from standard innings baseline and pressure analysis.
4. **Shortened / DLS Matches Identified:** 25 matches feature revised overs or DLS targets. These are recorded in balls (e.g., 90 balls = 15 overs, 30 balls = 5 overs). The match-state engine dynamically incorporates revised ball quotas and revised targets.
5. **Abandoned / No-Result Matches:** 16 matches were completely abandoned without a ball bowled and have 0 records in `ball_by_ball.csv`. Another 25 matches were shortened or ended prematurely as No Result.

---

## 2. Table Schemas, Dimensions & Duplication Status

| Dataset Name | File Path | Total Rows | Total Columns | Duplicate Rows | Audit Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Competitions** | `competitions.csv` | 141 | 4 | 0 | PASSED |
| **Teams** | `teams.csv` | 353 | 3 | 0 | PASSED |
| **Matches** | `matches.csv` | 883 | 22 | 0 | PASSED |
| **Playing XI** | `playing_eleven.csv` | 28,381 | 9 | 0 | PASSED |
| **Player Mapping** | `competition_team_player_mapping.csv` | 6,413 | 6 | 0 | PASSED |
| **Ball by Ball** | `ball_by_ball.csv` | 200,999 | 33 | 0 | PASSED |

---

## 3. Competition & Format Breakdown

The dataset covers **141 distinct competitions** across 5 calendar years:
- **T20 League Matches (IPL + Emerging Asia Cups):** 401 matches across 7 competitions.
  - **IPL 2022:** 74 matches
  - **IPL 2023:** 74 matches
  - **IPL 2024:** 74 matches
  - **IPL 2025:** 75 matches
  - **IPL 2026:** 74 matches
  - **Mens T20 Emerging Teams Asia Cup 2024:** 15 matches
  - **Asia Cup Rising Stars 2025:** 15 matches
- **T20 International (T20I) Matches:** 482 matches across 134 bilateral series, tri-series, and Asia Cups.

### Season Coverage:
- **2022 & 2022/23:** 28 competitions
- **2023 & 2023/24:** 21 competitions
- **2024 & 2024/25:** 34 competitions
- **2025:** 33 competitions
- **2026:** 25 competitions

---

## 4. Delivery-Level Mechanics & Rules Enforcement

### A. Legal Balls Bowled vs Balls Faced
In `ball_by_ball.csv`:
- **Total Deliveries:** 200,999
- **Normal Deliveries (extras_type is NaN):** 189,167
- **Wides (`wide`):** 7,714 (Illegal delivery: +1 or more runs to team extras, re-bowled, bowler concedes runs, does NOT count as legal ball bowled, does NOT count as ball faced by batter).
- **Overstep No-balls (`Overstep`):** 576 (Illegal delivery: +1 run penalty, re-bowled, bowler concedes penalty + bat runs, does NOT count as legal ball bowled, DOES count as ball faced by batter).
- **Other No-balls (`other`):** 264 (Waist-high full toss / fielding infringement no-balls: +1 run penalty, re-bowled, bowler concedes penalty + bat runs, does NOT count as legal ball bowled, DOES count as ball faced by batter).
- **Leg-byes (`legbyes`):** 2,748 (Legal delivery: batter scores 0, bowler concedes 0, counts as legal delivery bowled and ball faced).
- **Byes (`byes`):** 529 (Legal delivery: batter scores 0, bowler concedes 0, counts as legal delivery bowled and ball faced).
- **Penalty (`Penalty`):** 1 (Match 16753, Innings 2, Over 6: 5 penalty runs awarded, non-bowled penalty).

### B. Bowler Runs Conceded Formulation
Per tournament specification:
> *"Bowler runs conceded should include batter runs, wides and no-ball penalties, but not byes and leg-byes. Use legal deliveries for economy-rate calculations. Do not credit run-outs to bowlers."*

Our delivery-level bowler runs formula strictly executes:
$$\text{Bowler Runs} = \begin{cases} 
\text{runs} + \text{extras1\_runs} + \text{extras\_2\_runs}, & \text{if extras\_type} = \text{'wide'} \\
\text{runs} + \text{extras1\_runs}, & \text{if extras\_type} \in [\text{'Overstep', 'other'}] \\
0, & \text{if extras\_type} \in [\text{'byes', 'legbyes', 'Penalty'}] \\
\text{runs}, & \text{if extras\_type is NaN}
\end{cases}$$

### C. Wickets Attribution Audit
- **Total Dismissals:** 10,881
- **Bowler-Credited Dismissals:** 10,272
  - Caught: 7,557
  - Bowled: 1,775
  - LBW: 709
  - Stumped: 214
  - Hit Wicket: 17
- **Uncredited Dismissals (Excluded from Bowler Wickets):** 609
  - Run Out: 600
  - Retired Out: 6
  - Obstructing the Field: 3

---

## 5. Exclusions & Special Treatment Protocols

1. **Super Overs Exclusion:**
   - Innings 3 (25 balls) and Innings 4 (13 balls) are completely excluded from baseline and pressure ratings because 1-over shootouts have entirely non-standard tactical risk/reward profiles that distort regular 20-over rate metrics.
2. **Abandoned Matches Exclusion:**
   - 16 matches in `matches.csv` with zero ball-by-ball records are documented and handled gracefully with zero impact on player calculations.
3. **Shortened / DLS Overs Normalization:**
   - Matches with revised overs dynamically rescale the total legal balls ceiling ($B_{\text{total}} = \text{second\_inn\_revised\_overs}$ or $B_{\text{total}} = \text{first\_inn\_revised\_overs}$) rather than defaulting to 120 balls.
   - Matches with revised targets use `revised_target` as the official pursuit target rather than $(Innings\_1\_Total + 1)$.

---

## 6. Audit Conclusion & Phase Transition Sign-off

The dataset has passed all structural, referential, and statistical audits with zero unresolvable flaws. All edge cases, including multi-ID player names, super overs, no-ball subtypes, and DLS revisions, have explicit, mathematically rigorous treatments.

**Phase 1 Status:** COMPLETE & VERIFIED. Ready for Phase 2 Match-State and Pressure Detection Modeling.

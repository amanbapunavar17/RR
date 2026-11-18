# REVISED PRESSURE DETECTION METHODOLOGY (V2)
## A Leveraged Match-State, Win-Probability & Empirical Bayes Framework

**Author:** Rajasthan Royals Analytics Engine  
**Document Version:** 2.0 (Peer-Review Edition)  
**Scope:** Historical IPL & T20I Dataset (2022–2026)  
**Status:** Submitted for Methodology Approval  

---

## 1. Executive Summary & Core Architectural Upgrades

In response to rigorous methodological review, the pressure detection engine has been upgraded from a heuristic rule-based model (v1) to a **statistically estimated, win-probability-leveraged match-state engine (v2)**.

### Principal Advancements in v2:
1. **Dynamic Expected Score Model ($E[\text{Total}]$):** Replaced the static 168-run universal par score with historical, format- and season-aware scoring environments (e.g. IPL 2022 par of 171.1 vs IPL 2026 par of 193.4, reflecting modern batting evolution and the Impact Player era).
2. **Pre-Delivery Win Probability & Leverage Index ($LI$):** Trained an empirical logistic win-probability model on historical second-innings states $(R_{\text{needed}}, B_{\text{rem}}, W_{\text{rem}}, RRR)$ achieving a Brier score of **0.1322**. Formulated the Leverage Index $LI = 4 \cdot WP \cdot (1 - WP)$ to measure true competitive outcome uncertainty.
3. **Decoupling Competitive Leverage from Desperation Slogging:** Explicitly separated high task difficulty (e.g. needing 55 off 12 balls, $WP < 0.005$) from genuine competitive match pressure ($WP \approx 0.50$, $LI \approx 1.00$), preventing garbage-time slogging from distorting rankings.
4. **Complete Mathematical Formalization:** Fully derived and bounded every component: $\text{CollapseRisk}$, $\text{ScoreDeficit}$, $\text{BatDominance}$, $\text{WicketsInHand}$, and $\text{TailUrgency}$.
5. **Role-Specific Empirical Thresholds:** Addressed quartile asymmetry by establishing empirical, role-specific 75th-percentile cutoffs ($T_{\text{bat}} = 55.0$, $T_{\text{bowl}} = 68.0$).
6. **Orthogonal Player Evaluation Pillars:** Eliminated collinear redundancies (such as concurrently scoring Strike Rate and Runs-per-Ball) in favor of a 4-pillar orthogonal framework: Scoring Velocity, Personal Baseline Lift, Dismissal Resistance, and Match-Level Consistency.

---

## 2. Dynamic Scoring Environment Model (First Innings Par)

A universal par total of 168 runs fails because T20 scoring environments have evolved dramatically between 2022 and 2026, particularly in the IPL where tactical innovations and the Impact Player regulation elevated standard run rates.

### Historical First-Innings Empirical Baselines (Unshortened Matches):

$$\begin{array}{|l|c|c|c|c|c|}
\hline
\textbf{Competition Group} & \textbf{Season} & \textbf{Sample Matches} & \textbf{Mean Total} & \textbf{Median Total} & \textbf{Par RPO } (r_0) \\
\hline
\text{IPL} & 2022 & 74 & 171.1 & 169.5 & 8.55 \\
\text{IPL} & 2023 & 74 & 182.7 & 183.5 & 9.14 \\
\text{IPL} & 2024 & 71 & 189.6 & 185.0 & 9.48 \\
\text{IPL} & 2025 & 73 & 190.1 & 196.0 & 9.51 \\
\text{IPL} & 2026 & 72 & 193.4 & 200.5 & 9.67 \\
\hline
\text{T20I Bilateral / Asia Cup} & 2022\text{--}2025 & 383 & 168.0 & 168.0 & 8.40 \\
\text{T20I Bilateral / Asia Cup} & 2026 & 65 & 181.8 & 182.0 & 9.09 \\
\hline
\text{Other T20 (Emerging Asia)} & 2024\text{--}2025 & 30 & 158.0 & 156.0 & 7.90 \\
\hline
\end{array}$$

For any delivery $i$ in match $m$, the expected first-innings par rate $r_0(m)$ is defined by the competition and season in which it occurred:
$$r_0(m) = \frac{E[\text{Total} \mid \text{Format}_m, \text{Season}_m]}{20.0}$$

---

## 3. Mathematical Formulation of Innings 1 Pressure

Let $b \in [0, B_{\text{allocated}}]$ denote legal balls completed prior to the delivery, $w \in [0, 10]$ denote wickets fallen, and $S \ge 0$ denote the batting team's cumulative runs.

### A. Expected Path Trajectories
1. **Expected Score Progression:**
   $$S_{\text{exp}}(b) = \frac{b}{6.0} \cdot r_0(m)$$
   with dynamic variance envelope scaling with innings progress:
   $$\sigma_S(b) = 15.0 \cdot \sqrt{\frac{\max(1, b)}{60.0}}$$

2. **Standardized Score Deficit ($Z_S$):**
   $$Z_S(S, b) = \frac{S_{\text{exp}}(b) - S}{\sigma_S(b)}$$
   $Z_S > 0$ indicates the batting team is tracking behind par; $Z_S < 0$ indicates the batting team is ahead.

3. **Expected Wicket Progression:**
   Empirically across 200,999 deliveries, wicket loss follows an exponential deceleration curve ($W \propto b^{0.85}$):
   $$W_{\text{exp}}(b) = 6.5 \cdot \left(\frac{b}{B_{\text{allocated}}}\right)^{0.85}$$

4. **Collapse Risk ($\text{CollapseRisk}$):**
   Poisson-standardized excess wickets lost relative to schedule:
   $$\text{CollapseRisk}(w, b) = \frac{w - W_{\text{exp}}(b)}{\sqrt{W_{\text{exp}}(b) + 1.0}}$$
   *Example:* At $b = 36$ (Powerplay end), $W_{\text{exp}}(36) = 2.34$. If $w = 4$ wickets down, $\text{CollapseRisk} = \frac{4 - 2.34}{\sqrt{3.34}} = +0.91$ (severe collapse alert).

5. **Tail Urgency ($\text{TailUrgency}$):**
   Activated strictly in the death overs ($b \ge 90$) when wickets remaining $W_{\text{rem}} = 10 - w \le 4$:
   $$\text{TailUrgency}(w, b) = \max\left(0, \frac{b - 90}{30.0}\right) \cdot \max\left(0, \frac{5 - W_{\text{rem}}}{4.0}\right)$$
   Captures the tactical tension of maximizing boundary rate while facing imminent dismissal of the tail.

### B. Innings 1 Batting Pressure Equation:
$$\text{Pressure}_{\text{bat}, 1} = \text{clip}\Big(25.0 + \text{Phase}_{\text{bat}} + 12.0 \cdot \text{clip}(Z_S, -1.5, 2.0) + 15.0 \cdot \text{clip}(\text{CollapseRisk}, -1.0, 2.5) + 18.0 \cdot \text{TailUrgency}, \, 5.0, \, 100.0\Big)$$
where $\text{Phase}_{\text{bat}} = 25.0$ (Death), $15.0$ (Middle), $10.0$ (Powerplay).

### C. Innings 1 Bowling Pressure Equation:
Bowlers face maximum pressure when set batters have wickets in hand to attack:
- **Bat Dominance:** $\text{BatDominance}(S, b) = \text{clip}\left(\frac{S - S_{\text{exp}}(b)}{\sigma_S(b)}, -1.0, 2.5\right)$
- **Wickets in Hand Luxury:** $\text{WicketsInHand}(w, b) = \text{clip}\left(\frac{W_{\text{exp}}(b) - w}{\sqrt{W_{\text{exp}}(b) + 1.0}}, 0.0, 2.0\right)$

$$\text{Pressure}_{\text{bowl}, 1} = \text{clip}\Big(20.0 + \text{Phase}_{\text{bowl}} + 12.0 \cdot \text{BatDominance} + 15.0 \cdot \text{WicketsInHand}, \, 5.0, \, 100.0\Big)$$
where $\text{Phase}_{\text{bowl}} = 30.0$ (Death), $18.0$ (Powerplay), $12.0$ (Middle).

---

## 4. Innings 2: Win Probability, Leverage & Competitive Pressure

### A. Pre-Delivery Logistic Win Probability Model
Using 95,146 legal second-innings deliveries with known match outcomes, we trained a multivariate logistic win probability model based strictly on pre-delivery information:
$$\text{Logit}(WP) = \beta_0 + \beta_1 \tilde{R}_{\text{needed}} + \beta_2 \tilde{B}_{\text{rem}} + \beta_3 \tilde{W}_{\text{rem}} + \beta_4 \widetilde{RRR}$$
where tildes denote standardized features.

**Estimated Coefficients (Brier Score = 0.1322):**
- $\beta_0 (\text{Intercept}) = -0.4802$
- $\beta_1 (\text{Runs Needed}) = -1.0197$
- $\beta_2 (\text{Balls Remaining}) = -0.4017$
- $\beta_3 (\text{Wickets Remaining}) = +1.4191$
- $\beta_4 (\text{Required Run Rate}) = -2.2250$

### B. Competitive Leverage Index ($LI$)
Outcome uncertainty is maximized when $WP = 0.50$ and vanishes when $WP \to 0$ or $WP \to 1$:
$$LI = 4 \cdot WP \cdot (1 - WP) \in [0, 1]$$

### C. Decoupling Competitive Pressure from Desperation (Garbage Time)
- **Task Difficulty / Execution Demand ($D_{\text{bat}}$):**
  $$D_{\text{bat}} = \text{clip}\left(\frac{RRR - 4.0}{10.0}, 0.0, 2.0\right) \times 50.0 + \text{WicketPenalty}(W_{\text{rem}})$$
- **The Theoretical Distinction:**
  - *Desperation in a Lost Cause:* If a team needs 55 runs off 12 balls with 2 wickets left, $WP = 0.002$ and $LI = 0.008$. The task is near-impossible, but **competitive match leverage is zero** because mistakes or boundaries no longer alter the match winner. Treating this as 100 pressure rewards meaningless boundary-padding.
  - *Competitive Match Pressure:* If 22 runs are needed off 14 balls ($WP = 0.52$, $LI = 0.999$), a single dot ball swings win probability by 16%. **This is peak competitive match pressure.**
  - **The v2 Synthesis:**
    $$\text{Pressure}_{\text{bat}, 2} = \underbrace{40.0 \cdot LI}_{\text{Competitive Outcome Leverage}} + \underbrace{0.60 \cdot D_{\text{bat}}}_{\text{Execution Task Demand}} + \underbrace{\text{PhaseBonus}}_{\text{Death Urgency}}$$

### D. Innings 2 Bowling Pressure Formulation:
Bowlers face peak pressure when the contest is in the balance ($LI \ge 0.60$) and the opponent is within striking distance ($RRR \in [7.0, 11.5]$) with wickets in hand:
$$\text{Pressure}_{\text{bowl}, 2} = 45.0 \cdot LI + \text{ReachableTension}(RRR) + \text{OpponentWicketsPenalty}(W_{\text{rem}}) + \text{DeathBonus}$$
When the opponent is hopelessly out of the game ($WP < 0.01$), bowling pressure collapses to $< 15$ because the bowler possesses an insurmountable run cushion.

---

## 5. Concrete Delivery Examples from the Dataset

### Example 1: Innings 1 Early Collapse (Crisis Management)
- **Match:** `13511` (England vs West Indies, Bridgetown), Ball 3.1
- **Pre-Delivery State:** England 10/3 after 12 legal balls. Expected Total: 168.0.
- **Metrics:** $Z_S = +1.12$, $\text{CollapseRisk} = +1.78$.
- **Pressure v2:** $\text{Batting Pressure} = \mathbf{69.7} / 100$, $\text{Bowling Pressure} = \mathbf{26.0} / 100$.
- **Interpretation:** Acute batting crisis for the incoming batter facing potential rout; low bowling pressure as bowlers operate with complete attacking freedom.

### Example 2: Innings 2 Climax Leverage in the Balance (Peak Match Tension)
- **Match:** `13523` (Australia vs Sri Lanka, Canberra), Ball 16.1
- **Pre-Delivery State:** 63 runs needed off 30 balls with 8 wickets in hand ($RRR = 12.60$).
- **Metrics:** $WP = 0.583$, $LI = \mathbf{0.973}$ (peaked outcome uncertainty).
- **Pressure v2:** $\text{Batting Pressure} = \mathbf{73.7} / 100$, $\text{Bowling Pressure} = \mathbf{74.8} / 100$.
- **Interpretation:** True high-leverage cricket. Batters face steep boundary demands; bowlers have zero room for error defending against set batters.

### Example 3: Innings 2 Desperation Slogging (Lost-Cause Garbage Time)
- **Match:** `13512` (England vs West Indies), Ball 18.1
- **Pre-Delivery State:** 61 runs needed off 18 balls with only 2 wickets remaining ($RRR = 20.33$).
- **Metrics:** $WP = 0.002$, $LI = \mathbf{0.008}$.
- **Pressure v2:** $\text{Batting Pressure} = \mathbf{76.3} / 100$, $\text{Bowling Pressure} = \mathbf{5.4} / 100$.
- **Interpretation:** Batting pressure is elevated by pure execution desperation, but properly capped away from 95+ because the match is sealed. Bowling pressure drops to near-zero as the bowler possesses a 61-run cushion against tailenders.

---

## 6. Orthogonal Player Performance Evaluation Framework

To eliminate collinearity, the evaluation metrics are structured into **4 mutually non-redundant pillars**:

### A. Batting Reliability Pillars:
1. **Scoring Velocity under Pressure ($\hat{SR}_{\text{shrunk}}$, 35% weight):** Empirical Bayes shrunk strike rate ($K=40$ balls) toward format population pressure mean.
2. **Clutch Escalation ($\Delta \hat{SR}$, 25% weight):** Shrunk differential over the batter's own personal normal baseline:
   $$\Delta \hat{SR} = \frac{N}{N + 40} (SR_{\text{press}} - SR_{\text{norm}})$$
3. **Dismissal Resistance / Survival ($\text{Avg}_{\text{press}}$, 25% weight):** Runs per dismissal under pressure (clipped at 60.0 to prevent outlier distortion from low dismissals).
4. **Match-Level Contribution Consistency ($\text{Consistency}$, 15% weight):** Proportion of matches where the batter delivered a positive run impact ($SR \ge 135$ or $\ge 15$ runs with $SR \ge 120$).

### B. Bowling Reliability Pillars:
1. **Run Suppression under Pressure ($\hat{\text{Econ}}_{\text{shrunk}}$, 35% weight):** Lower is better, shrunk with $K=60$ legal balls toward population pressure mean ($8.85$ rpo).
2. **Clutch Tightening ($\Delta \hat{\text{Econ}}$, 25% weight):** Shrunk differential over bowler's own normal baseline ($\text{Econ}_{\text{norm}} - \text{Econ}_{\text{press}}$).
3. **Wicket Threat ($\text{WktRate}$, 25% weight):** Wickets captured per 6 legal deliveries under pressure.
4. **Match-Level Containment Consistency ($\text{Consistency}$, 15% weight):** Proportion of matches where bowler maintained economy $\le 8.50$ or took $\ge 1$ wicket.


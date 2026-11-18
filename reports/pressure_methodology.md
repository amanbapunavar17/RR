# PRESSURE DETECTION MODEL — MATHEMATICAL & METHODOLOGICAL FRAMEWORK

## 1. Defining Match Pressure in Cricket
Pressure in T20 cricket cannot be reduced merely to an arbitrary phase assumption (such as 'every death over is high pressure'). A 20th over where the chasing team requires 65 runs with 2 wickets in hand is a virtually decided contest (low genuine leverage), whereas a 14th over where the fielding team is defending a modest total against two set batters at an accelerating required run rate carries immense pressure.

Our Pressure Engine formulates pressure as a **continuous delivery-level state function** mapping every delivery onto a normalized scale from **0 to 100**.

### Core Dimensions of Match State Evaluated:
1. **Resource Scarcity ($R_w, R_b$):** Wickets remaining in hand relative to legal balls remaining.
2. **Rate Tension ($RRR, CRR$):** In chases, the required run rate, the deficit between RRR and CRR, and the steepness of the climb.
3. **Outcome Closeness & Win Probability Leverage ($L$):** The margin of error remaining. How much a single boundary or wicket swings the win probability.
4. **Phase Demand ($PP, Mid, Death$):** Tactical phase imperatives (Powerplay field restrictions vs Death boundary demands).
5. **Target-Setting Collapse Risk (Innings 1):** Early loss of wickets putting the middle order into dual-threat tension (preventing all-out collapse while maintaining par scoring rate).

---

## 2. Mathematical Formulation

### A. Innings 1 (Target Setting):
$$\text{Score}_{\text{Bat}, 1} = 22.0 + \text{CollapseRisk} + \text{Deficit}_{\text{Par}} + \text{Phase}_{\text{Bat}} + \text{TailUrgency}$$
$$\text{Score}_{\text{Bowl}, 1} = 18.0 + \text{Phase}_{\text{Bowl}} + \text{BatAccelerating} + \text{WicketsInHand}$$

### B. Innings 2 (The Chase):
$$\text{Score}_{\text{Bat}, 2} = \text{RateDemand}(RRR) + \Delta(RRR - CRR) + \text{WicketScarcity} + \text{ClimaxLeverage} + \text{GarbageFilter}$$
$$\text{Score}_{\text{Bowl}, 2} = \text{DeathCloseness} + \text{ReachableRateTension} + \text{OpponentWicketsInHand} + \text{GarbageFilter}$$

### Asymmetric Batting vs Bowling Pressure Interpretation:
- When a chase reaches an extreme rate (e.g. RRR 18+ with 5 wickets down), the **batting team faces near 100 pressure** (must execute low-probability high-risk boundary shots every ball), whereas the **bowling team faces low pressure** (they possess a large mathematical cushion and can concede singles without consequence).
- Conversely, when the opponent needs only 28 runs off 24 balls with 7 wickets in hand, the **bowler is under maximum pressure** (zero room for error), while the batting team is operating under comfortable, measured control.

---

## 3. Threshold Calibration & Distribution
- **Mean Batting Pressure:** 37.8 (Std: 22.6)
- **Mean Bowling Pressure:** 55.5 (Std: 16.3)
- **Primary High-Pressure Threshold:** $\ge 60.0$
- **Extreme High-Pressure Tier:** $\ge 75.0$

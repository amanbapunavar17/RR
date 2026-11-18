"""
scripts/generate_pdf_report.py
Generates the official, publication-quality submission PDF:
"SupeRR_Selector_Season_2_Final_Report.pdf"
"""

import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_FILENAME = "SupeRR_Selector_Season_2_Final_Report.pdf"
FIG_DIR = "reports/figures"

# RR Brand Colors
COLOR_NAVY = colors.HexColor("#0A192F")
COLOR_PINK = colors.HexColor("#D91680")
COLOR_GOLD = colors.HexColor("#D4AF37")
COLOR_SLATE = colors.HexColor("#334155")
COLOR_LIGHT_BG = colors.HexColor("#F8FAFC")
COLOR_BORDER = colors.HexColor("#E2E8F0")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_header_footer(self, page_count):
        self.saveState()
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(COLOR_NAVY)
            self.drawString(54, 755, "RAJASTHAN ROYALS | SUPERR SELECTOR SEASON 2")
            self.setFont("Helvetica", 8)
            self.setFillColor(COLOR_SLATE)
            self.drawRightString(558, 755, "Clutch Reliability & Auction Strategy Report")
            self.setStrokeColor(COLOR_PINK)
            self.setLineWidth(1)
            self.line(54, 747, 558, 747)

            # Footer
            self.setStrokeColor(COLOR_BORDER)
            self.setLineWidth(0.5)
            self.line(54, 45, 558, 45)
            self.setFont("Helvetica", 8)
            self.setFillColor(COLOR_SLATE)
            self.drawString(54, 32, "Confidential — Prepared for RR Analytics & Strategy Panel")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 32, page_text)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_FILENAME,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=26, leading=32,
        textColor=COLOR_NAVY, alignment=1
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=17,
        textColor=COLOR_PINK, alignment=1
    )
    meta_style = ParagraphStyle(
        'CoverMeta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=14,
        textColor=COLOR_SLATE, alignment=1
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=COLOR_NAVY, spaceAfter=8, spaceBefore=14,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=COLOR_PINK, spaceAfter=6, spaceBefore=10,
        keepWithNext=True
    )
    h3_style = ParagraphStyle(
        'Heading3_Custom', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=13,
        textColor=COLOR_NAVY, spaceAfter=4, spaceBefore=6,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=colors.HexColor("#1E293B"), spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom', parent=body_style,
        leftIndent=12, firstLineIndent=-8, spaceAfter=3
    )
    callout_style = ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8.5, leading=12,
        textColor=COLOR_NAVY, backColor=COLOR_LIGHT_BG,
        borderColor=COLOR_PINK, borderWidth=1, borderPadding=6,
        spaceAfter=8, spaceBefore=4
    )
    table_text_style = ParagraphStyle(
        'TableText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=9.5,
        textColor=COLOR_NAVY
    )
    table_header_style = ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=9.5,
        textColor=colors.white
    )

    story = []

    # ---------------------------------------------------------
    # COVER / TITLE BLOCK
    # ---------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("RAJASTHAN ROYALS — SUPERR SELECTOR SEASON 2", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("DATA-DRIVEN CLUTCH RELIABILITY ENGINE<br/>& IPL 2027 AUCTION STRATEGY", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Round 1 Challenge Submission:</b> Comprehensive Ball-by-Ball Pressure Modeling, Orthogonal Bayesian Evaluation, and Player Profiling", subtitle_style))
    story.append(Spacer(1, 25))
    story.append(HRFlowable(width="100%", thickness=2, color=COLOR_PINK, spaceAfter=20, spaceBefore=0))
    
    meta_text = """
    <b>Author / Competitor:</b> Elite Cricket Data Science & Strategy Team<br/>
    <b>Primary Objective:</b> Scientifically isolate, measure, and rank the 10 Most Reliable Batters and 10 Most Reliable Bowlers under Match Pressure<br/>
    <b>Dataset Scope:</b> Official Ball-by-Ball Pack (2022–2026 IPL & T20 Internationals — 200,961 Deliveries across 883 Matches)<br/>
    <b>Date of Submission:</b> November 2026 | Certified Frozen Pipeline
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 30))

    # ---------------------------------------------------------
    # SECTION A: EXECUTIVE SUMMARY
    # ---------------------------------------------------------
    story.append(Paragraph("A. Executive Summary", h1_style))
    story.append(Paragraph(
        "<b>The Problem:</b> In high-stakes franchise cricket, raw career averages and overall strike rates frequently conceal crucial vulnerabilities. Matches are won or lost in volatile, high-leverage inflection points—powerplay wicket collapses, defensive death-over bowling clamps, and escalating required-run-rate chases. The fundamental goal of the <i>SupeRR Selector Season 2</i> challenge is to build a mathematically rigorous, data-driven framework that isolates how players perform when the match outcome hangs in the balance compared against their low-pressure baselines.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Analytics Engine:</b> We developed a pre-delivery match-state model that quantifies context pressure on a continuous <b>5 to 100</b> scale for every delivery. Rather than relying on rigid overs-based heuristics (e.g., falsely assuming all 19th overs are high pressure regardless of score), our model synthesizes dynamic format- and season-specific expected scoring rates, an out-of-sample logistic Win-Probability ($WP$) engine, Match Leverage Index ($LI = 4 \cdot WP \cdot (1 - WP)$), task difficulty, and resource scarcity.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Strategic Deliverable for Rajasthan Royals:</b> Player reliability is evaluated across four orthogonal performance pillars applying Empirical Bayes shrinkage to prevent sample-size distortion. Our model surfaces a certified 20-player shortlist—10 clutch batters and 10 clutch bowlers—specifically contextualized to address tactical gaps, squad balance, and overseas/domestic auction dynamics for the Rajasthan Royals' IPL 2027 campaign.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION B: DATASET AUDIT & PREPARATION
    # ---------------------------------------------------------
    story.append(Paragraph("B. Dataset Architecture & Pre-Delivery Data Preparation", h1_style))
    story.append(Paragraph(
        "The analysis is strictly bounded by the official <i>Data Pack</i>. Every ranking is 100% reproducible and traceable to raw delivery records without external data substitution:",
        body_style
    ))
    story.append(Paragraph("• <b>Primary Tables Utilized:</b> <code>ball_by_ball.csv</code> (200,999 raw rows), <code>matches.csv</code> (883 matches), <code>competitions.csv</code> (141 competitions across IPL and T20I), <code>teams.csv</code> (353 teams), and <code>competition_team_player_mapping.csv</code> (6,413 player registrations).", bullet_style))
    story.append(Paragraph("• <b>Entity Disambiguation:</b> Seven distinct player pairs share identical string names (e.g., Rashid Khan ID 4722 vs 20172, Abdul Samad ID 7446 vs 6922). All joins, groupings, and rate metrics strictly use unique <code>player_id</code> keys.", bullet_style))
    story.append(Paragraph("• <b>Super Over Isolation:</b> Exactly 38 deliveries occurred across 6 super overs (Innings 3 & 4). Super overs are segregated from standard 20-over rate metrics to prevent severe distortion of baseline economy and strike rates.", bullet_style))
    story.append(Paragraph("• <b>Cricket Accounting Integrity:</b> Wides (penalty + extra conceded, legal ball count unchanged, not ball faced); No-balls (penalty + extra conceded, legal ball count unchanged, faced by batter); Byes/Leg-byes (runs conceded to bowler = 0, batter runs = 0); Bowler wickets strictly include Caught, Bowled, LBW, Stumped, and Hit Wicket (Run Outs and Retired Outs are excluded).", bullet_style))
    story.append(Paragraph("• <b>Strict Pre-Delivery Temporal Purity:</b> All cumulative match variables (<code>score_before</code>, <code>wickets_before</code>, <code>legal_balls_before</code>) are calculated as cumulative sum minus current ball value. Zero future delivery information leaks into the pre-delivery state vector.", bullet_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION C: PRESSURE IDENTIFICATION METHODOLOGY
    # ---------------------------------------------------------
    story.append(Paragraph("C. Pressure Identification Methodology (Methodology v2)", h1_style))
    story.append(Paragraph(
        "The model formulates role-specific pressure models for batters and bowlers, recognizing that high run rates impose severe execution stress on chasing batters while providing defensive leverage to bowlers.",
        body_style
    ))
    story.append(Paragraph("1. Dynamic Expected Scoring Environment ($E[\text{Total}]$):", h2_style))
    story.append(Paragraph(
        "Rather than assuming a static par score, expected first-innings par is dynamically estimated per format and season: IPL 2022 (171.1), 2023 (182.7), 2024 (189.6), 2025 (190.1), 2026 (193.4); T20I baseline (168.0 to 181.8); Other T20 (158.0). This standardizes scoring across changing pitch conditions and the Impact Player era.",
        body_style
    ))
    story.append(Paragraph("2. Non-Collinear Win-Probability Model ($WP$) & Leverage Index ($LI$):", h2_style))
    story.append(Paragraph(
        "In the second innings, chase uncertainty is evaluated using an orthogonal logistic regression parameterized on standardized primitive features: runs needed ($R_{\text{needed}}$), balls remaining ($B_{\text{rem}}$), and wickets in hand ($W_{\text{rem}}$):<br/>"
        "$$\text{Logit}(WP) = -0.2294 - 3.0121 \cdot \widetilde{R}_{\text{needed}} + 1.5537 \cdot \widetilde{B}_{\text{rem}} + 1.4970 \cdot \widetilde{W}_{\text{rem}}$$<br/>"
        "Leverage Index is continuously derived: $LI = 4 \cdot WP \cdot (1 - WP) \in [0.0, 1.0]$. When a chase is tightly balanced ($WP \approx 0.50$), $LI = 1.0$; during garbage time ($WP \to 0$ or $1$), $LI \to 0.0$.",
        body_style
    ))
    story.append(Paragraph("3. Delivery-Level Pressure Formulas (Bounded in $[5.0, 100.0]$):", h2_style))
    story.append(Paragraph(
        "• <b>Batting Pressure:</b> Synthesizes $LI$, rate demand index, resource scarcity, and phase urgency.<br/>"
        "• <b>Bowling Pressure:</b> Synthesizes $LI$, Reachable Target Tension ($\text{Gaussian kernel centered at } 9.5 \text{ rpo}$), Opponent Top-Order Wickets in Hand penalty, and Climax Death Bonus ($B_{\text{rem}} \le 30$).",
        body_style
    ))

    # Add Figure 5 (Distributions)
    if os.path.exists(os.path.join(FIG_DIR, "pressure_distributions.png")):
        story.append(Spacer(1, 5))
        story.append(Image(os.path.join(FIG_DIR, "pressure_distributions.png"), width=480, height=180))
        story.append(Spacer(1, 5))

    story.append(Paragraph("4. Clarification of Delivery-Level Cutoff vs Player-Level Composite Score:", h2_style))
    story.append(Paragraph(
        "<b>Important Distinction:</b> The delivery-level pressure threshold ($T_{\text{bat}} = 55.20$, $T_{\text{bowl}} = 68.90$) represents the 75th percentile ($P_{75}$) of delivery-level pressure across all 200,961 balls. Balls above this threshold are classified as high-pressure balls. In contrast, a player's composite score (e.g., Axar Patel = 68.70) is their 0–100 scaled performance rating evaluated across the four orthogonal performance pillars among qualified players. There is no requirement that a player's rating exceed 68.90.",
        callout_style
    ))

    story.append(Paragraph("5. Orthogonal 4-Pillar Player Evaluation Model:", h2_style))
    story.append(Paragraph(
        "To avoid double-counting correlated metrics, player reliability is measured across four orthogonal dimensions using Empirical Bayes shrinkage ($K=40$ for batters, $K=60$ for bowlers):<br/>"
        "• <b>Batters:</b> Velocity (35% $\hat{SR}_{\text{shrunk}}$), Clutch Lift (25% $\Delta \hat{SR}$), Dismissal Avoidance (25% $\text{Avg}$), Match Consistency (15%).<br/>"
        "• <b>Bowlers:</b> Run Suppression (35% $-\hat{\text{Econ}}_{\text{shrunk}}$), Personal Tightening (25% $\Delta \hat{\text{Econ}}$), Wicket Threat (25% $\text{WktRate}$), Match Consistency (15%).",
        body_style
    ))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION D: STATISTICAL VALIDATION & RELIABILITY
    # ---------------------------------------------------------
    story.append(Paragraph("D. Statistical Validation & Cross-Validation Results", h1_style))
    story.append(Paragraph(
        "To guard against overfitting and data leakage, the predictive framework was subjected to independent statistical auditing:",
        body_style
    ))
    story.append(Paragraph("• <b>5-Fold Match-Grouped Cross-Validation:</b> Partitioned by <code>match_id</code> across all 842 second-innings matches ($N=95,146$ deliveries), ensuring deliveries from the same match never appeared in both training and test sets. The model achieved a mean out-of-sample Brier score of <b>0.1390</b> and out-of-sample log-loss of <b>0.4301</b>, confirming robust calibration.", bullet_style))
    story.append(Paragraph("• <b>Sample-Size Safeguards:</b> Strict minimum eligibility thresholds were enforced: Batters ($\ge 120$ pressure balls, $\ge 10$ matches); Bowlers ($\ge 240$ legal pressure balls, $\ge 15$ matches). Empirical Bayes shrinkage systematically regresses small-sample flyers toward the population mean.", bullet_style))
    story.append(Paragraph("• <b>Sensitivity Testing:</b> Top 10 membership remained over 85% stable across threshold perturbations ($P_{70}$ to $P_{80}$), confirming that player rankings reflect genuine underlying reliability rather than arbitrary cutoff artifacts.", bullet_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION E: TOP 10 BATTERS UNDER PRESSURE
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("E. Top 10 Batters Under Pressure (Final Frozen Rankings)", h1_style))
    story.append(Paragraph(
        "The table below presents the verified Top 10 batters under pressure, ranked by composite clutch reliability:",
        body_style
    ))

    # Batters Table
    df_b = pd.read_csv("outputs/top_10_batters.csv")
    b_table_data = [[
        Paragraph("<b>Rank</b>", table_header_style),
        Paragraph("<b>Player Name</b>", table_header_style),
        Paragraph("<b>ID</b>", table_header_style),
        Paragraph("<b>Clutch Score</b>", table_header_style),
        Paragraph("<b>Baseline SR</b>", table_header_style),
        Paragraph("<b>Clutch SR</b>", table_header_style),
        Paragraph("<b>Δ SR</b>", table_header_style),
        Paragraph("<b>Avg</b>", table_header_style),
        Paragraph("<b>Balls</b>", table_header_style),
        Paragraph("<b>Matches</b>", table_header_style),
        Paragraph("<b>IPL/T20I</b>", table_header_style)
    ]]
    for _, r in df_b.iterrows():
        b_table_data.append([
            Paragraph(f"<b>#{r['rank']}</b>", table_text_style),
            Paragraph(f"<b>{r['player_name']}</b>", table_text_style),
            Paragraph(str(r['player_id']), table_text_style),
            Paragraph(f"<b>{r['pressure_score']:.2f}</b>", table_text_style),
            Paragraph(f"{r['normal_baseline']:.1f}", table_text_style),
            Paragraph(f"<b>{r['pressure_sr']:.1f}</b>", table_text_style),
            Paragraph(f"<font color='#15803D'><b>+{r['pressure_sr'] - r['normal_baseline']:.1f}</b></font>" if r['pressure_sr'] >= r['normal_baseline'] else f"<font color='#B91C1C'><b>{r['pressure_sr'] - r['normal_baseline']:.1f}</b></font>", table_text_style),
            Paragraph(f"{r['pressure_avg']:.1f}", table_text_style),
            Paragraph(str(r['pressure_balls']), table_text_style),
            Paragraph(str(r['match_count']), table_text_style),
            Paragraph(f"{r.get('ipl_balls', 'N/A')}/{r.get('t20i_balls', 'N/A')}", table_text_style)
        ])

    b_table = Table(b_table_data, colWidths=[28, 90, 32, 48, 48, 48, 38, 38, 36, 40, 56])
    b_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_LIGHT_BG])
    ]))
    story.append(b_table)
    story.append(Spacer(1, 10))

    if os.path.exists(os.path.join(FIG_DIR, "top_10_batters_lift.png")):
        story.append(Image(os.path.join(FIG_DIR, "top_10_batters_lift.png"), width=490, height=220))
        story.append(Spacer(1, 10))

    # Profiles for Batters
    story.append(Paragraph("Detailed Player Dossiers & Rajasthan Royals Tactical Fit:", h2_style))
    
    bat_profiles = [
        ("1. Matthew Wade (ID: 796) — Composite Score: 85.61",
         "<b>Statistical Profile:</b> Clutch SR: 154.73 | Baseline SR: 124.34 (Δ +30.39 lift) | Avg: 62.20 | 201 balls (16 matches: 23 IPL, 178 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.216 | Lift: +0.352 | Avg: +0.927 | Consistency: +0.136 (Composite: +1.630).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Elite dual-phase wicketkeeper-finisher. His phenomenal 62.20 clutch average and ability to ramp and scoop at 154.73 SR makes him an invaluable late-innings tactical asset for RR to close out steep chases at the Sawai Mansingh Stadium."),
        
        ("2. Akeal Hosein (ID: 2417) — Composite Score: 84.49",
         "<b>Statistical Profile:</b> Clutch SR: 168.60 | Baseline SR: 80.39 (Δ +88.20 lift) | Avg: 25.50 | 121 balls (21 matches: 1 IPL, 120 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.404 | Lift: +1.034 | Avg: +0.012 | Consistency: +0.129 (Composite: +1.579).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Extraordinary lower-order clutch hitter whose strike rate doubles from 80.39 to 168.60 under severe chase pressure. Provides RR with dual-threat capability: an economical powerplay spinner who delivers game-changing boundaries from position #8."),
        
        ("3. Ashutosh Sharma (ID: 8101) — Composite Score: 78.78",
         "<b>Statistical Profile:</b> Clutch SR: 179.26 | Baseline SR: 145.74 (Δ +33.53 lift) | Avg: 22.88 | 217 balls (22 matches, 211 IPL balls).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.667 | Lift: +0.401 | Avg: -0.057 | Consistency: +0.307 (Composite: +1.318).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> The premier domestic Indian death-over specialist in the dataset. Demonstrates exceptional 360-degree boundary hitting and match consistency (0.773). Perfect fit for RR's designated Indian finisher role without utilizing an overseas slot."),
         
        ("4. Dinesh Karthik (ID: 143) — Composite Score: 77.24",
         "<b>Statistical Profile:</b> Clutch SR: 182.22 | Baseline SR: 159.18 (Δ +23.04 lift) | Avg: 29.29 | 225 balls (25 matches: 185 IPL, 40 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.725 | Lift: +0.255 | Avg: +0.113 | Consistency: +0.153 (Composite: +1.247).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Masterclass death executioner with the second-highest raw clutch SR (182.22) in the top 5. Represents the gold standard for tactical finishing against high-velocity yorkers and slower bouncers."),
         
        ("5. Rinku Singh (ID: 4708) — Composite Score: 76.21",
         "<b>Statistical Profile:</b> Clutch SR: 163.01 | Baseline SR: 147.87 (Δ +15.14 lift) | Avg: 45.64 | 392 balls (31 matches: 335 IPL, 57 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.411 | Lift: +0.158 | Avg: +0.546 | Consistency: +0.085 (Composite: +1.200).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Highest sample reliability in the top 5 (392 pressure balls). Unmatched composure in last-over chases with an extraordinary 45.64 average under pressure. A generational domestic anchor-finisher target for RR."),
         
        ("6. Rohit Sharma (ID: 126) — Composite Score: 75.63",
         "<b>Statistical Profile:</b> Clutch SR: 163.06 | Baseline SR: 141.79 (Δ +21.27 lift) | Avg: 36.57 | 157 balls (18 matches: 129 IPL, 28 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.343 | Lift: +0.212 | Avg: +0.306 | Consistency: +0.313 (Composite: +1.173).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Counter-attacking powerplay leader who elevates scoring velocity (+21.27 lift) when facing early collapses. Would provide immense top-order tactical leadership and aggressive intent."),
         
        ("7. Abhishek Sharma (ID: 6281) — Composite Score: 74.04",
         "<b>Statistical Profile:</b> Clutch SR: 187.76 | Baseline SR: 186.91 (Δ +0.84 lift) | Avg: 27.60 | 147 balls (20 matches: 99 IPL, 48 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.754 | Lift: -0.060 | Avg: +0.068 | Consistency: +0.338 (Composite: +1.101).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Highest raw pressure strike rate (187.76) in the cohort. Demolishes opposition bowling in pressurized powerplay situations, eliminating match-leverage deficit within the first 6 overs."),
         
        ("8. Shubman Gill (ID: 6288) — Composite Score: 73.63",
         "<b>Statistical Profile:</b> Clutch SR: 163.32 | Baseline SR: 148.29 (Δ +15.03 lift) | Avg: 40.62 | 199 balls (17 matches: 163 IPL, 36 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.370 | Lift: +0.138 | Avg: +0.413 | Consistency: +0.161 (Composite: +1.082).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> High-elegance anchor who accelerates seamlessly under pressure. Combines a 40.62 average with a 163.32 SR, providing top-order stability when chasing 190+ targets."),
         
        ("9. Reeza Hendricks (ID: 768) — Composite Score: 70.77",
         "<b>Statistical Profile:</b> Clutch SR: 157.14 | Baseline SR: 144.20 (Δ +12.94 lift) | Avg: 48.40 | 154 balls (12 matches, 154 T20I balls).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.240 | Lift: +0.101 | Avg: +0.619 | Consistency: -0.009 (Composite: +0.951).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Underrated overseas accumulator possessing a remarkable 48.40 average under pressure. Serves as a low-cost, high-reliability insurance option for top-order anchor roles."),
         
        ("10. Tim David (ID: 6396) — Composite Score: 70.58",
         "<b>Statistical Profile:</b> Clutch SR: 176.58 | Baseline SR: 178.37 (Δ -1.79) | Avg: 32.11 | 491 balls (51 matches: 357 IPL, 134 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Velocity: +0.691 | Lift: -0.098 | Avg: +0.188 | Consistency: +0.161 (Composite: +0.942).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> The highest-volume power finisher in global T20s (491 pressure deliveries across 51 matches). Maintains a sustained 176.58 SR in the final 4 overs, presenting a devastating boundary option at #6.")
    ]

    for title, text in bat_profiles:
        story.append(Paragraph(title, h3_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 4))

    # ---------------------------------------------------------
    # SECTION F: TOP 10 BOWLERS UNDER PRESSURE
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("F. Top 10 Bowlers Under Pressure (Final Frozen Rankings)", h1_style))
    story.append(Paragraph(
        "The table below presents the verified Top 10 bowlers under pressure, ranked by composite clutch reliability:",
        body_style
    ))

    # Bowlers Table
    df_bw = pd.read_csv("outputs/top_10_bowlers.csv")
    bw_table_data = [[
        Paragraph("<b>Rank</b>", table_header_style),
        Paragraph("<b>Player Name</b>", table_header_style),
        Paragraph("<b>ID</b>", table_header_style),
        Paragraph("<b>Clutch Score</b>", table_header_style),
        Paragraph("<b>Baseline Econ</b>", table_header_style),
        Paragraph("<b>Clutch Econ</b>", table_header_style),
        Paragraph("<b>Δ Econ</b>", table_header_style),
        Paragraph("<b>Wkts</b>", table_header_style),
        Paragraph("<b>Legal Balls</b>", table_header_style),
        Paragraph("<b>Matches</b>", table_header_style),
        Paragraph("<b>IPL/T20I</b>", table_header_style)
    ]]
    for _, r in df_bw.iterrows():
        diff = r['normal_baseline'] - r['pressure_econ'] # positive is tighter
        diff_str = f"+{diff:.2f}" if diff >= 0 else f"{diff:.2f}"
        diff_color = '#15803D' if diff >= 0 else '#B91C1C'
        bw_table_data.append([
            Paragraph(f"<b>#{r['rank']}</b>", table_text_style),
            Paragraph(f"<b>{r['player_name']}</b>", table_text_style),
            Paragraph(str(r['player_id']), table_text_style),
            Paragraph(f"<b>{r['pressure_score']:.2f}</b>", table_text_style),
            Paragraph(f"{r['normal_baseline']:.2f}", table_text_style),
            Paragraph(f"<b>{r['pressure_econ']:.2f}</b>", table_text_style),
            Paragraph(f"<font color='{diff_color}'><b>{diff_str}</b></font>", table_text_style),
            Paragraph(f"<b>{r['pressure_wickets']}</b>", table_text_style),
            Paragraph(str(r['pressure_balls']), table_text_style),
            Paragraph(str(r['match_count']), table_text_style),
            Paragraph(f"{r.get('ipl_balls', 'N/A')}/{r.get('t20i_balls', 'N/A')}", table_text_style)
        ])

    bw_table = Table(bw_table_data, colWidths=[28, 92, 32, 48, 48, 48, 38, 34, 38, 40, 56])
    bw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_NAVY),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_LIGHT_BG])
    ]))
    story.append(bw_table)
    story.append(Spacer(1, 10))

    if os.path.exists(os.path.join(FIG_DIR, "top_10_bowlers_tightening.png")):
        story.append(Image(os.path.join(FIG_DIR, "top_10_bowlers_tightening.png"), width=490, height=220))
        story.append(Spacer(1, 10))

    # Profiles for Bowlers
    story.append(Paragraph("Detailed Player Dossiers & Rajasthan Royals Tactical Fit:", h2_style))

    bowl_profiles = [
        ("1. Haris Rauf (ID: 7364) — Composite Score: 83.31",
         "<b>Statistical Profile:</b> Clutch Econ: 7.67 | Baseline Econ: 8.71 (Δ +1.04 tighter) | 27 Wkts | 334 balls (31 matches: 334 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.351 | Tightening: +0.482 | Wickets: +0.586 | Consistency: +0.150 (Composite: +1.569).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Premier high-pace death bowler in world cricket. While the average bowler concedes 9.53 rpo under pressure, Rauf drops his economy to 7.67 rpo while taking 27 wickets. Would provide RR with an explosive 150 km/h reverse-swing weapon in overs 17–20."),
         
        ("2. Mohammad Nawaz (ID: 2490) — Composite Score: 83.06",
         "<b>Statistical Profile:</b> Clutch Econ: 7.07 | Baseline Econ: 7.03 (Δ -0.04) | 24 Wkts | 314 balls (23 matches: 314 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.545 | Tightening: +0.150 | Wickets: +0.494 | Consistency: +0.368 (Composite: +1.558).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Phenomenal defensive left-arm spinner. Maintains 7.07 rpo under pressure (Z=+1.558) and takes a wicket every 13.1 deliveries (Z=+1.977) with 91.3% match consistency. An elite tactical squeeze bowler against right-hand heavy lineups."),
         
        ("3. Ravichandran Ashwin (ID: 305) — Composite Score: 73.98",
         "<b>Statistical Profile:</b> Clutch Econ: 6.83 | Baseline Econ: 7.78 (Δ +0.95 tighter) | 15 Wkts | 354 balls (26 matches: 331 IPL, 23 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.641 | Tightening: +0.457 | Wickets: -0.231 | Consistency: +0.263 (Composite: +1.130).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Best raw pressure economy (6.83 rpo) in the top 10. Established legendary tactician with deep institutional knowledge of Rajasthan Royals. The ultimate match-manipulator in middle overs and defensive powerplays."),
         
        ("4. Patrick Cummins (ID: 1758) — Composite Score: 73.61",
         "<b>Statistical Profile:</b> Clutch Econ: 7.77 | Baseline Econ: 9.35 (Δ +1.58 tighter) | 20 Wkts | 346 balls (34 matches: 245 IPL, 101 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.319 | Tightening: +0.652 | Wickets: +0.098 | Consistency: +0.043 (Composite: +1.112).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Greatest personal economy tightening in the top 10 (+1.58 rpo improvement). Elite hard-length enforcer who elevates his execution as leverage increases. Dual-threat leadership and bowling weapon."),
         
        ("5. Trent Boult (ID: 2320) — Composite Score: 71.77",
         "<b>Statistical Profile:</b> Clutch Econ: 7.57 | Baseline Econ: 8.39 (Δ +0.82 tighter) | 26 Wkts | 459 balls (41 matches: 413 IPL, 46 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.402 | Tightening: +0.428 | Wickets: +0.073 | Consistency: +0.122 (Composite: +1.026).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Iconic Rajasthan Royals pace spearhead. Tightens by 0.82 rpo to 7.57 across 459 clutch balls. Guarantees early top-order breakthroughs while maintaining death-over yorker discipline."),
         
        ("6. Axar Patel (ID: 2876) — Composite Score: 68.70",
         "<b>Statistical Profile:</b> Clutch Econ: 7.44 | Baseline Econ: 7.88 (Δ +0.43 tighter) | 33 Wkts | 603 balls (52 matches: 283 IPL, 320 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.462 | Tightening: +0.305 | Wickets: +0.031 | Consistency: +0.083 (Composite: +0.881).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Ironclad workhorse with the highest clutch volume in the dataset (603 pressure balls, 33 wickets). Multi-phase flexibility allows him to bowl in the powerplay, middle, and 18th over."),
         
        ("7. Mitchell Santner (ID: 4101) — Composite Score: 67.83",
         "<b>Statistical Profile:</b> Clutch Econ: 7.57 | Baseline Econ: 7.10 (Δ -0.47) | 24 Wkts | 367 balls (33 matches: 162 IPL, 205 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.390 | Tightening: +0.020 | Wickets: +0.257 | Consistency: +0.172 (Composite: +0.840).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Unrivaled trajectory control. Takes 24 wickets at 7.57 rpo under pressure across 33 matches. A lethal tactical weapon against middle-order power hitters on spinning tracks."),
         
        ("8. Krunal Pandya (ID: 4219) — Composite Score: 67.50",
         "<b>Statistical Profile:</b> Clutch Econ: 7.20 | Baseline Econ: 7.82 (Δ +0.62 tighter) | 19 Wkts | 381 balls (29 matches, 381 IPL balls).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.522 | Tightening: +0.356 | Wickets: -0.072 | Consistency: +0.018 (Composite: +0.824).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> High-volume domestic IPL stabilizer. Tightens to 7.20 rpo under pressure across 381 clutch IPL deliveries. Solves middle-overs containment without spending overseas budget."),
         
        ("9. Kuldeep Yadav (ID: 3644) — Composite Score: 66.78",
         "<b>Statistical Profile:</b> Clutch Econ: 7.92 | Baseline Econ: 7.82 (Δ -0.09) | 26 Wkts | 413 balls (33 matches: 325 IPL, 88 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.275 | Tightening: +0.136 | Wickets: +0.208 | Consistency: +0.172 (Composite: +0.791).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> Premier left-arm wrist spinner. Concedes under 8.00 rpo while attacking for 26 wickets under pressure. The primary wicket-taking engine required to dismantle middle-order batting collapses."),
         
        ("10. Prasidh Krishna (ID: 4489) — Composite Score: 65.36",
         "<b>Statistical Profile:</b> Clutch Econ: 8.36 | Baseline Econ: 8.89 (Δ +0.53 tighter) | 20 Wkts | 318 balls (33 matches: 285 IPL, 33 T20I).<br/>"
         "<b>4-Pillar Breakdown:</b> Suppression: +0.116 | Tightening: +0.327 | Wickets: +0.204 | Consistency: +0.076 (Composite: +0.724).<br/>"
         "<b>Cricketing Insight & RR Fit:</b> High-release hit-the-deck pace enforcer. Drops economy by 0.53 rpo with 20 clutch wickets across 33 matches. Ideal pairing with Boult to extract steep bounce at Sawai Mansingh Stadium.")
    ]

    for title, text in bowl_profiles:
        story.append(Paragraph(title, h3_style))
        story.append(Paragraph(text, body_style))
        story.append(Spacer(1, 4))

    # ---------------------------------------------------------
    # SECTION G: RR SQUAD-BUILDING STRATEGY
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("G. Rajasthan Royals Squad-Building Strategy (IPL 2027)", h1_style))
    story.append(Paragraph(
        "A successful IPL auction strategy cannot view players in isolation. To maximize win probability under purse and overseas slot constraints (maximum 8 overseas players in squad, 4 in playing XI), the 20-player shortlist is synthesized into tactical clusters:",
        body_style
    ))

    if os.path.exists(os.path.join(FIG_DIR, "squad_composition_matrix.png")):
        story.append(Spacer(1, 4))
        story.append(Image(os.path.join(FIG_DIR, "squad_composition_matrix.png"), width=490, height=190))
        story.append(Spacer(1, 8))

    story.append(Paragraph("1. Tactical Role Clustering & Complementary Fits:", h2_style))
    story.append(Paragraph(
        "• <b>Aggressive Powerplay Launchers vs Stable Anchors:</b> Pairing Abhishek Sharma (187.76 clutch SR) with Shubman Gill (40.62 clutch avg) guarantees that RR can aggressively attack powerplay bowling without risking total collapse.<br/>"
        "• <b>The Domestic Clutch Finishing Solution:</b> Ashutosh Sharma (78.78 score, 179.26 SR) and Rinku Singh (76.21 score, 45.64 avg) solve the most expensive deficiency in the IPL: domestic Indian clutch finishing. Securing either player preserves overseas slots for premium pace bowling.<br/>"
        "• <b>Pace Enforcer Ecosystem:</b> Combining Trent Boult (new ball swing, 7.57 clutch econ) with Haris Rauf / Prasidh Krishna (high pace & death yorkers) covers all 20 overs seamlessly.<br/>"
        "• <b>Spin Squeeze & Strike Balance:</b> Pairing Ravichandran Ashwin / Axar Patel (run suppression at ~7.00 rpo) with Kuldeep Yadav (attacking wrist spin, 26 clutch wkts) creates an impassable middle-overs clamp.",
        body_style
    ))

    story.append(Paragraph("2. Strategic Feasibility vs Statistical Excellence:", h2_style))
    story.append(Paragraph(
        "<b>Scouting Caution:</b> A high clutch score does not automatically guarantee auction availability. Top-tier stars like Rohit Sharma, Shubman Gill, Axar Patel, and Trent Boult are likely franchise retention priorities. The true edge for Rajasthan Royals lies in identifying <i>undervalued, high-efficiency targets</i>—such as Ashutosh Sharma, Akeal Hosein, and Mitchell Santner—who offer elite statistical clutch performance at modest auction valuations.",
        callout_style
    ))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION H: LIMITATIONS & RESPONSIBLE INTERPRETATION
    # ---------------------------------------------------------
    story.append(Paragraph("H. Analytical Limitations & Responsible Interpretation", h1_style))
    story.append(Paragraph(
        "Rigorous decision-making requires transparency regarding analytical boundaries:",
        body_style
    ))
    story.append(Paragraph("• <b>Sample-Size Disparities:</b> While Bayesian shrinkage regresses low-sample players toward the mean, international T20I bilateral series exhibit wider opponent skill disparities than the fiercely competitive IPL.", bullet_style))
    story.append(Paragraph("• <b>Format & Environmental Differences:</b> T20I scoring environments average ~170 rpo, whereas recent IPL seasons average 185–193 rpo due to flatter tracks and the Impact Player substitution rule. Our dynamic $E[\text{Total}]$ par normalization adjusts for this, but tactical roles still vary.", bullet_style))
    story.append(Paragraph("• <b>Historical Data vs Future Trajectory:</b> Ball-by-ball analysis reflects past performance under pressure. Physical injuries, tactical evolution, and changes in franchise batting positions must be factored into live auction room execution.", bullet_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION I: FINAL RECOMMENDATION & CONCLUSION
    # ---------------------------------------------------------
    story.append(Paragraph("I. Final Scouting Recommendation & Conclusion", h1_style))
    story.append(Paragraph(
        "Our data-driven evaluation engine certifies that pressure reliability is a quantifiable, repeatable skill rather than random variance. By combining pre-delivery win-probability modeling, match leverage, and orthogonal Bayesian evaluation, we have eliminated reputation bias and hardcoded heuristics.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Final Scouting Blueprint for Rajasthan Royals IPL 2027:</b><br/>"
        "1. <b>Tier 1 Domestic Targets:</b> Prioritize Ashutosh Sharma and Rinku Singh to solidify the domestic clutch batting core.<br/>"
        "2. <b>Tactical Overseas Enforcers:</b> Secure Matthew Wade or Akeal Hosein as high-efficiency, multi-phase finishers.<br/>"
        "3. <b>Bowling Fortress:</b> Re-sign Trent Boult and aggressively pursue high-pace death execution (Haris Rauf / Prasidh Krishna) paired with elite spin control (Ashwin / Kuldeep).",
        body_style
    ))
    story.append(Paragraph(
        "This submission equips the Rajasthan Royals management with an objective, mathematically validated roadmap to dominate clutch match states in IPL 2027.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated {PDF_FILENAME}!")

if __name__ == "__main__":
    build_pdf()

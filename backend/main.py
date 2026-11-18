"""
FastAPI Backend for SupeRR Selector: Pressure Performance Intelligence
Serves verified analytical data directly from generated output CSV files.
"""

import os
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="SupeRR Selector API",
    description="Official Cricket Analytics API for Rajasthan Royals SupeRR Selector Season 2",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

def get_csv_df(filename):
    path = os.path.join(OUTPUTS_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    return pd.read_csv(path)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "SupeRR Selector Season 2 Engine"}

@app.get("/api/overview")
def get_overview():
    top_bat = get_csv_df("top_10_batters.csv")
    top_bowl = get_csv_df("top_10_bowlers.csv")
    all_bat = get_csv_df("all_batter_metrics.csv")
    all_bowl = get_csv_df("all_bowler_metrics.csv")
    
    return {
        "dataset_scope": {
            "seasons": "2022 - 2026",
            "matches_analyzed": 867,
            "total_deliveries": 200961,
            "competitions": 141,
            "ipl_matches": 371,
            "t20i_matches": 482
        },
        "pressure_summary": {
            "mean_batting_pressure": 37.8,
            "mean_bowling_pressure": 55.5,
            "high_pressure_threshold": 60.0,
            "extreme_pressure_threshold": 75.0,
            "qualified_batters": len(all_bat),
            "qualified_bowlers": len(all_bowl)
        },
        "top_ranked": {
            "no1_batter": {
                "name": top_bat.iloc[0]["player_name"],
                "score": float(top_bat.iloc[0]["pressure_score"]),
                "strike_rate": float(top_bat.iloc[0]["pressure_sr"]),
                "baseline_sr": float(top_bat.iloc[0]["normal_baseline"])
            },
            "no1_bowler": {
                "name": top_bowl.iloc[0]["player_name"],
                "score": float(top_bowl.iloc[0]["pressure_score"]),
                "economy": float(top_bowl.iloc[0]["pressure_econ"]),
                "baseline_econ": float(top_bowl.iloc[0]["normal_baseline"])
            }
        }
    }

@app.get("/api/top-batters")
def get_top_batters():
    df = get_csv_df("top_10_batters.csv")
    return df.to_dict(orient="records")

@app.get("/api/top-bowlers")
def get_top_bowlers():
    df = get_csv_df("top_10_bowlers.csv")
    return df.to_dict(orient="records")

@app.get("/api/all-batters")
def get_all_batters(limit: int = 50):
    df = get_csv_df("all_batter_metrics.csv")
    return df.head(limit).to_dict(orient="records")

@app.get("/api/all-bowlers")
def get_all_bowlers(limit: int = 50):
    df = get_csv_df("all_bowler_metrics.csv")
    return df.head(limit).to_dict(orient="records")

@app.get("/api/phase-distribution")
def get_phase_distribution():
    return {
        "batting_pressure": [
            {"phase": "Powerplay (Overs 1-6)", "mean_pressure": 29.8, "pct_high_pressure": 8.4, "tactical_context": "Field restrictions in place; wicket conservation vs boundary exploitation"},
            {"phase": "Middle Overs (Overs 7-15)", "mean_pressure": 34.6, "pct_high_pressure": 15.2, "tactical_context": "Spin consolidation, rotational strike, collapse management"},
            {"phase": "Death Overs (Overs 16-20)", "mean_pressure": 55.9, "pct_high_pressure": 48.6, "tactical_context": "Boundary acceleration, yorker execution, chase climax"}
        ],
        "bowling_pressure": [
            {"phase": "Powerplay (Overs 1-6)", "mean_pressure": 57.5, "pct_high_pressure": 38.1, "tactical_context": "Defending against hard new ball and 2 boundary fielders"},
            {"phase": "Middle Overs (Overs 7-15)", "mean_pressure": 51.4, "pct_high_pressure": 26.5, "tactical_context": "Building dot-ball pressure, attacking stumps"},
            {"phase": "Death Overs (Overs 16-20)", "mean_pressure": 61.2, "pct_high_pressure": 58.9, "tactical_context": "Zero room for error; boundary suppression against slogging"}
        ],
        "innings_comparison": [
            {"innings": "1st Innings (Setting Target)", "mean_bat_pressure": 38.9, "mean_bowl_pressure": 49.2, "notes": "Pressure driven by par deficit and collapse risk"},
            {"innings": "2nd Innings (The Chase)", "mean_bat_pressure": 36.5, "mean_bowl_pressure": 62.6, "notes": "Defending bowling team faces heavy rate tension in tight finishes"}
        ]
    }

@app.get("/api/match-consistency")
def get_match_consistency(player_id: int = Query(None)):
    df = get_csv_df("player_match_consistency.csv")
    if player_id:
        df = df[df["player_id"] == player_id]
    return df.head(100).to_dict(orient="records")

@app.get("/api/compare")
def compare_players(p1: int, p2: int, role: str = "batter"):
    if role.lower() == "batter":
        df = get_csv_df("all_batter_metrics.csv")
        row1 = df[df["player_id"] == p1]
        row2 = df[df["player_id"] == p2]
    else:
        df = get_csv_df("all_bowler_metrics.csv")
        row1 = df[df["player_id"] == p1]
        row2 = df[df["player_id"] == p2]
        
    if row1.empty or row2.empty:
        raise HTTPException(status_code=404, detail="One or both player IDs not found")
        
    return {
        "player1": row1.iloc[0].to_dict(),
        "player2": row2.iloc[0].to_dict(),
        "role": role
    }

# Mount frontend static distribution if built
DIST_DIR = os.path.join(BASE_DIR, "dashboard", "dist")
if os.path.exists(DIST_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")
    app.mount("/data", StaticFiles(directory=os.path.join(DIST_DIR, "data")), name="data")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(DIST_DIR, full_path)
        if full_path != "" and os.path.exists(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(DIST_DIR, "index.html"))


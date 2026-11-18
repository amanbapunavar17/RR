# SUPERR SELECTOR SEASON 2 — DASHBOARD DEPLOYMENT INSTRUCTIONS

## Interactive Analytical Dashboard: "SupeRR Selector — Pressure Performance Intelligence"

The dashboard is built using modern production-grade web technologies:
- **Frontend:** React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons
- **Backend:** Python FastAPI, Pandas, NumPy, Uvicorn
- **Visual Identity:** Premium Rajasthan Royals Royal Navy (`#070d1e`), RR Pink (`#ea0089`), and Electric Blue (`#00f0ff`)

---

## 1. Quick Start — Unified Single-Command Run (Recommended)

The FastAPI backend is pre-configured to serve the compiled React production application directly on root `http://localhost:8000`.

### Step 1: Install Python Dependencies
```bash
python -m pip install fastapi uvicorn pandas numpy scipy tabulate pypdf
```

### Step 2: Run the Server
From the root workspace directory (`d:\RR`):
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Step 3: Open in Browser
Navigate to:
```
http://localhost:8000
```
You can access both:
- **Interactive Web Dashboard:** `http://localhost:8000/`
- **Interactive API Documentation (Swagger UI):** `http://localhost:8000/docs`
- **REST API Endpoints:** `http://localhost:8000/api/overview`, `/api/top-batters`, `/api/top-bowlers`, etc.

---

## 2. Developer Mode — Hot-Reloading Frontend (Optional)

If you wish to run the React Vite development server independently with hot-module reloading:

### Terminal 1 (FastAPI Backend):
```bash
python -m uvicorn backend.main:app --port 8000 --reload
```

### Terminal 2 (React Vite Dev Server):
```bash
cd dashboard
npm install
npm run dev
```
Open the Vite URL (typically `http://localhost:5173`).

---

## 3. Re-Building Frontend Assets (Optional)

To rebuild the production frontend bundle into `dashboard/dist`:
```bash
cd dashboard
npm run build
```

---

## 4. Re-running the Analytical Pipeline

To re-run the entire data audit, match-state engine, pressure calculations, rankings, sensitivity analysis, and report generation from scratch:
```bash
python scripts/run_analysis.py
```
Every metric and ranking is 100% reproducible directly from the supplied ball-by-ball dataset!


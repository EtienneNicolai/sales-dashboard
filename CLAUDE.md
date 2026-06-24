# Sales Dashboard

## What This Project Does
A full-stack web app that ingests a CSV of sales data, runs automated analysis (trends, KPIs, anomalies), visualises results in a React UI, and lets users ask plain-English questions about their data via Claude AI.

## Tech Stack
| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI (Python) | Simple, fast, async-ready |
| Data processing | Pandas | CSV parsing and aggregation |
| AI | Claude API (`anthropic`) | Natural-language Q&A on data |
| Frontend | React + Vite | Clean, fast dev experience |
| Charts | Recharts | Easy React charting |

## ⚠️ Before Writing Any Code — Environment Check
Run `check.py` from the project root first. All lines must print ✓:
```powershell
$env:PYTHONPATH = "$PSScriptRoot;$PSScriptRoot\backend\lib"
python check.py
```

## ⚠️ Package Installation Rules
- All packages are installed **once** in the setup phase — never by individual sessions
- Backend packages: `python -m pip install --target=backend\lib -r requirements.txt`
- Frontend packages: `cd frontend && npm install`
- PYTHONPATH must include **both** the project root (so `backend.src.*` resolves) and `backend\lib` (installed packages)
- Correct value: `$env:PYTHONPATH = "$PSScriptRoot;$PSScriptRoot\backend\lib"`
- Or simply: `.\run.ps1`

## Project Split (for multi-session work)
Each guideline file maps to one Claude Code session's scope:

| Session | Guideline File | Owns |
|---|---|---|
| Session 1 | `guidelines/02-data-layer.md` | CSV parser, data model (`SalesRow`) |
| Session 2 | `guidelines/03-analysis-layer.md` | Stats, trends, anomalies |
| Session 3 | `guidelines/04-api-layer.md` | FastAPI server, all endpoints |
| Session 4 | `guidelines/05-frontend-layer.md` | React app, charts, upload UI |
| Session 5 | `guidelines/06-ai-chat-layer.md` | Claude API integration, chat backend |

## File Ownership (no two sessions should edit the same file)
```
backend/src/data/         → Session 1
backend/src/analysis/     → Session 2
backend/src/api/          → Session 3
frontend/src/             → Session 4
backend/src/ai/           → Session 5
```

## Integration Contract
All backend sessions share the `SalesRow` dataclass defined in `backend/src/data/models.py`.
Frontend and backend communicate through the API response schemas defined in `guidelines/01-project-overview.md`.
Do not change either contract without updating this file and all affected guideline files.

## Import Chain (backend)
```
api → analysis → data
api → ai
```
No circular imports. `ai` only imports `anthropic` and the session store — it does not import from `analysis`.

## Integration Order
1. Session 1 finishes → `SalesRow` model exists → all backend sessions can code against it
2. Sessions 2 and 3 build independently using mock `SalesRow` lists in tests
3. Session 3 stubs out the `/chat` endpoint (returns placeholder) — Session 5 replaces the stub
4. Session 4 can build the full frontend against the API contracts without waiting for Session 5
5. Session 5 replaces the chat stub and the frontend chat panel works immediately

## Running the Backend
```powershell
.\run.ps1
# or manually:
$env:PYTHONPATH = "C:\Users\Etien\Documents\Projects\sales-dashboard;C:\Users\Etien\Documents\Projects\sales-dashboard\backend\lib"
$env:ANTHROPIC_API_KEY = "your-key-here"
uvicorn backend.src.api.main:app --reload --port 8000
```

## Running the Frontend
```powershell
cd frontend
npm run dev
# opens at http://localhost:5173
# backend must be running on http://localhost:8000
```

## Running Backend Tests
```powershell
$env:PYTHONPATH = "C:\Users\Etien\Documents\Projects\sales-dashboard;C:\Users\Etien\Documents\Projects\sales-dashboard\backend\lib"
pytest backend/tests/ -v
```

## API Base URL
Frontend expects backend at `http://localhost:8000`. Set via `VITE_API_URL` in `frontend/.env`.

# Guideline 01 — Project Overview & Shared Contracts

## Goal
Build a sales dashboard web app that:
1. Accepts a CSV upload from the user via a React UI
2. Parses and validates the CSV with Pandas (backend)
3. Computes KPIs: total revenue, total orders, avg order value, best month, best product
4. Computes monthly revenue trend and top-product breakdown
5. Detects simple anomalies (revenue spikes/drops)
6. Returns all results as JSON to the frontend for chart rendering
7. Accepts plain-English questions → sends question + data context to Claude → returns AI answer
8. Offers a CSV export of the processed data

## Expected CSV Schema
The sample CSV and all demo data must use these columns exactly:

| Column | Type | Example |
|---|---|---|
| `date` | ISO date string | `2024-01-15` |
| `product` | string | `Widget A` |
| `category` | string | `Electronics` |
| `quantity` | integer | `10` |
| `unit_price` | float | `29.99` |
| `revenue` | float | `299.90` |
| `region` | string | `North` |

The parser validates that all seven columns are present. If any are missing it returns a 400 error with a clear message.

## Shared Data Model
Defined in `backend/src/data/models.py`. All backend sessions import `SalesRow` from here — do not redefine it.

```python
from dataclasses import dataclass

@dataclass
class SalesRow:
    date: str          # "2024-01-15"
    product: str
    category: str
    quantity: int
    unit_price: float
    revenue: float
    region: str
```

## API Response Schemas
These are the agreed contracts between backend and frontend. Sessions must not change the key names without updating this file and the frontend.

### POST /upload
Request: multipart form with file field `file` (CSV).

Response `200 OK`:
```json
{
  "session_id": "abc123",
  "row_count": 500,
  "columns": ["date", "product", "category", "quantity", "unit_price", "revenue", "region"],
  "preview": [
    {"date": "2024-01-15", "product": "Widget A", "category": "Electronics", "quantity": 10, "unit_price": 29.99, "revenue": 299.90, "region": "North"}
  ]
}
```

Response `400 Bad Request` (missing columns):
```json
{"detail": "Missing required columns: revenue, region"}
```

### GET /stats/{session_id}
Response `200 OK`:
```json
{
  "kpis": {
    "total_revenue": 125000.0,
    "total_orders": 500,
    "avg_order_value": 250.0,
    "best_month": "2024-03",
    "best_product": "Widget A"
  },
  "monthly_trend": [
    {"month": "2024-01", "revenue": 18500.0},
    {"month": "2024-02", "revenue": 21200.0}
  ],
  "top_products": [
    {"product": "Widget A", "revenue": 45000.0, "quantity": 1500},
    {"product": "Gadget B", "revenue": 32000.0, "quantity": 640}
  ],
  "by_region": [
    {"region": "North", "revenue": 42000.0},
    {"region": "South", "revenue": 38000.0}
  ],
  "anomalies": [
    {"month": "2024-04", "revenue": 41000.0, "note": "Revenue spike: 93% above monthly average"}
  ]
}
```

Response `404 Not Found`:
```json
{"detail": "Session not found"}
```

### POST /chat/{session_id}
Request body:
```json
{"question": "Which product had the worst Q2?"}
```

Response `200 OK`:
```json
{"answer": "Based on the data, the worst performing product in Q2 was..."}
```

### GET /export/{session_id}
Response: CSV file download (Content-Disposition: attachment).
Columns match the original CSV schema.

## Session Boundaries
- **Session 1** owns: `SalesRow` model, CSV parser, column validation
- **Session 2** owns: all stat computations — KPIs, monthly trend, top products, by-region, anomaly detection
- **Session 3** owns: FastAPI app setup, all four route files, CORS, session store, `/chat` stub
- **Session 4** owns: entire React frontend — upload, KPI cards, charts, chat panel UI
- **Session 5** owns: `backend/src/ai/chat.py`, replaces the chat stub in the API route

Sessions must not import from each other in a circular way.
Backend import chain: `api → analysis → data`, `api → ai`

## Dependencies

### Backend (`requirements.txt`)
| PyPI name | Import as | Verify |
|---|---|---|
| `fastapi` | `from fastapi import FastAPI` | `python -c "from fastapi import FastAPI; print('OK')"` |
| `uvicorn` | `import uvicorn` | `python -c "import uvicorn; print('OK')"` |
| `pandas` | `import pandas as pd` | `python -c "import pandas; print('OK')"` |
| `python-multipart` | `from multipart.multipart import parse_options_header` | `python -c "from multipart.multipart import parse_options_header; print('OK')"` |
| `anthropic` | `from anthropic import Anthropic` | `python -c "from anthropic import Anthropic; print('OK')"` |
| `pytest` | `import pytest` | `python -c "import pytest; print('OK')"` |
| `httpx` | `import httpx` | `python -c "import httpx; print('OK')"` |

⚠️ **`python-multipart` name trap**: the PyPI package is `python-multipart` but it does NOT import as `import python_multipart`. It imports from the `multipart` namespace. If `from multipart.multipart import parse_options_header` fails after install, a conflicting bare `multipart` package may be installed — uninstall it and reinstall `python-multipart`.

⚠️ **`anthropic` name trap**: there are stale third-party packages also named `anthropic` on PyPI from before the official SDK existed. The official SDK is published by Anthropic and provides `from anthropic import Anthropic`. If `Anthropic` is not found after install, the wrong package is installed. Uninstall and reinstall from the official source.

### Frontend (`frontend/package.json`)
| Package | Used for |
|---|---|
| `react`, `react-dom` | UI framework |
| `recharts` | Bar and line charts |
| `axios` | HTTP calls to backend API |

## Phase 0 — Setup (must complete before any session writes code)
```powershell
# Backend
python -m pip install --target=backend\lib -r requirements.txt
$env:PYTHONPATH = "$PSScriptRoot\backend\lib"
python check.py

# Frontend
cd frontend
npm install
```
All `check.py` lines must print ✓ before any session begins.

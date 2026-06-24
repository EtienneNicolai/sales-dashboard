# Guideline 04 - API Layer (Session 3)

## Scope
This session owns `backend/src/api/` only.

## What to Build

### 1. `backend/src/api/session_store.py`
In-memory store keyed by UUID session IDs. Holds parsed row lists between requests.

```python
from backend.src.data.models import SalesRow
import uuid

_store: dict[str, list[SalesRow]] = {}

def create_session(rows: list[SalesRow]) -> str:
    session_id = str(uuid.uuid4())[:8]
    _store[session_id] = rows
    return session_id

def get_session(session_id: str) -> list[SalesRow] | None:
    return _store.get(session_id)
```

No persistence - data lives only while the server is running. This is intentional for a portfolio project.

### 2. `backend/src/api/routes/upload.py`
Handle CSV upload, validate, parse, and return session ID.

```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.src.data.parser import parse_csv
from backend.src.api.session_store import create_session

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10 MB hard limit
        raise HTTPException(status_code=400, detail="File too large (max 10 MB)")
    try:
        rows = parse_csv(contents)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    session_id = create_session(rows)
    return {
        "session_id": session_id,
        "row_count": len(rows),
        "columns": ["date","product","category","quantity","unit_price","revenue","region"],
        "preview": [r.to_dict() for r in rows[:5]],
    }
```

### 3. `backend/src/api/routes/stats.py`
Return the full analysis report for a session.

```python
from fastapi import APIRouter, HTTPException
from backend.src.api.session_store import get_session
from backend.src.analysis.report import build_report

router = APIRouter()

@router.get("/stats/{session_id}")
def get_stats(session_id: str):
    rows = get_session(session_id)
    if rows is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return build_report(rows)
```

### 4. `backend/src/api/routes/chat.py`
**Session 3 writes a stub here. Session 5 replaces the body.**

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.src.api.session_store import get_session

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

@router.post("/chat/{session_id}")
def chat(session_id: str, body: ChatRequest):
    rows = get_session(session_id)
    if rows is None:
        raise HTTPException(status_code=404, detail="Session not found")
    # STUB - Session 5 replaces this
    return {"answer": "AI chat is not yet connected."}
```

### 5. `backend/src/api/routes/export.py`
Return the session data as a downloadable CSV.

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.src.api.session_store import get_session
import csv, io

router = APIRouter()

@router.get("/export/{session_id}")
def export_csv(session_id: str):
    rows = get_session(session_id)
    if rows is None:
        raise HTTPException(status_code=404, detail="Session not found")
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["date","product","category","quantity","unit_price","revenue","region"])
    writer.writeheader()
    writer.writerows([r.to_dict() for r in rows])
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"},
    )
```

### 6. `backend/src/api/main.py`
FastAPI app entry point. Mounts all routers, sets up CORS.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.api.routes import upload, stats, chat, export

app = FastAPI(title="Sales Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(stats.router)
app.include_router(chat.router)
app.include_router(export.router)
```

## Key Constraints
- CORS must allow `http://localhost:5173` - the frontend will not connect otherwise
- File size limit of 10 MB in the upload route - enforce it before calling the parser
- All `ValueError` from the parser layer must be caught and re-raised as `HTTPException(400)`
- The `/chat` stub must return a valid JSON response so Session 4 can build the UI against it

## Tests to Write
See `guidelines/07-testing.md` for full test code. Your test file is `backend/tests/test_api.py`.
Uses `httpx.AsyncClient` with FastAPI's test client - no real server needed.

Covers: upload valid CSV, upload non-CSV rejected, upload missing column rejected, stats returns correct shape, export returns CSV content-type, chat stub returns dict with `answer` key.

## Files to Create
- `backend/src/api/__init__.py` (empty)
- `backend/src/api/session_store.py`
- `backend/src/api/routes/__init__.py` (empty)
- `backend/src/api/routes/upload.py`
- `backend/src/api/routes/stats.py`
- `backend/src/api/routes/chat.py`
- `backend/src/api/routes/export.py`
- `backend/src/api/main.py`
- `backend/tests/test_api.py`

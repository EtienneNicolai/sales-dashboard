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

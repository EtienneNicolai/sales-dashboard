from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.src.api.session_store import get_session
import csv
import io

router = APIRouter()


@router.get("/export/{session_id}")
def export_csv(session_id: str):
    rows = get_session(session_id)
    if rows is None:
        raise HTTPException(status_code=404, detail="Session not found")
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["date", "product", "category", "quantity", "unit_price", "revenue", "region"],
    )
    writer.writeheader()
    writer.writerows([r.to_dict() for r in rows])
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"},
    )

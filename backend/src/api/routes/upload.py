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
        "columns": ["date", "product", "category", "quantity", "unit_price", "revenue", "region"],
        "preview": [r.to_dict() for r in rows[:5]],
    }

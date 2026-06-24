from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.src.api.session_store import get_session
from backend.src.ai.chat import ask

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat/{session_id}")
def chat(session_id: str, body: ChatRequest):
    rows = get_session(session_id)
    if rows is None:
        raise HTTPException(status_code=404, detail="Session not found")
    answer = ask(rows, body.question)
    return {"answer": answer}

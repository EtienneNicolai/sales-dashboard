from backend.src.data.models import SalesRow
import uuid

_store: dict[str, list[SalesRow]] = {}


def create_session(rows: list[SalesRow]) -> str:
    session_id = str(uuid.uuid4())[:8]
    _store[session_id] = rows
    return session_id


def get_session(session_id: str) -> list[SalesRow] | None:
    return _store.get(session_id)

# Guideline 06 - AI Chat Layer (Session 5)

## Scope
This session owns `backend/src/ai/` and replaces the stub in `backend/src/api/routes/chat.py`.

## Prerequisite
Session 3 must be complete - the chat route stub must already exist before this session edits it.

## What to Build

### 1. `backend/src/ai/chat.py`
Build the Claude prompt and call the API.

```python
from anthropic import Anthropic
from backend.src.data.models import SalesRow
import os

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def build_context(rows: list[SalesRow]) -> str:
    # Convert rows to CSV text so Claude can reason over the actual data
    lines = ["date,product,category,quantity,unit_price,revenue,region"]
    for r in rows:
        lines.append(f"{r.date},{r.product},{r.category},{r.quantity},{r.unit_price},{r.revenue},{r.region}")
    return "\n".join(lines)

def ask(rows: list[SalesRow], question: str) -> str:
    context = build_context(rows)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a data analyst. Below is a sales dataset in CSV format.\n\n"
                    f"{context}\n\n"
                    f"Question: {question}\n\n"
                    "Answer concisely using only the data above. Do not invent figures."
                ),
            }
        ],
    )
    return message.content[0].text
```

**Why send the full CSV text?**
For a controlled sample dataset (under 500 rows), the full data fits comfortably within Claude's context window. This is the simplest approach that gives Claude access to all the data it needs to answer specific questions accurately. A production system would use text-to-code execution (Claude generates pandas queries, the server runs them) - but that is out of scope here.

### 2. Replace the stub in `backend/src/api/routes/chat.py`
Replace only the route body - keep the router, imports, and `ChatRequest` model as Session 3 wrote them. Add the import and swap the return:

```python
from backend.src.ai.chat import ask   # add this import

@router.post("/chat/{session_id}")
def chat(session_id: str, body: ChatRequest):
    rows = get_session(session_id)
    if rows is None:
        raise HTTPException(status_code=404, detail="Session not found")
    answer = ask(rows, body.question)
    return {"answer": answer}
```

## Environment Variable
`ANTHROPIC_API_KEY` must be set before the server starts. It is read in `chat.py` at import time.
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```
Or add it to a `.env` file and load it with `python-dotenv` in `main.py`.

## Key Constraints
- Use model `claude-sonnet-4-6` - it's capable and cost-effective for Q&A tasks
- `max_tokens=1024` is sufficient for a data analysis answer - do not set it higher
- The `Anthropic` client reads `ANTHROPIC_API_KEY` from the environment - never hardcode the key
- If `ANTHROPIC_API_KEY` is missing, the server will raise a `KeyError` on startup - that's intentional, it's better than a silent failure at request time
- Do not import from `backend/src/analysis/` - the AI layer works directly from raw rows, not the report dict

## Tests to Write
See `guidelines/07-testing.md` for full test code. Your test file is `backend/tests/test_ai.py`.

Uses `unittest.mock.patch` to replace the Anthropic client - no real API calls in tests.

Covers: `build_context` produces valid CSV text, `ask` calls `client.messages.create` once with the question in the prompt, mock response is returned correctly.

## Files to Create
- `backend/src/ai/__init__.py` (empty)
- `backend/src/ai/chat.py`
- `backend/tests/test_ai.py`

## Files to Edit
- `backend/src/api/routes/chat.py` - replace stub body only

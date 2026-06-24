# Guideline 02 - Data Layer (Session 1)

## Scope
This session owns `backend/src/data/` only.

## What to Build

### 1. `backend/src/data/models.py`
Define the `SalesRow` dataclass (see `guidelines/01-project-overview.md` for exact fields).
This is the shared contract - define it here, import it everywhere else.

```python
from dataclasses import dataclass, asdict

@dataclass
class SalesRow:
    date: str
    product: str
    category: str
    quantity: int
    unit_price: float
    revenue: float
    region: str

    def to_dict(self) -> dict:
        return asdict(self)
```

### 2. `backend/src/data/parser.py`
Parse an uploaded CSV file into a list of `SalesRow` objects.

```python
import pandas as pd
from backend.src.data.models import SalesRow

REQUIRED_COLUMNS = {"date", "product", "category", "quantity", "unit_price", "revenue", "region"}

def parse_csv(file_bytes: bytes) -> list[SalesRow]:
    ...
```

Steps inside `parse_csv`:
1. Read bytes into a pandas DataFrame: `pd.read_csv(io.BytesIO(file_bytes))`
2. Validate that all `REQUIRED_COLUMNS` are present - raise `ValueError` with a clear message listing the missing columns if any are absent
3. Strip whitespace from string column names (handles CSVs with accidental spaces)
4. Cast types:
   - `quantity` → `int` (use `pd.to_numeric(..., errors='coerce').fillna(0).astype(int)`)
   - `unit_price`, `revenue` → `float`
   - `date` → keep as string
5. Drop rows where `revenue` is NaN or zero (they add noise to analysis)
6. Return a `list[SalesRow]` - one per row

Expose `REQUIRED_COLUMNS` as a module-level set so the API layer can reference it in error messages.

## Key Constraints
- No file I/O - receive `bytes`, return `list[SalesRow]`. The API layer handles the file upload.
- Raise `ValueError` for schema problems, not `HTTPException` - the API layer converts to HTTP 400.
- Keep `SalesRow` as a dataclass, not a dict - other layers depend on attribute access.
- Do not import from `backend/src/analysis/` or `backend/src/api/`.

## Tests to Write
See `guidelines/07-testing.md` for full test code. Your test file is `backend/tests/test_parser.py`.

Covers: valid CSV parses correctly, missing column raises ValueError, type casting, zero-revenue rows dropped.

## Files to Create
- `backend/src/data/__init__.py` (empty)
- `backend/src/data/models.py`
- `backend/src/data/parser.py`
- `backend/tests/__init__.py` (empty)
- `backend/tests/conftest.py` (Session 1 creates this - shared fixtures for all sessions)
- `backend/tests/test_parser.py`

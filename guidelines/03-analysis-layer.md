# Guideline 03 — Analysis Layer (Session 2)

## Scope
This session owns `backend/src/analysis/` only.

## What to Build

### 1. `backend/src/analysis/stats.py`
Compute all KPIs and aggregations from a list of `SalesRow` objects.

```python
from backend.src.data.models import SalesRow

def compute_kpis(rows: list[SalesRow]) -> dict:
    # Returns:
    # {
    #   "total_revenue": float,
    #   "total_orders": int,        # len(rows)
    #   "avg_order_value": float,   # total_revenue / total_orders
    #   "best_month": str,          # "2024-03" — month with highest revenue
    #   "best_product": str         # product name with highest total revenue
    # }

def monthly_trend(rows: list[SalesRow]) -> list[dict]:
    # Group by month (first 7 chars of date: "2024-01")
    # Returns: [{"month": "2024-01", "revenue": 18500.0}, ...]
    # Sorted ascending by month

def top_products(rows: list[SalesRow], top_n: int = 5) -> list[dict]:
    # Group by product, sum revenue and quantity
    # Returns: [{"product": "Widget A", "revenue": 45000.0, "quantity": 1500}, ...]
    # Sorted descending by revenue

def by_region(rows: list[SalesRow]) -> list[dict]:
    # Group by region, sum revenue
    # Returns: [{"region": "North", "revenue": 42000.0}, ...]
    # Sorted descending by revenue
```

Use Python's `collections.defaultdict` or convert to a pandas DataFrame internally — either is fine.
If `rows` is empty, all functions should return sensible empty values (empty list or zeroed dict) rather than raising.

### 2. `backend/src/analysis/anomalies.py`
Detect months where revenue is unusually high or low compared to the average.

```python
def detect_anomalies(rows: list[SalesRow], threshold: float = 1.5) -> list[dict]:
    # 1. Compute monthly revenue (reuse monthly_trend logic, or import it)
    # 2. Calculate mean monthly revenue
    # 3. Flag any month where revenue > mean * (1 + threshold) or < mean * (1 - threshold)
    # Returns: [{"month": "2024-04", "revenue": 41000.0, "note": "Revenue spike: 93% above monthly average"}, ...]
    # Returns [] if fewer than 3 months of data (not enough baseline)
```

`threshold=1.5` means flag anything more than 150% above or below average.
The `note` field should be human-readable: `"Revenue spike: 93% above monthly average"` or `"Revenue drop: 61% below monthly average"`.

### 3. `backend/src/analysis/report.py`
Compose a single report dict from all the above — this is what the API layer calls.

```python
from backend.src.analysis.stats import compute_kpis, monthly_trend, top_products, by_region
from backend.src.analysis.anomalies import detect_anomalies

def build_report(rows: list[SalesRow]) -> dict:
    return {
        "kpis": compute_kpis(rows),
        "monthly_trend": monthly_trend(rows),
        "top_products": top_products(rows),
        "by_region": by_region(rows),
        "anomalies": detect_anomalies(rows),
    }
```

This is the only function the API layer (`Session 3`) imports from this module.

## Import Rule
Only import from `backend/src/data/` (for the `SalesRow` model).
Do not import from `backend/src/api/` or `backend/src/ai/`.

## Tests to Write
See `guidelines/07-testing.md` for full test code. Your test file is `backend/tests/test_analysis.py`.

Covers: KPI totals, best month/product, monthly trend sort order, top products ranking, anomaly detection threshold, empty row handling.

## Files to Create
- `backend/src/analysis/__init__.py` (empty)
- `backend/src/analysis/stats.py`
- `backend/src/analysis/anomalies.py`
- `backend/src/analysis/report.py`
- `backend/tests/test_analysis.py`

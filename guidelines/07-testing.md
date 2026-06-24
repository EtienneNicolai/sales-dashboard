# Guideline 07 - Testing

## Overview
Each session writes tests for the layer it owns. All tests live in `backend/tests/`.

```powershell
$env:PYTHONPATH = "C:\Users\Etien\Documents\Projects\sales-dashboard\backend\lib"
pytest backend/tests/ -v
```

---

## Shared Fixtures - `backend/tests/conftest.py`
Session 1 creates this. All sessions import from here.

```python
import pytest
from backend.src.data.models import SalesRow

@pytest.fixture
def sample_rows():
    return [
        SalesRow(date="2024-01-15", product="Widget A", category="Electronics",
                 quantity=10, unit_price=29.99, revenue=299.90, region="North"),
        SalesRow(date="2024-01-20", product="Gadget B", category="Electronics",
                 quantity=5, unit_price=49.99, revenue=249.95, region="South"),
        SalesRow(date="2024-02-10", product="Widget A", category="Electronics",
                 quantity=8, unit_price=29.99, revenue=239.92, region="East"),
        SalesRow(date="2024-02-18", product="Pro License", category="Software",
                 quantity=3, unit_price=99.99, revenue=299.97, region="West"),
        SalesRow(date="2024-03-05", product="Gadget B", category="Electronics",
                 quantity=12, unit_price=49.99, revenue=599.88, region="North"),
        SalesRow(date="2024-03-22", product="Widget A", category="Electronics",
                 quantity=20, unit_price=29.99, revenue=599.80, region="South"),
    ]

@pytest.fixture
def sample_csv_bytes():
    return (
        b"date,product,category,quantity,unit_price,revenue,region\n"
        b"2024-01-15,Widget A,Electronics,10,29.99,299.90,North\n"
        b"2024-01-20,Gadget B,Electronics,5,49.99,249.95,South\n"
        b"2024-02-10,Widget A,Electronics,8,29.99,239.92,East\n"
    )

@pytest.fixture
def bad_csv_bytes():
    return b"date,product,quantity\n2024-01-15,Widget A,10\n"
```

---

## Session 1 Tests - `backend/tests/test_parser.py`

```python
import pytest
from backend.src.data.parser import parse_csv
from backend.src.data.models import SalesRow

def test_parse_csv_returns_sales_rows(sample_csv_bytes):
    rows = parse_csv(sample_csv_bytes)
    assert len(rows) == 3
    assert all(isinstance(r, SalesRow) for r in rows)

def test_parse_csv_correct_values(sample_csv_bytes):
    rows = parse_csv(sample_csv_bytes)
    assert rows[0].product == "Widget A"
    assert rows[0].revenue == 299.90
    assert rows[0].quantity == 10

def test_parse_csv_missing_columns_raises(bad_csv_bytes):
    with pytest.raises(ValueError, match="Missing required columns"):
        parse_csv(bad_csv_bytes)

def test_parse_csv_quantity_is_int(sample_csv_bytes):
    rows = parse_csv(sample_csv_bytes)
    assert isinstance(rows[0].quantity, int)

def test_parse_csv_revenue_is_float(sample_csv_bytes):
    rows = parse_csv(sample_csv_bytes)
    assert isinstance(rows[0].revenue, float)

def test_parse_csv_drops_zero_revenue_rows():
    csv_bytes = (
        b"date,product,category,quantity,unit_price,revenue,region\n"
        b"2024-01-15,Widget A,Electronics,10,29.99,299.90,North\n"
        b"2024-01-16,Bad Row,Electronics,0,0,0,North\n"
    )
    rows = parse_csv(csv_bytes)
    assert len(rows) == 1
```

---

## Session 2 Tests - `backend/tests/test_analysis.py`

```python
from backend.src.analysis.stats import compute_kpis, monthly_trend, top_products, by_region
from backend.src.analysis.anomalies import detect_anomalies
from backend.src.analysis.report import build_report

def test_compute_kpis_total_revenue(sample_rows):
    kpis = compute_kpis(sample_rows)
    expected = sum(r.revenue for r in sample_rows)
    assert abs(kpis["total_revenue"] - expected) < 0.01

def test_compute_kpis_total_orders(sample_rows):
    kpis = compute_kpis(sample_rows)
    assert kpis["total_orders"] == len(sample_rows)

def test_compute_kpis_best_product(sample_rows):
    kpis = compute_kpis(sample_rows)
    assert kpis["best_product"] == "Widget A"  # highest total revenue in sample

def test_monthly_trend_sorted(sample_rows):
    trend = monthly_trend(sample_rows)
    months = [t["month"] for t in trend]
    assert months == sorted(months)

def test_monthly_trend_correct_months(sample_rows):
    trend = monthly_trend(sample_rows)
    months = {t["month"] for t in trend}
    assert "2024-01" in months
    assert "2024-02" in months
    assert "2024-03" in months

def test_top_products_sorted_desc(sample_rows):
    products = top_products(sample_rows)
    revenues = [p["revenue"] for p in products]
    assert revenues == sorted(revenues, reverse=True)

def test_by_region_has_all_regions(sample_rows):
    regions_result = {r["region"] for r in by_region(sample_rows)}
    expected = {r.region for r in sample_rows}
    assert regions_result == expected

def test_detect_anomalies_returns_list(sample_rows):
    result = detect_anomalies(sample_rows)
    assert isinstance(result, list)

def test_detect_anomalies_empty_on_few_months():
    from backend.src.data.models import SalesRow
    two_month_rows = [
        SalesRow("2024-01-01","A","X",1,10.0,10.0,"N"),
        SalesRow("2024-02-01","A","X",1,10.0,10.0,"N"),
    ]
    assert detect_anomalies(two_month_rows) == []

def test_build_report_shape(sample_rows):
    report = build_report(sample_rows)
    assert "kpis" in report
    assert "monthly_trend" in report
    assert "top_products" in report
    assert "by_region" in report
    assert "anomalies" in report

def test_compute_kpis_empty_rows():
    kpis = compute_kpis([])
    assert kpis["total_revenue"] == 0
    assert kpis["total_orders"] == 0
```

---

## Session 3 Tests - `backend/tests/test_api.py`

```python
import pytest
from httpx import AsyncClient, ASGITransport
from backend.src.api.main import app

@pytest.fixture
def valid_csv():
    return (
        b"date,product,category,quantity,unit_price,revenue,region\n"
        b"2024-01-15,Widget A,Electronics,10,29.99,299.90,North\n"
        b"2024-02-10,Gadget B,Electronics,5,49.99,249.95,South\n"
        b"2024-03-01,Widget A,Electronics,8,29.99,239.92,East\n"
    )

@pytest.mark.asyncio
async def test_upload_valid_csv(valid_csv):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/upload", files={"file": ("sales.csv", valid_csv, "text/csv")})
    assert res.status_code == 200
    data = res.json()
    assert "session_id" in data
    assert data["row_count"] == 3
    assert len(data["preview"]) <= 5

@pytest.mark.asyncio
async def test_upload_non_csv_rejected():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/upload", files={"file": ("data.txt", b"hello", "text/plain")})
    assert res.status_code == 400

@pytest.mark.asyncio
async def test_upload_missing_columns_rejected():
    bad = b"date,product\n2024-01-01,Widget A\n"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/upload", files={"file": ("bad.csv", bad, "text/csv")})
    assert res.status_code == 400
    assert "Missing required columns" in res.json()["detail"]

@pytest.mark.asyncio
async def test_stats_returns_correct_shape(valid_csv):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        upload_res = await client.post("/upload", files={"file": ("sales.csv", valid_csv, "text/csv")})
        session_id = upload_res.json()["session_id"]
        stats_res = await client.get(f"/stats/{session_id}")
    assert stats_res.status_code == 200
    body = stats_res.json()
    assert "kpis" in body
    assert "monthly_trend" in body
    assert "top_products" in body

@pytest.mark.asyncio
async def test_stats_unknown_session():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/stats/doesnotexist")
    assert res.status_code == 404

@pytest.mark.asyncio
async def test_export_returns_csv(valid_csv):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        upload_res = await client.post("/upload", files={"file": ("sales.csv", valid_csv, "text/csv")})
        session_id = upload_res.json()["session_id"]
        export_res = await client.get(f"/export/{session_id}")
    assert export_res.status_code == 200
    assert "text/csv" in export_res.headers["content-type"]

@pytest.mark.asyncio
async def test_chat_stub_returns_answer(valid_csv):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        upload_res = await client.post("/upload", files={"file": ("sales.csv", valid_csv, "text/csv")})
        session_id = upload_res.json()["session_id"]
        chat_res = await client.post(f"/chat/{session_id}", json={"question": "What is the best product?"})
    assert chat_res.status_code == 200
    assert "answer" in chat_res.json()
```

---

## Session 5 Tests - `backend/tests/test_ai.py`

```python
from unittest.mock import MagicMock, patch
from backend.src.data.models import SalesRow
from backend.src.ai.chat import build_context, ask

SAMPLE_ROWS = [
    SalesRow("2024-01-15", "Widget A", "Electronics", 10, 29.99, 299.90, "North"),
    SalesRow("2024-02-10", "Gadget B", "Electronics", 5, 49.99, 249.95, "South"),
]

def test_build_context_is_valid_csv():
    context = build_context(SAMPLE_ROWS)
    lines = context.strip().split("\n")
    assert lines[0] == "date,product,category,quantity,unit_price,revenue,region"
    assert len(lines) == len(SAMPLE_ROWS) + 1  # header + data rows

def test_build_context_contains_product_names():
    context = build_context(SAMPLE_ROWS)
    assert "Widget A" in context
    assert "Gadget B" in context

def test_ask_calls_anthropic_once():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Widget A had the highest revenue.")]
    with patch("backend.src.ai.chat.client") as mock_client:
        mock_client.messages.create.return_value = mock_response
        answer = ask(SAMPLE_ROWS, "Which product had the highest revenue?")
    mock_client.messages.create.assert_called_once()
    assert answer == "Widget A had the highest revenue."

def test_ask_includes_question_in_prompt():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Answer")]
    with patch("backend.src.ai.chat.client") as mock_client:
        mock_client.messages.create.return_value = mock_response
        ask(SAMPLE_ROWS, "What is the best region?")
    call_args = mock_client.messages.create.call_args
    messages = call_args.kwargs["messages"]
    assert "What is the best region?" in messages[0]["content"]
```

---

## Running Tests
```powershell
# All tests
$env:PYTHONPATH = "C:\Users\Etien\Documents\Projects\sales-dashboard\backend\lib"
pytest backend/tests/ -v

# One session only
pytest backend/tests/test_parser.py -v
pytest backend/tests/test_analysis.py -v
pytest backend/tests/test_api.py -v
pytest backend/tests/test_ai.py -v

# Stop on first failure
pytest backend/tests/ -x

# Show print output
pytest backend/tests/ -v -s
```

## What Each File Owns
| File | Session | Tests |
|---|---|---|
| `backend/tests/conftest.py` | Session 1 | Shared fixtures |
| `backend/tests/test_parser.py` | Session 1 | CSV parsing, validation, type casting |
| `backend/tests/test_analysis.py` | Session 2 | KPIs, trends, anomalies, report shape |
| `backend/tests/test_api.py` | Session 3 | Upload, stats, export, chat stub |
| `backend/tests/test_ai.py` | Session 5 | Prompt building, Anthropic client mocking |

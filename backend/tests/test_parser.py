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

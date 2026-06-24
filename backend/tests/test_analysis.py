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
        SalesRow("2024-01-01", "A", "X", 1, 10.0, 10.0, "N"),
        SalesRow("2024-02-01", "A", "X", 1, 10.0, 10.0, "N"),
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

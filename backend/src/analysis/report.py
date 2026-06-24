from backend.src.analysis.stats import compute_kpis, monthly_trend, top_products, by_region
from backend.src.analysis.anomalies import detect_anomalies
from backend.src.data.models import SalesRow


def build_report(rows: list[SalesRow]) -> dict:
    return {
        "kpis": compute_kpis(rows),
        "monthly_trend": monthly_trend(rows),
        "top_products": top_products(rows),
        "by_region": by_region(rows),
        "anomalies": detect_anomalies(rows),
    }

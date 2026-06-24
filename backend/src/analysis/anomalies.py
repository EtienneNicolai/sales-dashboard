from backend.src.data.models import SalesRow
from backend.src.analysis.stats import monthly_trend


def detect_anomalies(rows: list[SalesRow], threshold: float = 1.5) -> list[dict]:
    trend = monthly_trend(rows)

    if len(trend) < 3:
        return []

    revenues = [entry["revenue"] for entry in trend]
    mean = sum(revenues) / len(revenues)

    if mean == 0:
        return []

    anomalies = []
    for entry in trend:
        revenue = entry["revenue"]
        pct_diff = (revenue - mean) / mean

        if pct_diff > threshold:
            pct_above = round(pct_diff * 100)
            note = f"Revenue spike: {pct_above}% above monthly average"
            anomalies.append({"month": entry["month"], "revenue": revenue, "note": note})
        elif pct_diff < -threshold:
            pct_below = round(abs(pct_diff) * 100)
            note = f"Revenue drop: {pct_below}% below monthly average"
            anomalies.append({"month": entry["month"], "revenue": revenue, "note": note})

    return anomalies

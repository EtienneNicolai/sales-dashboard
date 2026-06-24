from collections import defaultdict
from backend.src.data.models import SalesRow


def compute_kpis(rows: list[SalesRow]) -> dict:
    if not rows:
        return {
            "total_revenue": 0,
            "total_orders": 0,
            "avg_order_value": 0.0,
            "best_month": None,
            "best_product": None,
        }

    total_revenue = sum(r.revenue for r in rows)
    total_orders = len(rows)
    avg_order_value = total_revenue / total_orders

    monthly_revenue: dict[str, float] = defaultdict(float)
    for r in rows:
        month = r.date[:7]
        monthly_revenue[month] += r.revenue
    best_month = max(monthly_revenue, key=lambda m: monthly_revenue[m])

    product_revenue: dict[str, float] = defaultdict(float)
    for r in rows:
        product_revenue[r.product] += r.revenue
    best_product = max(product_revenue, key=lambda p: product_revenue[p])

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "best_month": best_month,
        "best_product": best_product,
    }


def monthly_trend(rows: list[SalesRow]) -> list[dict]:
    if not rows:
        return []

    monthly_revenue: dict[str, float] = defaultdict(float)
    for r in rows:
        month = r.date[:7]
        monthly_revenue[month] += r.revenue

    return [
        {"month": month, "revenue": monthly_revenue[month]}
        for month in sorted(monthly_revenue)
    ]


def top_products(rows: list[SalesRow], top_n: int = 5) -> list[dict]:
    if not rows:
        return []

    product_revenue: dict[str, float] = defaultdict(float)
    product_quantity: dict[str, int] = defaultdict(int)
    for r in rows:
        product_revenue[r.product] += r.revenue
        product_quantity[r.product] += r.quantity

    products = [
        {"product": product, "revenue": product_revenue[product], "quantity": product_quantity[product]}
        for product in product_revenue
    ]
    products.sort(key=lambda p: p["revenue"], reverse=True)
    return products[:top_n]


def by_region(rows: list[SalesRow]) -> list[dict]:
    if not rows:
        return []

    region_revenue: dict[str, float] = defaultdict(float)
    for r in rows:
        region_revenue[r.region] += r.revenue

    regions = [
        {"region": region, "revenue": region_revenue[region]}
        for region in region_revenue
    ]
    regions.sort(key=lambda r: r["revenue"], reverse=True)
    return regions

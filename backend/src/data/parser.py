import io

import pandas as pd

from backend.src.data.models import SalesRow

REQUIRED_COLUMNS = {"date", "product", "category", "quantity", "unit_price", "revenue", "region"}


def parse_csv(file_bytes: bytes) -> list[SalesRow]:
    df = pd.read_csv(io.BytesIO(file_bytes))

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Validate required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    # Cast types
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    df["revenue"] = df["revenue"].astype(float)
    df["date"] = df["date"].astype(str)

    # Drop rows where revenue is NaN or zero
    df = df[df["revenue"].notna() & (df["revenue"] != 0)]

    rows = [
        SalesRow(
            date=row["date"],
            product=row["product"],
            category=row["category"],
            quantity=int(row["quantity"]),
            unit_price=float(row["unit_price"]),
            revenue=float(row["revenue"]),
            region=row["region"],
        )
        for _, row in df.iterrows()
    ]

    return rows

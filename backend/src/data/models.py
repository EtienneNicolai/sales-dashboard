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

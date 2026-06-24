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

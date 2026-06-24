import pytest
from unittest.mock import MagicMock, patch
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
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Widget A had the highest revenue.")]
    with patch("backend.src.ai.chat.client") as mock_client:
        mock_client.messages.create.return_value = mock_response
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            upload_res = await client.post("/upload", files={"file": ("sales.csv", valid_csv, "text/csv")})
            session_id = upload_res.json()["session_id"]
            chat_res = await client.post(f"/chat/{session_id}", json={"question": "What is the best product?"})
    assert chat_res.status_code == 200
    assert "answer" in chat_res.json()

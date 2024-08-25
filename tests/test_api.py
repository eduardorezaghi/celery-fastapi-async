import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.post("/products/", json={"name": "Test Product", "category_id": 1, "price": 9.99})
    assert response.status_code == 200
    assert "task_id" in response.json()

@pytest.mark.asyncio
async def test_get_product():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/products/1")
    assert response.status_code == 200
    assert response.json()["product_name"] == "Chai"
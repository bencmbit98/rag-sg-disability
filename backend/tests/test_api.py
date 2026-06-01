import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "llm" in data
    assert "chunks_indexed" in data
    assert "embedding_loaded" in data
    assert "groq_connected" in data
    assert "chroma_status" in data

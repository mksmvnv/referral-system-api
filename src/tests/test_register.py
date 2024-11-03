import pytest

from httpx import AsyncClient

from src.main import app
from src.config import settings


API_PREFIX = settings.api.PREFIX


@pytest.mark.asyncio
async def test_register_referrer():
    url = f"{API_PREFIX}/referrers/register"
    params = {
        "username": "test",
        "email": "test@test.ru",
        "password": "Test12345!"
    }

    async with AsyncClient(app=app, base_url="http://api:8000") as client:
        response = await client.post(url, params=params)

    assert response.status_code == 200

    response_json = response.json()

    assert response_json["username"] == "pasha"
    assert response_json["status"] == "success"
    assert response_json["is_active"] is True
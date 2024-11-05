import pytest

from httpx import AsyncClient

from fastapi import status

from src.config import settings


API_PREFIX = settings.api.PREFIX


@pytest.mark.asyncio
async def test_register_without_referral_code(async_client: AsyncClient):
    response = await async_client.post(
        f"{API_PREFIX}/referrers/register",
        data={
            "username": "test",
            "email": "test@test.ru",
            "password": "Test12345!",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"username": "test", "status": "success"}

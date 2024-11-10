import pytest

from httpx import AsyncClient

from fastapi import status

from src.config import settings


API_PREFIX = settings.api.PREFIX


@pytest.mark.asyncio
async def test_create_referral_code(async_client: AsyncClient, login_user):
    token = await login_user("testuser", "Test12345!")
    headers = {"Authorization": f"Bearer {token}"}

    response = await async_client.post(
        f"{API_PREFIX}/referrers/create-referral-code", headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "referral_code" in data
    assert isinstance(data["referral_code"], str)
    assert len(data["referral_code"]) > 0

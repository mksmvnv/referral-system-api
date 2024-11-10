import pytest_asyncio

from typing import AsyncGenerator, Any, Optional

from httpx import ASGITransport, AsyncClient

from src.main import app


import pytest
from httpx import AsyncClient
from src.main import app
from src.config import settings


API_PREFIX = settings.api.PREFIX


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def register_user(async_client: AsyncClient):
    async def _register_user(
        username: str, email: str, password: str, referral_code: Optional[str]
    ):
        form_data = {
            "username": username,
            "email": email,
            "password": password,
        }
        if referral_code:
            form_data["referral_code"] = referral_code

        response = await async_client.post(
            f"{API_PREFIX}/referrers/register",
            data=form_data,  # Используйте form, чтобы данные передавались как Form
        )
        assert response.status_code == 200
        return response.json()

    return _register_user


@pytest_asyncio.fixture
async def login_user(async_client: AsyncClient, register_user):
    async def _login_user(username: str, password: str):
        # Сначала зарегистрируйте пользователя
        await register_user(
            username=username, email=f"{username}@test.ru", password=password
        )

        # Затем выполните логин
        response = await async_client.post(
            f"{API_PREFIX}/referrers/login",
            data={
                "username": username,
                "password": password,
            },  # Здесь используйте data для отправки данных в OAuth2PasswordRequestForm
        )
        assert response.status_code == 200
        token = response.json().get("access_token")
        assert token is not None
        return token

    return _login_user

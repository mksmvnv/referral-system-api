import pytest_asyncio

from typing import AsyncGenerator, Any

from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[Any, Any]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://api:8000"
    ) as ac:
        yield ac

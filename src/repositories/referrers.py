from pydantic import EmailStr

from sqlalchemy import select

from db import async_session_maker
from repositories.base import BaseRepository
from models.referrers import Referrer


class ReferrerRepository(BaseRepository):
    model = Referrer

    async def get_referrer_by_email(self, email: EmailStr):
        async with async_session_maker() as session:
            stmt = select(Referrer).filter(Referrer.email == email)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_referrer_by_username(self, username: str):
        async with async_session_maker() as session:
            stmt = select(Referrer).filter(Referrer.username == username)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

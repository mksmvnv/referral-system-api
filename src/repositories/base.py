from uuid import UUID
from typing import Optional
from abc import ABC, abstractmethod

from pydantic import EmailStr
from sqlalchemy import insert, select

from src.databases.postgres import async_session_maker
from src.models.referrers import Referrer
from src.models.referrals import Referral
from src.schemas.referrals import ReferralList


class AbstractRepository(ABC):
    @abstractmethod
    async def create():
        raise NotImplementedError

    @abstractmethod
    async def get_by_email():
        raise NotImplementedError

    @abstractmethod
    async def get_by_username():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    model = None

    async def create(self, data: dict) -> Optional[Referrer]:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()

    async def get_by_email(self, email: EmailStr) -> Optional[Referrer]:
        async with async_session_maker() as session:
            stmt = select(Referrer).filter(Referrer.email == email)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[Referrer]:
        async with async_session_maker() as session:
            stmt = select(Referrer).filter(Referrer.username == username)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def get_all(self, id: UUID) -> Optional[ReferralList]:
        async with async_session_maker() as session:
            stmt = select(Referral).filter(Referral.referrer_id == id)
            res = await session.execute(stmt)
            return res.scalars().all()

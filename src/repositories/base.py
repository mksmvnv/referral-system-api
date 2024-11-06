from uuid import UUID
from typing import Generic, Type, TypeVar, Optional, Coroutine, Any
from abc import ABC, abstractmethod

from pydantic import EmailStr
from sqlalchemy import insert, select

from src.databases.postgres import async_session_maker
from src.models.referrers import Referrer
from src.models.referrals import Referral
from src.schemas.referrals import ReferralList

T = TypeVar("T")


class AbstractRepository(ABC):
    @abstractmethod
    async def create(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: EmailStr):
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, id: UUID):
        raise NotImplementedError


class BaseRepository(AbstractRepository, Generic[T]):
    model: Optional[Type[T]] = None

    def __init__(self, model: Optional[Type[T]] = None):
        if model:
            self.model = model

    async def create(self, data: dict):
        if self.model is None:
            raise ValueError("Model is not set for this repository")

        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one_or_none()

    async def get_by_email(self, email: EmailStr):
        async with async_session_maker() as session:
            stmt = select(Referrer).filter(Referrer.email == email)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def get_by_username(self, username: str):
        async with async_session_maker() as session:
            stmt = select(Referrer).filter(Referrer.username == username)
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    async def get_all(self, id: UUID):
        async with async_session_maker() as session:
            stmt = select(Referral).filter(Referral.referrer_id == id)
            res = await session.execute(stmt)
            return res.scalars().all()

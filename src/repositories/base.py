from uuid import UUID

from abc import ABC, abstractmethod

from fastapi import HTTPException

from sqlalchemy import insert, select

from database import async_session


class AbstractRepository(ABC):
    @abstractmethod
    async def create():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    model = None

    async def create(self, data: dict) -> dict:
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_one(self, id: UUID) -> dict:
        async with async_session() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            user = res.scalar_one_or_none()

            if not user:
                raise HTTPException(
                    status_code=404, detail=f"User with id {id} not found"
                )

            return user

    async def get_all(self) -> list[dict]:
        async with async_session() as session:
            stmt = select(self.model)
            res = await session.execute(stmt)
            users = res.scalars().all()

            if not users:
                raise HTTPException(status_code=404, detail=f"Users not found")

            return users

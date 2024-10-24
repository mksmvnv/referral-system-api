from abc import ABC, abstractmethod

from sqlalchemy import insert

from db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def create():
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    model = None

    async def create(self, data: dict) -> dict:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

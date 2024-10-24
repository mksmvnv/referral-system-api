from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings


db_url = settings.postgres_url

async_engine = create_async_engine(db_url, echo=True)
async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)


class BaseModel(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

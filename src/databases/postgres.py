from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings


POSTGRES_URL = settings.postgres.URL

async_engine = create_async_engine(POSTGRES_URL, echo=True)
async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)


class BaseModel(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

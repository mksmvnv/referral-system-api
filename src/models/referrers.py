from uuid import uuid4

from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from pydantic import EmailStr

from db import BaseModel


class Referrer(BaseModel):
    __tablename__ = "referrers"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[EmailStr] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    referral_code: Mapped[UUID] = mapped_column(UUID, unique=True, nullable=True)

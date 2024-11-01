from uuid import uuid4

from sqlalchemy import UUID, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.databases.postgres import BaseModel


class Referrer(BaseModel):
    __tablename__ = "referrers"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    referrals = relationship("Referral", back_populates="referrer")

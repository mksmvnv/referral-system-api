from uuid import uuid4

from sqlalchemy import UUID, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.databases.postgres import BaseModel


class Referral(BaseModel):
    __tablename__ = "referrals"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    referral_code: Mapped[str] = mapped_column(String, nullable=True)

    referrer_id: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("referrers.id", ondelete="CASCADE"), index=True
    )
    referrer = relationship("Referrer", back_populates="referrals")

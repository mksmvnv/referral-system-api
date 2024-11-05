from uuid import UUID

from fastapi import HTTPException, status

from src.auth.hasher import Hasher

from src.databases.redis import RedisTools
from src.repositories.base import AbstractRepository
from src.schemas.referrers import ReferrerRegister


class ReferralService:
    def __init__(self, referral_repository: AbstractRepository) -> None:
        self.referral_repository: AbstractRepository = referral_repository()

    async def register(self, redis: RedisTools, register: ReferrerRegister) -> dict:
        if await self.referral_repository.get_by_email(
            register.email
        ) or await self.referral_repository.get_by_username(register.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Referral already exists"
            )

        email = await redis.get_email_by_referral_code(register.referral_code)

        if not email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Referral code not found"
            )

        referral = await self.referral_repository.get_by_email(email)

        hashed_password = Hasher.get_password_hash(register.password)
        referral_data = register.model_dump(exclude={"password"})
        referral_data["hashed_password"] = hashed_password
        referral_data["referrer_id"] = referral.id

        referral = await self.referral_repository.create(referral_data)
        return referral

    async def get_all_referrals(self, id: UUID) -> dict:
        referrals = await self.referral_repository.get_all(id)
        if not referrals:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Referrals not found"
            )
        return referrals

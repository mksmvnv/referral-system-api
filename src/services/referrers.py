from uuid import uuid4
from typing import Optional

from fastapi import HTTPException, status

from src.auth.hasher import Hasher
from src.auth.jwt import create_access_token

from src.databases.redis import RedisTools
from src.repositories.base import AbstractRepository
from src.schemas.referrers import ReferrerRegister, ReferrerLogin


class ReferrerService:
    def __init__(self, referrer_repository: AbstractRepository) -> None:
        self.referrer_repository: AbstractRepository = referrer_repository()

    async def authenticate(self, username: str, password: str) -> Optional[dict]:
        db_referrer = await self.referrer_repository.get_by_username(username)
        if not db_referrer or not Hasher.verify_password(
            password, db_referrer.hashed_password
        ):
            return None

        return db_referrer

    async def register(self, register: ReferrerRegister) -> dict:
        if await self.referrer_repository.get_by_email(
            register.email
        ) or await self.referrer_repository.get_by_username(register.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Referrer already exists"
            )

        hashed_password = Hasher.get_password_hash(register.password)

        referrer_data = register.model_dump(exclude={"password", "referral_code"})
        referrer_data["hashed_password"] = hashed_password

        referrer = await self.referrer_repository.create(referrer_data)
        return referrer

    async def login(self, referrer: ReferrerLogin) -> dict:
        db_referrer = await self.referrer_repository.get_by_username(referrer.username)

        if not await self.authenticate(referrer.username, referrer.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        if not db_referrer.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Referrer is inactive"
            )

        access_token = create_access_token(
            payload={
                "sub": db_referrer.email,
                "username": db_referrer.username,
            }
        )
        return access_token

    async def create_referral_code(self, redis: RedisTools, current_user: str) -> str:
        db_referrer = await self.referrer_repository.get_by_email(current_user)

        if not db_referrer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Referrer not found"
            )

        if not db_referrer.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Referrer is inactive"
            )

        email = db_referrer.email

        referral_code = str(uuid4())

        await redis.set_referral_code(email, referral_code)
        await redis.set_referral_code(referral_code, email)

        return referral_code

    async def delete_referral_code(self, redis: RedisTools, current_user: str) -> str:
        db_referrer = await self.referrer_repository.get_by_email(current_user)

        if not db_referrer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Referrer not found"
            )

        if not db_referrer.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Referrer is inactive"
            )

        email = db_referrer.email

        try:
            await redis.delete_referral_code(email)
            return True
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def get_referral_code(self, redis: RedisTools, email: str) -> str:
        db_referrer = await self.referrer_repository.get_by_email(email)

        if not db_referrer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Referrer not found"
            )

        if not db_referrer.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Referrer is inactive"
            )

        try:
            referral_code = await redis.get_referral_code_by_email(email)
            if not referral_code:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Referral code not found",
                )
            return referral_code
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

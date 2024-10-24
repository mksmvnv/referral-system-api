from typing import Annotated

from fastapi import Depends, HTTPException
from repositories.base import AbstractRepository

from schemas.referrers import ReferrerRegister
from utils.hasher import Hasher


class ReferrerService:
    def __init__(self, referrer_repository: AbstractRepository):
        self.referrer_repository: AbstractRepository = referrer_repository()

    async def register(self, register: Annotated[ReferrerRegister, Depends()]) -> dict:
        if await self.referrer_repository.get_referrer_by_email(
            register.email
        ) or await self.referrer_repository.get_referrer_by_username(register.username):
            raise HTTPException(status_code=400, detail="Credentials already exists")

        hashed_password = Hasher.get_password_hash(register.password)

        referrer_dict = register.model_dump()
        referrer_dict["password"] = hashed_password

        referrer = await self.referrer_repository.create(referrer_dict)

        return referrer

from typing import Annotated
from annotated_types import Len

from pydantic import BaseModel, EmailStr


class BaseReferrer(BaseModel):
    username: Annotated[str, Len(4, 32)]


class ReferrerRegister(BaseReferrer):
    email: Annotated[EmailStr, Len(4, 32)]
    password: Annotated[str, Len(8, 128)]
    referral_code: Annotated[str | None, ...] = None


class ReferrerLogin(BaseModel):
    username: Annotated[str, Len(4, 32)]
    password: Annotated[str, Len(8, 128)]


class ReferrerResponse(BaseModel):
    username: Annotated[str, Len(4, 32)]
    status: Annotated[str, ...]
    is_active: Annotated[bool, ...] = True

    class Config:
        from_attributes = True


class ReferralCodeResponse(BaseModel):
    referral_code: Annotated[str, ...]


class DeletedReferralCodeResponse(BaseModel):
    status: Annotated[str, ...]

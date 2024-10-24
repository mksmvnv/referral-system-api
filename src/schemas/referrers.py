from uuid import UUID
from typing import Annotated, Optional
from annotated_types import Len

from pydantic import BaseModel, EmailStr


class BaseReferrer(BaseModel):
    username: Annotated[str, Len(3, 32)]
    password: Annotated[str, Len(8, 128)]


class ReferrerRegister(BaseReferrer):
    email: Annotated[EmailStr, Len(3, 320)]


class ReferrerLogin(BaseReferrer):
    pass


class ReferrerResponse(BaseModel):
    username: Annotated[str, Len(3, 32)]
    status: Optional[str | None] = "failed"

    class ConfigDict:
        from_attributes = True


class ReferrerId(BaseModel):
    id: UUID

    class ConfigDict:
        from_attributes = True

from typing import Annotated
from annotated_types import Len

from pydantic import BaseModel


class BaseToken(BaseModel):
    access_token: Annotated[str, ...]
    token_type: Annotated[str, ...] = "bearer"


class TokenResponse(BaseToken):
    username: Annotated[str, Len(4, 32)]

    class Config:
        from_attributes = True

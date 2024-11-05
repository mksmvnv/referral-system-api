from typing import Annotated
from annotated_types import Len

from pydantic import BaseModel, ConfigDict


class BaseToken(BaseModel):
    access_token: Annotated[str, ...]
    token_type: Annotated[str, ...] = "bearer"


class TokenResponse(BaseToken):
    username: Annotated[str, Len(4, 32)]

    model_config = ConfigDict(from_attributes=True)

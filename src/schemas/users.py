from pydantic import BaseModel

from uuid import UUID
from datetime import datetime


class BaseUser(BaseModel):
    id: UUID
    username: str
    created_at: datetime


class UserCreate(BaseModel):
    username: str
    password: str

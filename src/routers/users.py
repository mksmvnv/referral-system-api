from uuid import UUID

from fastapi import APIRouter, Depends

from services.users import UserService
from repositories.users import UserRepository
from schemas.users import BaseUser, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=BaseUser)
async def create_user(user_schema: UserCreate = Depends()):
    new_user = await UserService(UserRepository).create_user(user_schema)
    return new_user


@router.get("/{user_id}", response_model=BaseUser)
async def get_user(user_id: UUID):
    user = await UserService(UserRepository).get_user(user_id)
    return user


@router.get("/", response_model=list[BaseUser])
async def get_users():
    users = await UserService(UserRepository).get_users()
    return users

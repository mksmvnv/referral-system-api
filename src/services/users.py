from uuid import UUID

from repositories.base import AbstractRepository
from schemas.users import UserCreate

from auth.hasher import Hasher


class UserService:
    def __init__(self, user_repository: AbstractRepository):
        self.user_repository: AbstractRepository = user_repository()

    async def create_user(self, user_schema: UserCreate) -> UserCreate:
        hashed_password = Hasher.bcrypt(user_schema.password)

        users_dict = user_schema.model_dump()
        users_dict["password"] = hashed_password

        new_user = await self.user_repository.create(users_dict)
        return new_user

    async def get_user(self, user_id: UUID) -> UserCreate:
        user = await self.user_repository.get_one(user_id)
        return user

    async def get_users(self) -> list[UserCreate]:
        users = await self.user_repository.get_all()
        return users

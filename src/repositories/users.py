from repositories.base import BaseRepository
from models.users import User


class UserRepository(BaseRepository):
    model = User

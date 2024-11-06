from src.models.referrers import Referrer
from src.repositories.base import BaseRepository


class ReferrerRepository(BaseRepository[Referrer]):
    def __init__(self):
        super().__init__(model=Referrer)

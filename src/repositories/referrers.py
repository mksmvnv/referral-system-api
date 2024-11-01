from src.models.referrers import Referrer
from src.repositories.base import BaseRepository


class ReferrerRepository(BaseRepository):
    model = Referrer

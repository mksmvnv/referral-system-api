from src.models.referrals import Referral
from src.repositories.base import BaseRepository


class ReferralRepository(BaseRepository[Referral]):
    def __init__(self):
        super().__init__(model=Referral)

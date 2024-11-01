from src.models.referrals import Referral
from src.repositories.base import BaseRepository


class ReferralRepository(BaseRepository):
    model = Referral

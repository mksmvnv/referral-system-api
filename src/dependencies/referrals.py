from src.services.referrals import ReferralService
from src.repositories.referrals import ReferralRepository


def referral_service() -> ReferralService:
    return ReferralService(ReferralRepository)

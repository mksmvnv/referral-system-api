from src.services.referrers import ReferrerService
from src.repositories.referrers import ReferrerRepository


def referrer_service() -> ReferrerService:
    referrer_repository = ReferrerRepository()
    return ReferrerService(referrer_repository)

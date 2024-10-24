from services.referrers import ReferrerService
from repositories.referrers import ReferrerRepository


def referrer_service() -> ReferrerService:
    return ReferrerService(ReferrerRepository)

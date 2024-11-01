from uuid import UUID

from fastapi import APIRouter

from src.databases.redis import RedisTools
from src.schemas.referrers import ReferralCodeResponse
from src.schemas.referrals import ReferralList
from src.dependencies.referrers import referrer_service
from src.dependencies.referrals import referral_service


router = APIRouter(prefix="/visitors", tags=["Visitors"])


@router.get("/get_referral_code", response_model=ReferralCodeResponse)
async def get_referral_code(email: str) -> ReferralCodeResponse:
    referral_code = await referrer_service().get_referral_code(
        redis=RedisTools, email=email
    )
    return ReferralCodeResponse(referral_code=referral_code)


@router.get("/get_all_referrals_by_id", response_model=ReferralList)
async def get_all_referrals_by_id(referrer_id: UUID) -> ReferralList:
    referrals = await referral_service().get_all_referrals(referrer_id)
    return ReferralList(referrals=referrals)

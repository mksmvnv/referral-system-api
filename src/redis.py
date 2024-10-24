from typing import Annotated
from pydantic import PositiveInt

from aioredis import Redis

from fastapi import Depends

from schemas.referrers import ReferrerId
from schemas.referrals import ReferralCode

from config import settings


async def store_referral_code(
    redis: Redis,
    referrer_id: Annotated[ReferrerId, Depends()],
    referral_code: Annotated[ReferralCode, Depends()],
    ttl: PositiveInt = settings.referral_code_expiry,
) -> None:
    key = f"referral: {referrer_id}"
    await redis.setex(key, ttl, referral_code)

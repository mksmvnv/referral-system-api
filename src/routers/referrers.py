from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.utils import decode_jwt
from src.databases.redis import RedisTools
from src.dependencies.referrals import referral_service
from src.dependencies.referrers import referrer_service
from src.schemas.tokens import TokenResponse
from src.schemas.referrers import (
    ReferrerRegister,
    ReferrerResponse,
    ReferralCodeResponse,
    DeletedReferralCodeResponse,
)


router = APIRouter(prefix="/referrers", tags=["Referrers"])


@router.post("/register", response_model=ReferrerResponse)
async def referrer_register(
    register: Annotated[ReferrerRegister, Depends()]
) -> ReferrerResponse:
    if not register.referral_code:
        await referrer_service().register(register=register)
    else:
        await referral_service().register(redis=RedisTools, register=register)
    return ReferrerResponse(username=register.username, status="success")


@router.post("/login", response_model=TokenResponse)
async def referrer_login(
    referrer: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> TokenResponse:
    access_token = await referrer_service().login(referrer)
    return TokenResponse(access_token=access_token, username=referrer.username)


@router.post("/create-referral-code", response_model=ReferralCodeResponse)
async def create_referral_code(
    current_user: str = Depends(decode_jwt),
) -> ReferralCodeResponse:
    referral_code = await referrer_service().create_referral_code(
        redis=RedisTools, current_user=current_user
    )
    return ReferralCodeResponse(referral_code=referral_code)


@router.post("/delete-referral-code", response_model=DeletedReferralCodeResponse)
async def delete_referral_code(
    current_user: str = Depends(decode_jwt),
) -> DeletedReferralCodeResponse:
    if await referrer_service().delete_referral_code(
        redis=RedisTools, current_user=current_user
    ):
        return DeletedReferralCodeResponse(status="deleted")

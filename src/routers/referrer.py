from typing import Annotated

from fastapi import APIRouter, Depends

from schemas.referrers import ReferrerRegister, ReferrerResponse
from dependencies.referrers import referrer_service


router = APIRouter()


@router.post("/register", response_model=ReferrerResponse)
async def referrer_register(referrer: Annotated[ReferrerRegister, Depends()]):
    referrer = await referrer_service().register(referrer)
    return ReferrerResponse(username=referrer.username, status="success")

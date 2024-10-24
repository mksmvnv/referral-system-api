from uuid import UUID
from typing import Annotated

from pydantic import BaseModel


class ReferralCode(BaseModel):
    code: Annotated[UUID, "Referral code"]

from uuid import UUID

from typing import List
from pydantic import BaseModel, StrictStr, StrictBool, StrictInt, ConfigDict


class Referral(BaseModel):
    username: StrictStr
    email: StrictStr
    is_active: StrictBool
    referral_code: StrictStr
    referrer_id: UUID

    model_config = ConfigDict(from_attributes=True)


class ReferralList(BaseModel):
    referrals: List[Referral]

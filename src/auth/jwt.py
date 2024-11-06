import jwt

from typing import Annotated, Optional

from datetime import datetime, timezone, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.config import settings


API_PREFIX = settings.api.PREFIX

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/referrers/login")

PRIVATE_KEY = settings.auth.PRIVATE_KEY_PATH.read_text()
PUBLIC_KEY = settings.auth.PUBLIC_KEY_PATH.read_text()

ALGORITHM = settings.auth.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(
    payload: Optional[dict] = None, expires_delta: Optional[timedelta] = None
) -> str:
    if not payload:
        raise ValueError("Payload cannot be empty")
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update(
        {
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
    )
    access_token = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return access_token


async def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(access_token, PUBLIC_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token does not contain user identifier",
            )
        return email
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

import jwt

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timezone, timedelta

from src.config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/referrers/login")

PRIVATE_KEY = settings.auth.PRIVATE_KEY_PATH.read_text()
PUBLIC_KEY = settings.auth.PUBLIC_KEY_PATH.read_text()

ALGORITHM = settings.auth.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES


def encode_jwt(payload: dict, expires_delta: Optional[timedelta] = None) -> str:
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
    encoded = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded


async def decode_jwt(token: Annotated[str, Depends(oauth2_schema)]) -> dict:
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        return email
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

import logging

from typing import Optional

from redis.asyncio import from_url, Redis

from src.config import settings


REDIS_URL = settings.redis.URL
REDIS_TTL = settings.redis.TTL


class RedisTools:
    __redis_connection: Optional[Redis] = None

    @classmethod
    async def get_connection(cls) -> Redis:
        if cls.__redis_connection is None:
            cls.__redis_connection = from_url(REDIS_URL, decode_responses=True)
        return cls.__redis_connection

    @classmethod
    async def set_referral_code(cls, key: str, value: str) -> str:
        redis = await cls.get_connection()
        try:
            await redis.setex(key, REDIS_TTL, value)
        except Exception:
            logging.error(f"Error setting referral code {key}: {value}")
        return value

    @classmethod
    async def get_referral_code_by_email(cls, email: str) -> Optional[str]:
        redis = await cls.get_connection()
        try:
            if await redis.exists(email):
                return await redis.get(email)
            return None
        except Exception:
            logging.error(f"Error getting referral code for {email}")
            return None

    @classmethod
    async def get_email_by_referral_code(
        cls, referral_code: Optional[str]
    ) -> Optional[str]:
        redis = await cls.get_connection()
        try:
            if referral_code is not None:
                if await redis.exists(referral_code):
                    return await redis.get(referral_code)
            return None
        except Exception:
            logging.error(f"Error getting email for {referral_code}")
            return None

    @classmethod
    async def delete_referral_code(cls, email: str) -> None:
        redis = await cls.get_connection()
        try:
            referral_code = await redis.get(email)
            if referral_code:
                await redis.delete(email)
                await redis.delete(referral_code)
        except Exception:
            logging.error(f"Error deleting referral code for {email}")

    @classmethod
    async def close_connection(cls) -> None:
        if cls.__redis_connection:
            await cls.__redis_connection.close()
            cls.__redis_connection = None


redis = RedisTools()

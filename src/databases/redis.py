import logging

from redis.asyncio import from_url, Redis

from src.config import settings

REDIS_URL = settings.redis.url
REDIS_TTL = settings.redis.ttl


class RedisTools:
    __redis_connection = None

    @classmethod
    async def get_connection(cls) -> Redis:
        if cls.__redis_connection is None:
            cls.__redis_connection = from_url(REDIS_URL)
        return cls.__redis_connection

    @classmethod
    async def set_referral_code(cls, email: str, referral_code: str):
        redis = await cls.get_connection()
        try:
            await redis.setex(email, REDIS_TTL, referral_code)
        except Exception as e:
            logging.error(f"Error setting referral code for {email}: {e}")
        return referral_code

    @classmethod
    async def get_referral_code(cls, email: str) -> str:
        redis = await cls.get_connection()
        try:
            if await redis.exists(email):
                referral_code = await redis.get(email)
                return referral_code.decode("utf-8")
            return None
        except Exception as e:
            logging.error(f"Error getting referral code for {email}: {e}")

    @classmethod
    async def check_referral_code(cls, referral_code: str) -> str:
        redis = await cls.get_connection()
        try:
            async for key in redis.scan_iter():
                value = await redis.get(key)
                if value and value.decode("utf-8") == referral_code:
                    return key.decode("utf-8")
            return False
        except Exception as e:
            logging.error(f"Error getting referral code for {referral_code}: {e}")

    @classmethod
    async def delete_referral_code(cls, email: str):
        redis = await cls.get_connection()
        try:
            await redis.delete(email)
        except Exception as e:
            logging.error(f"Error deleting referral code for {email}: {e}")

    @classmethod
    async def close_connection(cls):
        if cls.__redis_connection:
            await cls.__redis_connection.close()
            cls.__redis_connection = None

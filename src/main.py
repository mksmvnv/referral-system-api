import logging

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException, status

from src.databases.redis import RedisTools

from src.routers.referrers import router as referrer_router
from src.routers.visitors import router as visitor_router

from src.config import settings


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        await RedisTools.get_connection()
        logger.info("Connected to Redis")
        yield
    except Exception:
        logger.error("Failed to connect to Redis", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal service error. Please try again later.",
        )
    finally:
        try:
            await RedisTools.close_connection()
            logger.info("Closed connection to Redis")
        except Exception:
            logger.error("Failed to close connection to Redis", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal service error. Please try again later.",
            )


app = FastAPI(
    lifespan=lifespan,
    title="Referral System API",
    version="1.0.0",
)

app.include_router(referrer_router, prefix=settings.api.PREFIX)
app.include_router(visitor_router, prefix=settings.api.PREFIX)

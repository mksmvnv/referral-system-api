import logging

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException, status

from src.databases.redis import RedisTools

from src.routers.referrers import router as referrer_router
from src.routers.visitors import router as visitor_router

from src.config import settings


logging.basicConfig(
    filename="rsa.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        await RedisTools.get_connection()
        logging.info("Connected to Redis")
        yield
    except Exception:
        logging.error("Failed to connect to Redis")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to connect to Redis",
        )
    finally:
        try:
            await RedisTools.close_connection()
            logging.info("Closed connection to Redis")
        except Exception:
            logging.error("Failed to close connection to Redis")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to close connection to Redis",
            )


app = FastAPI(
    lifespan=lifespan,
    title="Referral System API",
    version="1.0.0",
)

app.include_router(referrer_router, prefix=settings.api.PREFIX)
app.include_router(visitor_router, prefix=settings.api.PREFIX)

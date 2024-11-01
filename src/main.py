from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI, HTTPException, status

from src.databases.redis import RedisTools

from src.routers.referrers import router as referrer_router
from src.routers.visitors import router as visitor_router

from src.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        await RedisTools.get_connection()
        yield
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        try:
            await RedisTools.close_connection()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )


app = FastAPI(
    lifespan=lifespan,
    title="Referral System API",
    version="1.0.0",
)

app.include_router(referrer_router, prefix=settings.api.prefix)
app.include_router(visitor_router, prefix=settings.api.prefix)

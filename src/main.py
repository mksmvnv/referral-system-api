from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from db import init_db
from routers.referrer import router as referrer_router

from config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, title="Referral System API")

app.include_router(referrer_router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import init_db
from routers.users import router as users_router

from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Referral system API", lifespan=lifespan)

app.include_router(users_router, prefix=settings.API_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

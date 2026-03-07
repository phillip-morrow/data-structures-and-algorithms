from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine
from app.models import Base
from app.routes import router
from app.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from app.database import async_session

    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM topics"))
        count = result.scalar()
        if count == 0:
            await seed_data(session)

    yield


app = FastAPI(title="DSA Practice", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

import fakeredis.aioredis
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.bot.database.orm_models import Base


@pytest.fixture
async def sessionmaker() -> async_sessionmaker:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    return sessionmaker


@pytest.fixture
def fake_redis():
    return fakeredis.aioredis.FakeRedis(decode_responses=True)

import os
import pytest
import pathlib
from typing import AsyncGenerator

from threading import Thread
from httpx import AsyncClient, ASGITransport

from src.database import session_maker, engine
from src.main import app
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine
from alembic.config import Config as AlembicConfig
from alembic.command import upgrade, downgrade


@pytest.fixture(scope="session")
async def test_engine() -> AsyncEngine:
    return engine


@pytest.fixture(scope="session")
async def test_session_maker() -> async_sessionmaker:
    return session_maker


@pytest.fixture(scope="function")
async def test_session(
    test_session_maker: async_sessionmaker,
) -> AsyncGenerator[AsyncSession]:
    async with test_session_maker(expire_on_commit=False) as Session:
        yield Session


@pytest.fixture(scope="session")
def alembic_config():
    path = pathlib.Path(os.path.dirname(__file__)).parent

    cfg = AlembicConfig(path / "alembic.ini")
    cfg.set_main_option("script_location", str(path / "alembic"))

    return cfg


@pytest.fixture(scope="class")
async def prepare_db(alembic_config: AlembicConfig):
    # Creation of db by create_all command
    # async with get_test_engine.begin() as connection:
    #     await connection.run_sync(BaseModel.metadata.drop_all)
    #     await connection.run_sync(BaseModel.metadata.create_all)

    # Creation of db by migration

    # Upgrade
    tread = Thread(target=upgrade, args=[alembic_config, "head"])
    tread.start()
    tread.join()

    yield

    # Downgrade
    tread = Thread(target=downgrade, args=[alembic_config, "base"])
    tread.start()
    tread.join()


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

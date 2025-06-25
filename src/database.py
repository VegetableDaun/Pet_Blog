from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import URL, MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.settings import DbEnvConfig

settings = DbEnvConfig()

url = URL.create(
    drivername=settings.driver_name,
    username=settings.user_name,
    password=settings.password,
    host=settings.host,
    port=settings.port,
    database=settings.database,
)

engine = create_async_engine(url=url, echo=True)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


class BaseModel(AsyncAttrs, DeclarativeBase):
    metadata = MetaData(schema="dev")
